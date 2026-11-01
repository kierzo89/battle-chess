"""Genuine raw484 init185 fixture controls; no compiler/assembler/LINK."""
from pathlib import Path
from dataclasses import replace
import copy,json,unittest,tempfile
import input_dialog_code16 as b
from omf import read_omf,OMFError
F=Path(__file__).parent/'fixtures/input_dialog';K='init_rays185'
def raw():return(F/'rays185.obj').read_bytes()
def obj():return read_omf(raw())
def unit():return copy.deepcopy(b.spec(K)['unit'])
class InitRays185Tests(unittest.TestCase):
 def reject(self,o):
  with self.assertRaises(OMFError):b.validate_object(o,K)
 def test_actual484_whole185(self):self.assertEqual(len(raw()),484);self.assertEqual(len(b.extract_code(raw(),K)[0]),185)
 def test_old_three_profiles_and_label_exact(self):
  old=json.loads((F/'rays185-parent-profiles.json').read_text());now=b.profiles();self.assertEqual(now['label'],old['label'])
  for k,v in old['ASM'].items():self.assertEqual(now['ASM'][k],v)
 def test_new_WORD_attribute(self):self.assertEqual(obj().segments[2].attributes,72)
 def test_select_BYTE_unchanged(self):self.assertEqual(b.spec('select_mode84')['snapshot']['segments']['2']['attributes'],40)
 def test_size_185(self):self.assertEqual(obj().segments[2].length,185)
 def test_native_complete_extent(self):self.assertEqual((b.spec(K)['base'],b.spec(K)['base']+b.spec(K)['size']),(0x9840,0x98f9))
 def test_actual70(self):self.assertEqual(b.spec(K)['instructions'],70)
 def test_one_real_PUBLIC0(self):p=obj().publics['_init_rays'];self.assertEqual((set(obj().publics),p.segment,p.offset,p.group,p.type_index),({'_init_rays'},2,0,0,0))
 def test_four_realexterns(self):self.assertEqual(set(obj().externals.values()),{'__chkstk','_fill_8a96','_move_lookup_tables','_rays'})
 def test_exact20fields(self):self.assertEqual(len(obj().fixups),20);self.assertEqual(len({f.offset for f in obj().fixups}),20)
 def test_external18_internal2(self):self.assertEqual([sum(f.target[0]==k for f in obj().fixups)for k in[2,0]],[18,2])
 def test_source_addends_in_actual_FIXUPP(self):
  o=obj();c=o.segments[2].chunks[0][1];self.assertTrue(all(c[f.offset:f.offset+2]==b'\0\0'for f in o.fixups));self.assertEqual([f.displacement for f in o.fixups if f.offset in[80,151,166,174]],[476,476,476,478])
 def test_two_actual_internal_nearJMP(self):self.assertEqual([(f.offset,f.frame,f.target,f.displacement)for f in obj().fixups if f.target[0]==0],[(45,(0,2),(0,2),179),(177,(0,2),(0,2),35)])
 def test_complete_native185(self):self.assertEqual(b.link_code(raw(),K)[0],(F/'rays185.native.bin').read_bytes())
 def test_four_load_bases_noMZ(self):
  for load in[0,1,4096,65535]:
   code,logs=b.link_code(raw(),K,load);self.assertEqual(code,(F/'rays185.native.bin').read_bytes());self.assertEqual(len(logs),20);self.assertFalse(any('mz_segment_relocation_image_offset'in x for x in logs))
 def test_native_MZ_empty(self):self.assertEqual(b.spec(K)['native_MZ'],[])
 def test_crossing_MZ_rejected(self):
  with self.assertRaises(OMFError):b._sites(b.spec(K),[0x983f])
 def test_interior_MZ_rejected(self):
  with self.assertRaises(OMFError):b._sites(b.spec(K),[0x9847])
 def test_exact_unit(self):b.validate_unit(unit())
 def test_wrong_size(self):
  u=unit();u['size']=184
  with self.assertRaises(OMFError):b.validate_unit(u)
 def test_wrong_source(self):
  u=unit();u['source']='other.asm'
  with self.assertRaises(OMFError):b.validate_unit(u)
 def test_wrong_public(self):
  u=unit();u['public_symbols']=['_alias']
  with self.assertRaises(OMFError):b.validate_unit(u)
 def test_cross_profile(self):
  with self.assertRaises(OMFError):b.extract_code(raw(),'select_mode84')
 def test_unknown_profile(self):
  with self.assertRaises(OMFError):b.spec('init_rays-other')
 def test_wrong_source_hash(self):
  with self.assertRaises(OMFError):b.source_policy(b'variant','asm/link/init_rays9840.asm')
 def test_exact_source_policy(self):b.source_policy((Path(__file__).parents[1]/'asm/link/init_rays9840.asm').read_bytes(),'asm/link/init_rays9840.asm')
 def test_BYTE_rejected_for185(self):o=obj();o.segments[2].attributes=40;self.reject(o)
 def test_extra_DATA_rejected(self):o=obj();o.segments[1].length=1;self.reject(o)
 def test_extra_PUBLIC_rejected(self):o=obj();o.publics['_alias']=o.publics['_init_rays'];self.reject(o)
 def test_frame8_instruction_change(self):
  o=obj();at,c=o.segments[2].chunks[0];v=bytearray(c);v[4]=6;o.segments[2].chunks[0]=(at,bytes(v));self.reject(o)
 def test_tail_rejected(self):o=obj();o.segments[2].length+=1;self.reject(o)
 def test_each_field_frame_rejected(self):
  for i,f in enumerate(obj().fixups):
   with self.subTest(offset=f.offset):o=obj();o.fixups[i]=replace(o.fixups[i],frame=(5,None));self.reject(o)
 def test_each_displacement_rejected(self):
  for i,f in enumerate(obj().fixups):
   with self.subTest(offset=f.offset):o=obj();o.fixups[i]=replace(o.fixups[i],displacement=(f.displacement or 0)+1);self.reject(o)
 def test_each_field_width_rejected(self):
  for i,f in enumerate(obj().fixups):
   with self.subTest(offset=f.offset):o=obj();o.fixups[i]=replace(o.fixups[i],width=4);self.reject(o)
 def test_checksum_change(self):
  r=bytearray(raw());r[-1]^=1
  with self.assertRaises(OMFError):b.extract_code(bytes(r),K)
 def test_owned_actual_evidence_closure(self):self.assertTrue(b._evidence(Path(__file__).parents[1],K))
 def test_changed_owned_evidence_rejected(self):
  from input_dialog_code_pins import EVIDENCE_PINS
  with tempfile.TemporaryDirectory()as td:
   root=Path(td)
   for n in EVIDENCE_PINS[K]:p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((Path(__file__).parents[1]/n).read_bytes())
   p=root/b.spec(K)['evidence_root']/'namespace-and-ABI.json';p.write_bytes(p.read_bytes()+b' ')
   with self.assertRaises(OMFError):b._evidence(root,K)
 def test_existing239_bounds_and_holds(self):
  a=json.loads((Path(__file__).parents[1]/b.spec(K)['evidence_root']/'namespace-and-ABI.json').read_text());c=a['bounds'];self.assertEqual((c['logical_records'],c['logical_bytes'],c['central_addend'],c['minimum_actual_initializer_index'],c['maximum_actual_initializer_index'],c['last_record_end_DS']),(239,956,476,0,238,0x57c0));self.assertTrue(c['malformed_inputs_held']);self.assertFalse(c['historical_capacity_container_TU_unique']);self.assertEqual(len(a['all_current_selected_callers']),1)
 def test_zeroC_and_DATA_credit(self):
  _,m=b.extract_code(raw(),K);self.assertEqual((m['C_credit'],m['DATA_byte_credit']),(0,0));self.assertFalse(m['historical_language_TU_or_C_unrepresentability_proven'])
 def test_negative_original_model_preserved(self):
  p=Path(__file__).parents[1]/b.spec(K)['evidence_root']/'comparison-terminal.json';self.assertTrue(json.loads(p.read_text())['prior_model_negative_preserved'])
if __name__=='__main__':unittest.main()
