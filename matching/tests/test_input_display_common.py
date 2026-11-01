from pathlib import Path
import sys,json,hashlib,dataclasses,copy,unittest,tempfile,importlib.util
from unittest.mock import patch
TEST=Path(__file__).resolve();M=TEST.parent.parent;FIXTURE=M/'build/input-display-common-stage'
temporary=tempfile.TemporaryDirectory(prefix='input-display-common-canonical-');D=Path(temporary.name);P=M;I=M/'src/link'
sys.path.insert(0,str(M))
import input_display_source_inputs as mod
import source_inputs as route
assert Path(mod.__file__).resolve()==M/'input_display_source_inputs.py'
assert Path(route.__file__).resolve()==M/'source_inputs.py'
from msc import compile_c
from omf import read_omf
J=lambda p:json.loads(p.read_text());W=lambda p,v:p.write_text(json.dumps(v,indent=2)+'\n')
ITEM=J(FIXTURE/'proposed-config-row.json');generation=[];generated={}
PRODUCTION=J(M/'config/source-inputs.json');assert next(r for r in PRODUCTION['source_allocations']if r['id']==ITEM['id'])==ITEM
W(D/'source-inputs.json',{'schema_version':1,'source_allocations':[ITEM]})
rb,rt=Path.read_bytes,Path.read_text
allowed={(M/'config/msc500.json').resolve(),(M/'toolchains/msc500/manifest.json').resolve()}
allowed|={(M/'toolchains/msc500'/f['name']).resolve()for f in J(M/'config/msc500.json')['files']}
def guarded(source,flags,**kw):
 allow=allowed|{Path(source).resolve()};reads=[];blocked=[]
 def good(p):return p.resolve()in allow or(p.parent.name.startswith('battlechess-msc-')and p.name in ['COMPILE.LOG','UNIT.OBJ'])
 def b(p):
  if not good(p):blocked.append(str(p));raise AssertionError('Generation read forbidden '+str(p))
  reads.append(str(p));return rb(p)
 def t(p,*a,**k):
  if not good(p):blocked.append(str(p));raise AssertionError('Generation read forbidden '+str(p))
  reads.append(str(p));return rt(p,*a,**k)
 with patch.object(Path,'read_bytes',b),patch.object(Path,'read_text',t):
  for x in [M.parent/'CHESS.EXE',M/'build/exepack/TRIM5_UNPACK.EXE',P/ITEM['evidence']['layout']['path']]:
   try:x.read_bytes()
   except AssertionError:pass
   else:raise AssertionError('target accessible')
  c=compile_c(source,flags,**kw)
 assert len(blocked)==3
 generation.append({'source':str(source),'reads':reads,'blocked':blocked,'source_sha256':c.source_sha256,'object_sha256':mod.sha(c.object_bytes),'compiler':{k:v for k,v in dataclasses.asdict(c).items()if k!='object_bytes'}})
 return c
class ClosedInputDisplayTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  variants={'good':(I/'input_display_state.c').read_text(),'wrong_width':'char cursor_colour_9850;\nint ready_9856;\n','initializer':'int cursor_colour_9850=0;\nint ready_9856;\n','extra_common':'int cursor_colour_9850;\nint ready_9856;\nint extra;\n','extra_DATA':'int cursor_colour_9850;\nint ready_9856;\nint extra=1;\n','extra_CODE':'int cursor_colour_9850;\nint ready_9856;\nint extra(void){return 1;}\n'}
  for n,s in variants.items():
   f=D/(n+'.c');f.write_text(s);c=guarded(f,mod.FLAGS,compiler='msc500');generated[n]=c;(D/(n+'.obj')).write_bytes(c.object_bytes)
 def test_complete_good_object(self):self.assertEqual([r['size']for r in mod.validate_object(generated['good'].object_bytes)],[2,2])
 def test_wrong_width(self):
  with self.assertRaises(ValueError):mod.validate_object(generated['wrong_width'].object_bytes)
 def test_initializer_not_COMMON(self):
  with self.assertRaises(ValueError):mod.validate_object(generated['initializer'].object_bytes)
 def test_extra_COMMON(self):
  with self.assertRaises(ValueError):mod.validate_object(generated['extra_common'].object_bytes)
 def test_extra_DATA(self):
  with self.assertRaises(ValueError):mod.validate_object(generated['extra_DATA'].object_bytes)
 def test_extra_CODE(self):
  with self.assertRaises(ValueError):mod.validate_object(generated['extra_CODE'].object_bytes)
 def test_checksum(self):
  b=bytearray(generated['good'].object_bytes);b[20]^=1
  with self.assertRaises(ValueError):mod.validate_object(bytes(b))
 def test_trailing_bytes(self):
  with self.assertRaises(ValueError):mod.validate_object(generated['good'].object_bytes+b'\0')
 def test_ordinary_route_fresh_guarded(self):
  with patch.object(route,'compile_c',guarded):r=route.build_source_inputs(P,M.parent/'CHESS.EXE',D/'ordinary-source-inputs',D/'source-inputs.json')
  self.assertEqual((r['matching_credit'],r['placement_proven']),(0,False));self.assertEqual(len(r['objects']),1);row=r['objects'][0];self.assertEqual((row['allocation_bytes'],row['initialized_bytes'],row['authored_C_function_credit']),(4,0,0));self.assertEqual([x['size']for x in row['definitions']],[2,2]);self.assertTrue(all(not x['resolved']for x in row['original_map_constraints']));W(D/'ordinary-result.json',r);W(D/'ordinary-report-inputs.json',route.report_inputs(r))
 def test_native_evidence(self):self.assertEqual([x['dgroup_offset']for x in mod.validate_evidence(P,mod.PINS,M.parent/'CHESS.EXE')],['0x9850','0x9856'])
 def test_native_address_profile(self):
  with patch.object(mod,'OFFSETS',[0x9851,0x9856]),self.assertRaisesRegex(ValueError,'fixed native scalar addresses'):mod.validate_evidence(P,mod.PINS,M.parent/'CHESS.EXE')
 def test_wrong_evidence_pin(self):
  p=copy.deepcopy(mod.PINS);p['ready_read']['sha256']='0'*64
  with self.assertRaisesRegex(ValueError,'evidence identity'):mod.validate_evidence(P,p,M.parent/'CHESS.EXE')
 def test_actual_evidence_bytes_tampered(self):
  with tempfile.TemporaryDirectory()as t:
   q=Path(t)
   for row in mod.PINS.values():x=q/row['path'];x.parent.mkdir(parents=True,exist_ok=True);x.write_bytes((P/row['path']).read_bytes())
   (q/mod.PINS['ready_read']['path']).write_text('{}')
   with self.assertRaisesRegex(ValueError,'evidence pin'):mod.validate_evidence(q,mod.PINS,M.parent/'CHESS.EXE')
 def test_source_mutation_before_generation(self):
  with tempfile.TemporaryDirectory()as t:
   q=Path(t);p=q/mod.SOURCE;p.parent.mkdir(parents=True);p.write_text('int ready_9856;')
   with self.assertRaisesRegex(ValueError,'source pin'):mod.build_input(ITEM,q,M.parent/'CHESS.EXE',q/'out',compiler_fn=lambda *a,**k:self.fail('unexpected compiler'))
 def test_duplicate_known_provider(self):
  with self.assertRaisesRegex(ValueError,'already matched definition'):route.build_source_inputs(P,M.parent/'CHESS.EXE',D/'bad-dup',D/'source-inputs.json',defined_symbols=['_ready_9856'])
 def test_duplicate_row(self):
  with tempfile.TemporaryDirectory()as t:
   cfg=Path(t)/'c.json';W(cfg,{'schema_version':1,'source_allocations':[ITEM,ITEM]})
   with patch.object(route,'compile_c',lambda *a,**k:generated['good']),self.assertRaisesRegex(ValueError,'duplicate source allocation'):route.build_source_inputs(P,M.parent/'CHESS.EXE',Path(t)/'out',cfg)
 def test_path_escape(self):
  with self.assertRaisesRegex(ValueError,'path escape'):mod.local(P,'../../CHESS.EXE')
for key,bad in [('id','other'),('backend','other'),('source','other.c'),('source_sha256','0'*64),('compiler','msc510'),('flags',['/AS']),('toolchain_manifest_sha256','0'*64),('objects',[]),('evidence',{})]:
 def test(self,key=key,bad=bad):
  row=copy.deepcopy(ITEM);row[key]=bad
  with self.assertRaises(ValueError):mod.validate_item(row)
 setattr(ClosedInputDisplayTests,'test_item_'+key,test)
def unknown(self):
 row=dict(ITEM,DS_offset='0x9850')
 with self.assertRaisesRegex(ValueError,'fields'):mod.validate_item(row)
ClosedInputDisplayTests.test_unknown_native_address_field=unknown
def change_record(raw,kind,transform):
 out=bytearray();done=False
 for k,offset,payload in read_omf(raw).records:
  if k==kind and not done:payload=transform(payload);done=True
  head=bytes([k])+(len(payload)+1).to_bytes(2,'little')+payload
  out.extend(head+bytes([(-sum(head))&255]))
 assert done
 return bytes(out)
def wrong_comdef_type(self):
 raw=change_record(generated['good'].object_bytes,0xb0,lambda p:p.replace(bytes.fromhex('80816202'),bytes.fromhex('80856202'),1))
 self.assertNotEqual(raw,generated['good'].object_bytes)
 with self.assertRaisesRegex(ValueError,'near signed-int'):mod.validate_object(raw)
def changed_debug_bytes(self):
 def mutate(p):
  b=bytearray(p);b[-1]^=1;return bytes(b)
 raw=change_record(generated['good'].object_bytes,0xa0,mutate)
 with self.assertRaisesRegex(ValueError,'whole genuine OMF'):mod.validate_object(raw)
def provenance_wrong_compiler(self):
 bad=dataclasses.replace(generated['good'],compiler='msc510')
 with self.assertRaisesRegex(ValueError,'fresh compiler provenance'):mod.build_input(ITEM,P,M.parent/'CHESS.EXE',D/'bad-meta',compiler_fn=lambda *a,**k:bad)
def evidence_read_must_follow_generation(self):
 with patch.object(mod,'validate_evidence',side_effect=AssertionError('should not reach evidence')),self.assertRaisesRegex(RuntimeError,'compiler stopped'):
  mod.build_input(ITEM,P,M.parent/'CHESS.EXE',D/'bad-order',compiler_fn=lambda *a,**k:(_ for _ in()).throw(RuntimeError('compiler stopped')))
ClosedInputDisplayTests.test_rechecks_signed_COMDEF_type=wrong_comdef_type
ClosedInputDisplayTests.test_checksum_valid_debug_mutation=changed_debug_bytes
ClosedInputDisplayTests.test_wrong_compiler_provenance=provenance_wrong_compiler
ClosedInputDisplayTests.test_source_generation_precedes_native_reads=evidence_read_must_follow_generation
if __name__=='__main__':
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(ClosedInputDisplayTests);ids=[x.id()for x in suite];result=unittest.TextTestRunner(verbosity=2).run(suite);W(D/'test-result.json',{'tests':result.testsRun,'ids':ids,'errors':len(result.errors),'failures':len(result.failures),'skipped':len(result.skipped),'passed':result.wasSuccessful(),'guarded_compiles':generation,'canonical_changes':False,'current_credit':0});sys.exit(not result.wasSuccessful())
