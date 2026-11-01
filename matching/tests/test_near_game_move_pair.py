"""Actual two positive whole OMF fixtures; no generation in focused controls."""
from pathlib import Path
from dataclasses import replace
import copy,hashlib,json,unittest
import near_game_code16 as b
from omf import read_omf
class ClosedMovePair(unittest.TestCase):
 keys=('undo_animation327','animate_move363')
 def raw(self,k):return(Path(__file__).parent/'fixtures/near_game'/(k+'.obj')).read_bytes()
 def each(self):
  for k in self.keys:yield k,b.spec(k),self.raw(k)
 def test_actual_whole_objects(self):
  for k,s,r in self.each():self.assertEqual(len(b.extract_code(r,k)[0]),s['size'])
 def test_actual_all_fields(self):
  for k,s,r in self.each():self.assertEqual(len(read_omf(r).fixups),18 if k==self.keys[0]else 14)
 def test_source_identity(self):
  for k,s,r in self.each():b.source_policy((Path(b.__file__).parent/s['unit']['source']).read_bytes(),s['unit']['source'])
 def test_source_extra_instruction_rejected(self):
  for k,s,r in self.each():
   with self.assertRaises(ValueError):b.source_policy((Path(b.__file__).parent/s['unit']['source']).read_bytes()+b'\nNOP\n',s['unit']['source'])
 def test_wrong_source_route_rejected(self):
  with self.assertRaises(ValueError):b.source_policy(b'RET\n','asm/link/unknown.asm')
 def test_profiles_not_interchangeable(self):
  with self.assertRaises(ValueError):b.extract_code(self.raw(self.keys[0]),self.keys[1])
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
    code,logs=b.link_code(r,k,load);self.assertEqual(code,ref['image'][s['base']:s['base']+s['size']]);self.assertEqual(len(logs),18 if k==self.keys[0]else 14)
 def test_complete_owned_evidence(self):
  from reference import build_reference,ORIGINAL_SHA256
  P=Path(b.__file__).parent;ref=build_reference(Path('/home/kierzo/chess/CHESS.EXE').read_bytes())
  for k,s,r in self.each():self.assertTrue(b.validate_evidence(s['unit'],P,ORIGINAL_SHA256,ref))
 def test_zero_credit_and_no_new_STORAGE(self):
  for k,s,r in self.each():
   code,m=b.extract_code(r,k);self.assertEqual(m['C_credit'],0);self.assertEqual(m['DATA_byte_credit'],0);self.assertEqual(m['native_MZ'],[])

 def test_exact_CODE_alignments(self):
  for k,s,r in self.each():self.assertEqual(read_omf(r).segments[2].attributes,40 if k==self.keys[0]else 72)
 def test_wrong_CODE_alignment_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);o.segments[2].attributes=72 if k==self.keys[0]else 40
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_recursive_CALL_actual_form(self):
  o=read_omf(self.raw(self.keys[0]));f=next(q for q in o.fixups if q.target[0]==0)
  self.assertEqual((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement),(2,57,2,1,False,(0,2),(0,2),None))
 def test_recursive_CALL_target_rejected(self):
  o=read_omf(self.raw(self.keys[0]));i=next(i for i,q in enumerate(o.fixups)if q.target[0]==0);o.fixups[i]=replace(o.fixups[i],target=(0,1))
  with self.assertRaises(ValueError):b.validate_object(o,self.keys[0])
