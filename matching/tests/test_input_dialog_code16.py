"""Closed fixture-only integrity controls. No assembler/compiler callbacks execute."""
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import unittest,copy,json,tempfile,os,builtins,io
from omf import read_omf,Fixup,OMFError
import input_dialog_code16 as b
F=Path(__file__).parent/'fixtures/input_dialog'
KEYS=['input_number306','dialog_button152']
def raw(i):return(F/('number.obj'if i==KEYS[0]else'dialog.obj')).read_bytes()
def obj(i):return read_omf(raw(i))
def unit(i):return copy.deepcopy(b.spec(i)['unit'])
class ClosedInputDialogTests(unittest.TestCase):
 def test_exact_two_profiles(self):self.assertEqual(set(b.profiles()['ASM']),set(KEYS)|{'select_mode84','init_rays185','type_chat161'})
 def test_number_whole_306_positive(self):self.assertEqual(len(b.extract_code(raw(KEYS[0]),KEYS[0])[0]),306)
 def test_dialog_whole_152_positive(self):self.assertEqual(len(b.extract_code(raw(KEYS[1]),KEYS[1])[0]),152)
 def test_both_exact_unit_contracts(self):
  for k in KEYS:b.validate_unit(unit(k))
 def test_unknown_profile_no_fallback(self):
  with self.assertRaises(OMFError):b.spec('other')
 def test_cross_profile_object_rejected(self):
  with self.assertRaises(OMFError):b.extract_code(raw(KEYS[0]),KEYS[1])
 def test_old307_negative_is_not_trimmed(self):
  with self.assertRaises(OMFError):b.extract_code((F/'negative307.obj').read_bytes(),KEYS[0])
 def test_byte_change_raw_object_rejected(self):
  r=bytearray(raw(KEYS[0]));r[-2]^=1
  with self.assertRaises(OMFError):b.extract_code(bytes(r),KEYS[0])
 def test_changed_loaded_chunk_rejected(self):
  o=obj(KEYS[0]);at,r=o.segments[2].chunks[0];o.segments[2].chunks[0]=(at,r[:-1]+bytes([r[-1]^1]))
  with self.assertRaises(OMFError):b.validate_object(o,KEYS[0])
 def test_extra_data_allocation_rejected(self):
  o=obj(KEYS[0]);o.segments[1].length=2
  with self.assertRaises(OMFError):b.validate_object(o,KEYS[0])
 def test_CODE_tail_rejected(self):
  o=obj(KEYS[0]);o.segments[2].length+=1
  with self.assertRaises(OMFError):b.validate_object(o,KEYS[0])
 def test_wrong_BYTE_attribute_rejected(self):
  o=obj(KEYS[1]);o.segments[2].attributes=40
  with self.assertRaises(OMFError):b.validate_object(o,KEYS[1])
 def test_alias_public_rejected(self):
  o=obj(KEYS[0]);o.publics['_alias']=o.publics['_get_number']
  with self.assertRaises(OMFError):b.validate_object(o,KEYS[0])
 def test_mutated_parsed_external_rejected(self):
  o=obj(KEYS[0]);o.externals[2]='__fake_stack'
  with self.assertRaises(OMFError):b.validate_object(o,KEYS[0])
 def test_duplicate_fixup_rejected(self):
  o=obj(KEYS[1]);o.fixups.append(o.fixups[0])
  with self.assertRaises(OMFError):b.validate_object(o,KEYS[1])
 def test_missing_fixup_rejected(self):
  o=obj(KEYS[1]);o.fixups.pop()
  with self.assertRaises(OMFError):b.validate_object(o,KEYS[1])
 def test_wrong_far_width_rejected(self):
  o=obj(KEYS[1]);i=next(i for i,f in enumerate(o.fixups)if f.width==4);f=o.fixups[i];o.fixups[i]=Fixup(f.segment,f.offset,2,f.location_type,f.segment_relative,f.frame,f.target,f.displacement,f.record_offset,f.raw)
  with self.assertRaises(OMFError):b.validate_object(o,KEYS[1])
 def test_wrong_group_frame_rejected(self):
  o=obj(KEYS[0]);i=next(i for i,f in enumerate(o.fixups)if f.frame==(1,1));f=o.fixups[i];o.fixups[i]=Fixup(f.segment,f.offset,f.width,f.location_type,f.segment_relative,(5,None),f.target,f.displacement,f.record_offset,f.raw)
  with self.assertRaises(OMFError):b.validate_object(o,KEYS[0])
 def test_raw_record_chronology_rejected(self):
  o=obj(KEYS[0]);o.records[0],o.records[1]=o.records[1],o.records[0]
  with self.assertRaises(OMFError):b.validate_object(o,KEYS[0])
 def test_snapshot_normalized_key_collision_rejected(self):
  with self.assertRaises(OMFError):b.canon({1:1,'1':2})
 def test_unit_wrong_source_rejected(self):
  u=unit(KEYS[0]);u['source']='asm/link/old.asm'
  with self.assertRaises(OMFError):b.validate_unit(u)
 def test_unit_wrong_native_origin_rejected(self):
  u=unit(KEYS[0]);u['image_offset']='0x1165'
  with self.assertRaises(OMFError):b.validate_unit(u)
 def test_unit_wrong_size_rejected(self):
  u=unit(KEYS[0]);u['size']=307
  with self.assertRaises(OMFError):b.validate_unit(u)
 def test_unit_wrong_far_segment_binding_rejected(self):
  u=unit(KEYS[1]);u['externals']['_update_pointer_11ef_0030']['segment']+=1
  with self.assertRaises(OMFError):b.validate_unit(u)
 def test_unit_unknown_metadata_rejected(self):
  u=unit(KEYS[0]);u['fallback']=True
  with self.assertRaises(OMFError):b.validate_unit(u)
 def test_unit_unknown_identity_rejected(self):
  u=unit(KEYS[0]);u['id']='alias'
  with self.assertRaises(OMFError):b.validate_unit(u)
 def test_number_all306_native_bytes(self):self.assertEqual(b.link_code(raw(KEYS[0]),KEYS[0])[0],(F/'number.native.bin').read_bytes())
 def test_dialog_all152_native_bytes(self):self.assertEqual(b.link_code(raw(KEYS[1]),KEYS[1])[0],(F/'dialog.native.bin').read_bytes())
 def test_dialog_four_full_load_bases(self):
  s=b.spec(KEYS[1]);gold=(F/'dialog.native.bin').read_bytes()
  for base in[0,1,4096,65535]:
   wanted=bytearray(gold)
   for site in s['native_MZ']:
    p=site-s['base'];wanted[p:p+2]=((int.from_bytes(wanted[p:p+2],'little')+base)&65535).to_bytes(2,'little')
   self.assertEqual(b.link_code(raw(KEYS[1]),KEYS[1],base)[0],wanted)
 def test_number_no_load_fixups(self):
  for base in[0,1,4096,65535]:self.assertEqual(b.link_code(raw(KEYS[0]),KEYS[0],base)[0],(F/'number.native.bin').read_bytes())
 def test_exact_dialog_MZ_site(self):
  code,logs=b.link_code(raw(KEYS[1]),KEYS[1]);self.assertEqual([r['mz_segment_relocation_image_offset']for r in logs if'mz_segment_relocation_image_offset'in r],[0xd9a2])
 def test_missing_dialog_MZ_rejected(self):
  with self.assertRaises(OMFError):b._sites(b.spec(KEYS[1]),[])
 def test_extra_number_MZ_rejected(self):
  with self.assertRaises(OMFError):b._sites(b.spec(KEYS[0]),[0x1174])
 def test_crossing_boundary_MZ_rejected(self):
  with self.assertRaises(OMFError):b._sites(b.spec(KEYS[0]),[0x1163])
 def test_bad_load_paragraph_rejected(self):
  with self.assertRaises(OMFError):b.link_code(raw(KEYS[0]),KEYS[0],65536)
 def test_source_hash_and_mnemonic_policy(self):
  project=Path(__file__).resolve().parents[1]
  for name in b.GEN_SOURCES:b.source_policy((project/name).read_bytes(),name)
 def test_changed_source_rejected(self):
  with self.assertRaises(OMFError):b.source_policy(b'DB 0\n',next(iter(b.GEN_SOURCES)))
 def test_unknown_source_rejected(self):
  with self.assertRaises(OMFError):b.source_policy(b'', 'asm/link/unknown.asm')
 def test_guard_rejects_oldnative_path_all_APIs(self):
  with tempfile.TemporaryDirectory()as t:
   root=Path(t);source=root/'source.asm';source.write_text('fixture');scratch=root/'scratch';scratch.mkdir();forbidden=root/'native.bin';forbidden.write_bytes(b'no')
   with b.generation_guard(source,root,scratch)as events:
    for fn in [lambda:forbidden.read_bytes(),lambda:builtins.open(forbidden,'rb'),lambda:io.open(forbidden,'rb'),lambda:os.open(forbidden,os.O_RDONLY)]:
     with self.assertRaises(OMFError):fn()
   self.assertGreaterEqual(len(events['blocked']),4)
 def test_guard_allows_only_source_and_newscratch(self):
  with tempfile.TemporaryDirectory()as t:
   root=Path(t);source=root/'source.asm';source.write_text('fixture');scratch=root/'scratch';scratch.mkdir()
   with b.generation_guard(source,root,scratch):self.assertEqual(source.read_text(),'fixture');(scratch/'new.txt').write_text('ok');self.assertEqual((scratch/'new.txt').read_text(),'ok')
 def test_guard_rejects_source_write(self):
  with tempfile.TemporaryDirectory()as t:
   root=Path(t);source=root/'source.asm';source.write_text('fixture');scratch=root/'scratch';scratch.mkdir()
   with b.generation_guard(source,root,scratch):
    with self.assertRaises(OMFError):source.write_text('no')
 def test_assemble_unknown_source_stops_before_generator(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t)/'unknown.asm';p.write_text('fixture')
   with patch.object(b,'_assemble_source',side_effect=AssertionError('generator must not run')):
    with self.assertRaises(OMFError):b.assemble(p,Path(t))
 def test_label_fixture_remains_generic_exact_array(self):
  o=read_omf((F/'label.obj').read_bytes());self.assertEqual(o.publics['_number_label_4c28'].type_index,0x205);self.assertEqual(o.segments[6].length,30);self.assertFalse(o.fixups)
 def test_label_validate_compiled_comparison_fixture(self):
  p=b.profiles()['label'];root=Path(__file__).resolve().parents[1];c=SimpleNamespace(object_bytes=(F/'label.obj').read_bytes(),source_sha256=p['source_sha256'],compiler='msc500',flags=['/AS','/Zl','/Zi'],source_name='UNIT.C',toolchain_manifest_sha256=p['manifest_sha256'],tool_hashes=p['tool_hashes']);self.assertEqual(b.validate_label_compiled(p['unit'],c,root)['PUBLIC_type'],'0x205')
 def test_label_wrong_array_UNIT_rejected(self):
  p=b.profiles()['label'];u=copy.deepcopy(p['unit']);u['size']=29
  with self.assertRaises(OMFError):b.validate_label_compiled(u,None,Path('.'))
 def test_label_wrong_flag_fixture_rejected(self):
  p=b.profiles()['label'];root=Path(__file__).resolve().parents[1];c=SimpleNamespace(source_sha256=p['source_sha256'],compiler='msc500',flags=['/AS','/Zi'],source_name='UNIT.C',toolchain_manifest_sha256=p['manifest_sha256'],tool_hashes=p['tool_hashes'])
  with self.assertRaises(OMFError):b.validate_label_compiled(p['unit'],c,root)
 def test_label_wrong_manifest_fixture_rejected(self):
  p=b.profiles()['label'];root=Path(__file__).resolve().parents[1];c=SimpleNamespace(source_sha256=p['source_sha256'],compiler='msc500',flags=['/AS','/Zl','/Zi'],source_name='UNIT.C',toolchain_manifest_sha256='wrong',tool_hashes=p['tool_hashes'])
  with self.assertRaises(OMFError):b.validate_label_compiled(p['unit'],c,root)
 def test_owned_actual_evidence_closure(self):
  project=Path(__file__).resolve().parents[1]
  for key in KEYS:self.assertTrue(b._evidence(project,key))
 def test_old_C306_frame_hold_is_not_ASM(self):
  with self.assertRaises(OMFError):b.extract_code((F/'held-c306.obj').read_bytes(),KEYS[0])
 def test_both_zero_Ccredit_and_historical_holds(self):
  for key in KEYS:
   code,meta=b.extract_code(raw(key),key);self.assertEqual(meta['C_credit'],0);self.assertFalse(meta['historical_language_TU_or_C_unrepresentability_proven'])
if __name__=='__main__':unittest.main()
