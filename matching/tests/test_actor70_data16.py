"""Exact typed Actor70 DATA, real LIDATA coverage and unchanged generic rejection."""
from pathlib import Path
import unittest,copy,json,hashlib
import actor70_data16 as a
from omf import read_omf,OMFError
from cdata import extract_data
from runtime_lidata16 import initialized_view,POLICY,decode_blocks
T=Path(__file__).with_name('fixtures')/'actor70_data16'
class ActorDataTests(unittest.TestCase):
 def setUp(self):self.raw=(T/'actor.obj').read_bytes();self.unit=json.loads((T/'unit.json').read_text())
 def test_complete_real_typed_DATA(self):
  data,p=a.validate_raw(self.raw);self.assertEqual(len(data),1960);self.assertEqual((p['literal_bytes'],p['iterated_bytes'],p['hole_fill_bytes']),(2,1958,0));self.assertEqual(p['field_offsets'],[0,2,4,6,8,10,11,12,14,16,18,20,22,26]);self.assertEqual([q['pointer_class']for q in p['pointer_graph']],[0x74,0x73,0x74]);self.assertEqual((p['ARRAY_bits'],p['STRUCT_bits']),(15680,224))
 def test_readonly_view(self):
  o=read_omf(self.raw);before=repr(o);v=initialized_view(o,2,policy=POLICY);self.assertEqual(repr(o),before);self.assertEqual(v.iterated_ranges,((2,1960),));self.assertEqual(o.segments[2].chunks,[(0,b'\0\0')])
 def test_generic_DATA_still_forbids(self):
  with self.assertRaisesRegex(OMFError,'LIDATA'):extract_data(read_omf(self.raw),'_actors')
 def test_unit_exact(self):a.validate_unit(self.unit)
 def test_capacity_change(self):
  u=copy.deepcopy(self.unit);u['size']=1959
  with self.assertRaises(a.ActorDataError):a.validate_unit(u)
 def test_no_extra_alias(self):
  u=copy.deepcopy(self.unit);u['externals']={'_alternate_actors':1504}
  with self.assertRaises(a.ActorDataError):a.validate_unit(u)
 def test_source_hash(self):self.assertEqual(hashlib.sha256((T/'actors_05e0.c').read_bytes()).hexdigest(),a.PROFILE['source_sha256'])
 def test_profile_actual_dtype(self):
  _,p=a.validate_raw(self.raw);self.assertEqual(p['field_types'][:11],[0x81]*5+[0x84]*2+[0x81]*4);self.assertEqual(p['field_names'][-3:],['frame','resource','next'])
 def test_decoder_bound(self):
  with self.assertRaises(ValueError):decode_blocks(bytes.fromhex('d3030000020000'),limit=1957)
 def test_decoder_truncated(self):
  with self.assertRaises(ValueError):decode_blocks(bytes.fromhex('d30300000200'),limit=1958)
 def test_decode_encoded_count(self):
  b,t=decode_blocks(bytes.fromhex('d3030000020000'),limit=1958);self.assertEqual(len(b),1958);self.assertEqual(t[0]['repeat'],979)
 def test_coverage_gap(self):
  o=read_omf(self.raw);o.records=[(k,at,(p[:3]+bytes.fromhex('d2030000020000'))if k==0xa2 else p)for k,at,p in o.records]
  with self.assertRaisesRegex(ValueError,'incomplete'):initialized_view(o,2,policy=POLICY)
 def test_overlap(self):
  o=read_omf(self.raw);o.records.append((0xa0,999,b'\x02\x01\0\0'))
  with self.assertRaisesRegex(ValueError,'overlap'):initialized_view(o,2,policy=POLICY)
 def test_extra_allocation_record(self):
  with self.assertRaises(a.ActorDataError):a.validate_raw(self.raw+b'\x88\x01\0\x77')
 def test_public_type_or_member_offset_tamper(self):
  # A wellformed changed TYPE body/checksum is still not the admitted genuine object.
  b=bytearray(self.raw);b[400]^=1;n=int.from_bytes(b[265:267],'little');start=264;end=start+3+n;b[end-1]=(-sum(b[start:end-1]))&255
  with self.assertRaises(a.ActorDataError):a.validate_raw(bytes(b))
 def test_accounting(self):self.assertEqual(a.PROFILE['DATA_accounting'],{'literal':2,'iterated':1958,'LINK_alignment':0,'hole_fill':0,'Cfunctions':0,'MZ':0})
if __name__=='__main__':unittest.main()
