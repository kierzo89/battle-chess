"""Prepared target-free hardgate controls; no compiler, native credit or LINK."""
from pathlib import Path
import copy,json,os,sys,unittest
M=Path(os.environ.get('BC_COUNTS_PROFILE_PROJECT',Path(__file__).resolve().parents[1])).resolve();sys.path[:0]=[str(M)];sys.dont_write_bytecode=True
from omf import read_omf
import owned_editor_ready9856_literal_const16 as old
import owned_editor_side_counts_literal_const16 as new
F=Path(__file__).resolve().parent/'fixtures/side_piece_counts';OLD=read_omf((F/'editor-old.obj').read_bytes());NEW=read_omf((F/'editor-new.obj').read_bytes());BEFORE=json.loads((F/'editor-old-metadata.json').read_text());AFTER=json.loads((F/'editor-new-metadata.json').read_text())
class EditorSideCountsHardgateTests(unittest.TestCase):
 def owners(self,rows):return[u for u in rows if u.get('owned_const')]
 def test_old_gate_old_actual_object(self):
  for u in self.owners(BEFORE):self.assertEqual(len(old.validate_layout(u,OLD)[1]),264)
 def test_new_gate_new_actual_object(self):
  for u in self.owners(AFTER):self.assertEqual(len(new.validate_layout(u,NEW)[1]),264)
 def test_old_gate_rejects_actual_new_object(self):
  for u in self.owners(BEFORE):
   with self.assertRaisesRegex(ValueError,'whole genuine OMF'):old.validate_layout(u,NEW)
 def test_new_gate_rejects_actual_old_object(self):
  for u in self.owners(AFTER):
   with self.assertRaisesRegex(ValueError,'whole genuine OMF'):new.validate_layout(u,OLD)
 def test_new_gate_rejects_old_profile_kind(self):
  with self.assertRaises(ValueError):new.validate_layout(self.owners(BEFORE)[0],NEW)
 def test_changed_binding_rejected(self):
  u=copy.deepcopy(self.owners(AFTER)[0]);u['externals']['_side_piece_counts']+=2
  with self.assertRaisesRegex(ValueError,'metadata mismatch'):new.validate_layout(u,NEW)
 def test_parsed_alias_rewrite_rejected(self):
  o=copy.deepcopy(NEW);key=next(k for k,v in o.externals.items()if v=='_side_piece_counts');o.externals[key]='_counts'
  with self.assertRaisesRegex(ValueError,'parsed-record congruence'):new.validate_layout(self.owners(AFTER)[0],o)
if __name__=='__main__':unittest.main()
