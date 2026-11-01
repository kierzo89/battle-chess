import unittest
from pathlib import Path
from dataclasses import replace
from omf import read_omf
from near_bss_layout_post16 import validate_client_frame
F=Path(__file__).resolve().parent/'fixtures/near_bss_layout190/mixed284.OBJ'
class BSSMixedFrameTests(unittest.TestCase):
 def fields(self):
  raw=F.read_bytes();o=read_omf(raw);return raw,[(f,o.externals[f.target[1]])for f in o.fixups if f.offset in (85,94,98,142)]
 def test_four_real_mixed_external_frames(self):
  raw,fields=self.fields();self.assertEqual(len(fields),4)
  for f,n in fields:self.assertEqual(validate_client_frame({'kind':'mixed-c-fa-authored-asm-whole-omf'},raw,f,n),'proven_MIXED284_external_PUBLIC_group1')
 def test_other_source_kind_rejected(self):
  raw,fields=self.fields()
  with self.assertRaises(Exception):validate_client_frame({'kind':'asm-whole-omf'},raw,*fields[0])
 def test_other_whole_object_rejected(self):
  raw,fields=self.fields()
  with self.assertRaises(Exception):validate_client_frame({'kind':'mixed-c-fa-authored-asm-whole-omf'},raw+b'x',*fields[0])
 def test_other_external_name_rejected(self):
  raw,fields=self.fields()
  with self.assertRaises(Exception):validate_client_frame({'kind':'mixed-c-fa-authored-asm-whole-omf'},raw,fields[0][0],'_fake')
 def test_unproved_other_F2_field_rejected(self):
  raw,fields=self.fields()
  with self.assertRaises(Exception):validate_client_frame({'kind':'mixed-c-fa-authored-asm-whole-omf'},raw,replace(fields[0][0],offset=86),fields[0][1])
 def test_old_wrong_F0_still_rejected(self):
  raw,fields=self.fields()
  with self.assertRaises(Exception):validate_client_frame({'kind':'mixed-c-fa-authored-asm-whole-omf'},raw,replace(fields[0][0],frame=(0,1)),fields[0][1])
