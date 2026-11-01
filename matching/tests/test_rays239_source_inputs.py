"""Closed Ray239 component tests; generated files only in TemporaryDirectory."""
from pathlib import Path
import copy,dataclasses,hashlib,importlib,json,sys,tempfile,unittest
from unittest.mock import patch
PROJECT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(PROJECT))
import rays239_source_inputs as profile
import source_inputs
from omf import read_omf
D=PROJECT/'build/rays239-source-profile-stage'
class Rays239Tests(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  assert Path(profile.__file__)==PROJECT/'rays239_source_inputs.py'and Path(source_inputs.__file__)==PROJECT/'source_inputs.py'
  c.item=json.loads((D/'proposed-source-input.json').read_text());c.raw=(PROJECT/profile.PINS['object']['path']).read_bytes()
 def mutate(self,k,fn,occurrence=0):
  out=[];seen=0
  for kind,at,payload in read_omf(self.raw).records:
   if kind==k:
    if seen==occurrence:payload=fn(payload)
    seen+=1
   raw=bytes([kind])+(len(payload)+1).to_bytes(2,'little')+payload;out.append(raw+bytes([-sum(raw)&255]))
  return b''.join(out)
 def bad(self,raw,regex=None):
  with self.assertRaisesRegex(ValueError,regex)if regex else self.assertRaises(ValueError):profile.validate_object(raw)
 def test_actual_complete239_956_zero_loaded(self):
  self.assertEqual(profile.validate_object(self.raw),[{'symbol':'_rays','type_index':519,'datatype':98,'size':956}]);o=read_omf(self.raw);self.assertFalse(o.publics);self.assertFalse(o.procedures);self.assertTrue(all(s.length==0 for s in o.segments.values()if s.class_name not in ['DEBSYM','DEBTYP']))
 def test_actual_wrong238_source_object_fails(self):self.bad((PROJECT/profile.PINS['wrong238']['path']).read_bytes(),'956')
 def test_common_zero_short_extra_extent_rejected(self):
  for n in [0,952,960]:self.bad(self.mutate(0xb0,lambda p:p[:-2]+n.to_bytes(2,'little')),'956')
 def test_type_storage_leaf_rejected(self):
  self.bad(self.mutate(0xb0,lambda p:p.replace(b'\x82\x07',b'\x82\x06')))
  self.bad(self.mutate(0xb0,lambda p:p.replace(b'\x62\x81',b'\x61\x81')))
  self.bad(self.mutate(0xb0,lambda p:p.replace(b'\x62\x81',b'\x62\x88')))
 def test_duplicate_or_extra_common_rejected(self):self.bad(self.mutate(0xb0,lambda p:p+p),'single')
 def test_alias_rejected(self):self.bad(self.mutate(0xb0,lambda p:p.replace(b'_rays',b'_fake')))
 def test_loaded_CODE_DATA_BSS_rejected(self):
  for n in [0,1,3]:self.bad(self.mutate(0x98,lambda p:p[:1]+b'\x01\0'+p[3:],n),'allocation')
 def test_member_unsignedness_rejected(self):self.bad(self.mutate(0xa0,lambda p:p.replace(bytes.fromhex('7f838500838100'),bytes.fromhex('7f838100838100')),1),'CodeView')
 def test_member_offset_rejected(self):self.bad(self.mutate(0xa0,lambda p:p.replace(b'step\x88\x02',b'step\x88\x01'),1),'CodeView')
 def test_array_CV_size_rejected(self):self.bad(self.mutate(0xa0,lambda p:p.replace(bytes.fromhex('7885e01d'),bytes.fromhex('7885c01d')),1),'CodeView')
 def test_debug_field_rejected(self):self.bad(self.mutate(0x9c,lambda p:p[:-1]+b'\x01',1))
 def test_PRODUCER_DGROUP_rejected(self):
  self.bad(self.mutate(0x80,lambda p:p.replace(b'UNIT.C',b'FAKE.C')),'filename');self.bad(self.mutate(0x9a,lambda p:p[:-1]+b'\x03'),'DGROUP')
 def test_checksum_truncate_EOF_rejected(self):
  for raw in [self.raw[:-1],self.raw+b'\0',bytes([self.raw[0]^1])+self.raw[1:],bytearray(self.raw)]:self.bad(raw)
 def test_unknown_or_capacity_item_rejected(self):
  profile.validate_item(self.item)
  for delta in [{'capacity':240},{'alias':'_rays'},{'source':'../rays.c'},{'source_sha256':'0'*64},{'flags':['/AM']},{'objects':[{'symbol':'_rays','size':True,'storage':'near-common'}]}]:
   with self.assertRaises(ValueError):profile.validate_item(dict(self.item,**delta))
 def test_source_mismatch_before_compiler(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);s=p/profile.SOURCE;s.parent.mkdir(parents=True);s.write_text('int rays[239];\n')
   with patch.object(profile,'compile_c',side_effect=AssertionError('must not compile')),self.assertRaisesRegex(ValueError,'source hash'):profile.build_input(self.item,p,PROJECT.parent/'CHESS.EXE',p/'out')
 def test_wrong_fresh_provenance_rejected(self):
  from msc import CompileResult
  c=CompileResult(object_bytes=self.raw,**json.loads((PROJECT/profile.PINS['compiler_controls']['path']).read_text())['controls'][0]['compiler'])
  with tempfile.TemporaryDirectory()as t:
   for delta in [{'source_name':'FAKE.C'},{'flags':['/AS']},{'tool_hashes':{}},{'compiler':'msc510'}]:
    wrong=dataclasses.replace(c,**delta)
    with self.assertRaisesRegex(ValueError,'provenance'):profile.build_input(self.item,PROJECT,PROJECT.parent/'CHESS.EXE',Path(t),compiler_fn=lambda*a,**k:wrong)
 def test_duplicate_selected_symbol_pre_generation(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);cfg=p/'cfg.json';cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[self.item]}))
   with patch.object(source_inputs,'compile_c',side_effect=AssertionError('must not compile')),self.assertRaisesRegex(ValueError,'duplicate allocation symbol'):source_inputs.build_source_inputs(PROJECT,PROJECT.parent/'CHESS.EXE',p/'out',config_path=cfg,defined_symbols={'_rays'})
 def test_duplicate_item_route_only_guard(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);cfg=p/'cfg.json';cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[self.item,self.item]}))
   with patch.object(profile,'build_input',return_value={'id':self.item['id']})as call,self.assertRaisesRegex(ValueError,'duplicate source allocation'):source_inputs.build_source_inputs(PROJECT,PROJECT.parent/'CHESS.EXE',p/'out',config_path=cfg)
   self.assertEqual(call.call_count,1)
 def test_no_path_escape(self):
  for n in ['../CHESS.EXE','/tmp/rays.c']:
   with self.assertRaises(ValueError):profile.local(PROJECT,n)
 def test_evidence_and_wrong_original_rejected(self):
  wrong=copy.deepcopy(self.item['evidence']);wrong['crt']['sha256']='0'*64
  with self.assertRaises(ValueError):profile.validate_evidence(PROJECT,wrong,PROJECT.parent/'CHESS.EXE')
  with tempfile.TemporaryDirectory()as t:
   p=Path(t)/'wrong.exe';p.write_bytes(b'MZbad')
   with self.assertRaises(ValueError):profile.validate_evidence(PROJECT,self.item['evidence'],p)
 def altered(self,key,fn,regex):
  row=profile.PINS[key];path=PROJECT/row['path'];data=json.loads(path.read_text());fn(data);raw=json.dumps(data).encode();pins=copy.deepcopy(profile.PINS);pins[key]['sha256']=hashlib.sha256(raw).hexdigest();original=Path.read_bytes
  def rb(p):return raw if p==path else original(p)
  with patch.object(profile,'PINS',pins),patch.object(Path,'read_bytes',rb),self.assertRaisesRegex(ValueError,regex):profile.validate_evidence(PROJECT,pins,PROJECT.parent/'CHESS.EXE')
 def test_historical_capacity_claim_rejected(self):self.altered('review',lambda p:p.update(historical_unique_capacity_container_owner_TU_MAP_proven=True),'historical')
 def test_held_initializer_credit_rejected(self):self.altered('review',lambda p:p.update(held_initializer_C_match_claimed=True),'heldC')
 def test_overlap_rejected(self):self.altered('review',lambda p:p.update(existing_native_anchored_COMMON_overlap=['fake']),'overlap')
 def test_pawn_width_rejected(self):self.altered('review',lambda p:p['upper_bound_independent_distinct_supplied_scalar'].update(size=4),'pawn upper')
 def test_native_primary_subject_rejected(self):self.altered('init_primary',lambda p:p['subject']['digest'].update(sha256='0'*64),'primary')
 def test_oracle_realgame_overclaim_rejected(self):self.altered('native_oracle',lambda p:p.update(not_C_match_or_complete_game_execution=False),'contract limits')
 def test_actual_native_extent_constraints(self):
  r=profile.validate_evidence(PROJECT,self.item['evidence'],PROJECT.parent/'CHESS.EXE');self.assertEqual(len(r),1);self.assertEqual(r[0]['logical_records'],239);self.assertFalse(r[0]['resolved']);self.assertFalse(r[0]['unique_historical_capacity_container_TU_type'])
 def test_all20_old_decoders_unchanged(self):
  rows=json.loads((D/'old20-profile-compatibility-inputs.json').read_text());self.assertEqual(len(rows),20)
  for r in rows:
   raw=(PROJECT/r['object']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),r['sha256']);defs=importlib.import_module(r['module']).validate_object(raw);self.assertEqual([d['symbol']for d in defs],[d['symbol']for d in r['definitions']])
if __name__=='__main__':unittest.main(verbosity=2)
