"""Bounded authentic initialized runtimeDATA; zero authored-C credit."""
import copy,dataclasses,hashlib,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
PROJECT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT))
import omf,library16,check,runtime_lidata16 as backend
from reference import build_reference,validate_expanded_read,ORIGINAL_SHA256
H=lambda b:hashlib.sha256(b).hexdigest()
def leaf(n,data):return n.to_bytes(2,'little')+b'\0\0'+bytes([len(data)])+data
def branch(n,*kids):return n.to_bytes(2,'little')+len(kids).to_bytes(2,'little')+b''.join(kids)
def record(kind,payload):
 r=bytes([kind])+(len(payload)+1).to_bytes(2,'little')+payload
 return r+bytes([-sum(r)&255])
def small_object(length,writes,fix=None):
 raw=record(0x80,b'\x01X')+record(0x96,b'\0\x05_DATA\x04DATA')+record(0x98,b'\x48'+length.to_bytes(2,'little')+b'\x02\x03\x01')
 for kind,off,data in writes:raw+=record(kind,b'\x01'+off.to_bytes(2,'little')+data)
 if fix is not None:raw+=record(0x9c,fix)
 return omf.read_omf(raw+record(0x8a,b'\0'))

class TreeTests(unittest.TestCase):
 def test_standard_nested_nonzero20(self):
  encoded=bytes.fromhex('020002000300000002404102000000025051')
  data,trees=backend.decode_blocks(encoded);self.assertEqual(data,bytes.fromhex('4041404140415051505140414041404150515051'));self.assertEqual(trees[0]['child_blocks'],2)
 def test_multiple_roots_and_leaf(self):
  self.assertEqual(backend.decode_blocks(leaf(3,b'ab')+leaf(2,b'Z'))[0],b'abababZZ')
 def test_zero_repeat_still_parses_children(self):
  self.assertEqual(backend.decode_blocks(branch(0,leaf(3,b'x')))[0],b'')
  with self.assertRaises(ValueError):backend.decode_blocks(branch(0,leaf(3,b'x'))[:-1])
 def test_each_truncated_standard_tree_rejected(self):
  e=branch(2,leaf(3,b'AB'),leaf(2,b'CD'))
  for end in range(len(e)):
   with self.subTest(end=end),self.assertRaises(ValueError):backend.decode_blocks(e[:end])
 def test_repeat_and_root_bound(self):
  for e in [leaf(65535,b'ab'),leaf(2,b'ab')+leaf(2,b'cd')]:
   with self.assertRaises(ValueError):backend.decode_blocks(e,limit=5)
 def test_nesting_bound(self):
  e=leaf(1,b'x')
  for _ in range(5):e=branch(1,e)
  with self.assertRaisesRegex(ValueError,'nesting'):backend.decode_blocks(e,max_depth=3)
 def test_malformed_inputs_and_limits(self):
  for e,kw in [(b'',{}),(b'\x01',{}),(leaf(1,b'x'),{'limit':True}),(leaf(1,b'x'),{'limit':65537}),(leaf(1,b'x'),{'max_depth':0})]:
   with self.subTest(e=e,kw=kw),self.assertRaises(ValueError):backend.decode_blocks(e,**kw)

class ViewTests(unittest.TestCase):
 def test_complete_mixed_real_record_kinds(self):
  o=small_object(4,[(0xa0,0,b'A'),(0xa2,1,leaf(2,b'B')),(0xa0,3,b'C')]);before=copy.deepcopy(o)
  v=backend.initialized_view(o,1,policy=backend.POLICY);self.assertEqual(v.data,b'ABBC');self.assertEqual(v.iterated_ranges,((1,3),));self.assertEqual([w['record_kind']for w in v.records],[0xa0,0xa2,0xa0]);self.assertEqual(o,before);self.assertTrue(o.segments[1].unsupported_data)
 def test_default_library_still_rejects_lidata(self):
  o=small_object(2,[(0xa2,0,leaf(2,b'A'))])
  with self.assertRaisesRegex(ValueError,'iterated data is unsupported'):library16.link_segment(o,1,{1:(0,0)},{},{})
 def test_holes_and_overlaps_rejected(self):
  for writes in [[(0xa2,0,leaf(2,b'B')),(0xa0,3,b'C')],[(0xa2,0,leaf(3,b'B')),(0xa0,2,b'C')]]:
   with self.subTest(writes=writes),self.assertRaises(ValueError):backend.initialized_view(small_object(4,writes),1,policy=backend.POLICY)
 def test_segment_overrun_and_undefined_index(self):
  with self.assertRaises(ValueError):backend.initialized_view(small_object(2,[(0xa2,0,leaf(3,b'A'))]),1,policy=backend.POLICY)
  o=small_object(2,[(0xa2,0,leaf(2,b'A'))]);o.records.append((0xa2,999,b'\x00\0\0'+leaf(1,b'A')))
  with self.assertRaises(ValueError):backend.initialized_view(o,1,policy=backend.POLICY)
 def test_fixup_inside_and_crossing_iterated_range_rejected(self):
  for at in [0,1]:
   o=small_object(3,[(0xa2,0,leaf(2,b'A')),(0xa0,2,b'B')]);o.fixups.append(omf.Fixup(1,at,2,1,True,(5,None),(0,1),None,999,b''))
   with self.subTest(at=at),self.assertRaisesRegex(ValueError,'iterated'):backend.initialized_view(o,1,policy=backend.POLICY)
 def test_actual_fixupp_after_lidata_rejected_by_original_parser(self):
  with self.assertRaisesRegex(ValueError,'without preceding LEDATA'):small_object(2,[(0xa2,0,leaf(2,b'A'))],bytes.fromhex('c4005401'))
 def test_thread_only_after_lidata_retained(self):
  o=small_object(2,[(0xa2,0,leaf(2,b'A'))],b'\x40\x01');self.assertEqual(backend.initialized_view(o,1,policy=backend.POLICY).data,b'AA')
 def test_unknown_policy_marker_waiver_or_chunk_changes_fail(self):
  for mode in ['policy','marker','chunk']:
   o=small_object(3,[(0xa2,0,leaf(2,b'A')),(0xa0,2,b'B')]);policy=backend.POLICY
   if mode=='policy':policy='magic-zeros'
   elif mode=='marker':o.segments[1].unsupported_data=False
   else:o.segments[1].chunks=[(2,b'C')]
   with self.subTest(mode=mode),self.assertRaises(ValueError):backend.initialized_view(o,1,policy=policy)
 def test_32bit_a3_still_rejected_by_original_parser(self):
  with self.assertRaisesRegex(ValueError,'unsupported 32-bit'):small_object(2,[(0xa3,0,leaf(2,b'A'))])

class AuthenticProfileTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.units=json.loads((PROJECT/'config/units.json').read_text());cls.unit=next(u for u in cls.units if u['id']=='runtime_data_crt0dat_s3');cls.config,cls.module,cls.member,cls.obj=check.runtime_inputs(cls.unit,PROJECT);cls.ref=build_reference((PROJECT.parent/'CHESS.EXE').read_bytes())
 def test_guarded_generation_only_library_config_manifest(self):
  allowed={PROJECT/'config/runtime500.json',PROJECT/'toolchains/runtime500/manifest.json',PROJECT/'toolchains/runtime500/SLIBC.LIB'};seen=[];blocked=[];rb=Path.read_bytes;rt=Path.read_text
  def guard(fn,p,*a,**kw):
   p=Path(p).resolve()
   if p not in allowed:blocked.append(str(p));raise ValueError('forbidden generation read')
   seen.append(str(p));return fn(p,*a,**kw)
  with patch.object(Path,'read_bytes',lambda p,*a,**kw:guard(rb,p,*a,**kw)),patch.object(Path,'read_text',lambda p,*a,**kw:guard(rt,p,*a,**kw)):
   for p in [PROJECT.parent/'CHESS.EXE',PROJECT/'build/exepack/TRIM5_UNPACK.EXE']:
    with self.assertRaises(ValueError):p.read_bytes()
   _,module,member,obj=check.runtime_inputs(self.unit,PROJECT);data,fixes=check.link_runtime_segment(obj,module)
  self.assertEqual(len(data),80);self.assertEqual(H(member.data),backend.MEMBER_SHA);self.assertEqual(len(blocked),2);self.assertEqual(set(seen),{str(x)for x in allowed});self.assertEqual([f['mz_relocation_image_offset']for f in fixes if f['mz_relocation_image_offset']is not None],[0x61614])
 def test_whole_native80_and_exact_loader_evidence(self):
  data,fixes=check.link_runtime_segment(self.obj,self.module);self.assertEqual(data,self.ref['image'][0x615d0:0x61620]);self.assertEqual(check.validate_rea_extent(self.unit,PROJECT,ORIGINAL_SHA256,self.ref),'ev_0d0fd3101983252c4321d147639a07d113d3b9d55ed9f6dc798af19740f46201');self.assertEqual(len(fixes),2)
 def test_fresh_standard_build_one_unit_preserves_whole_obj(self):
  with tempfile.TemporaryDirectory()as tmp:
   out=Path(tmp);r=check.build_unit(self.unit,self.ref['image'],PROJECT,'unused',output=out,reference=self.ref)
   self.assertEqual(r['status'],'runtime_matched');self.assertEqual(r['authored_c_credit'],0);self.assertEqual((out/'runtime'/('runtime_data_crt0dat_s3.obj')).read_bytes(),self.member.data);self.assertEqual((out/'runtime'/('runtime_data_crt0dat_s3.bin')).read_bytes(),self.ref['image'][0x615d0:0x61620]);p=r['emitted_segment'];self.assertEqual((p['literal_initialized_bytes'],p['iterated_initialized_bytes'],p['BSS_or_hole_fill_bytes']),(60,20,0));self.assertEqual(p['iterated_ranges'],[[40,43],[43,45],[45,60]])
 def test_all_existing_sl_library_contributions_remain_exact(self):
  baseline=json.loads((PROJECT/'build/crt0dat80-runtime-lidata-stage/baseline454-report.json').read_text());old={x['id']:x for x in baseline['units']}
  historical={x['id']for x in baseline['units']if x['language']=='runtime'and x['backend']=='msc500-library'}
  current={x['id']for x in self.units if x['language']=='runtime'and x['backend']=='msc500-library'}
  self.assertEqual(current,historical|{self.unit['id'],'runtime_atol'})
  n=0
  for unit in self.units:
   if unit['id']not in historical:continue
   with self.subTest(unit=unit['id']):
    _,module,member,obj=check.runtime_inputs(unit,PROJECT);self.assertNotIn('initialized_record_policy',module);a,fields=check.link_runtime_segment(obj,module);b,bfields=library16.link_segment(obj,module['segment'],{int(k):v for k,v in module['segments'].items()},{int(k):v for k,v in module['groups'].items()},module['externals']);self.assertEqual(a,b);self.assertEqual(fields,bfields);self.assertEqual(H(a),old[unit['id']]['actual_sha256']);self.assertEqual(H(member.data),old[unit['id']]['object_sha256']);n+=1
  self.assertEqual(n,len(historical))
 def test_original_crt0dat_code_still367_and_same_raw_object(self):
  unit=next(u for u in self.units if u['id']=='runtime_crt0dat');_,module,member,obj=check.runtime_inputs(unit,PROJECT);data,fields=check.link_runtime_segment(obj,module);self.assertEqual(len(data),367);self.assertEqual(len(fields),43);self.assertEqual(member.data,self.member.data);self.assertTrue(obj.segments[3].unsupported_data)
 def test_unit_tampering_prefixes_and_symbols_rejected(self):
  for change in [{'size':79},{'size':True},{'symbol':'_invented'},{'image_offset':'0x615d1'},{'runtime_kind':'code'},{'member':'CRT0DAT'}]:
   with self.subTest(change=change),self.assertRaises(ValueError):check.runtime_inputs(self.unit|change,PROJECT)
 def test_profile_policy_placement_and_length_tampering_rejected(self):
  for key,val in [('initialized_record_policy','other'),('segment',1),('size',79),('groups',{'1':0x5cc3})]:
   p=copy.deepcopy(self.module);p[key]=val
   with self.subTest(key=key),self.assertRaises(ValueError):backend.link_segment(self.obj,p)
 def test_data_fixup_tampering_rejected(self):
  o=copy.deepcopy(self.obj);f=next(f for f in o.fixups if f.segment==3);o.fixups[o.fixups.index(f)]=dataclasses.replace(f,displacement=71)
  with self.assertRaisesRegex(ValueError,'two genuine'):backend.link_segment(o,self.module)
 def test_no_object_or_marker_mutation(self):
  before=copy.deepcopy(self.obj);a,_=backend.link_segment(self.obj,self.module);self.assertEqual(self.obj,before);self.assertTrue(self.obj.segments[3].unsupported_data);self.assertEqual(H(a),'96088d90384a6d3d7b84cd1b6165beccef73e6d8cff4a46b5b008874c0dcbeca')
 def test_missing_or_extra_native_mz_rejected(self):
  a,fields=backend.link_segment(self.obj,self.module)
  for changed in [[],fields+[fields[1]],fields[:1]]:
   with self.subTest(count=len(changed)),self.assertRaises(ValueError):backend.validate_evidence(self.unit,PROJECT,ORIGINAL_SHA256,self.ref,a,changed)
 def test_actual_lidata_checksum_and_record_bounds_rejected(self):
  for mode in ['checksum','truncated_length']:
   raw=bytearray(self.member.data)
   if mode=='checksum':raw[491+7]^=1
   else:raw[492:494]=bytes.fromhex('ffff')
   with self.subTest(mode=mode),self.assertRaises(ValueError):omf.read_omf(bytes(raw))
 def test_independent_library_and_member_pins_required(self):
  data=(PROJECT/'toolchains/runtime500/SLIBC.LIB').read_bytes()
  with self.assertRaisesRegex(ValueError,'member SHA'):library16.extract_member(data,'CRT0DAT',backend.LIBRARY_SHA,'0'*64)
  with self.assertRaisesRegex(ValueError,'library SHA'):library16.extract_member(data[:-1],'CRT0DAT',backend.LIBRARY_SHA,backend.MEMBER_SHA)
 def test_four_load_bases_whole80(self):
  a,fields=backend.link_segment(self.obj,self.module);native=self.ref['image'][0x615d0:0x61620];self.assertEqual(a,native)
  for base in [0,1,0x1000,0xffff]:
   out=bytearray(a);out[68:70]=((int.from_bytes(out[68:70],'little')+base)&65535).to_bytes(2,'little');self.assertEqual(out[:68],native[:68]);self.assertEqual(out[70:],native[70:]);self.assertEqual(int.from_bytes(out[68:70],'little'),(0x5cc2+base)&65535);self.assertEqual(out[66:68],bytes.fromhex('f649'))

if __name__=='__main__':unittest.main()
