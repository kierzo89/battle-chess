import unittest,hashlib,json
from pathlib import Path
import graphics_screen_view_workspace_data16 as b
from graphics_screen_view_zero_omf16 import validate_obj,DataError
class SixView(unittest.TestCase):
 def setUp(self):self.raw=(Path(__file__).parent/'fixtures/graphics_screen_view/actual.obj').read_bytes()
 def test_whole(self):
  data,meta=b.extract_data(self.raw);self.assertEqual(data,bytes(86000));self.assertEqual(meta['expanded_bytes'],86000)
 def test_old_gate_rejects_six(self):
  from graphics_buffer_views_zero_omf16 import validate_obj as old
  with self.assertRaises(ValueError):old(self.raw)
 def test_new_gate_rejects_old(self):
  with self.assertRaises(DataError):validate_obj((Path(__file__).parent/'fixtures/graphics_screen_view/old-five.obj').read_bytes())
 def test_source(self):b.source_policy((b.M/b.SOURCE).read_bytes())
 def test_source_extra(self):
  with self.assertRaises(DataError):b.source_policy((b.M/b.SOURCE).read_bytes()+b'\nDB 0\n')
 def test_metadata(self):b.validate_unit(b._profile()['unit'])
 def test_metadata_extra(self):
  u=dict(b._profile()['unit'],size=86001)
  with self.assertRaises(DataError):b.validate_unit(u)
 def test_checksum(self):
  v=bytearray(self.raw);v[240]^=1
  with self.assertRaises(DataError):validate_obj(bytes(v))
 def mutate(self,at,replacement):
  v=bytearray(self.raw);n=int.from_bytes(v[at+1:at+3],'little');v[at+3:at+3+n-1]=replacement;v[at+2+n]=(-sum(v[at:at+2+n]))&255;return bytes(v)
 def test_nonzero(self):
  x=bytearray(self.raw[234:247]);x[-1]=1
  with self.assertRaises(DataError):validate_obj(self.mutate(231,x))
 def test_wrong_view(self):
  x=bytearray(self.raw[203:223]);x[-3]^=1
  with self.assertRaises(DataError):validate_obj(self.mutate(200,x))
 def test_extra_module(self):
  with self.assertRaises(DataError):validate_obj(self.raw+self.raw)
 def test_truncation(self):
  with self.assertRaises(DataError):validate_obj(self.raw[:-1])

 def test_full_evidence_preflight(self):
  from reference import build_reference,ORIGINAL_SHA256
  reference=build_reference(Path('/home/kierzo/chess/CHESS.EXE').read_bytes())
  result=b.validate_evidence(b._profile()['unit'],b.M,ORIGINAL_SHA256,reference)
  self.assertTrue(result)
