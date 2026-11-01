"""Pure finite tail874 controls, fixture comparisons never generation claims."""
from pathlib import Path
import sys,json,dataclasses,copy,hashlib,unittest
from unittest.mock import patch
M=Path(__file__).resolve().parents[1];F=M/'tests/fixtures/tail_undo874';sys.path[:0]=[str(M/'build_pipeline/engine_v1'),str(M)]
import mixed_tail_undo16 as b
import mixed_tail_undo_pipeline16 as p
import mixed_source_dispatch_tail16 as dispatch
import mixed_source_dispatch16 as legacy_dispatch
import near_bss_layout_post16 as bank
from mixed_tail_undo_source16 import compose_fresh,C_SOURCE_SHA256,TRANSFORM
from omf import read_omf
from reference import build_reference
H=lambda raw:hashlib.sha256(raw).hexdigest()
class Tail874(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.built=b.generation.FreshMixedBuild((F/'mixed.obj').read_bytes(),(F/'C5.obj').read_bytes(),(F/'FA.asm').read_bytes(),(F/'composed.asm').read_bytes(),json.loads((F/'generation.json').read_text()),{});cls.row=json.loads((F/'row.json').read_text());cls.profile=b.profile();cls.ref=build_reference((M.parent/'CHESS.EXE').read_bytes());cls.obj=read_omf(cls.built.object_bytes)
 def reject(self,f,*a,**kw):
  with self.assertRaises((ValueError,KeyError,AssertionError,TypeError)):f(*a,**kw)
 def edit_receipt(self,edit):
  r=copy.deepcopy(self.built.provenance);edit(r);self.reject(b._structural,dataclasses.replace(self.built,provenance=r))
 def test_whole874_all53(self):
  o,c,info,code=b._structural(self.built);self.assertEqual(len(code),874);self.assertEqual(len(o.fixups),53);self.assertEqual([info[n]['size']for n in ['transfer_task_758c','capture_task_75f6','task_ready_772d']],[106,311,130]);self.assertEqual(c.segments[1].length,548)
 def test_sidecar3451_not_SOURCE(self):self.assertEqual(len(self.built.c5_sidecar_bytes),3451);self.assertNotEqual(self.built.c5_sidecar_bytes,self.built.object_bytes)
 def test_all874_fourbases_noMZ(self):
  code,proof,info,rel=b.linked_whole(self.built,self.ref);self.assertEqual(code,self.ref['image'][0x758c:0x78f6]);self.assertTrue(all(x['whole_native_equal']for x in proof['four_bases']));self.assertEqual(proof['native_MZ'],[]);self.assertEqual(len(proof['all53fields']),53)
 def test_exact_four_units(self):
  for u in self.profile['units'].values():b.validate_unit(u)
 def test_augmented_report_not_unit(self):
  u=copy.deepcopy(self.profile['units']['transfer_task_758c']);u['status']='c_matched';self.reject(b.validate_unit,u)
 def test_legacy_backend_not_new_unit(self):
  for u in self.profile['original_units'].values():self.reject(b.validate_unit,u)
 def test_wrong_whole_RAW(self):self.reject(b._structural,dataclasses.replace(self.built,object_bytes=self.built.object_bytes+b'\0'))
 def test_wrong_sidecar(self):self.reject(b._structural,dataclasses.replace(self.built,c5_sidecar_bytes=self.built.object_bytes))
 def test_wrong_FA(self):self.reject(b._structural,dataclasses.replace(self.built,fresh_fa_bytes=self.built.fresh_fa_bytes+b'\r\n'))
 def test_wrong_composed_source(self):self.reject(b._structural,dataclasses.replace(self.built,mixed_source_bytes=self.built.mixed_source_bytes+b'\r\n'))
 def test_real_processes_required(self):self.edit_receipt(lambda r:r.update(processes=[]))
 def test_reaped_required(self):self.edit_receipt(lambda r:r['processes'][0].update(reaped=False))
 def test_success_required(self):self.edit_receipt(lambda r:r['processes'][1].update(returncode=1))
 def test_phase_order_exact(self):self.edit_receipt(lambda r:r['processes'].reverse())
 def test_actual_positive_PID(self):self.edit_receipt(lambda r:r['processes'][0].update(pid=0))
 def test_two_distinct_PIDs(self):self.edit_receipt(lambda r:r['processes'][1].update(pid=r['processes'][0]['pid']))
 def test_no_original_read_capability(self):self.edit_receipt(lambda r:r.update(native_original_oldOBJ_profile_inside_GEN=True))
 def test_all20_denials_required(self):self.edit_receipt(lambda r:r['guard']['blocked'].pop())
 def test_exact_flags(self):self.edit_receipt(lambda r:r.update(flags=['/AS','/Gs','/Os','/Zi']))
 def test_real_source_identities(self):self.edit_receipt(lambda r:r.update(source_SHA256='0'*64))
 def test_same_output_receipt(self):self.edit_receipt(lambda r:r.update(raw_mixed_SHA256='0'*64))
 def test_full_source_inverse(self):
  source,t=compose_fresh(self.built.fresh_fa_bytes,(F/'authored.asm').read_bytes(),c_source_sha256=C_SOURCE_SHA256);self.assertEqual(source,self.built.mixed_source_bytes);self.assertTrue(t['inverse_reconstructs_full_fresh_FA']);self.assertEqual(t,self.built.provenance['transform'])
 def test_no_FA_tail_change(self):self.reject(compose_fresh,self.built.fresh_fa_bytes.replace(b'\tnop\t\r\n',b'',1),(F/'authored.asm').read_bytes(),c_source_sha256=C_SOURCE_SHA256)
 def test_wrong_authored_source(self):self.reject(compose_fresh,self.built.fresh_fa_bytes,(F/'authored.asm').read_bytes()+b'\n',c_source_sha256=C_SOURCE_SHA256)
 def test_parsed_frame_mutation(self):
  changed=copy.deepcopy(self.obj);changed.fixups[0]=dataclasses.replace(changed.fixups[0],frame=(5,None));real=b.read_omf
  with patch.object(b,'read_omf',side_effect=lambda raw:changed if raw==self.built.object_bytes else real(raw)):self.reject(b._structural,self.built)
 def test_parsed_public_mutation(self):
  changed=copy.deepcopy(self.obj);changed.publics['_undo_animation']=dataclasses.replace(changed.publics['_undo_animation'],offset=548);real=b.read_omf
  with patch.object(b,'read_omf',side_effect=lambda raw:changed if raw==self.built.object_bytes else real(raw)):self.reject(b._structural,self.built)
 def test_exact_field_categories(self):self.assertEqual(self.profile['field_categories'],{'external_near_CALL_own_CODE':17,'actual_direct_MEMORY_GROUP1':12,'other_external_DATA_target_frame':11,'compiler_unqualified_OFFSET_external_target_frame':3,'compiler_FA_symbolic_local_E9':5,'actual_local_PUBLIC_near_CALL':2,'authored_explicit_OFFSET_DGROUP_WORD':3})
 def test_exact_finite_four_dispatch(self):self.assertEqual(set(dispatch.PROFILES),{'refresh_chat284_v1','restore_decoder340_v1','motion_special970_v1','tail_undo874_v1'})
 def test_old_two_dispatcher_unchanged(self):self.assertEqual(set(legacy_dispatch.PROFILES),{'refresh_chat284_v1','restore_decoder340_v1'})
 def test_new_row_valid(self):p.validate_row(self.row);dispatch.validate_row(self.row)
 def test_unknown_profile(self):r=copy.deepcopy(self.row);r['object_profile']='arbitrary';self.reject(dispatch.validate_row,r)
 def test_cross_profile(self):r=copy.deepcopy(self.row);r['object_profile']='restore_decoder340_v1';self.reject(dispatch.validate_row,r)
 def test_wrong_owner_roles(self):r=copy.deepcopy(self.row);r['selected_owners'].reverse();self.reject(p.validate_row,r)
 def test_no_extra_generator_capability(self):r=copy.deepcopy(self.row);r['generation_tools']['CHESS.EXE']='0'*64;self.reject(p.validate_row,r)
 def test_no_unreviewed_flags(self):r=copy.deepcopy(self.row);r['compiler_flags'].append('/Os');self.reject(p.validate_row,r)
 def test_seal_unknown_transform(self):self.reject(dispatch.module_for_seal,{'kind':b.KIND,'mixed_transform':'unknown'})
 def test_nonmixed_seal_default_unchanged(self):self.assertEqual(dispatch.seal_extra({'kind':'c-whole-omf'},[]),{});self.assertTrue(dispatch.validate_seal_row({'kind':'c-whole-omf'}))
 def test_calibration_actual_closure(self):self.assertTrue(b.validate_certificate(M)['calibration_only_not_fresh_witness'])
 def test_BSS_only_four_exact_F2(self):
  rows=[f for f in self.profile['actual_fields']if f['offset']in(29,40,156,291)];self.assertEqual(len(rows),4)
  for f in rows:q=next(q for q in self.obj.fixups if q.offset==f['offset']);self.assertEqual(bank.validate_client_frame(self.row,self.built.object_bytes,q,f['symbol']),'proven_MIXED874_external_PUBLIC_group1')
 def test_BSS_wrong_whole_RAW(self):q=next(q for q in self.obj.fixups if q.offset==40);self.reject(bank.validate_client_frame,self.row,self.built.object_bytes+b'\0',q,'_frames')
 def test_BSS_wrong_source(self):r=copy.deepcopy(self.row);r['source']='other.c';q=next(q for q in self.obj.fixups if q.offset==40);self.reject(bank.validate_client_frame,r,self.built.object_bytes,q,'_frames')
 def test_BSS_wrong_target(self):q=next(q for q in self.obj.fixups if q.offset==40);self.reject(bank.validate_client_frame,self.row,self.built.object_bytes,dataclasses.replace(q,target=(2,7)),'_frames')
 def test_BSS_F0_not_data_fallback(self):q=next(q for q in self.obj.fixups if q.offset==40);self.reject(bank.validate_client_frame,self.row,self.built.object_bytes,dataclasses.replace(q,frame=(0,1)),'_frames')
 def test_command_active_not_bank_exception(self):q=next(q for q in self.obj.fixups if q.offset==160);self.reject(bank.validate_client_frame,self.row,self.built.object_bytes,q,'_command_active')
 def test_old_capture311_gap_gate_retained(self):
  from extent import validate_extended_extent
  o,c,infos,raw=b._structural(self.built);linked,proof,infos,cr=b.linked_whole(self.built,self.ref)
  gate=validate_extended_extent(self.profile['original_units']['capture_task_75f6'],M,b.ORIGINAL_SHA256,infos['capture_task_75f6'],linked[106:417],source_object=c)
  self.assertEqual(gate['gap_bytes'],2);self.assertEqual(gate['reachable_body_bytes'],309)

 def test_sole_calibrated_WORD_immediate_qualifier(self):
  self.assertEqual(self.built.fresh_fa_bytes.count(b'\tand\tbx,63\r\n'),1);self.assertEqual(self.built.mixed_source_bytes.count(b'\tand\tbx,WORD PTR 63\r\n'),1);self.assertTrue(self.built.provenance['transform']['C_PROCs_exact_except_one_immediate_type_qualifier'])
 def test_unexpected_width_source_not_accepted(self):self.reject(compose_fresh,self.built.fresh_fa_bytes.replace(b'\tand\tbx,63\r\n',b'\tand\tbx,31\r\n'),(F/'authored.asm').read_bytes(),c_source_sha256=C_SOURCE_SHA256)
 def test_old_three_dispatcher_unchanged(self):
  import mixed_source_dispatch_motion16 as old_three
  self.assertEqual(set(old_three.PROFILES),{'refresh_chat284_v1','restore_decoder340_v1','motion_special970_v1'})
