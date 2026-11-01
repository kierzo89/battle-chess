"""Closed serial COMMON4/133 gates; canonical-ready, no global checker/LINK."""
from pathlib import Path
import copy,dataclasses,json,shutil,sys,tempfile,unittest
from unittest.mock import patch
PROJECT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(PROJECT))
import serial_ring_source_inputs as d
import source_inputs as dispatch
from omf import read_omf
assert Path(d.__file__).resolve()==PROJECT/'serial_ring_source_inputs.py'
assert Path(dispatch.__file__).resolve()==PROJECT/'source_inputs.py'
STAGE=PROJECT/'build/serial-ring-common-profile-stage'
ITEM=json.loads((STAGE/'profile-item.proposed.json').read_text())
PRODUCTION_CONFIG=json.loads((PROJECT/'config/source-inputs.json').read_text())
CONFIG=json.loads((STAGE/'source-inputs.proposed.json').read_text())
assert PRODUCTION_CONFIG['schema_version']==CONFIG['schema_version']and PRODUCTION_CONFIG['source_allocations'][:8]==CONFIG['source_allocations']
PREFIX=json.loads((STAGE/'base-source-inputs.json').read_text())
assert CONFIG['source_allocations']==PREFIX['source_allocations']+[ITEM]
TARGET=PROJECT.parent/'CHESS.EXE'

def mutate(blob,kind,fn):
 out=bytearray();at=0;done=False
 while at<len(blob):
  k=blob[at];size=int.from_bytes(blob[at+1:at+3],'little');p=blob[at+3:at+2+size]
  if k==kind and not done:p=bytes(fn(bytearray(p)));done=True
  head=bytes([k])+(len(p)+1).to_bytes(2,'little');out.extend(head+p+bytes([(-sum(head+p))&255]));at+=size+3
 assert done;return bytes(out)

def add_record(blob,kind,payload):
 size=len(payload)+1;head=bytes([kind])+size.to_bytes(2,'little');r=head+payload+bytes([(-sum(head+payload))&255])
 at=0
 while blob[at]!=0x8a:at+=int.from_bytes(blob[at+1:at+3],'little')+3
 return blob[:at]+r+blob[at:]

class SerialRingInputsTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.temp=tempfile.TemporaryDirectory();cls.project=Path(cls.temp.name)
  for item in CONFIG['source_allocations']:
   p=cls.project/item['source'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(PROJECT/item['source'],p)
   for row in item['evidence'].values():
    p=cls.project/row['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(PROJECT/row['path'],p)
  (cls.project/'config').mkdir(exist_ok=True);(cls.project/'config/source-inputs.json').write_text(json.dumps(CONFIG))
  cls.blob=(PROJECT/d.PINS['object']['path']).read_bytes()
 @classmethod
 def tearDownClass(cls):cls.temp.cleanup()
 def rejects(self,blob):
  with self.assertRaises(ValueError):d.validate_object(blob)
 def test_real_complete_object(self):
  rows=d.validate_object(self.blob);self.assertEqual([r['symbol']for r in rows],d.NAMES)
  self.assertEqual([r['size']for r in rows],[128,2,2,1]);self.assertEqual([r['type_index']for r in rows],[0x204,0xa4,0xa4,0x84])
  self.assertTrue(all(s.length==0 for s in read_omf(self.blob).segments.values()if s.class_name not in ['DEBSYM','DEBTYP']))
 def test_exact_numeric_leaf81(self):
  self.rejects(mutate(self.blob,0xb0,lambda p:p.replace(b'\x62\x81\x80\x00',b'\x62\x80',1)))
 def test_wrong_array_size(self):self.rejects(mutate(self.blob,0xb0,lambda p:p.replace(b'\x62\x81\x80\x00',b'\x62\x81\x81\x00',1)))
 def test_wrong_array_type(self):self.rejects(mutate(self.blob,0xb0,lambda p:p.replace(b'\x82\x04\x62',b'\x82\x05\x62',1)))
 def test_far_common_not_near(self):self.rejects(mutate(self.blob,0xb0,lambda p:p.replace(b'\x62\x81',b'\x61\x81',1)))
 def test_wrong_near_pointer_type_same_width(self):self.rejects(mutate(self.blob,0xb0,lambda p:p.replace(b'\x80\xa4\x62\x02',b'\x80\xa0\x62\x02',1)))
 def test_far_pointer_type_same_size_claim(self):self.rejects(mutate(self.blob,0xb0,lambda p:p.replace(b'\x80\xa4\x62\x02',b'\x80\xc4\x62\x02',1)))
 def test_pointer_wrong_size(self):self.rejects(mutate(self.blob,0xb0,lambda p:p.replace(b'\x80\xa4\x62\x02',b'\x80\xa4\x62\x04',1)))
 def test_signed_flag_wrong_type(self):self.rejects(mutate(self.blob,0xb0,lambda p:p.replace(b'\x80\x84\x62\x01',b'\x80\x80\x62\x01',1)))
 def test_word_flag_wrong_size(self):self.rejects(mutate(self.blob,0xb0,lambda p:p.replace(b'\x80\x84\x62\x01',b'\x80\x84\x62\x02',1)))
 def test_duplicate_common(self):self.rejects(mutate(self.blob,0xb0,lambda p:p+p))
 def test_renamed_common(self):self.rejects(mutate(self.blob,0xb0,lambda p:p.replace(b'_byte_read_cursor',b'_byte_read_curxor',1)))
 def test_wrong_source_name(self):self.rejects(mutate(self.blob,0x80,lambda p:p.replace(b'SCALARS',b'SCALARX',1)))
 def test_nonzero_loaded_SEGDEF(self):self.rejects(mutate(self.blob,0x98,lambda p:p[:1]+b'\x02\x00'+p[3:]))
 def test_group_directive_entry(self):
  for kind,fn in [(0x9a,lambda p:p[:-1]+b'\x01'),(0x88,lambda p:b'\0\x9e\0'),(0x8a,lambda p:b'\x01')]:
   with self.subTest(kind=kind):self.rejects(mutate(self.blob,kind,fn))
 def test_foreign_LIDATA_or_initialized_DATA(self):
  for kind,p in [(0xa2,b'\x02\0\0\x01\0\0\0\x01\0'),(0xa0,b'\x02\0\0\0')]:self.rejects(add_record(self.blob,kind,p))
 def test_public_alias(self):self.rejects(add_record(self.blob,0x90,b'\x01\x02\x05_fake\0\0\0'))
 def test_foreign_debug_fixup(self):self.rejects(mutate(self.blob,0x9c,lambda p:bytes([p[0]^1])+p[1:]))
 def test_all_bytes_and_checksums(self):
  for i in range(len(self.blob)):
   b=bytearray(self.blob);b[i]^=1
   with self.subTest(i=i):self.rejects(bytes(b))
 def test_closed_item_variants(self):
  for key,value in [('source','../state.c'),('source_sha256','0'*64),('compiler','msc510'),('flags',['/AS']),('objects',[]),('toolchain_manifest_sha256','0'*64),('backend','msc500-near-common-source-v1')]:
   x=copy.deepcopy(ITEM);x[key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):d.validate_item(x)
  x=copy.deepcopy(ITEM);x['source_name']='UNIT.C'
  with self.assertRaises(ValueError):d.validate_item(x)
 def test_compiler_precedes_any_target_read(self):
  class Stop(Exception):pass
  def compiler(*a,**kw):self.assertEqual(kw['source_name'],'SCALARS.C');raise Stop()
  with self.assertRaises(Stop):d.build_input(ITEM,self.project,self.project/'nonexistent-target',self.project/'never',compiler_fn=compiler)
 def test_source_change_rejected_before_compiler(self):
  p=self.project/d.SOURCE;before=p.read_bytes();p.write_bytes(before.replace(b'[128]',b'[129]'))
  try:
   with self.assertRaisesRegex(ValueError,'source pin'):d.build_input(ITEM,self.project,TARGET,self.project/'bad',compiler_fn=lambda *a,**k:self.fail('compiled changed source'))
  finally:p.write_bytes(before)
 def test_source_alias_rejected(self):
  p=self.project/d.SOURCE;before=p.read_bytes();other=p.with_name('alias.c');other.write_bytes(before);p.unlink();p.symlink_to(other)
  try:
   with self.assertRaisesRegex(ValueError,'alias/symlink'):d.build_input(ITEM,self.project,TARGET,self.project/'bad',compiler_fn=lambda *a,**k:self.fail('compiled alias'))
  finally:p.unlink();p.write_bytes(before);other.unlink()
 def test_evidence_nativeCRT_two_LINK_and_limits(self):
  constraints,compiler=d.validate_evidence(self.project,d.PINS,TARGET)
  self.assertEqual(len(constraints),4);self.assertTrue(all(not x['resolved']and not x['historical_capacity_unique']and x['larger_aggregate_ownership_unknown']for x in constraints))
  self.assertEqual(compiler['source_name'],'SCALARS.C')
 def test_missing_evidence(self):
  p=dict(d.PINS);p.pop('crt')
  with self.assertRaisesRegex(ValueError,'evidence set'):d.validate_evidence(self.project,p,TARGET)
 def test_tampered_evidence_each_key(self):
  for name,row in d.PINS.items():
   p=self.project/row['path'];before=p.read_bytes();p.write_bytes(before+b'X')
   try:
    with self.subTest(name=name),self.assertRaisesRegex(ValueError,'pin mismatch'):d.validate_evidence(self.project,d.PINS,TARGET)
   finally:p.write_bytes(before)
 def test_bad_original(self):
  target=self.project/'wrong.exe';target.write_bytes(b'wrong')
  with self.assertRaisesRegex(ValueError,'original target'):d.validate_evidence(self.project,d.PINS,target)
 def test_fresh_normal_source_input(self):
  row=d.build_input(ITEM,self.project,TARGET,self.project/'fresh-one')
  self.assertEqual(row['allocation_bytes'],133);self.assertEqual(row['initialized_bytes'],0);self.assertEqual(row['matching_credit'],0);self.assertFalse(row['placement_proven']);self.assertFalse(row['historical_capacity_unique'])
  self.assertEqual(row['compiler']['source_name'],'SCALARS.C')
 def test_fresh_all_eight_dispatch(self):
  result=dispatch.build_source_inputs(self.project,TARGET,self.project/'fresh-eight')
  self.assertEqual(len(result['objects']),8);self.assertEqual(sum(len(r['definitions'])for r in result['objects']),51)
  self.assertEqual(sum(r['allocation_bytes']for r in result['objects']),267);self.assertTrue(all(r['initialized_bytes']==r['matching_credit']==0 for r in result['objects']));self.assertEqual(result['matching_credit'],0)
  report=dispatch.report_inputs(result);self.assertEqual(len(report),8);self.assertEqual(len(report[-1]['definitions']),4)
 def test_duplicate_symbols_rejected_before_generation(self):
  cfg=self.project/'only.json';cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[ITEM]}))
  with patch.object(dispatch,'compile_c',side_effect=AssertionError('generation not expected')):
   with self.assertRaisesRegex(ValueError,'duplicate allocation'):dispatch.build_source_inputs(self.project,TARGET,self.project/'dup',config_path=cfg,defined_symbols=['_byte_ring_buffer'])
 def test_duplicate_source_id(self):
  cfg=self.project/'duplicate.json';cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[ITEM,ITEM]}))
  with patch.object(d,'build_input',return_value={'id':ITEM['id']}):
   with self.assertRaisesRegex(ValueError,'duplicate source'):dispatch.build_source_inputs(self.project,TARGET,self.project/'dup',config_path=cfg)
 def test_unknown_profile_still_rejected(self):
  cfg=self.project/'unknown.json';x=copy.deepcopy(ITEM);x['backend']='msc500-near-common-any';cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[x]}))
  with self.assertRaises(ValueError):dispatch.build_source_inputs(self.project,TARGET,self.project/'unknown',config_path=cfg)

if __name__=='__main__':unittest.main()
