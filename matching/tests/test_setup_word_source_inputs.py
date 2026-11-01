"""Isolated staged tests; never modifies canonical source-input files."""
import copy,importlib.util,json,shutil,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parent
sys.path.insert(0,str(PROJECT))
import setup_word_source_inputs as d
import source_inputs as dispatch
assert Path(d.__file__).resolve()==PROJECT/'setup_word_source_inputs.py'
assert Path(dispatch.__file__).resolve()==PROJECT/'source_inputs.py'
STAGE=PROJECT/'build/setup-word-common-profile'
ITEM=json.loads((STAGE/'profile-item.proposed.json').read_text())
PRODUCTION_CONFIG=json.loads((PROJECT/'config/source-inputs.json').read_text())
CONFIG=json.loads((PROJECT/'build/setup-word-common-profile/source-inputs.proposed.json').read_text())
assert len(CONFIG['source_allocations'])==6 and CONFIG['source_allocations'][-1]==ITEM
assert PRODUCTION_CONFIG['schema_version']==CONFIG['schema_version'] and PRODUCTION_CONFIG['source_allocations'][:6]==CONFIG['source_allocations']
TARGET=PROJECT.parent/'CHESS.EXE'
def mutate(blob,kind,fn):
 out=bytearray();at=0;done=False
 while at<len(blob):
  k=blob[at];n=int.from_bytes(blob[at+1:at+3],'little');payload=blob[at+3:at+2+n]
  if k==kind and not done:payload=fn(bytearray(payload));done=True
  head=bytes([k])+ (len(payload)+1).to_bytes(2,'little');out+=head+payload+bytes([(-sum(head+payload))&255]);at+=3+n
 assert done;return bytes(out)
class TestSetupWordCommon(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.temp=tempfile.TemporaryDirectory();cls.project=Path(cls.temp.name)
  for item in CONFIG['source_allocations']:
   src=cls.project/item['source'];src.parent.mkdir(parents=True,exist_ok=True)
   shutil.copyfile(PROJECT/item['source'],src)
   for row in item['evidence'].values():
    dst=cls.project/row['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(PROJECT/row['path'],dst)
  (cls.project/'config').mkdir();(cls.project/'config/source-inputs.json').write_text(json.dumps(CONFIG))
  cls.blob=(PROJECT/'build/setup-word-storage/SCALARS.OBJ').read_bytes()
 @classmethod
 def tearDownClass(cls):cls.temp.cleanup()
 def test_actual_complete_object(self):self.assertEqual([x['symbol'] for x in d.validate_object(self.blob)],d.NAMES)
 def test_primary_and_authentic_two_order_evidence(self):
  constraints,proof=d.validate_evidence(self.project,d.PINS,TARGET);self.assertEqual(len(constraints),3);self.assertTrue(all(not c['resolved'] for c in constraints));self.assertEqual(len(proof['authentic_LINK_trials']),2)
 def test_bad_checksum(self):
  b=bytearray(self.blob);b[-1]^=1
  with self.assertRaises(ValueError):d.validate_object(bytes(b))
 def test_closed_raw_records(self):
  changes=[(0xb0,lambda p:p.replace(b'\x80\x81\x62\x02',b'\x80\x82\x62\x02',1)),(0xb0,lambda p:p.replace(b'\x62\x02',b'\x62\x04',1)),(0xb0,lambda p:p.replace(b'\x62\x02',b'\x61\x02',1)),(0xb0,lambda p:p.replace(b'_setup_word_934a',b'_setup_word_934x',1)),(0xb0,lambda p:p+p[:21]),(0xb0,lambda p:p[21:42]+p[:21]+p[42:]),(0x9a,lambda p:p[:-1]+b'\x01'),(0x88,lambda p:b'\x00\x9e\x00'),(0x98,lambda p:p[:1]+b'\x02\x00'+p[3:]),(0x8a,lambda p:b'\x01')]
  for kind,fn in changes:
   with self.subTest(kind=kind),self.assertRaises(ValueError):d.validate_object(mutate(self.blob,kind,fn))
 def test_closed_item(self):
  for key,val in [('source','../dialog.c'),('flags',['/AS']),('compiler','msc510'),('source_sha256','0'*64),('toolchain_manifest_sha256','0'*64),('objects',[])]:
   x=copy.deepcopy(ITEM);x[key]=val
   with self.subTest(key=key),self.assertRaises(ValueError):d.validate_item(x)
 def test_every_object_byte_is_pinned(self):
  for at in range(len(self.blob)):
   b=bytearray(self.blob);b[at]^=1
   with self.subTest(offset=at),self.assertRaises(ValueError):d.validate_object(bytes(b))
 def test_compiler_runs_before_any_target_read(self):
  class StopGeneration(Exception):pass
  def compiler(*args,**kwargs):raise StopGeneration()
  with self.assertRaises(StopGeneration):d.build_input(ITEM,self.project,self.project/'target-never-created',self.project/'never',compiler_fn=compiler)
 def test_unknown_item_field(self):
  x=copy.deepcopy(ITEM);x['credit']=4
  with self.assertRaises(ValueError):d.validate_item(x)
 def test_missing_evidence(self):
  pins=dict(d.PINS);pins.pop('crt')
  with self.assertRaises(ValueError):d.validate_evidence(self.project,pins,TARGET)
 def test_tampered_pin_file(self):
  path=self.project/d.PINS['SCALARS-ACCESS-MAIN_pass']['path'];before=path.read_bytes();path.write_bytes(b'failed')
  try:
   with self.assertRaisesRegex(ValueError,'pin mismatch'):d.validate_evidence(self.project,d.PINS,TARGET)
  finally:path.write_bytes(before)
 def test_bad_original(self):
  t=self.project/'wrong.exe';t.write_bytes(b'wrong')
  with self.assertRaisesRegex(ValueError,'target pin'):d.validate_evidence(self.project,d.PINS,t)
 def test_fresh_setup_word_generation(self):
  row=d.build_input(ITEM,self.project,TARGET,self.project/'fresh-setup');self.assertEqual(row['allocation_bytes'],6);self.assertEqual(row['matching_credit'],0);self.assertEqual(row['initialized_bytes'],0);self.assertFalse(row['placement_proven'])
 def test_existing_five_plus_setup_fresh(self):
  result=dispatch.build_source_inputs(self.project,TARGET,self.project/'fresh-six');self.assertEqual(len(result['objects']),6);self.assertEqual(sum(len(x['definitions']) for x in result['objects']),30);self.assertEqual(sum(x['allocation_bytes'] for x in result['objects']),94);self.assertEqual(result['matching_credit'],0);self.assertTrue(all(x['initialized_bytes']==0 for x in result['objects']))
 def test_duplicate_admitted_definition_rejected_before_generation(self):
  cfg=self.project/'dialog-only.json';cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[ITEM]}))
  with patch.object(dispatch,'compile_c',side_effect=AssertionError('must not compile')):
   with self.assertRaisesRegex(ValueError,'duplicate allocation'):dispatch.build_source_inputs(self.project,TARGET,self.project/'dup',config_path=cfg,defined_symbols=['_setup_word_934a'])
 def test_duplicate_source_rejected(self):
  cfg=self.project/'dup-source.json';cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[ITEM,ITEM]}))
  with patch.object(d,'build_input',return_value={'id':ITEM['id']}):
   with self.assertRaisesRegex(ValueError,'duplicate source'):dispatch.build_source_inputs(self.project,TARGET,self.project/'dup2',config_path=cfg)
 def test_source_change_rejected_before_compiler(self):
  p=self.project/d.SOURCE;b=p.read_bytes();p.write_bytes(b+b'\n')
  try:
   with self.assertRaisesRegex(ValueError,'source pin'):d.build_input(ITEM,self.project,TARGET,self.project/'bad',compiler_fn=lambda *a,**k:self.fail('compiler called'))
  finally:p.write_bytes(b)
if __name__=='__main__':unittest.main()
