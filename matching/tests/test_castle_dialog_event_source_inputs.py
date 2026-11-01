"""Focused compatible castle/event profile controls; no target compiler in tests."""
from pathlib import Path
import copy,dataclasses,hashlib,importlib,json,sys,tempfile,unittest
from unittest.mock import patch
PROJECT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(PROJECT))
import castle_dialog_event_source_inputs as profile
import source_inputs
from omf import read_omf
D=PROJECT/'build/move-flash-coherent455-preparation-v3/castle-fixtures'
class CastleEventTests(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  assert Path(profile.__file__)==PROJECT/'castle_dialog_event_source_inputs.py'and Path(source_inputs.__file__)==PROJECT/'source_inputs.py'
  c.item=json.loads((D/'proposed-source-input.json').read_text());c.raw=(PROJECT/profile.PINS['object']['path']).read_bytes()
 def mutate(self,kind,fn,occurrence=0):
  out=[];seen=0
  for k,at,p in read_omf(self.raw).records:
   if k==kind:
    if seen==occurrence:p=fn(p)
    seen+=1
   raw=bytes([k])+(len(p)+1).to_bytes(2,'little')+p;out.append(raw+bytes([-sum(raw)&255]))
  return b''.join(out)
 def test_exact_record_two_typed_definitions_zero_loaded(self):
  defs=profile.validate_object(self.raw);self.assertEqual([d['size']for d in defs],[2,20]);o=read_omf(self.raw);self.assertFalse(o.publics);self.assertFalse(o.procedures);self.assertTrue(all(not s.length for s in o.segments.values()if s.class_name not in['DEBSYM','DEBTYP']))
 def test_genuine18_last_copied_word_rejected(self):
  with self.assertRaises(ValueError):profile.validate_object((PROJECT/profile.PINS['wrong18']['path']).read_bytes())
 def test_wrong_storage_member_offset_or_loaded_CODE_rejected(self):
  raws=[self.mutate(0xb0,lambda p:p.replace(b'\x62\x14',b'\x61\x14')),self.mutate(0xa0,lambda p:p.replace(b'word9\x88\x12',b'word9\x88\x10'),1),self.mutate(0x98,lambda p:p[:1]+b'\x01\0'+p[3:])]
  for raw in raws:
   with self.assertRaises(ValueError):profile.validate_object(raw)
 def test_exact_profile_fields_flags_and_source(self):
  profile.validate_item(self.item)
  for delta in[{'flags':['/AM']},{'source':'../state.c'},{'extra':True}]:
   with self.assertRaises(ValueError):profile.validate_item(dict(self.item,**delta))
 def test_source_hash_failure_before_generation(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);s=p/profile.SOURCE;s.parent.mkdir(parents=True);s.write_text('int castle_owner,dialog_event;\n')
   with patch.object(profile,'compile_c',side_effect=AssertionError('must not compile')),self.assertRaisesRegex(ValueError,'source hash'):profile.build_input(self.item,p,PROJECT.parent/'CHESS.EXE',p/'out')
 def test_fresh_tool_provenance_is_required(self):
  from msc import CompileResult
  c=CompileResult(object_bytes=self.raw,**json.loads((PROJECT/profile.PINS['generation']['path']).read_text())['compiler']);c=dataclasses.replace(c,tool_hashes={})
  with tempfile.TemporaryDirectory()as t,self.assertRaisesRegex(ValueError,'provenance'):profile.build_input(self.item,PROJECT,PROJECT.parent/'CHESS.EXE',Path(t),compiler_fn=lambda*a,**k:c)
 def test_duplicate_provided_symbol_before_generation(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);cfg=p/'cfg.json';cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[self.item]}))
   with patch.object(source_inputs,'compile_c',side_effect=AssertionError('must not compile')),self.assertRaisesRegex(ValueError,'duplicate allocation symbol'):source_inputs.build_source_inputs(PROJECT,PROJECT.parent/'CHESS.EXE',p/'out',config_path=cfg,defined_symbols={'_dialog_event'})
 def test_duplicate_item_calls_builder_only_once(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);cfg=p/'cfg.json';cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[self.item,self.item]}))
   with patch.object(profile,'build_input',return_value={'id':self.item['id']})as call,self.assertRaisesRegex(ValueError,'duplicate source allocation'):source_inputs.build_source_inputs(PROJECT,PROJECT.parent/'CHESS.EXE',p/'out',config_path=cfg)
   self.assertEqual(call.call_count,1)
 def test_actual_native13_fields_and20_copy_constraints(self):
  constraints=profile.validate_evidence(PROJECT,self.item['evidence'],PROJECT.parent/'CHESS.EXE');self.assertEqual([x['size']for x in constraints],[2,20]);self.assertEqual(constraints[1]['end_exclusive'],'0x52ea');self.assertFalse(constraints[1]['historical_storageclass_TU_MAP_proven'])
 def test_wrong_original_and_evidence_identity_rejected(self):
  pins=copy.deepcopy(profile.PINS);pins['native_fields']['sha256']='0'*64
  with self.assertRaises(ValueError):profile.validate_evidence(PROJECT,pins,PROJECT.parent/'CHESS.EXE')
  with tempfile.TemporaryDirectory()as t:
   p=Path(t)/'wrong.exe';p.write_bytes(b'MZbad')
   with self.assertRaises(ValueError):profile.validate_evidence(PROJECT,profile.PINS,p)
 def test_historical_storage_claim_or_DF_limit_removal_rejected(self):
  path=PROJECT/profile.PINS['native_fields']['path'];base=json.loads(path.read_text());read=Path.read_bytes
  for field,value in[('ordinary_DF_clear_C_ABI_assumed',False),('original_storageclass_static_TU_commonstart_or_MAP_proven',True)]:
   x=dict(base);x[field]=value;raw=json.dumps(x).encode();pins=copy.deepcopy(profile.PINS);pins['native_fields']['sha256']=hashlib.sha256(raw).hexdigest()
   with patch.object(profile,'PINS',pins),patch.object(Path,'read_bytes',lambda p:raw if p==path else read(p)),self.assertRaisesRegex(ValueError,'limits'):profile.validate_evidence(PROJECT,pins,PROJECT.parent/'CHESS.EXE')
 def test_all20_old_decoder_fixtures_unchanged(self):
  rows=json.loads((D/'old20-profile-compatibility-inputs.json').read_text());self.assertEqual(len(rows),20)
  for row in rows:
   raw=(PROJECT/row['object']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),row['sha256']);defs=importlib.import_module(row['module']).validate_object(raw);self.assertEqual([d['symbol']for d in defs],[d['symbol']for d in row['definitions']])
 def test_prior20_config_rows_unchanged_and_pending_components_absent(self):
  old=json.loads((D/'source-inputs.base20.json').read_text());new=json.loads((D/'source-inputs.castle-event-only21.json').read_text());self.assertEqual(new['source_allocations'][:-1],old['source_allocations']);self.assertEqual(len(old['source_allocations']),20);self.assertFalse(any(x['id']in['rays239-common','input-timer-common']for x in new['source_allocations']))
if __name__=='__main__':unittest.main(verbosity=2)
