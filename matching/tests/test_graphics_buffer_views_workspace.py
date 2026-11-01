"""Prepared adopted-module tests; no MASM/C5/LINK invocation."""
from pathlib import Path
import sys,json,copy,unittest,tempfile,inspect,builtins,io,os
from unittest.mock import patch
M=next(p for p in Path(__file__).resolve().parents if(p/'config/msc500.json').is_file());sys.path.insert(0,str(M));sys.dont_write_bytecode=True
import check
import graphics_buffer_views_workspace_data16 as b
import graphics_buffer_views_zero_omf16 as z
import graphics_splash_workspace_data16 as old_three
import graphics_workspace_data16 as old_two
from reference import build_reference
F=M/'tests/fixtures/graphics_buffer_views'
class GraphicsBufferViewTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.raw=(F/'actual.obj').read_bytes();cls.unit=json.loads((F/'unit.json').read_text());cls.ref=build_reference((M.parent/'CHESS.EXE').read_bytes());_,cls.meta=z.validate_obj(cls.raw)
 def reject(self,fn,*a):
  with self.assertRaises((ValueError,KeyError)):fn(*a)
 def bad_unit(self,k,v):u=copy.deepcopy(self.unit);u[k]=v;self.reject(b.validate_unit,u)
 def replace_record(self,index,payload=None,kind=None):
  r=self.meta['records'][index];at=r['file_offset'];oldn=int.from_bytes(self.raw[at+1:at+3],'little');body=bytes.fromhex(r['payload'])if payload is None else payload;k=r['kind']if kind is None else kind;new=bytes([k])+(len(body)+1).to_bytes(2,'little')+body;new+=bytes([-sum(new)%256]);return self.raw[:at]+new+self.raw[at+3+oldn:]
 def index(self,kind):return next(i for i,r in enumerate(self.meta['records'])if r['kind']==kind)
 def test_adopted_modules(self):self.assertEqual(Path(b.__file__).resolve(),M/'graphics_buffer_views_workspace_data16.py');self.assertEqual(Path(check.__file__).resolve(),M/'check.py')
 def test_exact_unit(self):b.validate_unit(self.unit)
 def test_source_path(self):self.bad_unit('source','src/data/graphics_splash_workspace.asm')
 def test_source_hash(self):self.bad_unit('source_sha256','0'*64)
 def test_foreign_backend(self):self.bad_unit('backend',old_three.BACKEND)
 def test_no_capacity_key(self):self.bad_unit('capacity',86000)
 def test_extent(self):self.bad_unit('size',86001)
 def test_no_extra_label(self):self.bad_unit('symbols',self.unit['symbols']+['_fake'])
 def test_preserved_whole_extent(self):
  data,meta=b.extract_data(self.raw);self.assertEqual(data,bytes(86000));self.assertEqual(data,self.ref['image'][0x120d0:0x270c0]);self.assertEqual([s['length']for s in meta['segments']],[53184,32816]);self.assertEqual(meta['fixups'],0)
 def test_five_real_views(self):self.assertEqual({n:(p['segment'],p['offset'])for n,p in self.meta['publics'].items()},z.PUBLICS);self.assertEqual(z.PUBLICS['_color_buffer'],(1,0x32e0));self.assertEqual(z.PUBLICS['_region_buffer'],(1,0x3f90));self.assertEqual(z.PUBLICS['_metadata_workspace'],(1,0xcc6c));self.assertEqual(z.PUBLICS['_splash_buffer'],(2,0))
 def test_no_new_credit(self):
  _,m=b.extract_data(self.raw);self.assertEqual(m['new_byte_credit'],0);self.assertEqual(m['new_native_MZ_credit'],0);self.assertFalse(m['historical_C_capacity_proven']);self.assertEqual(m['authored_asm_function_credit'],0)
 def test_old_three_gate_preserved(self):self.reject(b.extract_data,(F/'prior-three-public.obj').read_bytes());self.assertEqual(len(old_three.extract_data((F/'prior-three-public.obj').read_bytes())[0]),86000);self.reject(old_three.extract_data,self.raw)
 def test_old_two_gate_preserved(self):self.reject(old_two.extract_data,self.raw)
 def test_checksum(self):r=bytearray(self.raw);r[-1]^=1;self.reject(z.validate_obj,bytes(r))
 def test_truncation(self):self.reject(z.validate_obj,self.raw[:-1])
 def test_extra_module(self):self.reject(z.validate_obj,self.raw+self.raw)
 def test_unknown_raw_record(self):self.reject(z.validate_obj,self.replace_record(self.index(0x98),kind=0xb0))
 def test_segment_length(self):
  i=self.index(0x98);v=bytearray.fromhex(self.meta['records'][i]['payload']);v[1:3]=(53183).to_bytes(2,'little');self.reject(z.validate_obj,self.replace_record(i,bytes(v)))
 def test_private_combine(self):
  i=self.index(0x98);v=bytearray.fromhex(self.meta['records'][i]['payload']);v[0]=0x68;self.reject(z.validate_obj,self.replace_record(i,bytes(v)))
 def test_color_offset(self):
  i=self.index(0x90);v=bytearray.fromhex(self.meta['records'][i]['payload']);at=v.index(b'_color_buffer')+len('_color_buffer');v[at:at+2]=(13025).to_bytes(2,'little');self.reject(z.validate_obj,self.replace_record(i,bytes(v)))
 def test_duplicate_or_unproved_PUBLIC(self):
  i=self.index(0x90);v=bytes.fromhex(self.meta['records'][i]['payload']).replace(b'_region_buffer',b'_region_buffex');self.reject(z.validate_obj,self.replace_record(i,v))
 def test_nonzero_leaf(self):
  i=self.index(0xa2);v=bytearray.fromhex(self.meta['records'][i]['payload']);v[-1]=1;self.reject(z.validate_obj,self.replace_record(i,bytes(v)))
 def test_data_hole(self):
  i=self.index(0xa2);v=bytearray.fromhex(self.meta['records'][i]['payload']);v[1:3]=(1).to_bytes(2,'little');self.reject(z.validate_obj,self.replace_record(i,bytes(v)))
 def test_whole_evidence_and21_raw_clients(self):self.assertEqual(b.validate_evidence(self.unit,M,b.ORIGINAL_SHA256,self.ref),json.loads((M/self.unit['rea_evidence']).read_text())['evidence_id'])
 def test_evidence_dispatch(self):self.assertEqual(check.validate_rea_extent(self.unit,M,b.ORIGINAL_SHA256,self.ref),b.validate_evidence(self.unit,M,b.ORIGINAL_SHA256,self.ref))
 def test_evidence_tamper(self):
  old=Path.read_bytes;target=(M/self.unit['rea_evidence']).resolve()
  def read(p,*a,**kw):return b'{}'if Path(p).resolve()==target else old(p,*a,**kw)
  with patch.object(Path,'read_bytes',read):self.reject(b.validate_evidence,self.unit,M,b.ORIGINAL_SHA256,self.ref)
 def test_consumer_object_tamper(self):
  old=Path.read_bytes;target=(M/'evidence/graphics_buffer_views/consumer0.obj').resolve()
  def read(p,*a,**kw):return b'bad'if Path(p).resolve()==target else old(p,*a,**kw)
  with patch.object(Path,'read_bytes',read):self.reject(b.validate_evidence,self.unit,M,b.ORIGINAL_SHA256,self.ref)
 def test_native_MZ_cannot_be_invented(self):r=copy.deepcopy(self.ref);r['relocations']=list(r['relocations'])+[0x120d0];self.reject(b.validate_evidence,self.unit,M,b.ORIGINAL_SHA256,r)
 def test_native_pointer_field_not_waived(self):
  r=copy.deepcopy(self.ref);view=bytearray(r['image']);view[0x425d]^=1;r['image']=bytes(view);self.reject(b.validate_evidence,self.unit,M,b.ORIGINAL_SHA256,r)
 def test_exact_source(self):v=(M/b.SOURCE).read_bytes();b.source_policy(v);self.reject(b.source_policy,v+b'\nDB 0\n');self.assertEqual(list(inspect.signature(b._assemble_source).parameters),['source','project'])
 def test_fresh_route_not_cached(self):
  # Route mock only; genuine ordinary-route assembly requires root release.
  with patch.object(b,'_assemble_source',return_value=(self.raw,{'source_sha256':b.SOURCE_SHA256}))as gen:b.assemble(M/b.SOURCE,self.unit);b.assemble(M/b.SOURCE,self.unit);self.assertEqual(gen.call_count,2)
 def test_guard_all_open_APIs(self):
  with tempfile.TemporaryDirectory()as d:
   root=Path(d);src=root/'source.asm';src.write_bytes(b'x');scratch=root/'scratch';scratch.mkdir();forbidden=root/'reference.bin';forbidden.write_bytes(b'bad')
   with b.generation_guard(src,root,scratch)as events:
    self.assertEqual(src.read_bytes(),b'x');(scratch/'owned').write_bytes(b'ok')
    for fn in[lambda:forbidden.read_bytes(),lambda:builtins.open(forbidden,'rb'),lambda:io.open(forbidden,'rb'),lambda:os.open(forbidden,os.O_RDONLY)]:self.reject(fn)
    self.reject(src.write_bytes,b'changed');self.assertEqual(len(events['blocked']),5)
if __name__=='__main__':unittest.main()
