"""Closed WORDprovider; all generated files live under TemporaryDirectory."""
from pathlib import Path
import copy,dataclasses,hashlib,json,sys,tempfile,unittest
from unittest.mock import patch
PROJECT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(PROJECT))
import source_inputs
import turn_phase_source_inputs as profile
from omf import read_omf
D=PROJECT/'build/turn-phase-common-profile-stage';FIXTURE=PROJECT/'build/turn-phase-57cc-ownership'
class TurnPhaseCommonTests(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  assert Path(profile.__file__)==PROJECT/'turn_phase_source_inputs.py'
  assert Path(source_inputs.__file__)==PROJECT/'source_inputs.py'
  c.item=json.loads((D/'proposed-source-input.json').read_text());c.data=(FIXTURE/'candidate_state_57cc.obj').read_bytes()
 def mutate(self,kind,fn,*,occurrence=0):
  records=read_omf(self.data).records;out=bytearray();seen=0
  for k,at,p in records:
   if k==kind:
    if seen==occurrence:p=fn(p)
    seen+=1
   raw=bytes([k])+(len(p)+1).to_bytes(2,'little')+p;out.extend(raw+bytes([-sum(raw)&255]))
  return bytes(out)
 def bad(self,raw,regex=None):
  with self.assertRaisesRegex(ValueError,regex)if regex else self.assertRaises(ValueError):profile.validate_object(raw)
 def test_actual_WORD2_no_loaded_PUBLIC_or_function(self):
  self.assertEqual(profile.validate_object(self.data),[{'symbol':'_state_57cc','type_index':129,'datatype':98,'size':2}]);o=read_omf(self.data);self.assertFalse(o.publics);self.assertFalse(o.procedures);self.assertTrue(all(s.length==0 for s in o.segments.values()if s.class_name not in ['DEBSYM','DEBTYP']))
 def test_builtin_WORD_debug_and_sole_debug_field(self):
  o=read_omf(self.data);self.assertEqual(o.segments[5].chunks,[(0,bytes.fromhex('12050000000081000a73746174655f35376363'))]);self.assertEqual(o.externals,{1:'__acrtused',2:'_state_57cc'});self.assertEqual([(f.segment,f.offset,f.width,f.target)for f in o.fixups],[(5,2,4,(2,2))])
 def test_wrong_size1_and_zero_size_rejected(self):
  for size in [0,1,4]:self.bad(self.mutate(0xb0,lambda p:p[:-1]+bytes([size])),'COMDEF')
 def test_unsigned_and_BYTE_type_rejected(self):
  for typ in [0x80,0x84,0x85]:self.bad(self.mutate(0xb0,lambda p:p[:-3]+bytes([typ])+p[-2:]),'COMDEF')
 def test_far_or_unsupported_storage_rejected(self):
  for mode in [0x61,0x63]:self.bad(self.mutate(0xb0,lambda p:p[:-2]+bytes([mode])+p[-1:]))
 def test_extra_or_duplicate_definition_rejected(self):
  self.bad(self.mutate(0xb0,lambda p:p+p),'COMDEF')
 def test_alias_name_and_zero_length_symbol_rejected(self):
  self.bad(self.mutate(0xb0,lambda p:p.replace(b'_state_57cc',b'_search_end')))
  self.bad(self.mutate(0xb0,lambda p:bytes([0])+p[12:]))
 def test_wrong_loaded_CODE_DATA_or_BSS_size_rejected(self):
  for i in [0,1,3]:self.bad(self.mutate(0x98,lambda p:p[:1]+b'\x01\0'+p[3:],occurrence=i),'allocation')
 def test_checksum_truncation_EOF_and_rawtype_rejected(self):
  for raw in [self.data[:-1],self.data+b'\0',bytes([self.data[0]^1])+self.data[1:],bytearray(self.data)]:self.bad(raw)
 def test_DGROUP_and_producer_filename_changed_rejected(self):
  self.bad(self.mutate(0x9a,lambda p:p[:-1]+b'\x03'),'DGROUP');self.bad(self.mutate(0x80,lambda p:p.replace(b'UNIT.C',b'FAKE.C')),'filename')
 def test_debug_type_or_patch_bytes_changed_rejected(self):
  self.bad(self.mutate(0xa0,lambda p:p[:9]+b'\x84'+p[10:]),'debug');self.bad(self.mutate(0x9c,lambda p:p[:-1]+b'\x03',occurrence=1))
 def test_record_removal_and_extra_foreign_record_rejected(self):
  records=read_omf(self.data).records;extra=b'\xc2\x02\0\0';extra+=bytes([-sum(extra)&255]);self.bad(self.data[:-4]+extra+self.data[-4:])
 def test_exact_item_rejects_source_size_alias_capacity(self):
  profile.validate_item(self.item)
  for delta in [{'source':'../elsewhere.c'},{'source_sha256':'0'*64},{'compiler':'msc510'},{'flags':['/AM']},{'capacity':48},{'objects':[{'symbol':'_search_stack_end','size':2,'storage':'near-common'}]},{'objects':[{'symbol':'_state_57cc','size':True,'storage':'near-common'}]}]:
   with self.subTest(delta=delta),self.assertRaises(ValueError):profile.validate_item(dict(self.item,**delta))
 def test_wrong_evidence_pin_and_target_rejected(self):
  item=copy.deepcopy(self.item);item['evidence']['crt']['sha256']='0'*64
  with self.assertRaises(ValueError):profile.validate_item(item)
  with tempfile.TemporaryDirectory()as tmp:
   target=Path(tmp)/'bad.exe';target.write_bytes(b'MZbad')
   with self.assertRaises(ValueError):profile.validate_evidence(PROJECT,self.item['evidence'],target)
 def test_native_WORD_lifecycle_and_CRT_constraint(self):
  p=profile.validate_evidence(PROJECT,self.item['evidence'],PROJECT.parent/'CHESS.EXE');self.assertEqual(p[0]['dgroup_offset'],'0x57cc');self.assertEqual(p[0]['end_exclusive'],'0x57ce');self.assertFalse(p[0]['resolved']);self.assertFalse(p[0]['historical_COMMON_order_proven'])

 def test_escape_and_absolute_path_rejected(self):
  for name in ['../CHESS.EXE','/tmp/source.c']:
   with self.assertRaises(ValueError):profile.local(PROJECT,name)
 def test_changed_source_rejected_before_compiler(self):
  with tempfile.TemporaryDirectory()as tmp:
   p=Path(tmp);src=p/profile.SOURCE;src.parent.mkdir(parents=True);src.write_text('unsigned char state_57cc;\n')
   with patch.object(profile,'compile_c',side_effect=AssertionError('must not compile')),self.assertRaisesRegex(ValueError,'source hash'):profile.build_input(self.item,p,PROJECT.parent/'CHESS.EXE',p/'out')
 def test_duplicate_symbol_precedes_generation(self):
  with tempfile.TemporaryDirectory()as tmp:
   p=Path(tmp);cfg=p/'cfg.json';cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[self.item]}))
   with patch.object(source_inputs,'compile_c',side_effect=AssertionError('must not compile')),self.assertRaisesRegex(ValueError,'duplicate allocation symbol'):source_inputs.build_source_inputs(PROJECT,PROJECT.parent/'CHESS.EXE',p/'out',config_path=cfg,defined_symbols={'_state_57cc'})
 def test_duplicate_item_guard_preserves_dispatch_semantics(self):
  # Route-only control; actual fresh production proof is separate and never stubbed.
  with tempfile.TemporaryDirectory()as tmp:
   p=Path(tmp);cfg=p/'cfg.json';cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[self.item,self.item]}))
   with patch.object(profile,'build_input',return_value={'id':self.item['id']})as fn,self.assertRaisesRegex(ValueError,'duplicate source allocation'):source_inputs.build_source_inputs(PROJECT,PROJECT.parent/'CHESS.EXE',p/'out',config_path=cfg)
   self.assertEqual(fn.call_count,1)
 def test_client_proof_keeps_all_complete_allocations(self):
  p=json.loads((FIXTURE/'client-controls.json').read_text());self.assertEqual(p['status'],'PASS');self.assertEqual(len(p['sources']),2);self.assertEqual(sum(r['whole_CODE_size']for r in p['sources']),1758);self.assertEqual(sum(len(r['CVs'])for r in p['sources']),18);self.assertEqual(sum(r['raw_runtime_FIXUPP_count']for r in p['sources']),202);self.assertTrue(all(r['whole_CODE_native_exact']and len(r['wrong_binding_control'])==1 for r in p['sources']))

 def test_PUBLIC_alias_and_missing_COMDEF_rejected(self):
  def enc(k,p):
   raw=bytes([k])+(len(p)+1).to_bytes(2,'little')+p;return raw+bytes([-sum(raw)&255])
  records=read_omf(self.data).records;raw=b''.join(enc(k,p)for k,at,p in records if k!=0xb0);self.bad(raw)
  raw=self.data[:-4]+enc(0x90,bytes.fromhex('00040000')+b'\x0b_state_57cc'+bytes.fromhex('8084'))+self.data[-4:];self.bad(raw)
 def test_wrong_fresh_compiler_provenance_rejected(self):
  from msc import CompileResult
  meta=json.loads((FIXTURE/'compiler-controls.json').read_text())['controls'][0]['compiler'];c=CompileResult(object_bytes=self.data,**meta)
  for delta in [{'compiler':'msc510'},{'source_name':'FAKE.C'},{'flags':['/AS']},{'toolchain_manifest_sha256':'0'*64},{'tool_hashes':{}}]:
   wrong=dataclasses.replace(c,**delta)
   with tempfile.TemporaryDirectory()as tmp,self.subTest(delta=delta),self.assertRaisesRegex(ValueError,'provenance'):
    profile.build_input(self.item,PROJECT,PROJECT.parent/'CHESS.EXE',Path(tmp)/'out',compiler_fn=lambda *a,**k:wrong)

 def test_all19_existing_profile_objects_validate_unchanged(self):
  import importlib
  rows=json.loads((D/'old19-profile-compatibility-inputs.json').read_text());self.assertEqual(len(rows),19)
  for r in rows:
   raw=(PROJECT/r['object']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),r['sha256']);defs=importlib.import_module(r['module']).validate_object(raw);self.assertEqual([d['symbol']for d in defs],[d['symbol']for d in r['definitions']])

 def altered_evidence(self,key,mutate,regex):
  row=profile.PINS[key];path=PROJECT/row['path'];payload=json.loads(path.read_text());mutate(payload);raw=json.dumps(payload).encode();pins=copy.deepcopy(profile.PINS);pins[key]['sha256']=hashlib.sha256(raw).hexdigest();original=Path.read_bytes
  def changed(p):return raw if p==path else original(p)
  with patch.object(profile,'PINS',pins),patch.object(Path,'read_bytes',changed),self.assertRaisesRegex(ValueError,regex):profile.validate_evidence(PROJECT,pins,PROJECT.parent/'CHESS.EXE')
 def test_address_only_claim_rejected(self):
  self.altered_evidence('review',lambda p:p['actual_runtime_WORD_fields'][0].update(address_only=True),'real WORD')
 def test_wrong_native_coordinate_rejected(self):
  self.altered_evidence('review',lambda p:p['actual_runtime_WORD_fields'][0].update(native_field_image='0x7e64'),'coordinates')
 def test_wrong_count_rejected(self):
  self.altered_evidence('review',lambda p:p['actual_reference_counts'].update(_state=2),'exact10')
 def test_wrong_client_type_rejected(self):
  self.altered_evidence('review',lambda p:next(iter(p['actual_sources_AST'].values()))['declarations'][0].update(type='unsigned char'),'client int ABI')
 def test_wrong_primary_subject_rejected(self):
  self.altered_evidence('primary_0',lambda p:p['subject']['digest'].update(sha256='0'*64),'profile')
 def test_wrong_primary_loader_rejected(self):
  self.altered_evidence('primary_0',lambda p:p['analysis_profile']['parameters'].update(loader='BinaryLoader'),'profile')
 def test_wrong_CRT_bound_rejected(self):
  self.altered_evidence('crt',lambda p:p['normalized_result'].update(bytes_hex='00'*179),'CRT')
 def test_no_boolean_item_size(self):
  wrong=copy.deepcopy(self.item);wrong['objects'][0]['size']=True
  with self.assertRaises(ValueError):profile.validate_item(wrong)

 def test_wrong_primary_procedure_rejected(self):
  self.altered_evidence('primary_0',lambda p:p['parameters'].update(procedure='0x1801a'),'profile')
 def test_wrong_primary_operation_rejected(self):
  self.altered_evidence('primary_0',lambda p:p.update(operation='read_bytes'),'profile')
 def test_wrong_raw_field_symbol_rejected(self):
  self.altered_evidence('review',lambda p:p['actual_runtime_WORD_fields'][0].update(symbol='_madeup'),'raw client field')
if __name__=='__main__':unittest.main(verbosity=2)
