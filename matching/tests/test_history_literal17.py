"""Pure strict-profile controls; fixture bytes are never compiler inputs."""
from pathlib import Path
from copy import deepcopy
from dataclasses import replace
from unittest.mock import patch
import unittest,json
from omf import read_omf
from cdata import extract_data,CDataError
import history_input_literal_const16 as h
ROOT=Path(__file__).resolve().parents[1]
class HistoryLiteral17Tests(unittest.TestCase):
 def setUp(self):
  self.raw=(ROOT/'tests/fixtures/history_literal17/history-literal.obj').read_bytes();self.o=read_omf(self.raw);self.p=h.profile();self.u=deepcopy(self.p['unit_contracts']['accept_input_baaf']);self.d=deepcopy(self.p['unit_contracts']['input_message_4f0a'])
 def rejects(self,obj):
  with self.assertRaises(h.HistoryLiteralError):h.validate_object(obj)
 def test_complete_real_fixture(self):self.assertEqual(h.validate_object(self.o)['object_bytes'],2502)
 def test_exact_four_real_CV_extents(self):self.assertEqual(sorted((self.o.function_info(n)['offset'],self.o.function_info(n)['size'])for n in self.o.procedures),[(0,125),(125,120),(245,82),(327,12)])
 def test_complete_anonymous_literal(self):self.assertEqual(h.full(self.o,3),b'Jay was wrong #1\0');self.assertFalse(any(p.segment==3 for p in self.o.publics.values()))
 def test_explicit_real_ARRAY136_CHAR80(self):self.assertIn(bytes.fromhex('78858800838000'),h.full(self.o,6))
 def test_one_GROUP1_own_CONST_field(self):
  q=next(f for f in self.o.fixups if f.segment==1 and f.offset==311);self.assertEqual((q.frame,q.target,q.raw),((1,1),(0,3),bytes.fromhex('c4429c')))
 def test_no_external_input_alias(self):self.assertNotIn('_input_message',self.o.externals.values())
 def test_unknown_raw_record(self):o=deepcopy(self.o);o.records.append((0x99,0,b''));self.rejects(o)
 def test_CONST_nonzero_mutation(self):o=deepcopy(self.o);o.segments[3].chunks=[(0,b'X'+h.full(o,3)[1:])];self.rejects(o)
 def test_CONST_hole(self):o=deepcopy(self.o);o.segments[3].chunks=[(1,h.full(o,3)[1:])];self.rejects(o)
 def test_extra_BSS_allocation(self):o=deepcopy(self.o);o.segments[4].length=2;self.rejects(o)
 def test_missing_public(self):o=deepcopy(self.o);del o.publics['_accept_input'];self.rejects(o)
 def test_fake_data_public(self):o=deepcopy(self.o);o.publics['_input_message']=o.publics['_accept_input'];self.rejects(o)
 def test_actual_frame_cannot_be_F5(self):
  o=deepcopy(self.o);i=next(i for i,f in enumerate(o.fixups)if f.segment==1 and f.offset==311);o.fixups[i]=replace(o.fixups[i],frame=(5,None));self.rejects(o)
 def test_SEGDEF0_rejected(self):
  o=deepcopy(self.o);i=next(i for i,f in enumerate(o.fixups)if f.segment==1 and f.offset==311);o.fixups[i]=replace(o.fixups[i],target=(0,0));self.rejects(o)
 def test_incomplete_type_graph_mutation(self):o=deepcopy(self.o);o.segments[6].chunks[0]=(o.segments[6].chunks[0][0],b'\0'+o.segments[6].chunks[0][1][1:]);self.rejects(o)
 def test_CV_mutation(self):o=deepcopy(self.o);o.procedures['_accept_input']['length']=80;self.rejects(o)
 def test_all_five_unit_contracts(self):
  for u in self.p['unit_contracts'].values():self.assertEqual(h.validate_unit(u),u)
 def test_old_source_is_not_same_contract(self):self.u['source']='src/history_input_full_match.c';self.assertRaises(h.HistoryLiteralError,h.validate_unit,self.u)
 def test_data_generic_backend_not_allowed(self):self.d['backend']='msc500-data-omf';self.assertRaises(h.HistoryLiteralError,h.validate_unit,self.d)
 def test_descriptor_native_offset_not_flexible(self):self.u['owned_const']['data_address']['offset']+=2;self.assertRaises(h.HistoryLiteralError,h.validate_unit_metadata,self.u)
 def test_only_real_referencing_C_owner(self):self.assertRaises(h.HistoryLiteralError,h.validate_unit_metadata,self.p['unit_contracts']['empty_bb01'])
 def test_default_DATA_gate_still_rejects_fixture(self):self.assertRaises(CDataError,extract_data,self.o,'_accept_input')
 def test_duplicate_snapshot_key_rejected(self):self.assertRaises(h.HistoryLiteralError,h.canonical,{1:'a','1':'b'})
 def test_profile_tamper_rejected(self):
  real=Path.read_bytes
  def changed(path):
   b=real(path);return b+b' 'if path.name=='history_input_literal17_profile.json'else b
  with patch.object(Path,'read_bytes',changed):self.assertRaises(h.HistoryLiteralError,h.profile)
if __name__=='__main__':unittest.main()
