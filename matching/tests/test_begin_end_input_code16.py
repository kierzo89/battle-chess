"""Prepared component controls: no MASM/C5/LINK; adopted-module routing, exact OMF/evidence and source-only denial boundaries."""
from pathlib import Path
import sys,json,copy,dataclasses,unittest,tempfile,inspect,builtins,io,os
from unittest.mock import patch
M=Path(__file__).resolve().parents[1];sys.path.insert(0,str(M))
import begin_end_input_code16 as b
import check
from omf import read_omf
from reference import build_reference
F=Path(__file__).parent/'fixtures/begin_end_input'
class BeginEndInputTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.raw=(F/'actual.obj').read_bytes();cls.unit=json.loads((F/'unit.json').read_text());cls.obj=read_omf(cls.raw);cls.ref=build_reference((M.parent/'CHESS.EXE').read_bytes())
 def reject(self,fn,*args):
  with self.assertRaises((ValueError,KeyError)):fn(*args)
 def model_negative(self,edit):
  obj=copy.deepcopy(self.obj);edit(obj);self.reject(b.validate_object,obj)
 def test_adopted_modules(self):self.assertEqual(Path(b.__file__).resolve(),M/'begin_end_input_code16.py');self.assertEqual(Path(check.__file__).resolve(),M/'check.py')
 def test_exact_unit(self):b.validate_unit(self.unit);u=copy.deepcopy(self.unit);u['size']=179;self.reject(b.validate_unit,u)
 def test_no_unregistered_metadata(self):u=copy.deepcopy(self.unit);u['capacity']=180;self.reject(b.validate_unit,u)
 def test_whole_object(self):
  code,meta=b.extract_code(self.raw);self.assertEqual(len(code),180);self.assertEqual((meta['actual_DGROUP_fields'],meta['actual_near_CALL_fields']),(28,6));self.assertEqual(meta['native_MZ'],[]);self.assertEqual(meta['DATA_segment']['length'],0)
 def test_checksum(self):raw=bytearray(self.raw);raw[-1]^=1;self.reject(b.extract_code,bytes(raw))
 def test_source_pin_and_directives(self):src=(M/b.SOURCE).read_bytes();b.source_policy(src);self.reject(b.source_policy,src+b'\nDB 0\n')
 def test_generation_has_no_reference_argument(self):self.assertEqual(list(inspect.signature(b._assemble_source).parameters),['source','project'])
 def test_no_DATA_allocation(self):self.model_negative(lambda o:setattr(o.segments[1],'length',1))
 def test_WORD_preserved(self):self.model_negative(lambda o:setattr(o.segments[2],'attributes',0x28))
 def test_no_crop_or_tail(self):self.model_negative(lambda o:setattr(o.segments[2],'length',179))
 def test_no_public_alias(self):self.model_negative(lambda o:o.publics.__setitem__('_fake',dataclasses.replace(next(iter(o.publics.values())),name='_fake')))
 def test_odd_end_entry125(self):self.assertEqual(self.obj.publics['_end_input_102d'].offset,125);self.model_negative(lambda o:o.publics.__setitem__('_end_input_102d',dataclasses.replace(o.publics['_end_input_102d'],offset=126)))
 def test_all_raw_records_accounted(self):self.model_negative(lambda o:o.records.append((0xb0,9999,b'\0')))
 def test_no_external_alias(self):self.model_negative(lambda o:o.externals.__setitem__(1,'_different'))
 def test_DGROUP_cannot_be_empty_DATA_frame(self):
  def edit(o):i=next(i for i,f in enumerate(o.fixups)if f.segment_relative);o.fixups[i]=dataclasses.replace(o.fixups[i],frame=(0,1))
  self.model_negative(edit)
 def test_CALL_cannot_be_segment_relative(self):
  def edit(o):i=next(i for i,f in enumerate(o.fixups)if not f.segment_relative);o.fixups[i]=dataclasses.replace(o.fixups[i],segment_relative=True)
  self.model_negative(edit)
 def test_fixup_displacement_exact(self):self.model_negative(lambda o:o.fixups.__setitem__(0,dataclasses.replace(o.fixups[0],displacement=1)))
 def test_no_field_drop(self):self.model_negative(lambda o:o.fixups.pop())
 def test_zero_MZ_including_boundary(self):self.assertEqual(b._sites(self.ref['relocations']),[]);self.reject(b._sites,[b.BASE-1]);self.reject(b._sites,[b.BASE+179])
 def test_qualified_evidence(self):self.assertEqual(b.validate_evidence(self.unit,M,b.ORIGINAL_SHA256,self.ref),json.loads((M/b.RAW_EVIDENCE).read_text())['evidence_id'])
 def test_evidence_tamper(self):
  old=Path.read_bytes;target=(M/b.RAW_EVIDENCE).resolve()
  def read(p,*a,**kw):return b'{}'if Path(p).resolve()==target else old(p,*a,**kw)
  with patch.object(Path,'read_bytes',read):self.reject(b.validate_evidence,self.unit,M,b.ORIGINAL_SHA256,self.ref)
 def test_whole_native_fourbases_zeroC(self):
  code,meta=b.extract_code(self.raw);built=b.Build(self.raw,code,meta,{});linked,proof=b.validate_comparison(self.unit,built,self.ref['image'],M,self.ref['relocations']);self.assertEqual(len(linked),180);self.assertEqual(len(proof['relocations']),34);self.assertEqual(len(proof['four_load_bases']),4);self.assertEqual(proof['authored_c_function_credit'],0);self.assertEqual(proof['authored_asm_function_credit'],0);self.assertEqual(len(proof['unprovided_saved_BYTE']),4)
 def test_checker_evidence_dispatch(self):self.assertEqual(check.validate_rea_extent(self.unit,M,b.ORIGINAL_SHA256,self.ref),b.validate_evidence(self.unit,M,b.ORIGINAL_SHA256,self.ref))
 def test_ordinary_route_fresh_requests(self):
  # Two mocked calls verify routing only. Fixture is never a real generation cache.
  with tempfile.TemporaryDirectory()as d:
   p=Path(d);src=p/b.SOURCE;src.parent.mkdir(parents=True);src.write_bytes((M/b.SOURCE).read_bytes())
   with patch.object(b,'_assemble_source',return_value=(self.raw,{}))as gen:b.assemble(src,p);b.assemble(src,p);self.assertEqual(gen.call_count,2)
 def test_source_only_guard_all_open_APIs(self):
  with tempfile.TemporaryDirectory()as d:
   root=Path(d);source=root/'source.asm';source.write_bytes(b'source');scratch=root/'scratch';scratch.mkdir();forbidden=root/'old.obj';forbidden.write_bytes(b'old')
   with b.generation_guard(source,root,scratch)as events:
    self.assertEqual(source.read_bytes(),b'source');(scratch/'owned.txt').write_bytes(b'ok')
    for read in[lambda:forbidden.read_bytes(),lambda:builtins.open(forbidden,'rb'),lambda:io.open(forbidden,'rb'),lambda:os.open(forbidden,os.O_RDONLY)]:self.reject(read)
    self.reject(source.write_bytes,b'changed');self.assertEqual(len(events['blocked']),5)
 def test_guard_reference_and_output_denial(self):
  with tempfile.TemporaryDirectory()as d:
   root=Path(d);scratch=root/'scratch';scratch.mkdir();source=root/'source.asm';source.write_bytes(b'x')
   with b.generation_guard(source,root,scratch):
    for name in['CHESS.EXE','build/exepack/TRIM5_UNPACK.EXE','build/native.bin','old.obj','outside-write.txt']:
     self.reject((root/name).read_bytes);self.reject((root/name).write_bytes,b'bad')
if __name__=='__main__':unittest.main()
