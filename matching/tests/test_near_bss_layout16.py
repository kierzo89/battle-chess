import unittest,copy,json
from pathlib import Path
from unittest.mock import patch
import near_bss_layout16 as bss
import near_bss_layout_model as model
from omf import read_omf
F=Path(__file__).resolve().parent/'fixtures/near_bss_layout190'
class NearBSSLayoutTests(unittest.TestCase):
 def raw(self):return(F/'native_near_bss190.OBJ').read_bytes()
 def test_real_whole_object(self):self.assertEqual(bss.inspect(self.raw())['physical_uninitialized_bytes'],30986)
 def test_render_source(self):self.assertEqual(bss.H(model.render(bss.spec())),bss.SOURCE_SHA256)
 def test_evidence(self):self.assertTrue(bss.validate_evidence()['private_C4_excluded'])
 def test_exact190_186(self):
  o=read_omf(self.raw());self.assertEqual(len(o.publics),190);self.assertEqual(len({(p.segment,p.offset)for p in o.publics.values()}),186)
 def test_group1_only(self):self.assertEqual({p.group for p in read_omf(self.raw()).publics.values()},{1})
 def test_no_initialized_records(self):self.assertFalse(any(k in (0xa0,0xa2,0xb0,0xb8)for k,a,p in read_omf(self.raw()).records))
 def test_no_code_or_fixups(self):
  o=read_omf(self.raw());self.assertFalse(o.fixups);self.assertFalse(any(s.class_name=='CODE'for s in o.segments.values()))
 def test_checksum_mutation(self):
  raw=bytearray(self.raw());raw[-1]^=1
  with self.assertRaises(Exception):bss.inspect(bytes(raw))
 def test_extra_record(self):
  with self.assertRaises(Exception):bss.inspect(self.raw()+bytes.fromhex('8802000076'))
 def test_omit_private4_not_shift(self):
  s=copy.deepcopy(bss.spec());s['early_bank'][0]-=4
  with self.assertRaises(Exception):model.validate(s)
 def test_no_capacity_reinterpretation(self):
  s=copy.deepcopy(bss.spec());s['PUBLICs'][0]['native_interval'][1]+=1
  with self.assertRaises(Exception):model.validate(s)
 def test_unproved_alias_rejected(self):
  s=copy.deepcopy(bss.spec());s['PUBLICs'][1]['native_DS']=s['PUBLICs'][0]['native_DS']
  with self.assertRaises(Exception):model.validate(s)
 def test_reserved_end_not_provider(self):
  s=copy.deepcopy(bss.spec());s['PUBLICs'][0]['symbol']='_end'
  with self.assertRaises(Exception):model.validate(s)
 def test_owned_evidence_tamper(self):
  real=Path.read_bytes
  def tampered(p):
   data=real(p)
   return data+b'x'if p.name.endswith('near142-and-clusters.json')else data
  with patch.object(Path,'read_bytes',tampered):
   with self.assertRaises(Exception):bss.validate_evidence()
