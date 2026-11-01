from pathlib import Path
import sys,json,hashlib,dataclasses,copy,tempfile,shutil,unittest,importlib.util
from unittest.mock import patch
TEST=Path(__file__).resolve();M=TEST.parents[1];FIXTURE=M/'build/board-common-provider-stage'
TEMP=tempfile.TemporaryDirectory(prefix='board-common-canonical-');D=Path(TEMP.name);P=D/'physical-mirror';I=M/'src/link';sys.path.insert(0,str(M))
import board_source_inputs as mod
import source_inputs as route
assert Path(mod.__file__).resolve()==M/'board_source_inputs.py'
assert Path(route.__file__).resolve()==M/'source_inputs.py'
for row in mod.PINS.values():
 q=P/row['path'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((M/row['path']).read_bytes())
for path in [mod.SOURCE,mod.COHERENT_CONSUMER]:
 q=P/path;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((M/path).read_bytes())
from msc import compile_c
from omf import read_omf
J=lambda p:json.loads(p.read_text());W=lambda p,v:p.write_text(json.dumps(v,indent=2)+'\n')
ITEM=J(FIXTURE/'proposed-config-row.json');generated={};generation=[];rb,rt=Path.read_bytes,Path.read_text
assert next(r for r in J(M/'config/source-inputs.json')['source_allocations']if r['id']==ITEM['id'])==ITEM
W(D/'source-inputs.json',{'schema_version':1,'source_allocations':[ITEM]})
allowed={(M/'config/msc500.json').resolve(),(M/'toolchains/msc500/manifest.json').resolve()}|{(M/'toolchains/msc500'/r['name']).resolve()for r in J(M/'config/msc500.json')['files']}
def guarded(source,flags,**kw):
 allow=allowed|{Path(source).resolve()};reads=[];blocked=[]
 def good(p):return p.resolve()in allow or(p.parent.name.startswith('battlechess-msc-')and p.name in ['COMPILE.LOG','UNIT.OBJ'])
 def b(p):
  if not good(p):blocked.append(str(p));raise AssertionError('Forbidden generation read '+str(p))
  reads.append(str(p));return rb(p)
 def t(p,*a,**k):
  if not good(p):blocked.append(str(p));raise AssertionError('Forbidden generation read '+str(p))
  reads.append(str(p));return rt(p,*a,**k)
 with patch.object(Path,'read_bytes',b),patch.object(Path,'read_text',t):
  for target in [M.parent/'CHESS.EXE',M/'build/exepack/TRIM5_UNPACK.EXE',P/ITEM['evidence']['native_proof']['path']]:
   try:target.read_bytes()
   except AssertionError:pass
   else:raise AssertionError('Target accessible')
  c=compile_c(source,flags,**kw)
 assert len(blocked)==3
 meta=dataclasses.asdict(c);meta.pop('object_bytes');generation.append({'source':str(source),'actual_generation_reads':reads,'blocked_reads':blocked,'compiler':meta,'object_sha256':mod.sha(c.object_bytes)});return c
class BoardMinimumCommonTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  s=(I/'board_storage.c').read_text();variants={'good':s,'too_short119':s.replace('[120]','[119]'),'unreviewed_capacity128':s.replace('[120]','[128]'),'wrong_kind_signedness':s.replace('unsigned char','signed char'),'wrong_index_signedness':s.replace('int index','unsigned int index'),'initializer':s.replace('Cell board[120];\n','Cell board[120] = {{0,0,0}};\n',1).replace('extern Cell board[120] = {{0,0,0}};','extern Cell board[120];').replace('\nCell board[120];','\nCell board[120] = {{0,0,0}};'),'extra_COMMON':s+'int other;\n','extra_CODE':s+'int other(void){return 1;}\n'}
  assert '= {{0,0,0}}'in variants['initializer']
  for n,text in variants.items():
   p=D/(n+'.c');p.write_text(text);c=guarded(p,mod.FLAGS,compiler='msc500');generated[n]=c;(D/(n+'.obj')).write_bytes(c.object_bytes)
 def test_complete_natural_COMMON480(self):self.assertEqual(mod.validate_object(generated['good'].object_bytes),[{'symbol':'_board','size':480,'datatype':98,'type_index':519}])
 def test_ordinary_source_inputs_fresh_generation(self):
  with patch.object(route,'compile_c',guarded):r=route.build_source_inputs(P,M.parent/'CHESS.EXE',D/'ordinary-result',D/'source-inputs.json')
  self.assertEqual(r['matching_credit'],0);self.assertFalse(r['placement_proven']);row=r['objects'][0];self.assertEqual((row['allocation_bytes'],row['initialized_bytes'],row['matching_credit'],row['authored_C_function_credit']),(480,0,0,0));self.assertFalse(row['historical_capacity_proven']);self.assertFalse(row['original_map_constraints'][0]['resolved']);W(D/'ordinary-result.json',r);W(D/'ordinary-report-inputs.json',route.report_inputs(r))
 def test_reused_native_and_actual_LINK_evidence(self):self.assertEqual(mod.validate_evidence(P,mod.PINS,M.parent/'CHESS.EXE')[0]['minimum_observed_bytes'],480)
 def test_requires_actual_coherent_consumer(self):
  with tempfile.TemporaryDirectory()as t:
   q=Path(t)/'p';shutil.copytree(P,q);(q/mod.COHERENT_CONSUMER).write_bytes((M/'build/board-storage-identity-audit/original-board-turn.c').read_bytes())
   with self.assertRaisesRegex(ValueError,'coherent consumer Cell'):mod.validate_evidence(q,mod.PINS,M.parent/'CHESS.EXE')
 def test_source_pin_before_generation(self):
  with tempfile.TemporaryDirectory()as t:
   q=Path(t);p=q/mod.SOURCE;p.parent.mkdir(parents=True);p.write_text('char board[480];')
   with self.assertRaisesRegex(ValueError,'source pin'):mod.build_input(ITEM,q,M.parent/'CHESS.EXE',q/'out',compiler_fn=lambda *a,**k:self.fail('unexpected generation'))
 def test_bad_compiler_provenance(self):
  c=dataclasses.replace(generated['good'],compiler='msc510')
  with self.assertRaisesRegex(ValueError,'compiler provenance'):mod.build_input(ITEM,P,M.parent/'CHESS.EXE',D/'badcompiler',compiler_fn=lambda *a,**k:c)
 def test_generation_precedes_native_read(self):
  with patch.object(mod,'validate_evidence',side_effect=AssertionError('unexpected evidence read')),self.assertRaisesRegex(RuntimeError,'compiler stopped'):mod.build_input(ITEM,P,M.parent/'CHESS.EXE',D/'badorder',compiler_fn=lambda *a,**k:(_ for _ in()).throw(RuntimeError('compiler stopped')))
 def test_tampered_evidence_path(self):
  pins=copy.deepcopy(mod.PINS);pins['native_reset']['path']='other.json'
  with self.assertRaisesRegex(ValueError,'evidence identity'):mod.validate_evidence(P,pins,M.parent/'CHESS.EXE')
 def test_actual_native_bound_bytes_tampered(self):
  with tempfile.TemporaryDirectory()as t:
   q=Path(t)/'p';shutil.copytree(P,q);p=q/mod.PINS['native_proof']['path'];v=J(p);v['native_last_index']=118;W(p,v)
   with self.assertRaisesRegex(ValueError,'evidence pin'):mod.validate_evidence(q,mod.PINS,M.parent/'CHESS.EXE')
 def test_actual_retained_LINK_EXE_tampered(self):
  with tempfile.TemporaryDirectory()as t:
   q=Path(t)/'p';shutil.copytree(P,q);p=q/mod.PINS['BOARD-CLEAR-FILL-MAIN_UNIT.EXE']['path'];raw=bytearray(p.read_bytes());raw[-1]^=1;p.write_bytes(raw)
   with self.assertRaisesRegex(ValueError,'evidence pin'):mod.validate_evidence(q,mod.PINS,M.parent/'CHESS.EXE')
 def test_existing_provider_duplicate(self):
  with self.assertRaisesRegex(ValueError,'already matched definition'):route.build_source_inputs(P,M.parent/'CHESS.EXE',D/'baddup',D/'source-inputs.json',defined_symbols=['_board'])
 def test_duplicate_config_row(self):
  with tempfile.TemporaryDirectory()as t:
   q=Path(t);cfg=q/'c.json';W(cfg,{'schema_version':1,'source_allocations':[ITEM,ITEM]})
   with patch.object(route,'compile_c',lambda *a,**k:generated['good']),self.assertRaisesRegex(ValueError,'duplicate source allocation'):route.build_source_inputs(P,M.parent/'CHESS.EXE',q/'out',cfg)
 def test_checksum(self):
  raw=bytearray(generated['good'].object_bytes);raw[15]^=1
  with self.assertRaises(ValueError):mod.validate_object(bytes(raw))
 def test_trailing_object_bytes(self):
  with self.assertRaises(ValueError):mod.validate_object(generated['good'].object_bytes+b'\0')
 def test_path_escape(self):
  with self.assertRaisesRegex(ValueError,'path escape'):mod.local(P,'../../CHESS.EXE')
 def test_unknown_historical_capacity_claim(self):
  row=dict(ITEM,historical_capacity=120)
  with self.assertRaisesRegex(ValueError,'unknown fields'):mod.validate_item(row)
 def test_unknown_MAP_address(self):
  row=dict(ITEM,address='0xa8ba')
  with self.assertRaisesRegex(ValueError,'unknown fields'):mod.validate_item(row)
for name in ['too_short119','unreviewed_capacity128','wrong_kind_signedness','wrong_index_signedness','initializer','extra_COMMON','extra_CODE']:
 def test(self,name=name):
  with self.assertRaises(ValueError):mod.validate_object(generated[name].object_bytes)
 setattr(BoardMinimumCommonTests,'test_compiler_negative_'+name,test)
for key,bad in [('id','other'),('backend','other'),('compiler','msc510'),('flags',['/AS']),('source','other.c'),('source_sha256','0'*64),('toolchain_manifest_sha256','0'*64),('objects',[{'symbol':'_board','size':512,'storage':'near-common'}]),('evidence',{})]:
 def test(self,key=key,bad=bad):
  row=copy.deepcopy(ITEM);row[key]=bad
  with self.assertRaises(ValueError):mod.validate_item(row)
 setattr(BoardMinimumCommonTests,'test_profile_'+key,test)
if __name__=='__main__':
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(BoardMinimumCommonTests);ids=[t.id()for t in suite];r=unittest.TextTestRunner(verbosity=2).run(suite);W(D/'test-result.json',{'tests':r.testsRun,'ids':ids,'errors':len(r.errors),'failures':len(r.failures),'skipped':len(r.skipped),'passed':r.wasSuccessful(),'guarded_compiles':generation,'old_harness_executions_repeated':0,'new_allocated_matching_credit':0,'canonical_changes':False});sys.exit(not r.wasSuccessful())
