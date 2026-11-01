import unittest,copy,json
from pathlib import Path
from dataclasses import replace
from omf import read_omf
import serial248_code16 as old
import serial248_dgroup_code16 as new
import serial_code16 as route
F=Path(__file__).resolve().parent/'fixtures/serial248_dgroup'
class SerialDGROUPTests(unittest.TestCase):
 def obj(self):return read_omf((F/'serial248-DGROUP.OBJ').read_bytes())
 def reject(self,o):
  with self.assertRaises(Exception):new.extract_code(o)
 def test_positive(self):self.assertEqual(len(new.extract_code(self.obj())[0]),248)
 def test_old_gate_unchanged(self):self.assertEqual(len(old.extract_code(read_omf((F/'serial248-original-F0.OBJ').read_bytes()))[0]),248)
 def test_old_F0_rejected_new_gate(self):self.reject(read_omf((F/'serial248-original-F0.OBJ').read_bytes()))
 def test_both_routes(self):
  for name in ['serial248-original-F0.OBJ','serial248-DGROUP.OBJ']:self.assertEqual(len(route.extract_code(read_omf((F/name).read_bytes()))[0]),248)
 def test_no_CODE_change(self):self.assertEqual(new.extract_code(self.obj())[0],old.extract_code(read_omf((F/'serial248-original-F0.OBJ').read_bytes()))[0])
 def test_wrong_frame(self):
  o=self.obj();i=next(i for i,f in enumerate(o.fixups)if f.offset==150);o.fixups[i]=replace(o.fixups[i],frame=(0,1));self.reject(o)
 def test_wrong_target(self):
  o=self.obj();o.fixups[0]=replace(o.fixups[0],target=(2,1));self.reject(o)
 def test_missing_field(self):
  o=self.obj();o.fixups.pop();self.reject(o)
 def test_extra_PUBLIC(self):
  o=self.obj();o.publics['_fake']=replace(next(iter(o.publics.values())),name='_fake');self.reject(o)
 def test_extra_record(self):
  o=self.obj();o.records.append((0x88,99999,b'x'));self.reject(o)
 def test_CODE_tail(self):
  o=self.obj();at,b=o.segments[2].chunks[-1];o.segments[2].chunks[-1]=(at,b[:-1]);self.reject(o)
 def test_DATA_allocation(self):
  o=self.obj();o.segments[1].length=1;self.reject(o)
