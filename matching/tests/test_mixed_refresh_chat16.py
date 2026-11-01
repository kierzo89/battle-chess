"""Pure fixture checks: no fixture grants a live SOURCE or aggregate capability."""
from pathlib import Path
import unittest,json,dataclasses,tempfile,hashlib
from types import SimpleNamespace
import mixed_refresh_chat16 as mixed
import mixed_refresh_chat_generation16 as gen
import mixed_refresh_chat_source16 as source
import mixed_refresh_chat_pipeline16 as pipeline
ROOT=Path(__file__).resolve().parents[1]
F=ROOT/'tests/fixtures/mixed_refresh_chat'
class MixedObjectTests(unittest.TestCase):
 def setUp(self):self.b=gen.FreshMixedBuild((F/'mixed.obj').read_bytes(),(F/'C5.obj').read_bytes(),(F/'compiler-FA.asm').read_bytes(),(F/'composed.asm').read_bytes(),json.loads((F/'calibration-generation.json').read_text()),{})
 def test_exact_whole_calibration_roles(self):
  o,c,info,raw=mixed._structural(self.b);self.assertEqual(len(raw),284);self.assertEqual(info['size'],123);self.assertEqual(o.publics['_type_chat_14c1'].offset,123)
 def test_unrelated_CODE_mutation_rejected(self):
  raw=bytearray(self.b.object_bytes);raw[300]^=1
  with self.assertRaises(ValueError):mixed._structural(dataclasses.replace(self.b,object_bytes=bytes(raw)))
 def test_sidecar_cannot_be_game_object(self):
  with self.assertRaises(ValueError):mixed._structural(dataclasses.replace(self.b,object_bytes=self.b.c5_sidecar_bytes))
 def test_wrong_real_typed_sidecar_rejected(self):
  with self.assertRaises(ValueError):mixed._structural(dataclasses.replace(self.b,c5_sidecar_bytes=self.b.object_bytes))
 def test_changed_FA_rejected_postGEN(self):
  with self.assertRaises(ValueError):mixed._structural(dataclasses.replace(self.b,fresh_fa_bytes=self.b.fresh_fa_bytes+b';changed'))
 def test_changed_composition_rejected_postGEN(self):
  with self.assertRaises(ValueError):mixed._structural(dataclasses.replace(self.b,mixed_source_bytes=self.b.mixed_source_bytes+b';changed'))
 def test_process_phase_order_rejected(self):
  receipt=json.loads(json.dumps(self.b.provenance));receipt['processes'].reverse()
  with self.assertRaises(ValueError):mixed._structural(dataclasses.replace(self.b,provenance=receipt))
 def test_missing_second_real_process_rejected(self):
  receipt=json.loads(json.dumps(self.b.provenance));receipt['processes'].pop()
  with self.assertRaises(ValueError):mixed._structural(dataclasses.replace(self.b,provenance=receipt))
 def test_unclosed_process_rejected(self):
  receipt=json.loads(json.dumps(self.b.provenance));receipt['processes'][1]['reaped']=False
  with self.assertRaises(ValueError):mixed._structural(dataclasses.replace(self.b,provenance=receipt))
 def test_missing_active_guard_denial_rejected(self):
  receipt=json.loads(json.dumps(self.b.provenance));receipt['guard']['blocked'].pop()
  with self.assertRaises(ValueError):mixed._structural(dataclasses.replace(self.b,provenance=receipt))
class SourceAndMetadataTests(unittest.TestCase):
 def setUp(self):self.fa=(F/'compiler-FA.asm').read_bytes();self.chat=(F/'authored-chat.asm').read_bytes()
 def compose(self,fa=None,chat=None,sha=source.C_SOURCE_SHA256):return source.compose_fresh(self.fa if fa is None else fa,self.chat if chat is None else chat,c_source_sha256=sha)
 def test_source_transform_exact(self):self.assertEqual(self.compose()[0],(F/'composed.asm').read_bytes())
 def test_foreign_primary_source_rejected(self):
  with self.assertRaises(ValueError):self.compose(sha='0'*64)
 def test_changed_authored_body_rejected(self):
  changed=self.chat.replace(b'push bp',b'push ax',1);self.assertNotEqual(changed,self.chat)
  with self.assertRaises(ValueError):self.compose(chat=changed)
 def test_inside_procedure_NOP_not_dropped(self):
  with self.assertRaises(ValueError):self.compose(fa=self.fa.replace(b'_refresh_1446\tENDP',b'\tnop\t\r\n_refresh_1446\tENDP',1))
 def test_nonempty_debug_declaration_rejected(self):
  with self.assertRaises(ValueError):self.compose(fa=self.fa.replace(b'$$SYMBOLS\tENDS',b' db 1\r\n$$SYMBOLS\tENDS',1))
 def test_other_final_instruction_rejected(self):
  with self.assertRaises(ValueError):self.compose(fa=self.fa.replace(b'\tnop\t\r\n_TEXT\tENDS',b'\tint 3\r\n_TEXT\tENDS',1))
 def test_BYTE_wrapper_substitution_rejected(self):
  with self.assertRaises(ValueError):self.compose(fa=self.fa.replace(b"_TEXT\tSEGMENT  WORD PUBLIC 'CODE'",b"_TEXT\tSEGMENT  BYTE PUBLIC 'CODE'",1))
 def test_two_exact_owner_rows(self):
  for u in mixed.profile()['units'].values():mixed.validate_unit(u)
 def test_C_extent_cannot_grow_to_mixed_extent(self):
  u=dict(mixed.profile()['units']['refresh_1446']);u['size']=284
  with self.assertRaises(ValueError):mixed.validate_unit(u)
 def test_chat_cannot_be_credited_C(self):
  u=dict(mixed.profile()['units']['type_chat_code161']);u['language']='c'
  with self.assertRaises(ValueError):mixed.validate_unit(u)
class PipelineTests(unittest.TestCase):
 def row(self):
  d=json.loads((ROOT/'build_pipeline/engine_v1/descriptor.json').read_text());return next(r for r in d['rows']if r['kind']==pipeline.KIND)
 def test_exact_mixed_descriptor_role(self):self.assertTrue(pipeline.validate_row(self.row()))
 def test_second_real_source_required(self):
  r=self.row();r['generation_sources'].pop()
  with self.assertRaises(ValueError):pipeline.validate_row(r)
 def test_same_address_fake_owner_not_accepted(self):
  r=self.row();r['selected_owners'][1]='alias_chat'
  with self.assertRaises(ValueError):pipeline.validate_row(r)
 def test_expected_profile_cannot_be_GEN_tool(self):
  r=self.row();r['generation_tools']['mixed_refresh_chat_profile.json']='0'*64
  with self.assertRaises(ValueError):pipeline.validate_row(r)
 def test_sidecar_game_path_rejected(self):
  r={'kind':pipeline.KIND,'generation_sources':pipeline.SOURCES,'mixed_transform':pipeline.TRANSFORM,'selected_owners':pipeline.OWNERS,'typed_C5_sidecar':{'role':'comparison_only_excluded_from_SOURCE','path':'same.obj','sha256':'0'*64},'object_path':'same.obj'}
  with self.assertRaises(ValueError):pipeline.validate_seal_row(r)
 def test_regular_file_descriptor_not_PIPE(self):
  with(F/'mixed.obj').open('rb')as f:
   with self.assertRaises(AssertionError):gen.Guard(F,{}).allow(f.fileno(),False,'inert_test')
 def test_host_object_injection_denied(self):
  with self.assertRaises(ValueError):gen.Guard(F,{}).allow(F/'injected.obj',True,'inert_test')
 def test_profile_read_outside_scratch_denied(self):
  with tempfile.TemporaryDirectory()as tmp:
   with self.assertRaises(ValueError):gen.Guard(Path(tmp),{}).allow(ROOT/'mixed_refresh_chat_profile.json',False,'inert_test')
class PhaseBoundaryTests(unittest.TestCase):
 def context(self,root,masm=False):
  d=json.loads((ROOT/'build_pipeline/engine_v1/descriptor.json').read_text());r=next(r for r in d['rows']if r['kind']==pipeline.KIND);o=SimpleNamespace(project=ROOT,descriptor=d);phase='MASM'if masm else'C5';work=root/phase;compiler='msc510'if masm else'msc500';cmd='T:\\MASM /Mx UNIT.ASM,UNIT.OBJ,UNIT.LST,UNIT.CRF;'if masm else'T:\\CL.EXE /c /AS /Zi /FaC:\\UNIT.ASM /FoC:\\UNIT.OBJ C:\\UNIT.C'
  conf='mount c "'+str(work)+'"\nmount t "'+str(ROOT/'toolchains'/compiler)+'" -ro\n';submitted={str(work/'dosbox.conf'):conf.encode(),str(work/'BUILD.BAT'):(cmd+' > C:\\BUILD.LOG\n').encode()};events={'processes':[],'submitted':submitted}
  if not masm:submitted[str(work/'UNIT.C')]=(ROOT/'src/refresh_1446_match.c').read_bytes()
  else:
   events['processes']=[{'mixed_phase':'C5','object':SimpleNamespace(poll=lambda:0)}];events['_mixed_read_bytes']={'C5/UNIT.OBJ':(F/'C5.obj').read_bytes(),'C5/UNIT.ASM':(F/'compiler-FA.asm').read_bytes(),pipeline.SOURCES[0]['path']:(ROOT/pipeline.SOURCES[0]['path']).read_bytes(),pipeline.SOURCES[1]['path']:(ROOT/pipeline.SOURCES[1]['path']).read_bytes()};submitted[str(work/'UNIT.ASM')]=(F/'composed.asm').read_bytes()
  argv=[d['tools']['DOSBox']['path'],'-conf',str(work/'dosbox.conf'),'-noconsole'];return o,r,events,argv
 def test_inert_C5_phase_contract(self):
  with tempfile.TemporaryDirectory()as t:
   root=Path(t);o,r,e,a=self.context(root);self.assertEqual(pipeline.before_process(o,r,e,root,a,{}),'C5')
 def test_wrong_submitted_C_source_denied(self):
  with tempfile.TemporaryDirectory()as t:
   root=Path(t);o,r,e,a=self.context(root);e['submitted'][str(root/'C5/UNIT.C')]=b'foreign'
   with self.assertRaises(ValueError):pipeline.before_process(o,r,e,root,a,{})
 def test_inert_MASM_phase_derivation_contract(self):
  with tempfile.TemporaryDirectory()as t:
   root=Path(t);o,r,e,a=self.context(root,True);self.assertEqual(pipeline.before_process(o,r,e,root,a,{}),'MASM')
 def test_MASM_without_actual_C5_output_read_denied(self):
  with tempfile.TemporaryDirectory()as t:
   root=Path(t);o,r,e,a=self.context(root,True);e['_mixed_read_bytes'].pop('C5/UNIT.OBJ')
   with self.assertRaises(ValueError):pipeline.before_process(o,r,e,root,a,{})
 def test_MASM_before_C5_termination_denied(self):
  with tempfile.TemporaryDirectory()as t:
   root=Path(t);o,r,e,a=self.context(root,True);e['processes'][0]['object']=SimpleNamespace(poll=lambda:None)
   with self.assertRaises(ValueError):pipeline.before_process(o,r,e,root,a,{})
 def test_injected_MASM_source_denied(self):
  with tempfile.TemporaryDirectory()as t:
   root=Path(t);o,r,e,a=self.context(root,True);e['submitted'][str(root/'MASM/UNIT.ASM')]+=b'wrong'
   with self.assertRaises(ValueError):pipeline.before_process(o,r,e,root,a,{})
if __name__=='__main__':unittest.main()
