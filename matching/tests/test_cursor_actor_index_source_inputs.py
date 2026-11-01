"""Prepared adopted-module controls; mock routes do not establish fresh generation."""
from pathlib import Path
import sys,json,copy,unittest,tempfile,dataclasses,io,builtins,os
from unittest.mock import patch
M=next(p for p in Path(__file__).resolve().parents if(p/'config/msc500.json').is_file());sys.path.insert(0,str(M));sys.dont_write_bytecode=True
import cursor_actor_index_source_inputs as b
import source_inputs
from msc import CompileResult
from omf import read_omf
F=M/'tests/fixtures/cursor_actor57d0'
class CursorActorIndexTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.raw=(F/'actual.obj').read_bytes();cls.item=json.loads((F/'item.json').read_text());cls.o=read_omf(cls.raw)
 def reject(self,fn,*a,**k):
  with self.assertRaises((ValueError,KeyError)):fn(*a,**k)
 def bad_item(self,key,value):r=copy.deepcopy(self.item);r[key]=value;self.reject(b.validate_item,r)
 def raw_edit(self,index,payload=None,kind=None):
  k,at,v=self.o.records[index];oldn=int.from_bytes(self.raw[at+1:at+3],'little');p=v if payload is None else payload;head=bytes([k if kind is None else kind])+(len(p)+1).to_bytes(2,'little')+p;new=head+bytes([-sum(head)%256]);return self.raw[:at]+new+self.raw[at+3+oldn:]
 def idx(self,k):return next(i for i,(kind,a,p)in enumerate(self.o.records)if kind==k)
 def test_adopted(self):self.assertEqual(Path(b.__file__).resolve(),M/'cursor_actor_index_source_inputs.py');self.assertEqual(Path(source_inputs.__file__).resolve(),M/'source_inputs.py')
 def test_item_exact(self):b.validate_item(self.item)
 def test_wrong_source(self):self.bad_item('source','src/link/alias.c')
 def test_wrong_flags(self):self.bad_item('flags',['/AS','/Zi'])
 def test_no_historical_capacity_key(self):self.bad_item('capacity',2)
 def test_wrong_size(self):self.bad_item('objects',[{'symbol':'_cursor_actor_57d0','size':4,'storage':'near-common'}])
 def test_no_alias_definition(self):self.bad_item('objects',self.item['objects']+[{'symbol':'_search_frame','size':2,'storage':'near-common'}])
 def test_pinned_evidence(self):self.bad_item('evidence',{})
 def test_exact_scalar_object(self):self.assertEqual(b.validate_object(self.raw),[{'symbol':'_cursor_actor_57d0','type_index':129,'datatype':98,'size':2}])
 def test_checksum(self):v=bytearray(self.raw);v[-1]^=1;self.reject(b.validate_object,bytes(v))
 def test_truncated(self):self.reject(b.validate_object,self.raw[:-1])
 def test_foreign_record(self):self.reject(b.validate_object,self.raw_edit(self.idx(0xb0),kind=0xff))
 def test_unsigned_type(self):
  i=self.idx(0xb0);v=bytearray(self.o.records[i][2]);v[v.index(bytes.fromhex('8081'))+1]=0x85;self.reject(b.validate_object,self.raw_edit(i,bytes(v)))
 def test_larger_scalar(self):
  i=self.idx(0xb0);v=self.o.records[i][2][:-1]+b'\4';self.reject(b.validate_object,self.raw_edit(i,v))
 def test_far_common(self):
  i=self.idx(0xb0);v=self.o.records[i][2].replace(b'\x62\x02',b'\x61\x02');self.reject(b.validate_object,self.raw_edit(i,v))
 def test_hidden_loaded_storage(self):
  i=self.idx(0x98);v=bytearray(self.o.records[i][2]);v[1:3]=(2).to_bytes(2,'little');self.reject(b.validate_object,self.raw_edit(i,bytes(v)))
 def test_extra_sameaddress_PUBLIC(self):self.reject(b.validate_object,self.raw_edit(self.idx(0xb0),kind=0x90))
 def test_actual_native_evidence(self):c=b.validate_evidence(M,self.item['evidence'],M.parent/'CHESS.EXE');self.assertEqual(c[0]['size'],2);self.assertEqual(c[0]['initialized_byte_credit'],0);self.assertFalse(c[0]['actor_capacity_or_SearchFrame_alias_claim'])
 def test_evidence_tamper(self):
  old=Path.read_bytes;target=(M/b.PINS['ownership']['path']).resolve()
  def read(p,*a,**k):return b'{}'if Path(p).resolve()==target else old(p,*a,**k)
  with patch.object(Path,'read_bytes',read):self.reject(b.validate_evidence,M,self.item['evidence'],M.parent/'CHESS.EXE')
 def test_client_object_tamper(self):
  old=Path.read_bytes;target=(M/b.PINS['client_0']['path']).resolve()
  def read(p,*a,**k):return b'bad'if Path(p).resolve()==target else old(p,*a,**k)
  with patch.object(Path,'read_bytes',read):self.reject(b.validate_evidence,M,self.item['evidence'],M.parent/'CHESS.EXE')
 def fake(self):return CompileResult(self.raw,'route mock only',('mock',),b.SOURCE_SHA,b.MANIFEST_SHA,b.TOOLS,tuple(b.FLAGS),'msc500','UNIT.C')
 def test_fresh_route_requested_each_time(self):
  # Mocks only; root must exercise a real ordinary route separately.
  with tempfile.TemporaryDirectory()as tmp:
   with patch.object(b,'compile_c',return_value=self.fake())as c:
    x=b.build_input(self.item,M,M.parent/'CHESS.EXE',Path(tmp)/'a');y=b.build_input(self.item,M,M.parent/'CHESS.EXE',Path(tmp)/'b');self.assertEqual(c.call_count,2);self.assertEqual(x['allocation_bytes'],2);self.assertEqual(y['initialized_bytes'],0);self.assertEqual(x['matching_credit'],0);self.assertEqual(len(x['compiler']['source_tool_scratch_guard']['blocked']),5)
 def test_ordinary_dispatch_and_duplicate_gate(self):
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp);cfg=root/'one.json';cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[self.item]}))
   with patch.object(source_inputs,'compile_c',return_value=self.fake())as c:
    result=source_inputs.build_source_inputs(M,M.parent/'CHESS.EXE',root/'out',cfg);self.assertEqual(len(result['objects']),1);self.assertEqual(result['objects'][0]['allocation_bytes'],2);self.assertEqual(c.call_count,1)
   cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[self.item,self.item]}))
   with patch.object(source_inputs,'compile_c',return_value=self.fake())as c:self.reject(source_inputs.build_source_inputs,M,M.parent/'CHESS.EXE',root/'dup',cfg)
   cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[self.item]}))
   with patch.object(source_inputs,'compile_c',return_value=self.fake()):self.reject(source_inputs.build_source_inputs,M,M.parent/'CHESS.EXE',root/'defined',cfg,defined_symbols=['_cursor_actor_57d0'])
 def test_guard_all_open_APIs(self):
  with tempfile.TemporaryDirectory()as d:
   root=Path(d);src=root/'source.c';src.write_bytes(b'int cursor_actor_57d0;');outside=root/'target.obj';outside.write_bytes(b'old');config=root/'config';config.mkdir();(config/'msc500.json').write_text(json.dumps({'files':[]}))
   with b.scope(src,root)as events:
    self.assertEqual(src.read_bytes(),b'int cursor_actor_57d0;')
    for fn in[lambda:outside.read_bytes(),lambda:builtins.open(outside,'rb'),lambda:io.open(outside,'rb'),lambda:os.open(outside,os.O_RDONLY)]:self.reject(fn)
    self.reject(src.write_bytes,b'bad');self.assertEqual(len(events['blocked']),5)
if __name__=='__main__':unittest.main()
