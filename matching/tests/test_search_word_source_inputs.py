"""Canonical-ready tests; fixtures remain in the explicitly named staged proof directory."""
from pathlib import Path
import copy,importlib.util,json,struct,sys,tempfile,unittest,ast
from unittest.mock import patch
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'config/msc500.json').is_file())
STAGE=ROOT/'build/search-word-common-followup';IMPL=STAGE/'implementation'
# When copied to canonical tests, require the real canonical module; staging uses its exact proposed copy.
if Path(__file__).resolve().parent.name=='tests':
 sys.path.insert(0,str(ROOT));import search_word_source_inputs as profile
 assert Path(profile.__file__).resolve()==ROOT/'search_word_source_inputs.py'
else:
 sys.path[:0]=[str(IMPL),str(ROOT)];import search_word_source_inputs as profile
 assert Path(profile.__file__).resolve()==IMPL/'search_word_source_inputs.py'
from omf import read_omf
from msc import compile_c
if Path(__file__).resolve().parent.name=='tests':
 import source_inputs as dispatch
 assert Path(dispatch.__file__).resolve()==ROOT/'source_inputs.py'
else:
 spec=importlib.util.spec_from_file_location('search_word_staged_dispatch',IMPL/'source_inputs.py');dispatch=importlib.util.module_from_spec(spec);spec.loader.exec_module(dispatch)
RAW=(STAGE/'positive.obj').read_bytes();BAD=(STAGE/'initialized_wrong.obj').read_bytes();ITEM=json.loads((STAGE/'proposed-source-input-reviewed.json').read_text());MIRROR=STAGE/'physical-mirror';TARGET=ROOT.parent/'CHESS.EXE'
def rebuild(transform):
 out=bytearray()
 for index,(k,_,payload)in enumerate(read_omf(RAW).records):
  k,payload=transform(index,k,bytearray(payload));b=bytes([k])+struct.pack('<H',len(payload)+1)+bytes(payload);out+=b+bytes([(-sum(b))&255])
 return bytes(out)
def change(kind,fun,ordinal=0):
 count=[0]
 def f(i,k,p):
  if k==kind:
   if count[0]==ordinal:p=bytearray(fun(p))
   count[0]+=1
  return k,p
 return rebuild(f)
class SearchWords(unittest.TestCase):
 def reject(self,raw):
  with self.assertRaises((ValueError,AssertionError)):profile.validate_object(raw)
 def test_positive_whole_object(self):
  ds=profile.validate_object(RAW);self.assertEqual([d['symbol']for d in ds],profile.NAMES);self.assertTrue(all(d['size']==2 and d['datatype']==0x62 and d['type_index']==0x81 for d in ds))
 def test_actual_initialized_negative(self):self.reject(BAD)
 def test_size4(self):self.reject(change(0xb0,lambda p:p.replace(b'\x80\x81\x62\x02',b'\x80\x81\x62\x04',1)))
 def test_unsigned_type(self):self.reject(change(0xb0,lambda p:p.replace(b'\x80\x81\x62\x02',b'\x80\x85\x62\x02',1)))
 def test_far_common(self):self.reject(change(0xb0,lambda p:p.replace(b'\x80\x81\x62\x02',b'\x80\x81\x61\x02',1)))
 def test_name_identity(self):self.reject(change(0xb0,lambda p:p.replace(b'_first_score',b'_First_score',1)))
 def test_duplicate_definition(self):self.reject(change(0xb0,lambda p:p+p[:1+p[0]+4]))
 def test_missing_common(self):self.reject(change(0xb0,lambda p:p[1+p[0]+4:]))
 def test_extra_DATA_allocation(self):self.reject(change(0x98,lambda p:p[:1]+b'\x02\0'+p[3:],ordinal=1))
 def test_debug_extent(self):self.reject(change(0x98,lambda p:p[:1]+b'\x7e\0'+p[3:],ordinal=4))
 def test_debug_payload_type(self):self.reject(change(0xa0,lambda p:p.replace(b'\x81\0',b'\x85\0',1)))
 def test_loaded_LEDATAnotdebug(self):self.reject(change(0xa0,lambda p:b'\x02'+p[1:]))
 def test_fixup_width(self):self.reject(change(0x9c,lambda p:b'\xc4'+p[1:],ordinal=1))
 def test_fixup_frame(self):self.reject(change(0x9c,lambda p:p[:2]+b'\x46'+p[3:],ordinal=1))
 def test_fixup_target(self):self.reject(change(0x9c,lambda p:p[:3]+b'\x06'+p[4:],ordinal=1))
 def test_foreign_linker_directive(self):self.reject(change(0x88,lambda p:b'foreign'))
 def test_DGROUP(self):self.reject(change(0x9a,lambda p:p[:-1]+b'\x01'))
 def test_MODEND_entry(self):self.reject(change(0x8a,lambda p:b'\x40'))
 def test_whole_CV_identity(self):self.reject(change(0xa0,lambda p:p.replace(b'first_score',b'First_score',1)))
 def test_object_checksum(self):
  b=bytearray(RAW);b[10]^=1;self.reject(b)
 def test_truncated_object(self):self.reject(RAW[:-1])
 def test_exact_item(self):profile.validate_item(ITEM)
 def test_metadata_identity_changes(self):
  for key,value in [('id','foreign'),('backend','msc500-near-common-setup-word-v1'),('source','../escape.c'),('source_sha256','0'*64),('compiler','msc510'),('flags',['/AS','/Zi']),('toolchain_manifest_sha256','0'*64),('evidence',{})]:
   with self.subTest(key=key):
    item=copy.deepcopy(ITEM);item[key]=value
    with self.assertRaises(ValueError):profile.validate_item(item)
 def test_object_selection_size(self):
  item=copy.deepcopy(ITEM);item['objects'][0]['size']=4
  with self.assertRaises(ValueError):profile.validate_item(item)
 def test_object_selection_name(self):
  item=copy.deepcopy(ITEM);item['objects'][0]['symbol']='_foreign'
  with self.assertRaises(ValueError):profile.validate_item(item)
 def test_unknown_metadata(self):
  with self.assertRaises(ValueError):profile.validate_item(dict(ITEM,placement=[0x5cc2,0x53f6]))
 def test_evidence_mutation(self):
  pins=copy.deepcopy(profile.PINS);pins['native']['sha256']='0'*64
  with self.assertRaises(ValueError):profile.validate_evidence(MIRROR,pins,TARGET)
 def test_target_identity(self):
  with tempfile.TemporaryDirectory()as d:
   p=Path(d)/'fake.exe';p.write_bytes(b'MZ')
   with self.assertRaises(ValueError):profile.validate_evidence(MIRROR,profile.PINS,p)
 def test_changed_source_rejected_before_generation(self):
  with tempfile.TemporaryDirectory()as t:
   project=Path(t);p=project/profile.SOURCE;p.parent.mkdir(parents=True);p.write_bytes((STAGE/'search_words.c').read_bytes()+b'\n')
   with self.assertRaises(ValueError):profile.build_input(ITEM,project,TARGET,project/'out',compiler_fn=lambda *a,**k:(_ for _ in ()).throw(AssertionError('must not compile')))
 def test_fresh_compiler_metadata_rejects_before_native_access(self):
  from msc import CompileResult
  import dataclasses
  meta=json.loads((STAGE/'positive-generation.json').read_text())['compiler'];c=CompileResult(object_bytes=RAW,**meta)
  for key,value in [('tool_hashes',{}),('toolchain_manifest_sha256','0'*64),('source_sha256','0'*64),('source_name','FOREIGN.C'),('compiler','msc510'),('flags',['/AS'])]:
   with self.subTest(key=key):
    bad=dataclasses.replace(c,**{key:value})
    with patch.object(profile,'validate_evidence',side_effect=AssertionError('must fail before target access')):
     with self.assertRaises(ValueError):profile.build_input(ITEM,MIRROR,TARGET,STAGE/'unexpected',compiler_fn=lambda *a,**k:bad)
 def test_actual_native_evidence_constraints(self):
  rows=profile.validate_evidence(MIRROR,profile.PINS,TARGET);self.assertEqual(len(rows),6);self.assertTrue(all(not r['resolved']and not r['native_final_MAP_or_BSS_order_proven']for r in rows))
 def test_path_escape(self):
  with self.assertRaises(ValueError):profile.local(MIRROR,'../../escape')
 def test_duplicate_selected_provider_rejected_before_generation(self):
  with patch.object(dispatch,'compile_c',side_effect=AssertionError('unexpected compile')):
   with self.assertRaises(ValueError):dispatch.build_source_inputs(MIRROR,TARGET,STAGE/'unexpected',defined_symbols=profile.NAMES[:1])
 def test_duplicate_row_rejected(self):
  cfg={'schema_version':1,'source_allocations':[ITEM,ITEM]}
  # First profile built through an explicit inert result only to isolate registry duplicate logic, no positive build claim.
  with tempfile.TemporaryDirectory()as t:
   p=Path(t)/'config.json';p.write_text(json.dumps(cfg))
   with patch.object(profile,'build_input',return_value={'id':ITEM['id']}):
    with self.assertRaises(ValueError):dispatch.build_source_inputs(MIRROR,TARGET,STAGE/'unexpected',config_path=p)
 def test_absent_config_backwards_compatible(self):
  r=dispatch.build_source_inputs(MIRROR,TARGET,STAGE/'unexpected',config_path=STAGE/'definitely-absent.json');self.assertEqual(r['objects'],[]);self.assertEqual(r['matching_credit'],0)
 def test_dispatcher_patch_is_only_new_branch(self):
  a=ast.parse((IMPL/'source_inputs.base.py').read_text());b=ast.parse((IMPL/'source_inputs.py').read_text());fn=next(n for n in b.body if isinstance(n,ast.FunctionDef)and n.name=='build_source_inputs');loop=next(n for n in fn.body if isinstance(n,ast.For));new=loop.body[1];self.assertIsInstance(new,ast.If);self.assertIn(profile.BACKEND,ast.unparse(new.test));del loop.body[1];self.assertEqual(ast.dump(a),ast.dump(b))
 def test_real_fresh_dispatcher_generation_target_guard(self):
  tool=ROOT/'toolchains/msc500';cfg=json.loads((ROOT/'config/msc500.json').read_text());src=MIRROR/profile.SOURCE;allowed={src.resolve(),(ROOT/'config/msc500.json').resolve(),(tool/'manifest.json').resolve(),*((tool/x['name']).resolve()for x in cfg['files'])};rb,rt=Path.read_bytes,Path.read_text;calls=[];reads=[]
  def good(p):return p.resolve()in allowed or(p.parent.name.startswith('battlechess-msc-')and p.name in['COMPILE.LOG','UNIT.OBJ'])
  def gb(p):
   self.assertTrue(good(p),'unexpected generation input '+str(p));reads.append(str(p));return rb(p)
  def gt(p,*a,**kw):
   self.assertTrue(good(p),'unexpected generation input '+str(p));reads.append(str(p));return rt(p,*a,**kw)
  def guarded(*a,**kw):
   with patch.object(Path,'read_bytes',gb),patch.object(Path,'read_text',gt):
    for p in [TARGET,ROOT/'build/exepack/TRIM5_UNPACK.EXE',MIRROR/profile.PINS['native']['path']]:
     with self.assertRaises(AssertionError):p.read_bytes()
    c=compile_c(*a,**kw)
   calls.append(c);return c
  with tempfile.TemporaryDirectory()as t,patch.object(dispatch,'compile_c',guarded):result=dispatch.build_source_inputs(MIRROR,TARGET,Path(t))
  self.assertEqual(len(calls),1);self.assertEqual(len(result['objects']),1);o=result['objects'][0];self.assertEqual(o['object_sha256'],profile.OBJECT_SHA);self.assertEqual(o['allocation_bytes'],12);self.assertEqual(o['initialized_bytes'],0);self.assertEqual(o['matching_credit'],0);self.assertFalse(o['placement_proven']);self.assertFalse(o['diagnostic_LINK_or_CRT_execution_claim']);self.assertEqual(o['definitions'],profile.validate_object(RAW))
  # Store complete actual fresh result separately from the fixed reviewed fixtures.
  if Path(__file__).resolve().parent.name!='tests':
   (STAGE/'fresh-dispatcher-production.json').write_text(json.dumps({'result':result,'generation_reads':reads,'actual_compiler_invocations':1,'guard_original_carrier_native_primary':True},indent=2)+'\n')
if __name__=='__main__':unittest.main(verbosity=2)
