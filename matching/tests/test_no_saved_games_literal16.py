"""Actual literal16 fixture, generic DATA extraction and owned evidence only; no generation."""
from pathlib import Path
import json,unittest
from cdata import extract_data
from omf import read_omf
from reference import build_reference
class Literal16(unittest.TestCase):
 def fixture(self):return(Path(__file__).parent/'fixtures/near_game/no_saved_games515c.obj').read_bytes()
 def test_actual_complete_DATA16(self):
  o=read_omf(self.fixture());data,m=extract_data(o,'_no_saved_games');self.assertEqual(data,b'No games saved.\0');self.assertEqual(o.publics['_no_saved_games'].type_index,0x205)
 def test_no_extra_loaded_allocation(self):
  o=read_omf(self.fixture());self.assertEqual(o.segments[2].length,16);self.assertFalse(o.fixups);self.assertFalse(o.procedures);self.assertTrue(all(s.length==0 for s in o.segments.values()if s.index not in[2,6]))
 def test_exact_public_no_alias(self):
  o=read_omf(self.fixture());self.assertEqual(set(o.publics),{'_no_saved_games'});p=o.publics['_no_saved_games'];self.assertEqual((p.group,p.segment,p.offset),(1,2,0))
 def test_complete_primary_and_first_NUL(self):
  P=Path(__file__).resolve().parent.parent;ev=json.loads((P/'evidence/readonly_messages/no_saved_games515c.json').read_text());data,_=extract_data(read_omf(self.fixture()),'_no_saved_games');n=ev['normalized_result'];self.assertEqual(n['returned_bytes'],16);self.assertTrue(n['complete']);self.assertEqual(bytes.fromhex(n['bytes_hex']),data);self.assertEqual(data.index(0),15)
 def test_whole_original_literal_no_MZ(self):
  ref=build_reference(Path('/home/kierzo/chess/CHESS.EXE').read_bytes());data,_=extract_data(read_omf(self.fixture()),'_no_saved_games');self.assertEqual(ref['image'][0x61d7c:0x61d8c],data);self.assertFalse([x for x in ref['relocations']if 0x61d7b<=x<0x61d8c])
 def test_truncation_rejected(self):
  with self.assertRaises(ValueError):read_omf(self.fixture()[:-1])
 def test_checksum_rejected(self):
  r=self.fixture()
  with self.assertRaises(ValueError):read_omf(r[:-1]+bytes([r[-1]^1]))
 def test_wrong_symbol_rejected(self):
  with self.assertRaises(ValueError):extract_data(read_omf(self.fixture()),'_alias')
