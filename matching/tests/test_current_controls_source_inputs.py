"""Canonical-ready tests. All generated files stay in TemporaryDirectory."""
from pathlib import Path
import copy,dataclasses,hashlib,importlib,json,shutil,sys,tempfile,unittest
from unittest.mock import patch
M=Path(__file__).resolve().parents[1];sys.path.insert(0,str(M));sys.dont_write_bytecode=True
import current_controls_source_inputs as b
import source_inputs as dispatch
from current_controls_profile_pins import PINS
assert Path(b.__file__).resolve()==(M/'current_controls_source_inputs.py').resolve()
assert Path(dispatch.__file__).resolve()==(M/'source_inputs.py').resolve()
F=M/'build/current-controls-storage-review'
ITEM={'id':'current-controls-common','backend':b.BACKEND,'source':b.SOURCE,'source_sha256':b.SOURCE_SHA,'compiler':'msc500','flags':b.FLAGS,'toolchain_manifest_sha256':b.MANIFEST_SHA,'objects':[{'symbol':'_current_controls','size':4,'storage':'near-common'}],'evidence':PINS}
TARGET=Path('/home/kierzo/chess/CHESS.EXE')
def mutation(kind,transform):
 raw=(F/'near.obj').read_bytes();out=bytearray();at=0;done=False
 while at<len(raw):
  n=int.from_bytes(raw[at+1:at+3],'little');end=at+3+n;p=raw[at+3:end-1]
  if raw[at]==kind and not done:p=transform(p);done=True
  record=bytes([raw[at]])+(len(p)+1).to_bytes(2,'little')+p;out.extend(record+bytes([(-sum(record))&255]));at=end
 assert done
 return bytes(out)
class CurrentControlsProfile(unittest.TestCase):
 def test_real_frozen_object(self):self.assertEqual(b.validate_object((F/'near.obj').read_bytes()),[{'symbol':'_current_controls','type_index':0x208,'datatype':0x62,'size':4}])
 def test_far_pointer_model_rejected(self):
  with self.assertRaises(ValueError):b.validate_object((F/'far.obj').read_bytes())
 def test_initialized_model_rejected(self):
  with self.assertRaises(ValueError):b.validate_object((F/'initialized.obj').read_bytes())
 def test_checksum(self):
  p=bytearray((F/'near.obj').read_bytes());p[-1]^=1
  with self.assertRaisesRegex(ValueError,'checksum'):b.validate_object(bytes(p))
 def test_common_width(self):
  with self.assertRaises(ValueError):b.validate_object(mutation(0xb0,lambda p:p[:-1]+b'\x08'))
 def test_common_storage(self):
  with self.assertRaises(ValueError):b.validate_object(mutation(0xb0,lambda p:p[:-2]+b'\x61'+p[-1:]))
 def test_common_union_type(self):
  with self.assertRaises(ValueError):b.validate_object(mutation(0xb0,lambda p:p[:-3]+b'\x09'+p[-2:]))
 def test_common_name(self):
  with self.assertRaises(ValueError):b.validate_object(mutation(0xb0,lambda p:p.replace(b'_current_controls',b'_current_controlX')))
 def test_duplicate_common(self):
  with self.assertRaises(ValueError):b.validate_object(mutation(0xb0,lambda p:p+p))
 def test_dgroup(self):
  with self.assertRaises(ValueError):b.validate_object(mutation(0x9a,lambda p:p[:-1]+b'\x01'))
 def test_member_cv(self):
  with self.assertRaises(ValueError):b.validate_object(mutation(0xa0,lambda p:p[:-1]+bytes([p[-1]^1])))
 def test_metadata_extra(self):
  x=copy.deepcopy(ITEM);x['capacity']=4
  with self.assertRaises(ValueError):b.validate_item(x)
 def test_metadata_type(self):
  x=copy.deepcopy(ITEM);x['objects'][0]['size']=8
  with self.assertRaises(ValueError):b.validate_item(x)
 def test_metadata_evidence(self):
  x=copy.deepcopy(ITEM);x['evidence']['object']['sha256']='0'*64
  with self.assertRaises(ValueError):b.validate_item(x)
 def test_metadata_source_alias(self):
  x=copy.deepcopy(ITEM);x['source']='src/link/alias.c'
  with self.assertRaises(ValueError):b.validate_item(x)
 def test_metadata_flags(self):
  x=copy.deepcopy(ITEM);x['flags']=['/AM','/Zl','/Zi']
  with self.assertRaises(ValueError):b.validate_item(x)
 def test_metadata_tools(self):
  x=copy.deepcopy(ITEM);x['toolchain_manifest_sha256']='0'*64
  with self.assertRaises(ValueError):b.validate_item(x)
 def test_native_full_evidence(self):
  c,frozen=b.validate_evidence(M,PINS,TARGET)
  self.assertEqual(c[0]['dgroup_offset'],'0xb0ce');self.assertEqual(c[0]['end_exclusive'],'0xb0d2');self.assertFalse(c[0]['resolved'])
 def test_wrong_target(self):
  with tempfile.TemporaryDirectory()as td:
   p=Path(td)/'wrong.exe';p.write_bytes(b'MZ wrong')
   with self.assertRaisesRegex(ValueError,'target pin'):b.validate_evidence(M,PINS,p)
 def test_evidence_missing(self):
  with tempfile.TemporaryDirectory()as td:
   with self.assertRaises(FileNotFoundError):b.validate_evidence(Path(td),PINS,TARGET)
 def test_source_changed_before_compiler(self):
  with tempfile.TemporaryDirectory()as td:
   project=Path(td);p=project/b.SOURCE;p.parent.mkdir(parents=True);p.write_bytes((M/b.SOURCE).read_bytes()+b' ')
   with self.assertRaisesRegex(ValueError,'source pin'):b.build_input(ITEM,project,TARGET,project/'out',compiler_fn=lambda *a,**kw:(_ for _ in()).throw(AssertionError('must not compile')))
 def test_source_symlink(self):
  with tempfile.TemporaryDirectory()as td:
   project=Path(td);p=project/b.SOURCE;p.parent.mkdir(parents=True);p.symlink_to(M/b.SOURCE)
   with self.assertRaisesRegex(ValueError,'alias/symlink'):b.build_input(ITEM,project,TARGET,project/'out')
 def test_normal_dispatch_generation_precedes_target_read(self):
  from msc import compile_c
  with tempfile.TemporaryDirectory()as td:
   root=Path(td);cfg=root/'selection.json';cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[ITEM]}));in_compiler=False;reads=[];real=Path.read_bytes
   def guarded(p):
    q=Path(p).resolve();reads.append((str(q),in_compiler))
    if in_compiler:
     allowed=q==(M/b.SOURCE).resolve()or q.is_relative_to((M/'toolchains/msc500').resolve())or(q.parent.name.startswith('battlechess-msc-')and q.name in ['COMPILE.LOG','UNIT.OBJ'])
     if not allowed:raise AssertionError('non-source/compiler input read during generation: '+str(q))
    return real(p)
   def compiler(*a,**kw):
    nonlocal in_compiler
    in_compiler=True
    try:return compile_c(*a,**kw)
    finally:in_compiler=False
   with patch.object(Path,'read_bytes',guarded),patch.object(dispatch,'compile_c',compiler):r=dispatch.build_source_inputs(M,TARGET,root/'objects',cfg)
   self.assertEqual(len(r['objects']),1);row=r['objects'][0];self.assertEqual(row['object_sha256'],b.OBJECT_SHA);self.assertEqual(row['allocation_bytes'],4);self.assertEqual(row['matching_credit'],0);self.assertFalse(row['placement_proven']);self.assertEqual(row['initialized_bytes'],0)
   self.assertTrue(any(q==str(TARGET)and not during for q,during in reads));self.assertFalse(any(q==str(TARGET)and during for q,during in reads))
 def test_duplicate_dispatch(self):
  with tempfile.TemporaryDirectory()as td:
   p=Path(td)/'cfg.json';p.write_text(json.dumps({'schema_version':1,'source_allocations':[ITEM,ITEM]}))
   with self.assertRaisesRegex(ValueError,'duplicate source'):dispatch.build_source_inputs(M,TARGET,Path(td)/'objects',p)
 def test_existing_public_duplicate(self):
  with tempfile.TemporaryDirectory()as td:
   p=Path(td)/'cfg.json';p.write_text(json.dumps({'schema_version':1,'source_allocations':[ITEM]}))
   with self.assertRaisesRegex(ValueError,'duplicate allocation symbol'):dispatch.build_source_inputs(M,TARGET,Path(td)/'objects',p,defined_symbols=['_current_controls'])
 def test_local_escape(self):
  with self.assertRaises(ValueError):b.local(M,'../escape')
 def test_original_eleven_object_decoders(self):
  # Read-only compatibility: preserve all eleven exact existing full objects.
  manifest=M/'build/current-controls-common-profile-stage/old-profile-objects.json';rows=json.loads(manifest.read_text());self.assertEqual(len(rows),11)
  names=['source_inputs','clock_source_inputs','side_history_source_inputs','book_source_inputs','dialog_source_inputs','setup_word_source_inputs','arena_snapshot_source_inputs','serial_ring_source_inputs','search_word_source_inputs','ui_word_source_inputs','evaluation_control_source_inputs']
  for row,name in zip(rows,names):
   module=importlib.import_module(name);raw=Path(row['object']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),row['object_sha256']);actual=module.validate_object(raw);self.assertEqual([(x['symbol'],x['size'])for x in actual],[(x['symbol'],x['size'])for x in row['definitions']])
if __name__=='__main__':unittest.main()
