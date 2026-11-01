"""Three actual whole C5 DATA fixtures; no generation or fabricated positive objects."""
from pathlib import Path
import json,hashlib,unittest
from dataclasses import replace
from omf import read_omf
from cdata import extract_data
from reference import build_reference
class ResetDATA45(unittest.TestCase):
 def each(self):
  P=Path(__file__).parent/'fixtures/near_game';meta=json.loads((P/'reset_DATA45-fixtures.json').read_text())
  for role,s in meta.items():yield role,s,(P/(role+'.obj')).read_bytes()
 def test_actual_whole_DATA_and_PUBLIC(self):
  for role,s,r in self.each():
   self.assertEqual(hashlib.sha256(r).hexdigest(),s['object_sha256']);o=read_omf(r);data,_=extract_data(o,s['symbol']);self.assertEqual(len(data),s['size']);self.assertEqual(set(o.publics),{s['symbol']});self.assertEqual(o.publics[s['symbol']].type_index,s['actual_PUBLIC']['type_index'])
 def test_complete_actual_TYPE_stream(self):
  for role,s,r in self.each():
   o=read_omf(r);tb=bytearray(o.segments[6].length)
   for at,b in o.segments[6].chunks:tb[at:at+len(b)]=b
   at=0;k=512;nodes={}
   while at<len(tb):
    self.assertEqual(tb[at],1);n=int.from_bytes(tb[at+1:at+3],'little');nodes[hex(k)]=tb[at+3:at+3+n].hex();at+=3+n;k+=1
   self.assertEqual(nodes,s['actual_TYPE'])
 def test_no_extra_allocation_or_FIXUP(self):
  for role,s,r in self.each():
   o=read_omf(r);self.assertFalse(o.fixups);self.assertFalse(o.procedures);self.assertTrue(all(v.length==0 for i,v in o.segments.items()if i not in[2,6]));self.assertFalse([k for k,at,p in o.records if k in[0xb0,0xb8]])
 def test_complete_primary_and_native_bytes(self):
  ref=build_reference(Path('/home/kierzo/chess/CHESS.EXE').read_bytes());P=Path(__file__).resolve().parent.parent
  for role,s,r in self.each():
   data,_=extract_data(read_omf(r),s['symbol']);self.assertEqual(data,ref['image'][s['image']:s['image']+s['size']]);q=json.loads((P/s['primary']).read_text())['normalized_result'];self.assertTrue(q['complete']);self.assertEqual(q['returned_bytes'],s['size']);self.assertEqual(bytes.fromhex(q['bytes_hex']),data)
 def test_first_NUL_excludes_padding(self):
  for role,s,r in self.each():
   data,_=extract_data(read_omf(r),s['symbol'])
   if role!='editormap7':self.assertEqual(data.index(0),s['size']-1)
 def test_editor_inverse_on_valid0_through6(self):
  for role,s,r in self.each():
   if role=='editormap7':
    data,_=extract_data(read_omf(r),s['symbol']);kind=[0,2,5,6,1,3,4];self.assertEqual([data[k]for k in kind],list(range(7)))
 def test_wrong_symbol_rejected(self):
  for role,s,r in self.each():
   with self.assertRaises(ValueError):extract_data(read_omf(r),'_alias')
 def test_checksum_rejected(self):
  for role,s,r in self.each():
   with self.assertRaises(ValueError):read_omf(r[:-1]+bytes([r[-1]^1]))
 def test_truncation_rejected(self):
  for role,s,r in self.each():
   with self.assertRaises(ValueError):read_omf(r[:-1])
 def test_no_CODE_native_MZ(self):
  ref=build_reference(Path('/home/kierzo/chess/CHESS.EXE').read_bytes())
  for role,s,r in self.each():self.assertFalse([p for p in ref['relocations']if max(p,s['image'])<min(p+2,s['image']+s['size'])])
