"""Adopted-module controls; mocked compiler routes do not prove fresh generation."""
from pathlib import Path
import sys,json,copy,unittest,tempfile,io,builtins,os
from unittest.mock import patch
M=next(p for p in Path(__file__).resolve().parents if(p/'config/msc500.json').is_file());sys.path.insert(0,str(M));sys.dont_write_bytecode=True
import independent_control_cells15_source_inputs as b
import source_inputs
from msc import CompileResult
from omf import read_omf
F=M/'tests/fixtures/independent_control_cells15'
class IndependentControlCells15Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.raw=(F/'actual.obj').read_bytes();cls.item=json.loads((F/'item.json').read_text());cls.o=read_omf(cls.raw)
 def reject(self,fn,*args,**kw):
  with self.assertRaises((ValueError,KeyError)):fn(*args,**kw)
 def bad_item(self,k,v):r=copy.deepcopy(self.item);r[k]=v;self.reject(b.validate_item,r)
 def idx(self,k):return next(i for i,(kind,at,p)in enumerate(self.o.records)if kind==k)
 def raw_edit(self,index,payload=None,kind=None):
  k,at,v=self.o.records[index];n=int.from_bytes(self.raw[at+1:at+3],'little');p=v if payload is None else payload;head=bytes([k if kind is None else kind])+(len(p)+1).to_bytes(2,'little')+p;new=head+bytes([-sum(head)%256]);return self.raw[:at]+new+self.raw[at+3+n:]
 def changed_common(self,before,after):
  i=self.idx(0xb0);old=self.o.records[i][2];new=old.replace(before,after,1);self.assertNotEqual(old,new);mutated=self.raw_edit(i,new);self.assertNotEqual(mutated,self.raw);return mutated
 def fake(self):return CompileResult(self.raw,'MOCK route only',('mock',),b.SOURCE_SHA,b.MANIFEST_SHA,b.TOOLS,tuple(b.FLAGS),'msc500','UNIT.C')
 def test_adopted_modules(self):self.assertEqual(Path(b.__file__).resolve(),M/'independent_control_cells15_source_inputs.py');self.assertEqual(Path(source_inputs.__file__).resolve(),M/'source_inputs.py')
 def test_exact_registry_profile(self):b.validate_item(self.item)
 def test_wrong_source(self):self.bad_item('source','src/link/aliases.c')
 def test_wrong_flags(self):self.bad_item('flags',['/AS','/Zi'])
 def test_no_capacity_or_alias_key(self):self.bad_item('capacity',6)
 def test_wrong_definition_size(self):
  v=copy.deepcopy(self.item['objects']);v[0]['size']=3;self.bad_item('objects',v)
 def test_byte_cannot_replace_word_type(self):self.reject(b.validate_object,self.changed_common(bytes.fromhex('80816202'),bytes.fromhex('80846202')))
 def test_near_pointer_cannot_be_far(self):self.reject(b.validate_object,self.changed_common(bytes.fromhex('80a46202'),bytes.fromhex('80a06202')))
 def test_ulong_cannot_be_word(self):self.reject(b.validate_object,self.changed_common(bytes.fromhex('80866204'),bytes.fromhex('80866202')))
 def test_signed_int_cannot_be_unsigned(self):self.reject(b.validate_object,self.changed_common(bytes.fromhex('80816202'),bytes.fromhex('80856202')))
 def test_unsigned_byte_cannot_be_signed(self):self.reject(b.validate_object,self.changed_common(bytes.fromhex('80846201'),bytes.fromhex('80806201')))
 def test_no_extra_record_latch_definition(self):self.bad_item('objects',self.item['objects']+[{'symbol':'_record_latch','size':1,'storage':'near-common'}])
 def test_wellformed_far_common_rejected(self):self.reject(b.validate_object,self.changed_common(bytes.fromhex('6202'),bytes.fromhex('610102')))
 def test_fifteen_definitions_in_one_record(self):
  d=b.validate_object(self.raw);self.assertEqual(len(d),15);self.assertEqual(sum(x['size']for x in d),27);self.assertEqual(len([1 for k,a,p in self.o.records if k==0xb0]),1)
 def test_checksum(self):v=bytearray(self.raw);v[-1]^=1;self.reject(b.validate_object,bytes(v))
 def test_truncation(self):self.reject(b.validate_object,self.raw[:-1])
 def test_unknown_record(self):self.reject(b.validate_object,self.raw_edit(self.idx(0xb0),kind=0xff))
 def test_local_common_rejected(self):self.reject(b.validate_object,self.raw_edit(self.idx(0xb0),kind=0xb2))
 def test_duplicate_definition(self):
  i=self.idx(0xb0);p=self.o.records[i][2];first=p[:1+p[0]+2+1+1];self.reject(b.validate_object,self.raw_edit(i,p+first))
 def test_debug_type_cannot_disagree(self):
  i=self.idx(0xa0);p=bytearray(self.o.records[i][2]);self.assertEqual(p[9],0x86);p[9]=0x85;self.reject(b.validate_object,self.raw_edit(i,bytes(p)))
 def test_debug_target_binding(self):
  f=self.o.fixups[0];i=next(i for i,(k,at,p)in enumerate(self.o.records)if at==f.record_offset);p=self.o.records[i][2];self.assertEqual(p.count(f.raw),1);new=bytearray(f.raw);new[-1]=2 if new[-1]!=2 else 3;self.assertNotEqual(bytes(new),f.raw);self.reject(b.validate_object,self.raw_edit(i,p.replace(f.raw,bytes(new),1)))
 def test_hidden_loaded_storage(self):
  i=self.idx(0x98);p=bytearray(self.o.records[i][2]);p[1:3]=(1).to_bytes(2,'little');self.reject(b.validate_object,self.raw_edit(i,bytes(p)))
 def test_wellformed_extra_PUBLIC_rejected(self):
  at=next(a for k,a,p in self.o.records if k==0x8a);payload=b'\x01\x02\x06_alias\0\0\0';head=b'\x90'+(len(payload)+1).to_bytes(2,'little')+payload;record=head+bytes([-sum(head)%256]);self.reject(b.validate_object,self.raw[:at]+record+self.raw[at:])
 def test_near_storage_required_in_row(self):
  v=copy.deepcopy(self.item['objects']);v[0]['storage']='far-common';self.bad_item('objects',v)
 def test_real_thread_record_not_field(self):
  i=self.idx(0x9c);self.assertEqual(self.o.records[i][2].hex(),'000301020201030440014501');p=bytearray(self.o.records[i][2]);p[-1]^=1;self.reject(b.validate_object,self.raw_edit(i,bytes(p)))
 def test_native_typed_closure(self):
  c=b.validate_evidence(M,self.item['evidence'],M.parent/'CHESS.EXE');self.assertEqual([x['size']for x in c],[4,2,2,2,1,1,2,1,2,2,2,1,1,2,2]);self.assertTrue(all(x['initialized_byte_credit']==0 and not x['neighbor_capacity_claim']for x in c))
 def test_evidence_tamper(self):
  old=Path.read_bytes;target=(M/b.PINS['ownership']['path']).resolve()
  def read(p,*a,**k):return b'{}'if Path(p).resolve()==target else old(p,*a,**k)
  with patch.object(Path,'read_bytes',read):self.reject(b.validate_evidence,M,self.item['evidence'],M.parent/'CHESS.EXE')
 def test_current254_scope_tamper(self):
  old=Path.read_bytes;target=(M/b.PINS['current_scope']['path']).resolve()
  def read(p,*a,**k):return b'{}'if Path(p).resolve()==target else old(p,*a,**k)
  with patch.object(Path,'read_bytes',read):self.reject(b.validate_evidence,M,self.item['evidence'],M.parent/'CHESS.EXE')
 def test_whole_client_tamper(self):
  old=Path.read_bytes;target=(M/b.PINS['client_0']['path']).resolve()
  def read(p,*a,**k):return b'bad'if Path(p).resolve()==target else old(p,*a,**k)
  with patch.object(Path,'read_bytes',read):self.reject(b.validate_evidence,M,self.item['evidence'],M.parent/'CHESS.EXE')
 def test_near_accounting(self):
  totals=source_inputs.COMMON_totals([{'definitions':b.validate_object(self.raw)}]);self.assertEqual(totals,{'near':{'contributions':1,'definitions':15,'bytes':27},'far':{'contributions':0,'definitions':0,'bytes':0}})
 def test_standard_callback_without_dosbox_override(self):
  calls=[]
  def callback(source,flags,*,compiler='msc500'):calls.append((source,flags,compiler));return self.fake()
  result,meta=b.invoke_standard(M/b.SOURCE,M,callback);self.assertEqual(len(calls),1);self.assertFalse(meta['host_default_dosbox']['explicit_dosbox_override']);self.assertEqual(len(meta['active_open_API_probes']),20)
 def test_near_far_accounting_separate(self):
  far={'symbol':'_kept_far','size':70000,'communal_kind':0x61,'storage':'far-common','element_count':70000,'element_bytes':1}
  totals=source_inputs.COMMON_totals([{'definitions':b.validate_object(self.raw)},{'definitions':[far]}]);self.assertEqual(totals['near']['bytes'],27);self.assertEqual(totals['near']['definitions'],15);self.assertEqual(totals['far']['bytes'],70000)
 def test_default_host_pin(self):
  with patch.object(b.shutil,'which',return_value='/wrong/dosbox'):self.reject(b.invoke_standard,M/b.SOURCE,M,lambda *a,**k:self.fake())
 def test_each_route_requests_fresh_compile(self):
  with tempfile.TemporaryDirectory()as d:
   with patch.object(b,'compile_c',return_value=self.fake())as c:
    x=b.build_input(self.item,M,M.parent/'CHESS.EXE',Path(d)/'a');y=b.build_input(self.item,M,M.parent/'CHESS.EXE',Path(d)/'b');self.assertEqual(c.call_count,2);self.assertEqual(x['allocation_bytes'],27);self.assertEqual(y['initialized_bytes'],0);self.assertEqual(x['matching_credit'],0)
 def test_ordinary_dispatch_duplicate_and_existing_definition(self):
  with tempfile.TemporaryDirectory()as d:
   root=Path(d);cfg=root/'one.json';cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[self.item]}))
   with patch.object(source_inputs,'compile_c',return_value=self.fake())as c:
    result=source_inputs.build_source_inputs(M,M.parent/'CHESS.EXE',root/'out',cfg);self.assertEqual(len(result['objects']),1);self.assertEqual(result['objects'][0]['allocation_bytes'],27);self.assertEqual(c.call_count,1)
   cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[self.item,self.item]}))
   with patch.object(source_inputs,'compile_c',return_value=self.fake()):self.reject(source_inputs.build_source_inputs,M,M.parent/'CHESS.EXE',root/'duplicate',cfg)
   cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[self.item]}))
   with patch.object(source_inputs,'compile_c',return_value=self.fake()):self.reject(source_inputs.build_source_inputs,M,M.parent/'CHESS.EXE',root/'defined',cfg,defined_symbols=['_menu_state'])
 def test_all_open_APIs_and_source_write_denied(self):
  with tempfile.TemporaryDirectory()as d:
   root=Path(d);src=root/'source.c';src.write_text('int pointer_x;');outside=root/'old.obj';outside.write_bytes(b'old');config=root/'config';config.mkdir();(config/'msc500.json').write_text(json.dumps({'files':[]}))
   with b.scope(src,root)as events:
    self.assertEqual(src.read_text(),'int pointer_x;')
    for fn in[lambda:outside.read_bytes(),lambda:builtins.open(outside,'rb'),lambda:io.open(outside,'rb'),lambda:os.open(outside,os.O_RDONLY)]:self.reject(fn)
    self.reject(src.write_text,'bad');self.assertEqual(len(events['blocked']),5)
 def test_regular_descriptor_not_reference_backdoor(self):
  with tempfile.TemporaryDirectory()as d:
   root=Path(d);src=root/'source.c';src.write_text('int pointer_x;');outside=root/'old.obj';outside.write_bytes(b'old');config=root/'config';config.mkdir();(config/'msc500.json').write_text(json.dumps({'files':[]}))
   with outside.open('rb')as old:
    with b.scope(src,root):self.reject(builtins.open,old.fileno(),'rb')
if __name__=='__main__':unittest.main()
