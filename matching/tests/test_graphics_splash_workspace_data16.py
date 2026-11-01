from pathlib import Path
import unittest,json,sys,copy
D=Path(__file__).resolve().parent;M=next(p for p in D.parents if(p/'config/msc500.json').is_file());sys.dont_write_bytecode=True;sys.path[:0]=[str(D),str(M)]
import graphics_splash_workspace_data16 as b
from graphics_splash_workspace_zero_omf16 import DataError
from reference import build_reference,validate_expanded_read
class GraphicsSplashWorkspaceDataTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.u=json.loads((M/'tests/fixtures/graphics_splash_workspace/unit.json').read_text());cls.raw=(M/'tests/fixtures/graphics_splash_workspace/actual.obj').read_bytes();cls.e=json.loads((M/'evidence/rea_graphics_workspace_86000.json').read_text());cls.ref=build_reference((M.parent/'CHESS.EXE').read_bytes())
 def bad_unit(self,key,value):
  u=copy.deepcopy(self.u);u[key]=value
  with self.assertRaises(DataError):b.validate_unit(u)
 def test_complete_two_segment_actual_object(self):
  data,meta=b.extract_data(self.raw);self.assertEqual(len(data),86000);self.assertEqual(data,self.ref['image'][0x120d0:0x270c0]);self.assertEqual([x['length']for x in meta['segments']],[53184,32816]);self.assertEqual(meta['fixups'],0)
 def test_real_splash_segment_view_and_original_extent(self):
  _,meta=b.extract_data(self.raw);self.assertEqual(meta['publics']['_splash_buffer']['segment'],2);self.assertEqual(meta['publics']['_splash_buffer']['offset'],0);self.assertEqual(0x120d0+53184,0x1f090)
 def test_actual_complete_REA_evidence(self):
  data,_=b.extract_data(self.raw);self.assertEqual(validate_expanded_read(self.e,self.u,data,self.ref,emitted_mz_sites=[]),self.e['evidence_id'])
 def test_no_C_or_capacity_credit(self):
  _,meta=b.extract_data(self.raw);self.assertEqual(meta['C_functions'],0);self.assertEqual(meta['C_DATA'],0);self.assertFalse(meta['historical_C_capacity_proven']);self.assertFalse(meta['original_global_MAP_proven'])
 def test_exact_metadata_accepts(self):b.validate_unit(self.u)
 def test_source_bytes_are_pinned(self):self.bad_unit('source_sha256','0'*64)
 def test_tool_bytes_are_pinned(self):self.bad_unit('assembler_sha256','0'*64)
 def test_foreign_backend_rejected(self):self.bad_unit('backend','nasm-data-omf')
 def test_partial_span_rejected(self):self.bad_unit('size',65520)
 def test_larger_span_rejected(self):self.bad_unit('size',86001)
 def test_wrong_origin_rejected(self):self.bad_unit('image_offset','0x120c2')
 def test_extra_alias_rejected(self):self.bad_unit('symbols',self.u['symbols']+['_screen_view'])
 def test_wrong_public_order_rejected(self):self.bad_unit('symbols',list(reversed(self.u['symbols'])))
 def test_other_reference_region_rejected(self):self.bad_unit('reference_region','unchanged-prefix')
 def test_other_source_path_rejected(self):self.bad_unit('source','src/guessed_array.c')
 def test_invented_C_capacity_key_rejected(self):self.bad_unit('C_capacity',86000)
 def test_truncated_object_rejected(self):
  with self.assertRaises(DataError):b.extract_data(self.raw[:-1])
 def test_unknown_complete_record_rejected(self):
  payload=b'\0';header=b'\xff\2\0'+payload;record=header+bytes([-sum(header)%256])
  with self.assertRaises(DataError):b.extract_data(self.raw+record)
 def test_incomplete_REA_read_rejected(self):
  e=copy.deepcopy(self.e);e['normalized_result']['complete']=False
  with self.assertRaises(ValueError):validate_expanded_read(e,self.u,bytes(86000),self.ref,emitted_mz_sites=[])
 def test_wrong_REA_target_rejected(self):
  e=copy.deepcopy(self.e);e['subject']['digest']['sha256']='0'*64
  with self.assertRaises(ValueError):validate_expanded_read(e,self.u,bytes(86000),self.ref,emitted_mz_sites=[])
 def test_fabricated_internal_relocation_rejected(self):
  with self.assertRaises(ValueError):validate_expanded_read(self.e,self.u,bytes(86000),self.ref,emitted_mz_sites=[0x120d0])
if __name__=='__main__':unittest.main(verbosity=2)
