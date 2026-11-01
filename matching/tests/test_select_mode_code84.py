"""Actual select84 fixture only; no generation, fake positive objects, or LINK."""
from pathlib import Path
from dataclasses import replace
import copy,json,unittest
from unittest.mock import patch
import input_dialog_code16 as b
from omf import read_omf,OMFError
F=Path(__file__).parent/'fixtures/input_dialog'
K='select_mode84'
def raw():return (F/'select84.obj').read_bytes()
def unit():return copy.deepcopy(b.spec(K)['unit'])
class Select84Tests(unittest.TestCase):
 def reject(self,o):
  with self.assertRaises(OMFError):b.validate_object(o,K)
 def test_actual_whole292(self):self.assertEqual(len(raw()),292);self.assertEqual(len(b.extract_code(raw(),K)[0]),84)
 def test_old_profiles_and_label_exact(self):
  parent=json.loads((F/'select84-parent-profiles.json').read_text());now=b.profiles();self.assertEqual(now['label'],parent['label'])
  for k,v in parent['ASM'].items():self.assertEqual(now['ASM'][k],v)
 def test_BYTE_only_exact_new_spec(self):self.assertEqual(b.spec(K)['snapshot']['segments']['2']['attributes'],40)
 def test_old_WORD_specs_preserved(self):
  for k in ['input_number306','dialog_button152']:self.assertEqual(b.spec(k)['snapshot']['segments']['2']['attributes'],72)
 def test_odd_native_extent(self):self.assertEqual((b.spec(K)['base'],b.spec(K)['base']+b.spec(K)['size']),(0x17f9,0x184d))
 def test_exact26(self):self.assertEqual(b.spec(K)['instructions'],26)
 def test_public(self):self.assertEqual(set(read_omf(raw()).publics),{'_select_mode'})
 def test_exact_unit(self):b.validate_unit(unit())
 def test_wrong_size(self):
  u=unit();u['size']=83
  with self.assertRaises(OMFError):b.validate_unit(u)
 def test_wrong_source(self):
  u=unit();u['source']='other.asm'
  with self.assertRaises(OMFError):b.validate_unit(u)
 def test_cross_profile(self):
  with self.assertRaises(OMFError):b.extract_code(raw(),'dialog_button152')
 def test_raw_checksum_change(self):
  r=bytearray(raw());r[-1]^=1
  with self.assertRaises(OMFError):b.extract_code(bytes(r),K)
 def test_WORD_alignment_rejected(self):
  o=read_omf(raw());o.segments[2].attributes=72;self.reject(o)
 def test_extra_DATA_rejected(self):
  o=read_omf(raw());o.segments[1].length=1;self.reject(o)
 def test_extra_PUBLIC_rejected(self):
  o=read_omf(raw());o.publics['_alias']=o.publics['_select_mode'];self.reject(o)
 def test_local_store_change(self):
  o=read_omf(raw());at,c=o.segments[2].chunks[0];v=bytearray(c);v[25]^=1;o.segments[2].chunks[0]=(at,bytes(v));self.reject(o)
 def test_tail_rejected(self):
  o=read_omf(raw());o.segments[2].length+=1;self.reject(o)
 def test_each_field_frame_rejected(self):
  for i in range(5):
   o=read_omf(raw());o.fixups[i]=replace(o.fixups[i],frame=(5,None));self.reject(o)
 def test_each_field_width_rejected(self):
  for i in range(5):
   o=read_omf(raw());o.fixups[i]=replace(o.fixups[i],width=1);self.reject(o)
 def test_five_fields(self):self.assertEqual([f.offset for f in read_omf(raw()).fixups],[7,17,42,70,75])
 def test_two_MZ(self):self.assertEqual(b.spec(K)['native_MZ'],[0x1841,0x1846])
 def test_fourbases_complete(self):
  base,_=b.link_code(raw(),K)
  for load in [0,1,4096,65535]:
   linked,logs=b.link_code(raw(),K,load);wanted=bytearray(base)
   for site in b.spec(K)['native_MZ']:
    p=site-0x17f9;wanted[p:p+2]=((int.from_bytes(wanted[p:p+2],'little')+load)&65535).to_bytes(2,'little')
   self.assertEqual(linked,wanted);self.assertEqual(len(logs),5)
 def test_complete_native_hash(self):self.assertEqual(b.H(b.link_code(raw(),K)[0]),b.spec(K)['native_sha256'])
 def test_boundary_MZ_not_waived(self):
  with self.assertRaises(OMFError):b._sites(b.spec(K),[0x1841,0x1846,0x17f8])
 def test_missing_MZ_rejected(self):
  with self.assertRaises(OMFError):b._sites(b.spec(K),[0x1841])
 def test_unknown_profile_rejected(self):
  with self.assertRaises(OMFError):b.spec('select84-other')
 def test_source_hash_rejected(self):
  with self.assertRaises(OMFError):b.source_policy(b'; source variant','asm/link/select_mode17f9.asm')
 def test_no_credit(self):
  _,m=b.extract_code(raw(),K);self.assertEqual((m['C_credit'],m['DATA_byte_credit']),(0,0));self.assertFalse(m['historical_language_TU_or_C_unrepresentability_proven'])
 def test_real_FAR_providers(self):self.assertEqual([x['symbol']for x in b.spec(K)['external_fields']if x['kind']=='FAR-CALL'],['_graphics_begin','_graphics_end'])
 def test_complete_owned_evidence_scope(self):
  from input_dialog_code_pins import EVIDENCE_PINS
  self.assertEqual(len(EVIDENCE_PINS[K]),9)
 def test_actual_evidence_closure(self):b._evidence(Path(__file__).parents[1],K)
 def test_changed_owned_evidence_rejected(self):
  import tempfile,shutil
  from input_dialog_code_pins import EVIDENCE_PINS
  with tempfile.TemporaryDirectory()as td:
   root=Path(td)
   for n in EVIDENCE_PINS[K]:
    p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((Path(__file__).parents[1]/n).read_bytes())
   p=root/b.spec(K)['evidence_root']/'operand-contract.json';p.write_bytes(p.read_bytes()+b' ')
   with self.assertRaises(OMFError):b._evidence(root,K)
if __name__=='__main__':unittest.main()
