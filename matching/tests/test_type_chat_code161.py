"""Actual469 chat161 integrity/native/ABI controls; no compiler/MASM/LINK."""
from pathlib import Path
from dataclasses import replace
import copy,json,unittest,tempfile
import input_dialog_code16 as b
from omf import read_omf,OMFError
F=Path(__file__).parent/'fixtures/input_dialog';K='type_chat161'
def raw():return(F/'chat161.obj').read_bytes()
def obj():return read_omf(raw())
def unit():return copy.deepcopy(b.spec(K)['unit'])
class TypeChat161Tests(unittest.TestCase):
 def reject(self,o):
  with self.assertRaises(OMFError):b.validate_object(o,K)
 def evidence(self):return b._evidence(Path(__file__).parents[1],K)
 def test_actual469_whole161(self):self.assertEqual(len(raw()),469);self.assertEqual(len(b.extract_code(raw(),K)[0]),161)
 def test_old_four_profiles_and_label_exact(self):
  old=json.loads((F/'chat161-parent-profiles.json').read_text());now=b.profiles();self.assertEqual(now['label'],old['label'])
  for k,v in old['ASM'].items():self.assertEqual(now['ASM'][k],v)
 def test_BYTE_attribute(self):self.assertEqual(obj().segments[2].attributes,40)
 def test_prior_alignment_contracts_unchanged(self):
  for k,a in [('input_number306',72),('dialog_button152',72),('select_mode84',40),('init_rays185',72)]:self.assertEqual(b.spec(k)['snapshot']['segments']['2']['attributes'],a)
 def test_exact161(self):self.assertEqual(obj().segments[2].length,161)
 def test_odd_native_entry_and_end(self):self.assertEqual((b.spec(K)['base'],b.spec(K)['base']+b.spec(K)['size']),(0x14c1,0x1562))
 def test_exact73(self):self.assertEqual(b.spec(K)['instructions'],73)
 def test_one_real_PUBLIC0(self):p=obj().publics['_type_chat_14c1'];self.assertEqual((set(obj().publics),p.segment,p.offset,p.group,p.type_index),({'_type_chat_14c1'},2,0,0,0))
 def test_eight_realexterns(self):self.assertEqual(set(obj().externals.values()),{'__chkstk','_begin_input_0fb0','_end_input_102d','_fill_region_1780','_text_input_1064','_restore_region_58b0','_write_bytes_dbb5','_menu_state'})
 def test_all9external_fields(self):self.assertEqual(len(obj().fixups),9);self.assertTrue(all(f.target[0]==2 for f in obj().fixups));self.assertEqual(len({f.offset for f in obj().fixups}),9)
 def test_eight_nearCALL_oneDS(self):self.assertEqual([sum(x['kind']==k for x in b.spec(K)['external_fields'])for k in ['near-CALL','DGROUP']],[8,1])
 def test_nointernal_fields(self):self.assertEqual(b.spec(K)['internal_fields'],[])
 def test_frame48_and_message_BP40(self):
  code=b.link_code(raw(),K)[0];self.assertEqual(code[3:6],bytes.fromhex('b83000'));self.assertIn(bytes.fromhex('8d46d8'),code);self.assertIn(bytes.fromhex('c647d80d'),code)
 def test_complete_native161(self):self.assertEqual(b.link_code(raw(),K)[0],(F/'chat161.native.bin').read_bytes())
 def test_fourbases_noMZ(self):
  for load in[0,1,4096,65535]:
   code,logs=b.link_code(raw(),K,load);self.assertEqual(code,(F/'chat161.native.bin').read_bytes());self.assertEqual(len(logs),9);self.assertFalse(any('mz_segment_relocation_image_offset'in x for x in logs))
 def test_nativeMZ_empty(self):self.assertEqual(b.spec(K)['native_MZ'],[])
 def test_crossing_MZ_rejected(self):
  with self.assertRaises(OMFError):b._sites(b.spec(K),[0x14c0])
 def test_interior_MZ_rejected(self):
  with self.assertRaises(OMFError):b._sites(b.spec(K),[0x14c8])
 def test_exact_unit(self):b.validate_unit(unit())
 def test_wrong_size(self):
  u=unit();u['size']=160
  with self.assertRaises(OMFError):b.validate_unit(u)
 def test_wrong_source(self):
  u=unit();u['source']='other.asm'
  with self.assertRaises(OMFError):b.validate_unit(u)
 def test_wrong_PUBLIC(self):
  u=unit();u['public_symbols']=['_alias']
  with self.assertRaises(OMFError):b.validate_unit(u)
 def test_cross_profile(self):
  with self.assertRaises(OMFError):b.extract_code(raw(),'select_mode84')
 def test_unknown_profile(self):
  with self.assertRaises(OMFError):b.spec('chat-other')
 def test_wrong_source_hash(self):
  with self.assertRaises(OMFError):b.source_policy(b'variant','asm/link/type_chat14c1.asm')
 def test_exact_source_policy(self):b.source_policy((Path(__file__).parents[1]/'asm/link/type_chat14c1.asm').read_bytes(),'asm/link/type_chat14c1.asm')
 def test_WORD_rejected(self):o=obj();o.segments[2].attributes=72;self.reject(o)
 def test_extra_DATA_rejected(self):o=obj();o.segments[1].length=1;self.reject(o)
 def test_alias_PUBLIC_rejected(self):o=obj();o.publics['_alias']=o.publics['_type_chat_14c1'];self.reject(o)
 def test_frame40_variant_rejected(self):
  o=obj();at,c=o.segments[2].chunks[0];v=bytearray(c);v[4]=40;o.segments[2].chunks[0]=(at,bytes(v));self.reject(o)
 def test_NOP_tail_rejected(self):
  o=obj();at,c=o.segments[2].chunks[0];o.segments[2].chunks[0]=(at,c+b'\x90');o.segments[2].length+=1;self.reject(o)
 def test_each_field_frame_rejected(self):
  for i,f in enumerate(obj().fixups):
   with self.subTest(offset=f.offset):o=obj();o.fixups[i]=replace(o.fixups[i],frame=(5,None));self.reject(o)
 def test_each_field_displacement_rejected(self):
  for i,f in enumerate(obj().fixups):
   with self.subTest(offset=f.offset):o=obj();o.fixups[i]=replace(o.fixups[i],displacement=1);self.reject(o)
 def test_each_field_width_rejected(self):
  for i,f in enumerate(obj().fixups):
   with self.subTest(offset=f.offset):o=obj();o.fixups[i]=replace(o.fixups[i],width=4);self.reject(o)
 def test_checksum_rejected(self):
  r=bytearray(raw());r[-1]^=1
  with self.assertRaises(OMFError):b.extract_code(bytes(r),K)
 def test_actual_evidence_closure(self):self.assertTrue(self.evidence())
 def test_changed_context_evidence_rejected(self):
  from input_dialog_code_pins import EVIDENCE_PINS
  with tempfile.TemporaryDirectory()as td:
   root=Path(td)
   for n in EVIDENCE_PINS[K]:p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((Path(__file__).parents[1]/n).read_bytes())
   p=root/b.spec(K)['evidence_root']/'full-context.json';p.write_bytes(p.read_bytes()+b' ')
   with self.assertRaises(OMFError):b._evidence(root,K)
 def test_two_callers_eight_providers_and_held_negatives(self):
  a=json.loads((Path(__file__).parents[1]/b.spec(K)['evidence_root']/'namespace-and-ABI.json').read_text());self.assertEqual((len(a['actual_current_callers']),len(a['existing_real_providers'])),(2,8));self.assertTrue(a['minimum_buffer38_C_frame40_vs_native48_negative_preserved']);self.assertTrue(a['two_meaningful_live_counts_CODE288_CV287_tail90_negative_preserved']);self.assertTrue(a['whole_C_tail90_never_reused_or_trimmed'])
 def test_original_full_context_is_real285_read(self):
  e=self.evidence()[b.spec(K)['evidence_root']+'/full-context.json'];self.assertEqual(e['operation'],'read_bytes');self.assertEqual((e['parameters']['address'],e['parameters']['length']),('0x11446',285));self.assertEqual(e['subject']['digest']['sha256'],b.ORIGINAL_SHA256)
 def test_zero_credit_and_no_historicallanguage_claim(self):
  _,m=b.extract_code(raw(),K);self.assertEqual((m['C_credit'],m['DATA_byte_credit']),(0,0));self.assertFalse(m['historical_language_TU_or_C_unrepresentability_proven'])
if __name__=='__main__':unittest.main()
