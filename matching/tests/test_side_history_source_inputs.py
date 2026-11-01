"""Closed third COMMON profile and all-three-profile source-only gates."""
import copy,dataclasses,importlib.util,json,shutil,struct,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
PROJECT=next(p for p in Path(__file__).resolve().parents if(p/'config/msc500.json').exists())
STAGE=Path(__file__).resolve().parent
sys.path[:0]=[str(STAGE),str(PROJECT)]
import side_history_source_inputs as side
from msc import compile_c
from omf import read_omf
spec=importlib.util.spec_from_file_location('staged_source_inputs_side',(STAGE/'source_inputs.py'if(STAGE/'source_inputs.py').exists()else PROJECT/'source_inputs.py'))
dispatch=importlib.util.module_from_spec(spec);spec.loader.exec_module(dispatch)

def record(kind,payload):
 b=bytes([kind])+struct.pack('<H',len(payload)+1)+payload
 return b+bytes([-sum(b)&255])

def mutate(data,kind,change):
 out=[];changed=False
 for k,_,p in read_omf(data).records:
  if k==kind and not changed:p=change(p);changed=True
  out.append(record(k,p))
 assert changed
 return b''.join(out)

class SideHistoryInputsTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.config=json.loads((PROJECT/'build/side-history-profile/source-inputs.proposed.json').read_text())
  cls.item=cls.config['source_allocations'][2]
  cls.compiled={}
  for name,source in [('asset_selectors.c','src/link/asset_selectors.c'),('clock_state.c','src/link/clock_state.c'),('side_history_state.c','build/side-history-storage/scalars.c')]:
   cls.compiled[name]=compile_c(PROJECT/source,side.FLAGS,compiler='msc500')
  cls.obj=cls.compiled['side_history_state.c'].object_bytes
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(prefix='bc-side-profile-test-');self.addCleanup(self.tmp.cleanup)
  self.project=Path(self.tmp.name)/'matching';self.project.mkdir();self.out=self.project/'objects'
  for item in self.config['source_allocations']:
   source=PROJECT/('build/side-history-storage/scalars.c'if item['source']==side.SOURCE else item['source'])
   p=self.project/item['source'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,p)
   for row in item['evidence'].values():
    p=self.project/row['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(PROJECT/row['path'],p)
  self.path=self.project/'registry.json'
 def run_config(self,config=None,defined=()):
  self.path.write_text(json.dumps(self.config if config is None else config))
  with patch.object(dispatch,'compile_c',side_effect=lambda p,*a,**kw:self.compiled[Path(p).name]):
   return dispatch.build_source_inputs(self.project,PROJECT.parent/'CHESS.EXE',self.out,self.path,defined_symbols=defined)
 def bad_obj(self,raw):
  with self.assertRaises(ValueError):side.validate_object(raw)
 def test_fresh_actual_whole_object_and_full_CV_types(self):
  self.assertEqual(side.sha(self.obj),side.OBJECT_SHA)
  rows=side.validate_object(self.obj)
  self.assertEqual([r['symbol']for r in rows],side.NAMES)
  self.assertEqual([r['size']for r in rows],[2]*5+[8]);self.assertEqual([r['type_index']for r in rows],[0x81]*5+[522])
  obj=read_omf(self.obj);self.assertFalse(obj.publics);self.assertEqual([obj.segments[i].length for i in(5,6)],[129,177])
 def test_fresh_real_build_zero_credit_and_unresolved_MAP(self):
  built=side.build_input(self.item,self.project,PROJECT.parent/'CHESS.EXE',self.out)
  self.assertEqual(built['allocation_bytes'],18);self.assertEqual(built['initialized_bytes'],0)
  self.assertEqual(built['matching_credit'],0);self.assertFalse(built['placement_proven'])
  self.assertEqual((self.out/'side-history-common.obj').read_bytes(),self.obj)
  self.assertTrue(all(not c['resolved']for c in built['original_map_constraints']))
  self.assertEqual([c['dgroup_offset']for c in built['original_map_constraints']],[hex(x)for x in side.OFFSETS])
 def test_all_three_profiles_seventeen_definitions(self):
  result=self.run_config();self.assertEqual(len(result['objects']),3)
  self.assertEqual([r['allocation_bytes']for r in result['objects']],[32,12,18])
  self.assertEqual(sum(len(r['definitions'])for r in result['objects']),17)
  self.assertEqual(sum(r['allocation_bytes']for r in result['objects']),62)
  self.assertEqual(sum(r['initialized_bytes']for r in result['objects']),0)
  self.assertEqual(result['matching_credit'],0);self.assertFalse(result['placement_proven'])
  self.assertEqual([len(r['definitions'])for r in dispatch.report_inputs(result)],[8,3,6])
  self.assertFalse({'units','summary','c_matched_bytes','source_data_bytes','verified_image_span_bytes'}&set(result))
 def test_original_two_profiles_outputs_unchanged(self):
  config=copy.deepcopy(self.config);config['source_allocations'].pop()
  result=self.run_config(config)
  self.assertEqual([r['object_sha256']for r in result['objects']],[dispatch.OBJECT_SHA,__import__('clock_source_inputs').OBJECT_SHA])
  self.assertEqual([len(r['definitions'])for r in result['objects']],[8,3])
 def test_all_profile_orderings(self):
  for order in[(2,0,1),(1,2,0)]:
   c=copy.deepcopy(self.config);c['source_allocations']=[c['source_allocations'][i]for i in order]
   self.assertEqual([r['id']for r in self.run_config(c)['objects']],[self.config['source_allocations'][i]['id']for i in order])
 def test_absent_and_empty_registry_unchanged(self):
  self.assertEqual(dispatch.build_source_inputs(self.project,Path('absent'),self.out,self.project/'absent.json')['objects'],[])
  self.assertEqual(self.run_config({'schema_version':1,'source_allocations':[]})['objects'],[])
 def test_duplicate_side_source_and_selected_provider(self):
  c=copy.deepcopy(self.config);c['source_allocations'].append(copy.deepcopy(self.item))
  with self.assertRaisesRegex(ValueError,'duplicate'):self.run_config(c)
  for n in side.NAMES:
   with self.subTest(n=n),self.assertRaisesRegex(ValueError,'already matched'):self.run_config(defined=[n])
 def test_duplicate_source_across_profiles_rejected(self):
  c=copy.deepcopy(self.config);c['source_allocations'][2]['source']=c['source_allocations'][1]['source']
  with self.assertRaisesRegex(ValueError,'duplicate'):self.run_config(c)
 def test_closed_metadata_and_no_credit_override(self):
  for k,v in [('id','other'),('backend','msc500-near-common-clock-v1'),('source','../side.c'),('source_sha256','0'*64),
              ('compiler','msc510'),('flags',['/AS']),('toolchain_manifest_sha256','0'*64),('matching_credit',18)]:
   row=copy.deepcopy(self.item);row[k]=v
   with self.subTest(k=k),self.assertRaises(ValueError):side.validate_item(row)
 def test_incomplete_or_retyped_definition_list(self):
  for edit in(lambda r:r['objects'].pop(),lambda r:r['objects'][0].update(size=4),
              lambda r:r['objects'][-1].update(size=6),lambda r:r['objects'][0].update(symbol='_oldalias'),
              lambda r:r['objects'][0].update(storage='far-common')):
   row=copy.deepcopy(self.item);edit(row)
   with self.assertRaises(ValueError):side.validate_item(row)
 def test_unknown_backend_cannot_fall_through(self):
  c=copy.deepcopy(self.config);c['source_allocations'][2]['backend']='unsupported'
  with self.assertRaises(ValueError):self.run_config(c)
 def test_source_changed_rejected_before_compile(self):
  (self.project/side.SOURCE).write_text('int temporary=0;')
  with patch.object(side,'compile_c',side_effect=AssertionError('must not compile')):
   with self.assertRaisesRegex(ValueError,'source pin'):side.build_input(self.item,self.project,PROJECT.parent/'CHESS.EXE',self.out)
 def test_compiler_source_flags_name_manifest_tool_command(self):
  c=self.compiled['side_history_state.c']
  for changed in(dataclasses.replace(c,source_sha256='0'*64),dataclasses.replace(c,compiler='msc510'),
     dataclasses.replace(c,flags=('/AS',)),dataclasses.replace(c,source_name='OTHER.C'),
     dataclasses.replace(c,toolchain_manifest_sha256='0'*64),dataclasses.replace(c,tool_hashes={}),dataclasses.replace(c,command=())):
   with self.assertRaises(ValueError):side.build_input(self.item,self.project,PROJECT.parent/'CHESS.EXE',self.out,compiler_fn=lambda *a,**k:changed)
 def test_source_mutation_during_compile(self):
  def altered(*a,**kw):(self.project/side.SOURCE).write_bytes(b'int different;');return self.compiled['side_history_state.c']
  with self.assertRaisesRegex(ValueError,'provenance'):side.build_input(self.item,self.project,PROJECT.parent/'CHESS.EXE',self.out,compiler_fn=altered)
 def test_evidence_pins_closed_identity(self):
  for key in self.item['evidence']:
   row=copy.deepcopy(self.item);row['evidence'][key]['sha256']='0'*64
   with self.subTest(key=key),self.assertRaises(ValueError):side.validate_item(row)
  with self.assertRaises(ValueError):side.local(self.project,'../escape')
 def test_primary_runtime_review_and_link_artifacts_tampered(self):
  for key in ['crt','review','layout','SCALARS-MAIN_exe','MAIN-SCALARS_map','runtime','helper_library','linker']+sorted(k for k in self.item['evidence']if k.startswith('native_')):
   p=self.project/self.item['evidence'][key]['path'];before=p.read_bytes();p.write_bytes(before+b'changed')
   with self.subTest(key=key),self.assertRaisesRegex(ValueError,'evidence pin'):side.validate_evidence(self.project,self.item['evidence'],PROJECT.parent/'CHESS.EXE')
   p.write_bytes(before)
 def semantic_tamper(self,key,edit,message):
  pins=copy.deepcopy(self.item['evidence']);path=self.project/pins[key]['path']
  data=json.loads(path.read_text());edit(data);before=path.read_bytes();path.write_text(json.dumps(data))
  pins[key]['sha256']=side.sha(path.read_bytes())
  try:
   with patch.object(side,'PINS',pins):
    with self.assertRaisesRegex(ValueError,message):side.validate_evidence(self.project,pins,PROJECT.parent/'CHESS.EXE')
  finally:path.write_bytes(before)
 def test_native_CRT_subject_load_profile_and_complete_read_semantics(self):
  for edit,message in [
   (lambda e:e['subject']['digest'].update(sha256='0'*64),'subject/profile'),
   (lambda e:e['analysis_profile']['parameters'].update(load_segment='0x1001'),'subject/profile'),
   (lambda e:e['parameters'].update(length=178),'subject/profile'),
   (lambda e:e['normalized_result'].update(complete=False),'complete original CRT'),
   (lambda e:e['normalized_result'].update(bytes_hex='00'+e['normalized_result']['bytes_hex'][2:]),'complete original CRT')]:
   self.semantic_tamper('crt',edit,message)
 def test_native_scalar_size_operand_and_CRT_containment_semantics(self):
  self.semantic_tamper('review',lambda r:r['native_bindings'][0].update(size=4),'scalar extent')
  self.semantic_tamper('review',lambda r:r['native_bindings'][0]['native_access_fields'][0].update(encoded_hex='c957'),'operand mismatch')
  self.semantic_tamper('review',lambda r:r['native_width_windows'][-1].update(hex='bfacb0becacba5a5a5'),'width windows')
 def test_actual_LINK_MZ_execution_and_clear_scope_semantics(self):
  self.semantic_tamper('layout',lambda r:r['authentic_LINK_trials'][0].update(execution_exit_zero=False),'proof identity')
  self.semantic_tamper('layout',lambda r:r['authentic_LINK_trials'][0].update(MZ_sites=[]),'MZ set')
  self.semantic_tamper('layout',lambda r:r['authentic_LINK_trials'][0].update(CRTzero_range=[0,65535]),'clear bounds')
 def test_complete_diagnostic_CODE_and_DATA_semantics(self):
  self.semantic_tamper('layout',lambda r:r['authentic_LINK_trials'][0]['complete_CODE'].update(hex='00'),'complete diagnostic CODE')
  self.semantic_tamper('layout',lambda r:r['authentic_LINK_trials'][0]['diagnostic_DATA'].update(hex='0000'),'complete diagnostic DATA')
 def test_wrong_original_target(self):
  p=self.project/'wrong.exe';p.write_bytes(b'MZwrong')
  with self.assertRaisesRegex(ValueError,'target pin'):side.validate_evidence(self.project,self.item['evidence'],p)
 def test_raw_checksum_length_and_eof(self):
  raw=bytearray(self.obj);raw[250]^=1
  for b in(bytes(raw),self.obj[:-1],self.obj+b'\0'):self.bad_obj(b)
 def test_not_far_and_exact_int_Move_sizes(self):
  for before,after in[(b'\x62\x02',b'\x61\x01\x02'),(b'\x62\x02',b'\x62\x04'),(b'\x62\x08',b'\x62\x06')]:
   self.bad_obj(mutate(self.obj,0xb0,lambda p:p.replace(before,after,1)))
 def test_signedness_and_Move_type_index(self):
  for before,after in[(b'\x80\x81',b'\x80\x85'),(b'\x82\x0a',b'\x82\x09')]:self.bad_obj(mutate(self.obj,0xb0,lambda p:p.replace(before,after,1)))
 def test_missing_extra_reordered_and_alias_names(self):
  for f in(lambda p:b'',lambda p:p+p[:18],lambda p:p.replace(b'temporary',b'temp_ar_y',1)):
   self.bad_obj(mutate(self.obj,0xb0,f))
 def test_loaded_or_debug_allocations_changed(self):
  rows=read_omf(self.obj).records
  for index in range(4,10):
   self.bad_obj(b''.join(record(k,p[:1]+b'\x02\0'+p[3:]if i==index else p)for i,(k,_,p)in enumerate(rows)))
 def test_EXTRA_COMMON_PUBLIC_LIDATA_LEDATA(self):
  for k,p in [(0xb0,b'\x04_more\x80\x81\x62\x02'),(0x90,b'\x01\x02\x04_more\0\0\0'),
              (0xa2,bytes.fromhex('020000020000000100')),(0xa0,bytes.fromhex('02000000'))]:
   self.bad_obj(self.obj[:-5]+record(k,p)+self.obj[-5:])
 def test_group_startup_marker_directive_and_entrypoint(self):
  for k,f in[(0x9a,lambda p:b'\x02\xff\x02'),(0x88,lambda p:b'\0\x9e'),(0x8a,lambda p:b'\x80'),(0x8c,lambda p:b'\x04_fake\x01')]:self.bad_obj(mutate(self.obj,k,f))
 def test_complete_debug_Move_members_and_fixups(self):
  rows=read_omf(self.obj).records
  # Mutate the CV type stream while maintaining checksums; matching COMMON8
  # size/index alone cannot admit changed layout/field/union data.
  changed=False;out=[]
  for k,_,p in rows:
   if k==0xa0 and p[0]==6:p=p[:-1]+bytes([p[-1]^1]);changed=True
   out.append(record(k,p))
  self.assertTrue(changed);self.bad_obj(b''.join(out))
  for before,after in[(bytes.fromhex('cc6d'),bytes.fromhex('c46d')),(bytes.fromhex('5607'),bytes.fromhex('5606'))]:
   self.bad_obj(b''.join(record(k,p.replace(before,after,1)if k==0x9c else p)for k,_,p in rows))
 def test_failure_leaves_no_new_success_object(self):
  row=copy.deepcopy(self.item);row['objects'].pop()
  with self.assertRaises(ValueError):side.build_input(row,self.project,PROJECT.parent/'CHESS.EXE',self.out)
  self.assertFalse(self.out.exists())

if __name__=='__main__':unittest.main()
