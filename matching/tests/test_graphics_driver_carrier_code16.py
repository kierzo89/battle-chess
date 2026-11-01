from pathlib import Path
import copy,hashlib,json,unittest
from unittest.mock import patch
import graphics_driver_carrier_code16 as b
from graphics_driver_carrier_omf16 import CarrierError
P=Path(__file__).resolve().parents[1]
FIXTURE=P/'tests/fixtures/graphics_driver_carrier/UNIT.OBJ'
def altered(raw,kind,index,value):
 out=bytearray(raw);p=0
 while out[p]!=kind:p+=3+int.from_bytes(out[p+1:p+3],'little')
 n=int.from_bytes(out[p+1:p+3],'little');out[p+3+index]=value;out[p+2+n]=(-sum(out[p:p+2+n]))&255;return bytes(out)
class DriverCarrierTests(unittest.TestCase):
 def setUp(self):self.raw=FIXTURE.read_bytes()
 def test_actual_whole_object_and_mixed_accounting(self):
  code,m=b.extract_code(self.raw);self.assertEqual(len(code),3616);self.assertEqual(code[:12].hex(),'e91a0ee9170ee9140ee9110e');self.assertEqual(code[12:],bytes(3604));self.assertEqual(m['mnemonic_bytes'],12);self.assertEqual(m['physical_zero_DATA_bytes'],3604);self.assertEqual(m['procedures'],0);self.assertEqual(m['C_credit'],0)
 def test_exact_five_publics_and_four_real_fixups(self):
  _,m=b.extract_code(self.raw);self.assertEqual({k:v['offset']for k,v in m['publics'].items()},b.PUBLICS);self.assertEqual(m['internal_fixups'],4);self.assertEqual(m['internal_MZ'],[])
 def test_fixup_must_be_self_relative(self):
  with self.assertRaises(CarrierError):b.extract_code(altered(self.raw,0x9c,0,0xc4))
 def test_fixup_offset_must_own_real_instruction_operand(self):
  with self.assertRaises(CarrierError):b.extract_code(altered(self.raw,0x9c,1,2))
 def test_fixup_frame_cannot_change(self):
  with self.assertRaises(CarrierError):b.extract_code(altered(self.raw,0x9c,3,2))
 def test_fixup_target_cannot_change(self):
  with self.assertRaises(CarrierError):b.extract_code(altered(self.raw,0x9c,4,2))
 def test_private_landing_cannot_change(self):
  with self.assertRaises(CarrierError):b.extract_code(altered(self.raw,0x9c,5,0x1e))
 def test_initialized_tail_cannot_be_nonzero(self):
  with self.assertRaises(CarrierError):b.extract_code(altered(self.raw,0xa2,8,1))
 def test_segment_cannot_be_byte_aligned(self):
  with self.assertRaises(CarrierError):b.extract_code(altered(self.raw,0x98,0,0x20))
 def test_segment_capacity_cannot_expand(self):
  with self.assertRaises(CarrierError):b.extract_code(altered(self.raw,0x98,1,0x21))
 def test_checksum_corruption_rejected(self):
  x=bytearray(self.raw);x[-1]^=1
  with self.assertRaises(CarrierError):b.extract_code(bytes(x))
 def test_changed_source_rejected_before_MASM(self):
  import tempfile
  with tempfile.TemporaryDirectory()as t:
   p=Path(t)/'source.asm';p.write_text('nop\n')
   with patch.object(b.subprocess,'run',side_effect=AssertionError('assembler must not run')):
    with self.assertRaises(CarrierError):b._assemble_source(p,Path(t))
if __name__=='__main__':unittest.main()
