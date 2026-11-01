"""Actual two positive whole OMF fixtures; no generation in focused controls."""
from pathlib import Path
from dataclasses import replace
import copy,hashlib,json,unittest
import near_game_code16 as b
from omf import read_omf
class ClosedSave610FAR(unittest.TestCase):
 keys=('save_cc72_610',)
 def raw(self,k):
  filename={'decode_frame_directory289':'decode_directory289'}.get(k,k)
  return(Path(__file__).parent/'fixtures/near_game'/(filename+'.obj')).read_bytes()
 def each(self):
  for k in self.keys:yield k,b.spec(k),self.raw(k)
 def test_actual_whole_objects(self):
  for k,s,r in self.each():self.assertEqual(len(b.extract_code(r,k)[0]),s['size'])
 def test_actual_all_fields(self):
  for k,s,r in self.each():self.assertEqual(len(read_omf(r).fixups),52)
 def test_source_identity(self):
  for k,s,r in self.each():b.source_policy((Path(b.__file__).parent/s['unit']['source']).read_bytes(),s['unit']['source'])
 def test_source_extra_instruction_rejected(self):
  for k,s,r in self.each():
   with self.assertRaises(ValueError):b.source_policy((Path(b.__file__).parent/s['unit']['source']).read_bytes()+b'\nNOP\n',s['unit']['source'])
 def test_wrong_source_route_rejected(self):
  with self.assertRaises(ValueError):b.source_policy(b'RET\n','asm/link/unknown.asm')
 def test_profiles_not_interchangeable(self):
  closed=('decode_frame_directory289', 'load_group_frames1030', 'load_asset_group178', 'undo_animation327', 'animate_move363', 'save_cc72_610')
  for actual in closed:
   for wrong in closed:
    if actual==wrong:continue
    with self.subTest(actual=actual,wrong=wrong):
     with self.assertRaises(ValueError):b.extract_code(self.raw(actual),wrong)
 def test_all_closed_6_whole_fixtures_regression(self):
  for key in ('decode_frame_directory289', 'load_group_frames1030', 'load_asset_group178', 'undo_animation327', 'animate_move363', 'save_cc72_610'):
   with self.subTest(profile=key):
    raw=self.raw(key);code,metadata=b.extract_code(raw,key);self.assertEqual(len(code),b.spec(key)['size']);self.assertEqual(hashlib.sha256(raw).hexdigest(),b.spec(key)['object_sha256'])
 def test_checksum_rejected(self):
  for k,s,r in self.each():
   with self.assertRaises(ValueError):b.extract_code(r[:-1]+bytes([r[-1]^1]),k)
 def test_truncation_rejected(self):
  for k,s,r in self.each():
   with self.assertRaises(ValueError):b.extract_code(r[:-1],k)
 def test_unknown_profile_rejected(self):
  with self.assertRaises(ValueError):b.spec('load_unknown')
 def test_unit_extent_rejected(self):
  for k,s,r in self.each():
   u=copy.deepcopy(s['unit']);u['size']+=1
   with self.assertRaises(ValueError):b.validate_unit(u)
 def test_unit_extra_key_rejected(self):
  for k,s,r in self.each():
   u=copy.deepcopy(s['unit']);u['waiver']=True
   with self.assertRaises(ValueError):b.validate_unit(u)
 def test_unit_wrong_symbol_rejected(self):
  for k,s,r in self.each():
   u=copy.deepcopy(s['unit']);u['public_symbols']=['_alias']
   with self.assertRaises(ValueError):b.validate_unit(u)
 def test_unit_wrong_native_binding_rejected(self):
  for k,s,r in self.each():
   u=copy.deepcopy(s['unit']);n=next(iter(u['externals']));u['externals'][n]+=1
   with self.assertRaises(ValueError):b.validate_unit(u)
 def test_raw_records_missing_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);o.records=o.records[:-1]
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_raw_records_payload_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);z,at,p=o.records[0];o.records[0]=(z,at,p+b'x')
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_CODE_hole_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);at,p=o.segments[2].chunks[0];o.segments[2].chunks[0]=(1,p)
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_CODE_byte_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);at,p=o.segments[2].chunks[0];o.segments[2].chunks[0]=(at,bytes([p[0]^1])+p[1:])
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_CODE_extent_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);o.segments[2].length+=1
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_DATA_allocation_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);o.segments[1].length=1
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_PUBLIC_alias_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);o.publics['_alias']=next(iter(o.publics.values()))
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_PUBLIC_frame_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);n=next(iter(o.publics));o.publics[n]=replace(o.publics[n],group=1)
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_missing_FIXUP_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);o.fixups=o.fixups[:-1]
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_FIXUP_frame_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);o.fixups[0]=replace(o.fixups[0],frame=(5,None))
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_FIXUP_target_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);o.fixups[0]=replace(o.fixups[0],target=(2,65535))
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_FIXUP_displacement_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);o.fixups[0]=replace(o.fixups[0],displacement=(o.fixups[0].displacement or 0)+1)
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_wrong_load_rejected(self):
  for k,s,r in self.each():
   with self.assertRaises(ValueError):b.link_code(r,k,65536)
 def test_full_native_fourbases(self):
  from reference import build_reference
  ref=build_reference(Path('/home/kierzo/chess/CHESS.EXE').read_bytes())
  for k,s,r in self.each():
   for load in[0,1,4096,65535]:
    code,logs=b.link_code(r,k,load);expected=bytearray(ref['image'][s['base']:s['base']+s['size']])
    for site in s['native_MZ']:
     at=site-s['base'];expected[at:at+2]=((int.from_bytes(expected[at:at+2],'little')+load)&65535).to_bytes(2,'little')
    self.assertEqual(code,expected);self.assertEqual(len(logs),52)
    self.assertEqual(sorted(q['mz_segment_relocation_image_offset']for q in logs if 'mz_segment_relocation_image_offset'in q),s['native_MZ'])
 def test_complete_owned_evidence(self):
  from reference import build_reference,ORIGINAL_SHA256
  ref=build_reference(Path('/home/kierzo/chess/CHESS.EXE').read_bytes())
  for k,s,r in self.each():self.assertTrue(b.validate_evidence(s['unit'],Path(b.__file__).parent,ORIGINAL_SHA256,ref))
 def test_zero_credit_no_storage(self):
  for k,s,r in self.each():
   _,m=b.extract_code(r,k);self.assertEqual(m['C_credit'],0);self.assertEqual(m['DATA_byte_credit'],0);self.assertEqual(len(m['native_MZ']),6)
 def test_all_six_actual_FAR_frames(self):
  o=read_omf(self.raw(self.keys[0]));far=[f for f in o.fixups if f.width==4]
  self.assertEqual(len(far),6)
  for f in far:self.assertEqual((f.location_type,f.segment_relative,f.frame),(3,True,(2,f.target[1])))
 def test_each_far_frame_rejected(self):
  raw=self.raw(self.keys[0]);o=read_omf(raw)
  for i,f in enumerate(o.fixups):
   if f.width==4:
    q=read_omf(raw);q.fixups[i]=replace(f,frame=(5,None))
    with self.assertRaises(ValueError):b.validate_object(q,self.keys[0])
 def test_each_far_width_rejected(self):
  raw=self.raw(self.keys[0]);o=read_omf(raw)
  for i,f in enumerate(o.fixups):
   if f.width==4:
    q=read_omf(raw);q.fixups[i]=replace(f,width=2)
    with self.assertRaises(ValueError):b.validate_object(q,self.keys[0])
 def test_missing_native_MZ_rejected(self):
  s=b.spec(self.keys[0])
  with self.assertRaises(ValueError):b._sites(s,s['native_MZ'][:-1])
 def test_extra_native_MZ_rejected(self):
  s=b.spec(self.keys[0])
  with self.assertRaises(ValueError):b._sites(s,s['native_MZ']+[s['base']])
 def test_crossing_native_MZ_rejected(self):
  s=b.spec(self.keys[0])
  with self.assertRaises(ValueError):b._sites(s,s['native_MZ']+[s['base']-1])
 def test_actual_CODE_alignment_WORD(self):self.assertEqual(read_omf(self.raw(self.keys[0])).segments[2].attributes,72)
 def test_V1_failure_and_V2_are_distinct(self):
  s=b.spec(self.keys[0]);P=Path(b.__file__).parent/s['evidence_root'];negative=json.loads((P/'V1-negative-binder.json').read_text());self.assertTrue(negative)
  g=json.loads((P/'generation.json').read_text());self.assertEqual(g['actual_MASM_calls'],1);self.assertEqual(g['status'],'COMPLETE')
