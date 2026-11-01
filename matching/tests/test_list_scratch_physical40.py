"""Real physical DATA40 fixture; pure integrity negatives, no generators."""
from pathlib import Path
from copy import deepcopy
from dataclasses import replace
from unittest.mock import patch
import hashlib,json,struct,unittest
import asm_data16 as backend
from omf import read_omf,OMFError
ROOT=Path(__file__).resolve().parents[1]
FIX=ROOT/'tests/fixtures/list_scratch_physical40'
SYMS=['_left_list_scratch','_right_list_scratch']
def load():return read_omf((FIX/'actual196.obj').read_bytes())
def extract(o,syms=SYMS):return backend._extract_data(o,syms,2)
class PhysicalScratch40(unittest.TestCase):
 def test_actual_raw_fixture_hash(self):
  self.assertEqual(hashlib.sha256((FIX/'actual196.obj').read_bytes()).hexdigest(),'929f17c234fdf248bb0fdc7e4dbd12f6328af1d7b8c7361e87030ddba93025eb')
 def test_complete_real_DATA40_and_two_group1_views(self):
  o=load();before=deepcopy(o);data,meta=extract(o)
  self.assertEqual(data,bytes([255]+[0]*19+[255]+[0]*19));self.assertEqual(o,before)
  self.assertEqual([(p['name'],p['group'],p['offset'])for p in meta['publics']],[(SYMS[0],1,0),(SYMS[1],1,20)])
  self.assertEqual(meta['emitted_mz_sites'],[]);self.assertEqual(meta['authored_c_credit'],0);self.assertEqual(meta['function_credit'],0)
 def test_source_complete_numeric_DW_model(self):
  m=backend.parse_source((FIX/'source.asm').read_bytes());data,_=extract(load())
  self.assertEqual(m['symbols'],SYMS);self.assertEqual(m['offsets'],dict(zip(SYMS,[0,20])))
  self.assertEqual(m['element_width'],2);self.assertEqual(data,b''.join(struct.pack('<H',x)for x in m['numeric_values']))
 def test_source_exact_production_pin(self):
  q=json.loads((FIX/'unit.json').read_text());backend.validate_unit(q)
  self.assertEqual(hashlib.sha256((ROOT/q['source']).read_bytes()).hexdigest(),q['source_sha256'])
 def test_checksum_mutation_rejected(self):
  raw=bytearray((FIX/'actual196.obj').read_bytes());raw[-1]^=1
  with self.assertRaises(OMFError):read_omf(bytes(raw))
 def test_missing_second_PUBLIC_is_not_complete_contribution(self):
  o=load();del o.publics[SYMS[1]]
  with self.assertRaises(backend.ASMDataError):extract(o)
 def test_extra_PUBLIC_is_not_accepted(self):
  o=load();o.publics['_invented']=replace(o.publics[SYMS[1]],name='_invented',offset=22)
  with self.assertRaises(backend.ASMDataError):extract(o)
 def test_subset_public_selection_rejected(self):
  with self.assertRaises(backend.ASMDataError):extract(load(),SYMS[:1])
 def test_public_group0_rejected_despite_DGROUP_membership(self):
  o=load();o.publics[SYMS[1]]=replace(o.publics[SYMS[1]],group=0)
  with self.assertRaises(backend.ASMDataError):extract(o)
 def test_alias_PUBLIC_positions_rejected(self):
  o=load();o.publics[SYMS[1]]=replace(o.publics[SYMS[1]],offset=0)
  with self.assertRaises(backend.ASMDataError):extract(o)
 def test_uninitialized_tail_rejected(self):
  o=load();next(iter(o.segments.values())).length+=2
  with self.assertRaises(backend.ASMDataError):extract(o)
 def test_complete_extent_hole_rejected(self):
  o=load();s=next(iter(o.segments.values()));at,data=s.chunks[0];s.chunks[0]=(at+2,data[2:])
  with self.assertRaises(backend.ASMDataError):extract(o)
 def test_overlapping_data_write_rejected(self):
  o=load();s=next(iter(o.segments.values()));s.chunks.append((0,b'\xff\0'))
  with self.assertRaises(backend.ASMDataError):extract(o)
 def test_common_record_is_not_initialized_literal_storage(self):
  o=load();o.records.append((0xb0,0,b''))
  with self.assertRaises(backend.ASMDataError):extract(o)
 def test_reserved_LIDATA_not_accepted_in_generic_DW(self):
  o=load();o.records.append((0xa2,0,b''))
  with self.assertRaises(backend.ASMDataError):extract(o)
 def test_old_comma_GLOBAL_grammar_remains_rejected(self):
  src=(FIX/'source.asm').read_bytes().replace(b'global _left_list_scratch\nglobal _right_list_scratch',b'global _left_list_scratch, _right_list_scratch')
  with self.assertRaises(backend.ASMDataError):backend.parse_source(src)
 def test_mixed_DD_DW_rejected(self):
  with self.assertRaises(backend.ASMDataError):backend.parse_source((FIX/'source.asm').read_bytes()+b'\ndd 0\n')
 def test_reservation_cannot_replace_observed_opaque_zero_values(self):
  src=(FIX/'source.asm').read_bytes().replace(b'dw 0,0,0,0 ; bytes32..39',b'resw 4 ; bytes32..39')
  with self.assertRaises(backend.ASMDataError):backend.parse_source(src)
 def test_wrong_source_pin_rejects_before_tool_lookup(self):
  q=json.loads((FIX/'unit.json').read_text());q['source_sha256']='0'*64
  with patch.object(backend.shutil,'which',side_effect=AssertionError('tool lookup must remain unreachable')):
   with self.assertRaises(backend.ASMDataError):backend.assemble(FIX/'source.asm',q)
 def test_primary_whole40_not_gap_inferred_zero_filler(self):
  e=json.loads((FIX/'REA40.json').read_text());n=e['normalized_result'];data,_=extract(load())
  self.assertEqual(e['evidence_id'],'ev_44e5d811399391ab10fb2c879b31444ef389e025f3b5d890c60cccd2d63c18ec')
  self.assertTrue(n['complete']);self.assertEqual(n['returned_bytes'],40);self.assertEqual(bytes.fromhex(n['bytes_hex']),data)
 def test_operational22_and_opaque18_not_two_C20_capacities(self):
  p=json.loads((FIX/'operational-proof.json').read_text());self.assertEqual(p['minimum_valid_operational_storage'],[10,12])
  self.assertEqual(max(x['payload_length']for x in p['records'][:36]),9);self.assertEqual(max(x['payload_length']for x in p['records'][36:]),11)
  self.assertIn('original C array capacity',p['holds']);self.assertEqual(p['new_matching_credit'],0)
 def test_actual_LINK_frame_proof_and_negative_receipt_remain_honest(self):
  p=json.loads((FIX/'retained290.json').read_text());self.assertEqual(p['status'],'LINK_SUCCESS_WITH_POSTCHECK_SCHEMA_NEGATIVE')
  self.assertEqual(p['producer_status_preserved'],'FAILED');self.assertEqual(p['producer_outer_exit'],1);self.assertEqual(p['actual_DOSBox_exit'],0)
  self.assertIsNone(p['strict_actual_diagnostics']['summary_error_count']);self.assertEqual(p['strict_actual_diagnostics']['undefined_symbols'],[])
  self.assertEqual([len(p['all2_CODE_fields']),len(p['all2_DEBUG_fields_comparison_only'])],[2,2]);self.assertFalse(p['full_executable_match'])
