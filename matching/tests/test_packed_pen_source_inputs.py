"""Closed BYTEprovider; all generated files live under TemporaryDirectory."""
from pathlib import Path
import copy,dataclasses,hashlib,json,sys,tempfile,unittest
from unittest.mock import patch
PROJECT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(PROJECT))
import source_inputs
import packed_pen_source_inputs as profile
from omf import read_omf
D=PROJECT/'build/packed-pen-common-profile-stage';FIXTURE=PROJECT/'build/pen8172-boundary-identity'
class PackedPenCommonTests(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  assert Path(profile.__file__)==PROJECT/'packed_pen_source_inputs.py'
  assert Path(source_inputs.__file__)==PROJECT/'source_inputs.py'
  c.item=json.loads((D/'proposed-source-input.json').read_text());c.data=(FIXTURE/'provider.obj').read_bytes()
 def mutate(self,kind,fn,*,occurrence=0):
  records=read_omf(self.data).records;out=bytearray();seen=0
  for k,at,p in records:
   if k==kind:
    if seen==occurrence:p=fn(p)
    seen+=1
   raw=bytes([k])+(len(p)+1).to_bytes(2,'little')+p;out.extend(raw+bytes([-sum(raw)&255]))
  return bytes(out)
 def bad(self,raw,regex=None):
  with self.assertRaisesRegex(ValueError,regex)if regex else self.assertRaises(ValueError):profile.validate_object(raw)
 def test_actual_BYTE1_no_loaded_PUBLIC_or_function(self):
  self.assertEqual(profile.validate_object(self.data),[{'symbol':'_packed_pen','type_index':132,'datatype':98,'size':1}]);o=read_omf(self.data);self.assertFalse(o.publics);self.assertFalse(o.procedures);self.assertTrue(all(s.length==0 for s in o.segments.values()if s.class_name not in ['DEBSYM','DEBTYP']))
 def test_builtin_BYTE_debug_and_sole_debug_field(self):
  o=read_omf(self.data);self.assertEqual(o.segments[5].chunks,[(0,bytes.fromhex('12050000000084000a7061636b65645f70656e'))]);self.assertEqual(o.externals,{1:'__acrtused',2:'_packed_pen'});self.assertEqual([(f.segment,f.offset,f.width,f.target)for f in o.fixups],[(5,2,4,(2,2))])
 def test_wrong_size2_and_zero_size_rejected(self):
  for size in [0,2]:self.bad(self.mutate(0xb0,lambda p:p[:-1]+bytes([size])),'COMDEF')
 def test_signed_and_WORD_type_rejected(self):
  for typ in [0x80,0x81]:self.bad(self.mutate(0xb0,lambda p:p[:-3]+bytes([typ])+p[-2:]),'COMDEF')
 def test_far_or_unsupported_storage_rejected(self):
  for mode in [0x61,0x63]:self.bad(self.mutate(0xb0,lambda p:p[:-2]+bytes([mode])+p[-1:]))
 def test_extra_or_duplicate_definition_rejected(self):
  self.bad(self.mutate(0xb0,lambda p:p+p),'COMDEF')
 def test_alias_name_and_zero_length_symbol_rejected(self):
  self.bad(self.mutate(0xb0,lambda p:p.replace(b'_packed_pen',b'_search_end')))
  self.bad(self.mutate(0xb0,lambda p:bytes([0])+p[12:]))
 def test_wrong_loaded_CODE_DATA_or_BSS_size_rejected(self):
  for i in [0,1,3]:self.bad(self.mutate(0x98,lambda p:p[:1]+b'\x01\0'+p[3:],occurrence=i),'allocation')
 def test_checksum_truncation_EOF_and_rawtype_rejected(self):
  for raw in [self.data[:-1],self.data+b'\0',bytes([self.data[0]^1])+self.data[1:],bytearray(self.data)]:self.bad(raw)
 def test_DGROUP_and_producer_filename_changed_rejected(self):
  self.bad(self.mutate(0x9a,lambda p:p[:-1]+b'\x03'),'DGROUP');self.bad(self.mutate(0x80,lambda p:p.replace(b'UNIT.C',b'FAKE.C')),'filename')
 def test_debug_type_or_patch_bytes_changed_rejected(self):
  self.bad(self.mutate(0xa0,lambda p:p[:9]+b'\x81'+p[10:]),'debug');self.bad(self.mutate(0x9c,lambda p:p[:-1]+b'\x03',occurrence=1))
 def test_record_removal_and_extra_foreign_record_rejected(self):
  records=read_omf(self.data).records;extra=b'\xc2\x02\0\0';extra+=bytes([-sum(extra)&255]);self.bad(self.data[:-4]+extra+self.data[-4:])
 def test_exact_item_rejects_source_size_alias_capacity(self):
  profile.validate_item(self.item)
  for delta in [{'source':'../elsewhere.c'},{'source_sha256':'0'*64},{'compiler':'msc510'},{'flags':['/AM']},{'capacity':48},{'objects':[{'symbol':'_search_stack_end','size':1,'storage':'near-common'}]},{'objects':[{'symbol':'_packed_pen','size':True,'storage':'near-common'}]}]:
   with self.subTest(delta=delta),self.assertRaises(ValueError):profile.validate_item(dict(self.item,**delta))
 def test_wrong_evidence_pin_and_target_rejected(self):
  item=copy.deepcopy(self.item);item['evidence']['crt']['sha256']='0'*64
  with self.assertRaises(ValueError):profile.validate_item(item)
  with tempfile.TemporaryDirectory()as tmp:
   target=Path(tmp)/'bad.exe';target.write_bytes(b'MZbad')
   with self.assertRaises(ValueError):profile.validate_evidence(PROJECT,self.item['evidence'],target)
 def test_native_BYTE_and_address_sentinel_no_capacity(self):
  p=profile.validate_evidence(PROJECT,self.item['evidence'],PROJECT.parent/'CHESS.EXE');self.assertEqual(p[0]['dgroup_offset'],'0x8172');self.assertEqual(p[0]['end_exclusive'],'0x8173');self.assertFalse(p[0]['resolved']);self.assertFalse(p[0]['search_array_capacity_proven'])
 def test_escape_and_absolute_path_rejected(self):
  for name in ['../CHESS.EXE','/tmp/source.c']:
   with self.assertRaises(ValueError):profile.local(PROJECT,name)
 def test_changed_source_rejected_before_compiler(self):
  with tempfile.TemporaryDirectory()as tmp:
   p=Path(tmp);src=p/profile.SOURCE;src.parent.mkdir(parents=True);src.write_text('int packed_pen;\n')
   with patch.object(profile,'compile_c',side_effect=AssertionError('must not compile')),self.assertRaisesRegex(ValueError,'source hash'):profile.build_input(self.item,p,PROJECT.parent/'CHESS.EXE',p/'out')
 def test_duplicate_symbol_precedes_generation(self):
  with tempfile.TemporaryDirectory()as tmp:
   p=Path(tmp);cfg=p/'cfg.json';cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[self.item]}))
   with patch.object(source_inputs,'compile_c',side_effect=AssertionError('must not compile')),self.assertRaisesRegex(ValueError,'duplicate allocation symbol'):source_inputs.build_source_inputs(PROJECT,PROJECT.parent/'CHESS.EXE',p/'out',config_path=cfg,defined_symbols={'_packed_pen'})
 def test_duplicate_item_guard_preserves_dispatch_semantics(self):
  # Route-only control; actual fresh production proof is separate and never stubbed.
  with tempfile.TemporaryDirectory()as tmp:
   p=Path(tmp);cfg=p/'cfg.json';cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[self.item,self.item]}))
   with patch.object(profile,'build_input',return_value={'id':self.item['id']})as fn,self.assertRaisesRegex(ValueError,'duplicate source allocation'):source_inputs.build_source_inputs(PROJECT,PROJECT.parent/'CHESS.EXE',p/'out',config_path=cfg)
   self.assertEqual(fn.call_count,1)
 def test_client_proof_keeps_all_allocations_and_held80(self):
  p=json.loads((FIXTURE/'proof.json').read_text());self.assertEqual(len(p['generation']),3);self.assertEqual([r['selected_functions']for r in p['source_controls']],[19,1]);self.assertTrue(all(r['all_loaded_CODE_DATA_CONST_BSS_bytes_equal']for r in p['source_controls']));self.assertEqual(p['source_controls'][0]['whole_CODE_length'],5350);self.assertEqual(len(p['source_controls'][0]['whole_native_byte_differences']),3);self.assertFalse(p['source_controls'][0]['whole_native_matches'])
 def test_PUBLIC_alias_and_missing_COMDEF_rejected(self):
  def enc(k,p):
   raw=bytes([k])+(len(p)+1).to_bytes(2,'little')+p;return raw+bytes([-sum(raw)&255])
  records=read_omf(self.data).records;raw=b''.join(enc(k,p)for k,at,p in records if k!=0xb0);self.bad(raw)
  raw=self.data[:-4]+enc(0x90,bytes.fromhex('00040000')+b'\x0b_packed_pen'+bytes.fromhex('8084'))+self.data[-4:];self.bad(raw)
 def test_wrong_fresh_compiler_provenance_rejected(self):
  from msc import CompileResult
  proof=json.loads((FIXTURE/'proof.json').read_text());meta=next(g['compiler']for g in proof['generation']if g['name']=='provider');c=CompileResult(object_bytes=self.data,**meta)
  for delta in [{'compiler':'msc510'},{'source_name':'FAKE.C'},{'flags':['/AS']},{'toolchain_manifest_sha256':'0'*64},{'tool_hashes':{}}]:
   wrong=dataclasses.replace(c,**delta)
   with tempfile.TemporaryDirectory()as tmp,self.subTest(delta=delta),self.assertRaisesRegex(ValueError,'provenance'):
    profile.build_input(self.item,PROJECT,PROJECT.parent/'CHESS.EXE',Path(tmp)/'out',compiler_fn=lambda *a,**k:wrong)
 def test_all16_existing_profile_objects_validate_unchanged(self):
  import importlib
  old=PROJECT/'build/menu-paused-common-followup';rows=json.loads((old/'old-profile-compatibility-inputs.json').read_text());self.assertEqual(len(rows),16)
  for r in rows:
   raw=(old/r['object']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),r['sha256']);defs=importlib.import_module(r['module']).validate_object(raw);self.assertEqual([d['symbol']for d in defs],[d['symbol']for d in r['definitions']])
if __name__=='__main__':unittest.main(verbosity=2)
