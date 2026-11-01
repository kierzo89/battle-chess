"""Permanent integrity and semantic-regression controls; fixture comparisons only."""
from pathlib import Path
from types import SimpleNamespace
import copy,json,unittest
from unittest.mock import patch
from omf import read_omf,OMFError,Fixup
from link16 import link_function
import event_text_unsigned_context as c
import event_unsigned_runtime_identity as h
import event_pointer_unsigned_source_inputs as p
from event_pointer_unsigned_graphs import pointer_graph
F=Path(__file__).parent/'fixtures/event_text_unsigned'
def obj(n='new-event.obj'):return read_omf((F/n).read_bytes())
def unit(name='decimal_digits_5dca'):return copy.deepcopy(c.profile()['unit_contracts'][name])
class UnsignedEventContextTests(unittest.TestCase):
 def test_genuine_whole_new_object(self):self.assertIsNotNone(c.validate_object(obj()))
 def test_complete_three_units(self):
  for u in c.profile()['unit_contracts'].values():c.validate_unit(u)
 def test_old_signed_whole_object_rejected(self):
  with self.assertRaises(OMFError):c.validate_object(obj('old-event.obj'))
 def test_changed_loaded_byte_rejected(self):
  o=obj();at,b=o.segments[1].chunks[0];o.segments[1].chunks[0]=(at,bytes([b[0]^1])+b[1:])
  with self.assertRaises(OMFError):c.validate_object(o)
 def test_changed_debug_byte_rejected(self):
  o=obj();at,b=o.segments[5].chunks[0];o.segments[5].chunks[0]=(at,bytes([b[0]^1])+b[1:])
  with self.assertRaises(OMFError):c.validate_object(o)
 def test_changed_TYPE_graph_rejected(self):
  o=obj();o.segments[6].length+=1
  with self.assertRaises(OMFError):c.validate_object(o)
 def test_changed_PARSED_external_rejected(self):
  o=obj();o.externals[3]='__aNldiv'
  with self.assertRaises(OMFError):c.validate_object(o)
 def test_duplicate_normalized_snapshot_key_rejected(self):
  with self.assertRaises(OMFError):c.canonical({1:'a','1':'b'})
 def test_source_legacy_selection_rejected(self):
  u=unit();u['source']='src/event_text_match.c'
  with self.assertRaises(OMFError):c.validate_unit(u)
 def test_changed_flags_rejected(self):
  u=unit();u['flags']=['/AS','/Zi']
  with self.assertRaises(OMFError):c.validate_unit(u)
 def test_unknown_unit_rejected(self):
  u=unit();u['id']='other'
  with self.assertRaises(OMFError):c.validate_unit(u)
 def test_two_real_unsigned_helper_fields(self):
  r=h.validate_used_fields(obj(),unit());self.assertEqual([(x['symbol'],x['native_offset'])for x in r['used_real_helpers']],[('__aNulrem',0xf402),('__aNuldiv',0xf39c)])
 def test_signed_div_name_at_unsigned_target_rejected(self):
  o=obj();o.externals[3]='__aNldiv';u=unit();u['externals']['__aNldiv']=0xf39c
  with self.assertRaisesRegex(OMFError,'identity mismatch'):h.validate_used_fields(o,u)
 def test_signed_remainder_name_at_unsigned_target_rejected(self):
  o=obj();o.externals[4]='__aNlrem';u=unit();u['externals']['__aNlrem']=0xf402
  with self.assertRaisesRegex(OMFError,'incorrectly signed'):h.validate_used_fields(o,u)
 def test_old_signed_normalized_CODE_can_fit_but_identity_rejects(self):
  old=obj('old-event.obj');new=obj();u=unit();e=dict(u['externals']);e['__aNldiv']=e['__aNuldiv'];e['__aNlrem']=e['__aNulrem'];a,_=link_function(old,u['symbol'],0x5dca,e);b,_=link_function(new,u['symbol'],0x5dca,u['externals']);self.assertEqual(a,b)
  u['externals']=e
  with self.assertRaises(OMFError):h.validate_used_fields(old,u)
 def test_correct_signed_div_entry_still_wrong_event_context(self):
  o=obj('old-event.obj');u=unit();u['externals']['__aNldiv']=0xf87c;u['externals']['__aNlrem']=0xf402
  with self.assertRaises(OMFError):h.validate_used_fields(o,u)
 def test_wrong_unsigned_target_rejected(self):
  u=unit();u['externals']['__aNuldiv']=0xf87c
  with self.assertRaises(OMFError):h.validate_used_fields(obj(),u)
 def test_wrong_near_binding_type_rejected(self):
  u=unit();u['externals']['__aNuldiv']={'segment':0,'offset':0xf39c}
  with self.assertRaises(OMFError):h.validate_used_fields(obj(),u)
 def test_unknown_helper_no_generic_normalizer(self):
  o=obj();o.externals[3]='__aNalias';u=unit();u['externals']['__aNalias']=0xf39c
  with self.assertRaises(OMFError):h.validate_used_fields(o,u)
 def test_wait_functions_have_no_helper_calls(self):
  for n in ['wait_exit_event_5d48','wait_pointer_event_5d7a']:self.assertEqual(h.validate_used_fields(obj(),unit(n))['used_real_helpers'],[])
 def test_unused_metadata_explicitly_not_identity_credit(self):
  u=unit('wait_exit_event_5d48');u['externals']['__aNldiv']=0xf39c;r=h.validate_used_fields(obj(),u);self.assertTrue(r['unused_metadata_is_not_callee_ownership_proof']);self.assertIn('__aNldiv',r['unused_metadata_bindings'])
  with self.assertRaises(OMFError):c.validate_unit(u)
 def test_wrong_field_relative_mode_rejected(self):
  o=obj();i=next(i for i,f in enumerate(o.fixups)if f.segment==1 and f.target==(2,3));f=o.fixups[i];o.fixups[i]=Fixup(f.segment,f.offset,f.width,f.location_type,True,f.frame,f.target,f.displacement,f.record_offset,f.raw)
  with self.assertRaises(OMFError):h.validate_used_fields(o,unit())
 def test_complete_pointer_graphs_match_real_producer(self):
  provider=obj('provider.obj');event=obj();main=obj('main.obj')
  for n in ['_event_context','_current_event']:self.assertEqual(pointer_graph(provider,n),pointer_graph(event,n))
  self.assertEqual(pointer_graph(provider,'_current_event'),pointer_graph(main,'_current_event'))
 def test_wrong_pointer_graph_source_rejected(self):
  o=obj();o.externals[6]='_not_current_event'
  with self.assertRaises(OMFError):pointer_graph(o,'_current_event')
 def test_exact_near_pointee_prefix_sizes(self):
  self.assertEqual(pointer_graph(obj(),'_current_event')['to']['struct_bits'],160);self.assertEqual(pointer_graph(obj(),'_event_context')['to']['struct_bits'],96)
 def test_legacy_producer_gate_still_accepts_same_real_raw(self):self.assertEqual(len(p.validate_object((F/'provider.obj').read_bytes())),2)
 def test_new_provider_item_exact(self):p.validate_item(json.loads((F/'new-provider-item.json').read_text()))
 def test_old_provider_backend_not_silently_admitted(self):
  x=json.loads((F/'new-provider-item.json').read_text());x['backend']='msc500-near-common-event-pointers-v1'
  with self.assertRaises(ValueError):p.validate_item(x)
 def test_provider_extent_change_rejected(self):
  x=json.loads((F/'new-provider-item.json').read_text());x['objects'][0]['size']=4
  with self.assertRaises(ValueError):p.validate_item(x)
 def test_stale_active_event_source_evidence_rejected(self):
  x=json.loads((F/'new-provider-item.json').read_text());x['evidence']['active_event_source']=x['evidence']['legacy_event_consumer']
  with self.assertRaises(ValueError):p.validate_item(x)
if __name__=='__main__':unittest.main()
