"""Pure integrity/route guards; fixtures cannot mint fresh SOURCE/aggregate caps."""
from pathlib import Path
from copy import deepcopy
from dataclasses import replace
import unittest,json,types
from unittest.mock import patch
import mixed_restore_decoder16 as new
import mixed_restore_decoder_generation16 as gen
import mixed_restore_decoder_source16 as src
import mixed_restore_decoder_pipeline16 as phase
import mixed_source_dispatch16 as dispatch
import mixed_refresh_chat_pipeline16 as oldphase
import near_bss_layout_post16 as bss
from omf import read_omf
ROOT=Path(__file__).resolve().parents[1];F=ROOT/'tests/fixtures/restore_decoder340'
def fixture():return gen.FreshMixedBuild((F/'mixed.obj').read_bytes(),(F/'C5.obj').read_bytes(),(F/'compiler-FA.asm').read_bytes(),(F/'composed.asm').read_bytes(),json.loads((F/'calibration-generation.json').read_text()),{})
class WholeMixed340(unittest.TestCase):
 def setUp(self):self.b=fixture()
 def test_whole_CODE340_and_CV51(self):
  o,c,info,code=new._structural(self.b);self.assertEqual(len(code),340);self.assertEqual(info['size'],51);self.assertEqual(c.segments[info['segment']].length,52);self.assertEqual(o.publics['_decode_frame_directory'].offset,51)
 def test_full_native_all31_fourbases_noMZ(self):
  from reference import build_reference
  ref=build_reference((ROOT.parent/'CHESS.EXE').read_bytes());code,p,info,rel=new.linked_whole(self.b,ref);self.assertEqual(code,ref['image'][0x2ce0:0x2e34]);self.assertEqual(len(p['all31fields']),31);self.assertEqual(len(p['four_bases']),4);self.assertEqual(p['native_MZ'],[])
 def test_wrong_raw_byte_rejected(self):
  raw=bytearray(self.b.object_bytes);raw[-2]^=1
  with self.assertRaises(ValueError):new._structural(replace(self.b,object_bytes=bytes(raw)))
 def test_sidecar_not_game_object(self):
  with self.assertRaises(ValueError):new._structural(replace(self.b,object_bytes=self.b.c5_sidecar_bytes))
 def test_game_object_not_sidecar(self):
  with self.assertRaises(ValueError):new._structural(replace(self.b,c5_sidecar_bytes=self.b.object_bytes))
 def test_FA_not_archived_changed_input(self):
  with self.assertRaises(ValueError):new._structural(replace(self.b,fresh_fa_bytes=self.b.fresh_fa_bytes+b';bad'))
 def test_composed_source_unchanged(self):
  with self.assertRaises(ValueError):new._structural(replace(self.b,mixed_source_bytes=self.b.mixed_source_bytes+b';bad'))
 def test_unreaped_process_rejected(self):
  p=deepcopy(self.b.provenance);p['processes'][0]['reaped']=False
  with self.assertRaises(ValueError):new._structural(replace(self.b,provenance=p))
 def test_nonzero_process_rejected(self):
  p=deepcopy(self.b.provenance);p['processes'][1]['returncode']=1
  with self.assertRaises(ValueError):new._structural(replace(self.b,provenance=p))
 def test_wrong_phase_order_rejected(self):
  p=deepcopy(self.b.provenance);p['processes'].reverse()
  with self.assertRaises(ValueError):new._structural(replace(self.b,provenance=p))
 def test_missing_denial_rejected(self):
  p=deepcopy(self.b.provenance);p['guard']['blocked'].pop()
  with self.assertRaises(ValueError):new._structural(replace(self.b,provenance=p))
 def test_native_GEN_capability_rejected(self):
  p=deepcopy(self.b.provenance);p['native_original_oldOBJ_profile_inside_GEN']=True
  with self.assertRaises(ValueError):new._structural(replace(self.b,provenance=p))
 def test_wrong_flags_rejected(self):
  p=deepcopy(self.b.provenance);p['flags']=['/AS','/Zi']
  with self.assertRaises(ValueError):new._structural(replace(self.b,provenance=p))
 def test_parsed_frame_mutation_rejected(self):
  o=read_omf(self.b.object_bytes);i=next(i for i,f in enumerate(o.fixups)if f.offset==241);o.fixups[i]=replace(o.fixups[i],frame=(2,6));real=new.read_omf
  with patch.object(new,'read_omf',lambda raw:o if raw==self.b.object_bytes else real(raw)):
   with self.assertRaises(ValueError):new._structural(self.b)
 def test_parsed_EXTRA_PUBLIC_rejected(self):
  o=read_omf(self.b.object_bytes);o.publics['_fake']=replace(o.publics['_restore_active_arena'],name='_fake');real=new.read_omf
  with patch.object(new,'read_omf',lambda raw:o if raw==self.b.object_bytes else real(raw)):
   with self.assertRaises(ValueError):new._structural(self.b)
 def test_unit_exact_two_contracts(self):
  for u in new.profile()['units'].values():new.validate_unit(u)
 def test_augmented_report_not_strict_unit(self):
  u=dict(new.profile()['units']['restore_active_arena_2ce0'],status='c_matched')
  with self.assertRaises(ValueError):new.validate_unit(u)
 def test_owner_language_not_reclassified(self):
  u=dict(new.profile()['units']['decode_frame_directory_code289'],language='c')
  with self.assertRaises(ValueError):new.validate_unit(u)
class SourceComposeAndDispatcher(unittest.TestCase):
 def setUp(self):self.row=json.loads((F/'new-row.json').read_text());self.legacy=json.loads((F/'legacy-row.json').read_text())
 def test_exact_fresh_source_transform_inverse(self):
  value,p=src.compose_fresh((F/'compiler-FA.asm').read_bytes(),(F/'decoder.asm').read_bytes(),c_source_sha256=src.C_SOURCE_SHA256);self.assertEqual(value,(F/'composed.asm').read_bytes());self.assertTrue(p['all_source_metadata_transform_inverse_exact'])
 def test_unrecognized_FA_tail_rejected(self):
  with self.assertRaises(ValueError):src.compose_fresh((F/'compiler-FA.asm').read_bytes()+b'nop', (F/'decoder.asm').read_bytes(),c_source_sha256=src.C_SOURCE_SHA256)
 def test_changed_real_ASM_rejected(self):
  with self.assertRaises(ValueError):src.compose_fresh((F/'compiler-FA.asm').read_bytes(),(F/'decoder.asm').read_bytes()+b'nop',c_source_sha256=src.C_SOURCE_SHA256)
 def test_wrong_primary_identity_rejected(self):
  with self.assertRaises(ValueError):src.compose_fresh((F/'compiler-FA.asm').read_bytes(),(F/'decoder.asm').read_bytes(),c_source_sha256='0'*64)
 def test_two_finite_profiles(self):self.assertEqual(set(dispatch.PROFILES),{'refresh_chat284_v1','restore_decoder340_v1'})
 def test_old_profile_delegation_unchanged(self):self.assertIs(dispatch.module_for_row(self.legacy),oldphase);self.assertTrue(dispatch.validate_row(self.legacy))
 def test_new_profile_delegation(self):self.assertIs(dispatch.module_for_row(self.row),phase);self.assertTrue(dispatch.validate_row(self.row))
 def test_unknown_profile_rejected(self):
  self.row['object_profile']='guess'
  with self.assertRaises(ValueError):dispatch.validate_row(self.row)
 def test_new_source_old_profile_rejected(self):
  self.row['object_profile']='refresh_chat284_v1'
  with self.assertRaises(ValueError):dispatch.validate_row(self.row)
 def test_wrong_flags_row_rejected(self):
  self.row['compiler_flags']=['/AS','/Zi']
  with self.assertRaises(ValueError):dispatch.validate_row(self.row)
 def test_wrong_owner_order_rejected(self):
  self.row['selected_owners'].reverse()
  with self.assertRaises(ValueError):dispatch.validate_row(self.row)
 def test_unlisted_source_read_cap_rejected(self):
  self.row['generation_tools']['native.bin']='0'*64
  with self.assertRaises(ValueError):dispatch.validate_row(self.row)
 def test_legacy_nonmixed_seal_unchanged(self):self.assertTrue(dispatch.validate_seal_row({'kind':'c-whole-omf'}));self.assertEqual(dispatch.seal_extra({'kind':'c-whole-omf'},[]),{})
 def test_unknown_sealed_transform_rejected(self):
  with self.assertRaises(ValueError):dispatch.validate_seal_row({'kind':phase.KIND,'mixed_transform':'guess'})
 def test_no_sidecar_as_SOURCE(self):
  r={'kind':phase.KIND,'generation_sources':phase.SOURCES,'mixed_transform':phase.TRANSFORM,'selected_owners':phase.OWNERS,'typed_C5_sidecar':{'role':'comparison_only_excluded_from_SOURCE','path':'same.obj','sha256':'0'*64},'object_path':'same.obj'}
  with self.assertRaises(ValueError):dispatch.validate_seal_row(r)
class BSSExactF2(unittest.TestCase):
 def setUp(self):self.row=json.loads((F/'new-row.json').read_text());self.raw=(F/'mixed.obj').read_bytes();self.o=read_omf(self.raw);self.fields=json.loads((F/'BSS16.json').read_text())
 def test_all16_exact_fields(self):
  for v in self.fields:
   f=next(f for f in self.o.fixups if f.offset==v['offset']);self.assertEqual(bss.validate_client_frame(self.row,self.raw,f,v['symbol']),'proven_MIXED340_external_PUBLIC_group1')
 def test_wrong_BSS_raw_rejected(self):
  f=next(f for f in self.o.fixups if f.offset==1)
  with self.assertRaises(AssertionError):bss.validate_client_frame(self.row,self.raw+b'x',f,'_active_data_b0ca')
 def test_wrong_BSS_target_rejected(self):
  f=next(f for f in self.o.fixups if f.offset==1)
  with self.assertRaises(AssertionError):bss.validate_client_frame(self.row,self.raw,f,'_arena_cursor')
 def test_wrong_BSS_displacement_rejected(self):
  f=next(f for f in self.o.fixups if f.offset==41)
  with self.assertRaises(AssertionError):bss.validate_client_frame(self.row,self.raw,replace(f,displacement=0),'_active_arena_9344')
 def test_wrong_BSS_offset_rejected(self):
  f=next(f for f in self.o.fixups if f.offset==1)
  with self.assertRaises(AssertionError):bss.validate_client_frame(self.row,self.raw,replace(f,offset=2),'_active_data_b0ca')
 def test_near_CODE_F0_is_not_BSS_fallback(self):
  f=next(f for f in self.o.fixups if f.offset==241)
  with self.assertRaises(AssertionError):bss.validate_client_frame(self.row,self.raw,f,'_huff_decode_stream')
 def test_wrong_BSS_source_row_rejected(self):
  f=next(f for f in self.o.fixups if f.offset==1);self.row['source']='src/other.c'
  with self.assertRaises(AssertionError):bss.validate_client_frame(self.row,self.raw,f,'_active_data_b0ca')
