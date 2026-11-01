import unittest,copy
from pathlib import Path
import near_game_code16 as b
from omf import read_omf
class NearGame(unittest.TestCase):
 def setUp(self):
  self.key='decode_frame_directory289';self.s=b.spec(self.key);self.u=copy.deepcopy(self.s['unit']);self.raw=(Path(__file__).parent/'fixtures/near_game/decode_directory289.obj').read_bytes()
 def test_extract(self):self.assertEqual(len(b.extract_code(self.raw,self.key)[0]),289)
 def test_unit(self):b.validate_unit(self.u)
 def test_unknown_profile(self):
  with self.assertRaises(ValueError):b.spec('unknown')
 def test_unit_extent(self):
  self.u['size']=290
  with self.assertRaises(ValueError):b.validate_unit(self.u)
 def test_unit_symbol(self):
  self.u['public_symbols']=['_fake']
  with self.assertRaises(ValueError):b.validate_unit(self.u)
 def test_unit_native_binding(self):
  self.u['externals']['_huff_decode_stream']+=1
  with self.assertRaises(ValueError):b.validate_unit(self.u)
 def test_source(self):b.source_policy((Path(b.__file__).parent/self.u['source']).read_bytes(),self.u['source'])
 def test_source_extra(self):
  with self.assertRaises(ValueError):b.source_policy((Path(b.__file__).parent/self.u['source']).read_bytes()+b'\nNOP\n',self.u['source'])
 def test_object_change(self):
  r=bytearray(self.raw);r[-1]^=1
  with self.assertRaises(ValueError):b.extract_code(bytes(r),self.key)
 def test_rawrecords_change(self):
  o=read_omf(self.raw);o.records=o.records[:-1]
  with self.assertRaises(ValueError):b.validate_object(o,self.key)
 def test_field_change(self):
  o=read_omf(self.raw);o.fixups=o.fixups[:-1]
  with self.assertRaises(ValueError):b.validate_object(o,self.key)
 def test_coverage_change(self):
  o=read_omf(self.raw);o.segments[2].chunks=[]
  with self.assertRaises(ValueError):b.validate_object(o,self.key)
 def test_full_native_evidence(self):
  from reference import build_reference,ORIGINAL_SHA256
  p=Path(b.__file__).parent;r=build_reference(Path('/home/kierzo/chess/CHESS.EXE').read_bytes());self.assertTrue(b.validate_evidence(self.u,p,ORIGINAL_SHA256,r))
 def test_fourbases(self):
  from reference import build_reference
  r=build_reference(Path('/home/kierzo/chess/CHESS.EXE').read_bytes())
  for load in [0,1,4096,65535]:
   code,fields=b.link_code(self.raw,self.key,load);self.assertEqual(code,r['image'][0x2d13:0x2e34]);self.assertEqual(len(fields),15)
 def test_loadrange(self):
  with self.assertRaises(ValueError):b.link_code(self.raw,self.key,65536)
