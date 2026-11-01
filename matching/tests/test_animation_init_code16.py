"""Focused closed animation backend tests; no genuine assembler invocation."""
from pathlib import Path
import sys,json,copy,dataclasses,unittest,tempfile,inspect,hashlib
from unittest.mock import patch
M=Path(__file__).resolve().parents[1];sys.path.insert(0,str(M))
import animation_init_code16 as b
import check
from omf import read_omf
from reference import build_reference
F=Path(__file__).parent/'fixtures/animation_init'
class AnimationInitTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.raw=(F/'actual.obj').read_bytes();cls.unit=json.loads((F/'unit.json').read_text());cls.obj=read_omf(cls.raw);cls.ref=build_reference((M.parent/'CHESS.EXE').read_bytes())
 def reject(self,fn,*args):
  with self.assertRaises((ValueError,KeyError)):fn(*args)
 def model_negative(self,edit):
  obj=copy.deepcopy(self.obj);edit(obj);self.reject(b.validate_object,obj)
 def test_adopted_modules(self):self.assertEqual(Path(b.__file__).resolve(),M/'animation_init_code16.py');self.assertEqual(Path(check.__file__).resolve(),M/'check.py')
 def test_closed_metadata(self):b.validate_unit(self.unit);u=copy.deepcopy(self.unit);u['size']=1082;self.reject(b.validate_unit,u)
 def test_complete_object(self):
  code,meta=b.extract_code(self.raw);self.assertEqual(len(code),1083);self.assertEqual((meta['actual_external_fields'],meta['actual_internal_fields']),(38,1));self.assertEqual(meta['DATA_segment']['length'],0)
 def test_first_actual_wrong_frame_object_rejected(self):self.reject(b.extract_code,(F/'wrong-frame.obj').read_bytes())
 def test_checksum(self):raw=bytearray(self.raw);raw[-1]^=1;self.reject(b.extract_code,bytes(raw))
 def test_source_exact_and_no_target_parameter(self):
  src=(M/b.SOURCE).read_bytes();b.source_policy(src);self.reject(b.source_policy,src+b'\nDB 0\n');self.assertEqual(list(inspect.signature(b._assemble_source).parameters),['source','project'])
 def test_no_hidden_allocation(self):self.model_negative(lambda o:setattr(o.segments[1],'length',2))
 def test_WORD_alignment_preserved(self):self.model_negative(lambda o:setattr(o.segments[2],'attributes',0x28))
 def test_CODE_tail_not_trimmed(self):self.model_negative(lambda o:setattr(o.segments[2],'length',1084))
 def test_no_extra_PUBLIC_alias(self):self.model_negative(lambda o:o.publics.__setitem__('_fake',dataclasses.replace(o.publics['_init_animation'],name='_fake')))
 def test_raw_record_inventory(self):self.model_negative(lambda o:o.records.append((0xb0,9999,b'\0')))
 def test_external_name_contract(self):self.model_negative(lambda o:o.externals.__setitem__(1,'_wrong_stream'))
 def test_near_DATA_member_frame_rejected(self):
  def edit(o):i=next(i for i,f in enumerate(o.fixups)if f.offset==128);o.fixups[i]=dataclasses.replace(o.fixups[i],frame=(0,1))
  self.model_negative(edit)
 def test_splash_DGROUP_frame_rejected(self):
  def edit(o):i=next(i for i,f in enumerate(o.fixups)if f.offset==203);o.fixups[i]=dataclasses.replace(o.fixups[i],frame=(1,1))
  self.model_negative(edit)
 def test_internal_relative_field_required(self):self.model_negative(lambda o:o.fixups.__setitem__(next(i for i,f in enumerate(o.fixups)if f.offset==939),dataclasses.replace(next(f for f in o.fixups if f.offset==939),displacement=70)))
 def test_internal_field_cannot_be_dropped(self):self.model_negative(lambda o:o.fixups.remove(next(f for f in o.fixups if f.offset==939)))
 def test_three_MZ_order_independent(self):self.assertEqual(b._sites(list(reversed(b.NATIVE_MZ))),b.NATIVE_MZ)
 def test_MZ_duplicates_and_missing_rejected(self):self.reject(b._sites,b.NATIVE_MZ+b.NATIVE_MZ[:1]);self.reject(b._sites,b.NATIVE_MZ[:-1])
 def test_real_evidence(self):self.assertEqual(b.validate_evidence(self.unit,M,b.ORIGINAL_SHA256,self.ref),json.loads((M/b.RAW_EVIDENCE).read_text())['evidence_id'])
 def test_evidence_tamper(self):
  old=Path.read_bytes;target=(M/b.RAW_EVIDENCE).resolve()
  def read(p,*a,**k):return b'{}'if Path(p).resolve()==target else old(p,*a,**k)
  with patch.object(Path,'read_bytes',read):self.reject(b.validate_evidence,self.unit,M,b.ORIGINAL_SHA256,self.ref)
 def test_whole_native_four_bases_and_no_C_credit(self):
  code,meta=b.extract_code(self.raw);built=b.Build(self.raw,code,meta,{});linked,proof=b.validate_comparison(self.unit,built,self.ref['image'],M,self.ref['relocations']);self.assertEqual(linked,self.ref['image'][b.BASE:b.BASE+b.SIZE]);self.assertEqual(len(proof['relocations']),39);self.assertEqual(len(proof['four_load_bases']),4);self.assertEqual(proof['authored_c_function_credit'],0);self.assertTrue(proof['WORD_neighbor_join_held'])
 def test_ordinary_checker_metadata_dispatch(self):self.assertEqual(check.validate_rea_extent(self.unit,M,b.ORIGINAL_SHA256,self.ref),b.validate_evidence(self.unit,M,b.ORIGINAL_SHA256,self.ref))
 def test_mock_routing_requests_generator_each_time(self):
  # Explicit route mock, not actual source-generation proof or a cache fixture.
  with tempfile.TemporaryDirectory()as d:
   p=Path(d);src=p/b.SOURCE;src.parent.mkdir(parents=True);src.write_bytes((M/b.SOURCE).read_bytes())
   with patch.object(b,'_assemble_source',return_value=(self.raw,{'source_sha256':b.SOURCE_SHA256}))as gen:
    a=b.assemble(src,p);c=b.assemble(src,p);self.assertEqual(a.object_bytes,c.object_bytes);self.assertEqual(gen.call_count,2)
if __name__=='__main__':unittest.main()
