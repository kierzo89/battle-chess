from pathlib import Path
import sys,json,copy,unittest,hashlib,importlib.util,dataclasses,tempfile
from unittest.mock import patch
M=Path(__file__).resolve().parents[1];D=M/'build/mode8176-common-followup';sys.path.insert(0,str(M))
import asset_mode_source_inputs as profile
assert Path(profile.__file__).resolve()==(M/'asset_mode_source_inputs.py').resolve(), 'canonical module path required'
sp=importlib.util.spec_from_file_location('canonical_mode_dispatcher',M/'source_inputs.py');dispatcher=importlib.util.module_from_spec(sp);sp.loader.exec_module(dispatcher)
from msc import compile_c
from omf import read_omf
OUT=Path(tempfile.mkdtemp(prefix='mode8176-profile-tests-'))
J=lambda p:json.loads(p.read_text());item=J(D/'canonical-ready/proposed-source-input.json');raw=(D/'positive.obj').read_bytes()
def rewrite(data,which,fn):
 out=bytearray();hit=False
 for k,at,p in read_omf(data).records:
  if not hit and k==which and (which!=0x9c or p[:1]==b'\xcc'):p=fn(bytearray(p));hit=True
  rec=bytes([k])+(len(p)+1).to_bytes(2,'little')+bytes(p);out+=rec+bytes([(-sum(rec))&255])
 assert hit;return bytes(out)
class Tests(unittest.TestCase):
 def test_positive_complete_object(self):
  self.assertEqual(profile.validate_object(raw),[{'symbol':'_mode_8176','type_index':129,'datatype':98,'size':2}])
 def test_native_evidence(self):
  c=profile.validate_evidence(M,item['evidence'],M.parent/'CHESS.EXE');self.assertEqual(c[0]['dgroup_offset'],'0x8176');self.assertFalse(c[0]['resolved'])
 def test_fresh_normal_dispatcher_guarded(self):
  reads=[];blocked=[];real=compile_c
  def guarded(source,flags,**kwargs):
   rb,rt=Path.read_bytes,Path.read_text;allow={source.resolve(),(M/'config/msc500.json').resolve(),(M/'toolchains/msc500/manifest.json').resolve()}|{(M/'toolchains/msc500'/x['name']).resolve()for x in J(M/'config/msc500.json')['files']}
   def good(p):return p.resolve()in allow or(p.parent.name.startswith('battlechess-msc-')and p.name in['COMPILE.LOG','UNIT.OBJ'])
   def b(p):
    if not good(p):blocked.append(str(p));raise AssertionError('forbidden generation read')
    reads.append(str(p));return rb(p)
   def t(p,*a,**k):
    if not good(p):blocked.append(str(p));raise AssertionError('forbidden generation read')
    reads.append(str(p));return rt(p,*a,**k)
   with patch.object(Path,'read_bytes',b),patch.object(Path,'read_text',t):
    for p in[M.parent/'CHESS.EXE',M/'build/exepack/TRIM5_UNPACK.EXE',M/'evidence/rea_ui_92ab.json']:
     with self.assertRaises(AssertionError):p.read_bytes()
    return real(source,flags,**kwargs)
  cfg=OUT/'test-new-selection.json';cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[item]}))
  with patch.object(dispatcher,'compile_c',guarded):result=dispatcher.build_source_inputs(M,M.parent/'CHESS.EXE',OUT/'normal-output',cfg)
  self.assertEqual(len(result['objects']),1);o=result['objects'][0];self.assertEqual(o['object_sha256'],profile.OBJECT_SHA);self.assertEqual((o['allocation_bytes'],o['initialized_bytes'],o['matching_credit']),(2,0,0));self.assertFalse(result['placement_proven']);self.assertEqual(len(blocked),3)
  (OUT/'normal-production.json').write_text(json.dumps({'result':result,'guarded_generation_reads':reads,'blocked_reads':blocked},indent=2)+'\n')
 def test_byte_control_rejected(self):
  with self.assertRaises(ValueError):profile.validate_object((D/'byte.obj').read_bytes())
 def test_unsigned_control_rejected(self):
  with self.assertRaises(ValueError):profile.validate_object((D/'unsigned.obj').read_bytes())
 def test_initialized_control_rejected(self):
  with self.assertRaises(ValueError):profile.validate_object((D/'initialized.obj').read_bytes())
 def test_dual_alias_control_rejected(self):
  with self.assertRaises(ValueError):profile.validate_object((D/'extra_alias.obj').read_bytes())
 def test_extra_loaded_control_rejected(self):
  with self.assertRaises(ValueError):profile.validate_object((D/'extra_loaded.obj').read_bytes())
 def test_empty_config_backward_compatibility(self):
  p=OUT/'test-empty.json';p.write_text(json.dumps({'schema_version':1,'source_allocations':[]}));self.assertEqual(dispatcher.build_source_inputs(M,M.parent/'CHESS.EXE',OUT/'unused',p)['objects'],[])
 def test_absent_config_backward_compatibility(self):
  self.assertEqual(dispatcher.build_source_inputs(M,M.parent/'CHESS.EXE',OUT/'unused',OUT/'missing-config.json')['objects'],[])
 def test_existing_defined_symbol_rejected_before_compile(self):
  p=OUT/'test-new-selection.json';p.write_text(json.dumps({'schema_version':1,'source_allocations':[item]}))
  with patch.object(dispatcher,'compile_c')as compile:
   with self.assertRaises(ValueError):dispatcher.build_source_inputs(M,M.parent/'CHESS.EXE',OUT/'unused',p,defined_symbols=['_mode_8176'])
   compile.assert_not_called()
 def test_actor_definition_forbids_dual_native_allocation(self):
  p=OUT/'test-new-selection.json';p.write_text(json.dumps({'schema_version':1,'source_allocations':[item]}))
  with patch.object(dispatcher,'compile_c')as compile:
   with self.assertRaises(ValueError):dispatcher.build_source_inputs(M,M.parent/'CHESS.EXE',OUT/'unused',p,defined_symbols=['_actors_ready'])
   compile.assert_not_called()
 def test_old_dispatcher_unchanged_outside_additive_branch(self):
  base=(D/'implementation/source_inputs.base.py').read_text();new=(D/'implementation/source_inputs.py').read_text();begin=new.index("        if item['backend'] == 'msc500-near-common-asset-mode-v1':");end=new.index("        require(item['id'] == 'asset-selector-common'",begin);self.assertEqual(new[:begin]+new[end:],base)
 def test_wrong_evidence_selection(self):
  p=copy.deepcopy(item['evidence']);p['crt']['sha256']='0'*64
  with self.assertRaises(ValueError):profile.validate_evidence(M,p,M.parent/'CHESS.EXE')
 def test_native_not_file_backed(self):
  from reference import build_reference
  image=build_reference((M.parent/'CHESS.EXE').read_bytes())['image'];self.assertGreaterEqual(0x5cc20+0x8176,len(image))
 def test_old_profile_remains_closed(self):
  import source_inputs
  with self.assertRaises(ValueError):source_inputs.validate_object(raw)
 def test_no_actor_definition(self):
  self.assertEqual(profile.NAMES,['_mode_8176']);self.assertNotIn(b'actors_ready',(D/'positive.c').read_bytes())

def bad_item(name,key,value):
 def f(self):
  v=copy.deepcopy(item);v[key]=value
  with self.assertRaises(ValueError):profile.validate_item(v)
 f.__name__=name;setattr(Tests,name,f)
for name,key,value in [('test_wrong_id','id','foreign'),('test_wrong_backend','backend','msc500-near-common-source-v1'),('test_wrong_source','source','elsewhere.c'),('test_wrong_source_pin','source_sha256','0'*64),('test_wrong_compiler','compiler','msc510'),('test_wrong_flags','flags',['/AS','/Zi']),('test_wrong_tools_manifest','toolchain_manifest_sha256','0'*64),('test_wrong_size','objects',[{'symbol':'_mode_8176','size':4,'storage':'near-common'}]),('test_wrong_name','objects',[{'symbol':'_actors_ready','size':2,'storage':'near-common'}]),('test_extra_name','objects',[{'symbol':'_mode_8176','size':2,'storage':'near-common'},{'symbol':'_actors_ready','size':2,'storage':'near-common'}]),('test_initialized_kind','objects',[{'symbol':'_mode_8176','size':2,'storage':'initialized'}])]:bad_item(name,key,value)
def mutation(name,kind,fn):
 def f(self):
  data=rewrite(raw,kind,fn)
  with self.assertRaises(ValueError):profile.validate_object(data)
 f.__name__=name;setattr(Tests,name,f)
mutation('test_comdef_byte_size',0xb0,lambda p:p[:-1]+b'\x01')
mutation('test_comdef_unsigned_type',0xb0,lambda p:p[:-4]+b'\x80\x85\x62\x02')
mutation('test_comdef_far_kind',0xb0,lambda p:p[:-2]+b'\x61\x02')
mutation('test_changed_group',0x9a,lambda p:p[:-1]+b'\x01')
mutation('test_entry_point',0x8a,lambda p:b'\x40')
mutation('test_wrong_debug_fixup',0x9c,lambda p:p[:1]+b'\x03'+p[2:])
mutation('test_wrong_cv_payload',0xa0,lambda p:p[:-1]+bytes([p[-1]^1]))
mutation('test_changed_source_name',0x80,lambda p:p.replace(b'UNIT',b'FAIL'))
if __name__=='__main__':unittest.main(verbosity=2)
