"""One genuine menu-active scalar COMMON, never an alias allocation."""
from pathlib import Path
import ast,copy,hashlib,importlib,json,sys,tempfile,unittest
from unittest.mock import patch
PROJECT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(PROJECT))
import source_inputs
import menu_paused_source_inputs as profile
from omf import read_omf
D=PROJECT/'build/menu-paused-common-followup'

class MenuPausedCommonTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  assert Path(profile.__file__).resolve()==PROJECT/'menu_paused_source_inputs.py'
  assert Path(source_inputs.__file__).resolve()==PROJECT/'source_inputs.py'
  cls.item=json.loads((D/'proposed-source-input.json').read_text());cls.proof=json.loads((D/'proof.json').read_text());cls.route=json.loads((D/'normal-route-proof.json').read_text());cls.data=(D/'positive.obj').read_bytes()
 def test_actual_signed_int_COMMON2_no_loaded_or_PUBLIC(self):
  defs=profile.validate_object(self.data);self.assertEqual(defs,[{'symbol':'_paused','type_index':129,'datatype':98,'size':2}]);o=read_omf(self.data);self.assertFalse(o.publics);self.assertFalse(o.procedures)
  self.assertTrue(all(not s.length for s in o.segments.values()if s.class_name not in ['DEBTYP','DEBSYM']))
 def test_actual_builtin_CV_type_and_debug_FAR16_only(self):
  o=read_omf(self.data);self.assertEqual(o.externals,{1:'__acrtused',2:'_paused'});self.assertEqual(o.segments[5].chunks,[(0,bytes.fromhex('0e0500000000810006706175736564'))]);self.assertEqual(o.segments[6].length,0)
  self.assertEqual([(f.segment,f.offset,f.width,f.location_type,f.target)for f in o.fixups],[(5,2,4,3,(2,2))])
 def test_all_three_genuine_negative_source_objects_reject(self):
  for name in ['wrong_unsigned','wrong_width','wrong_initialized']:
   with self.subTest(name=name),self.assertRaises(ValueError):profile.validate_object((D/(name+'.obj')).read_bytes())
 def test_checksum_truncation_and_extra_bytes_reject(self):
  for data in [self.data[:-1],self.data+b'\0',bytes([self.data[0]^1])+self.data[1:]]:
   with self.assertRaises(ValueError):profile.validate_object(data)
 def test_wrong_raw_input_type_reject(self):
  with self.assertRaises(ValueError):profile.validate_object(bytearray(self.data))
 def test_exact_item_source_identity_no_width_alias_capacity_metadata(self):
  profile.validate_item(self.item)
  for changes in [{'source':'src/link/other.c'},{'source_sha256':'0'*64},{'compiler':'msc510'},{'flags':['/AM']},{'objects':[{'symbol':'_pending_input_988e','size':2,'storage':'near-common'}]},{'capacity':1},{'initialized_bytes':2}]:
   with self.subTest(changes=changes),self.assertRaises(ValueError):profile.validate_item(dict(self.item,**changes))
 def test_evidence_pin_identity_fails_closed(self):
  item=copy.deepcopy(self.item);item['evidence']['crt']['sha256']='0'*64
  with self.assertRaises(ValueError):profile.validate_item(item)
  with self.assertRaises(ValueError):profile.validate_evidence(PROJECT,item['evidence'],PROJECT.parent/'CHESS.EXE')
 def test_relative_source_path_and_escape_rejected(self):
  for name in ['/tmp/source.c','../CHESS.EXE']:
   with self.assertRaises(ValueError):profile.local(PROJECT,name)
 def test_full_native_lifecycle_and_CRT_evidence(self):
  result=profile.validate_evidence(PROJECT,self.item['evidence'],PROJECT.parent/'CHESS.EXE')
  self.assertEqual(result[0]['dgroup_offset'],'0x988e');self.assertEqual(result[0]['end_exclusive'],'0x9890');self.assertFalse(result[0]['resolved']);self.assertFalse(result[0]['historical_COMMON_order_proven'])
 def test_bad_target_cannot_create_common_native_constraint(self):
  with tempfile.TemporaryDirectory()as tmp:
   p=Path(tmp)/'bad.exe';p.write_bytes(b'MZnot-original')
   with self.assertRaises(ValueError):profile.validate_evidence(PROJECT,self.item['evidence'],p)
 def test_no_existing_provider_or_guessed_extent(self):
  p=self.proof;self.assertTrue(p['no_provided_symbol_at_exact_aliases']);self.assertEqual(p['other_existing_COMMON_anchors_unresolved_here'],[]);self.assertEqual(p['native_file_backed_bytes'],0);self.assertEqual(p['native_MZ'],[])
  self.assertEqual(p['source_defined_names'],['_paused']);self.assertEqual(p['alias_not_independently_allocated'],'_pending_input_988e')
 def test_actual_selected_global_views_and_ten_real_WORD_fields(self):
  p=self.proof;self.assertEqual(len(p['actual_current_runtime_fields']),10);self.assertEqual(len(p['actual_native_WORD_references']),10)
  self.assertEqual(set(p['actual_selected_global_declarations']),{'src/main_input_exit_match.c','src/search_engine_a4d4_b9ba_match.c','src/keyboard_command_context_match.c'})
  self.assertTrue(all(x['type']=='int'and x['storage']=='extern'for ds in p['actual_selected_global_declarations'].values()for x in ds))
 def test_actual_fresh_normal_route_is_zero_credit_and_target_free(self):
  p=self.route;self.assertEqual(p['fresh_compiles'],1);self.assertEqual(len(p['blocked_original_carrier']),2);r=p['result']['objects'][0]
  self.assertEqual(r['allocation_bytes'],2);self.assertEqual(r['initialized_bytes'],0);self.assertEqual(r['matching_credit'],0);self.assertEqual(r['authored_C_function_credit'],0);self.assertFalse(r['placement_proven']);self.assertEqual(r['object_sha256'],hashlib.sha256(self.data).hexdigest())
 def test_changed_source_rejected_before_compiler(self):
  with tempfile.TemporaryDirectory()as tmp:
   p=Path(tmp)/profile.SOURCE;p.parent.mkdir(parents=True);p.write_text('long paused;\n')
   with patch.object(profile,'compile_c',side_effect=AssertionError('compiler must not run')),self.assertRaisesRegex(ValueError,'source hash'):profile.build_input(self.item,Path(tmp),PROJECT.parent/'CHESS.EXE',Path(tmp)/'out')
 def test_duplicate_symbol_guard_precedes_any_generation(self):
  with tempfile.TemporaryDirectory()as tmp:
   p=Path(tmp);config=p/'cfg.json';config.write_text(json.dumps({'schema_version':1,'source_allocations':[self.item]}))
   with patch.object(source_inputs,'compile_c',side_effect=AssertionError('must not compile')),self.assertRaisesRegex(ValueError,'duplicate allocation symbol'):source_inputs.build_source_inputs(PROJECT,PROJECT.parent/'CHESS.EXE',p/'out',config_path=config,defined_symbols={'_paused'})
 def test_duplicate_item_guard_uses_existing_dispatch_semantics(self):
  # This is a routing unit control only, not a fake normal generation report.
  with tempfile.TemporaryDirectory()as tmp:
   p=Path(tmp);config=p/'cfg.json';config.write_text(json.dumps({'schema_version':1,'source_allocations':[self.item,self.item]}))
   with patch.object(profile,'build_input',return_value=copy.deepcopy(self.route['result']['objects'][0]))as stub,self.assertRaisesRegex(ValueError,'duplicate source allocation'):source_inputs.build_source_inputs(PROJECT,PROJECT.parent/'CHESS.EXE',p/'out',config_path=config)
   self.assertEqual(stub.call_count,1)
 def test_old16_closed_profile_objects_still_validate(self):
  rows=json.loads((D/'old-profile-compatibility-inputs.json').read_text());self.assertEqual(len(rows),16)
  for row in rows:
   data=(D/row['object']).read_bytes();self.assertEqual(hashlib.sha256(data).hexdigest(),row['sha256']);module=importlib.import_module(row['module']);defs=module.validate_object(data)
   self.assertEqual([d['symbol']for d in defs],[d['symbol']for d in row['definitions']])
 def test_existing_dispatcher_bytes_recovered_by_removing_only_new_branch(self):
  old=(D/'implementation/source_inputs.base.py').read_text();new=(D/'implementation/source_inputs.py').read_text();start=new.index("        if item['backend'] == 'msc500-near-common-menu-paused-v1':\n");end=new.index("        if item['backend'] == 'msc500-near-common-event-pointers-v1':\n",start)
  self.assertEqual(new[:start]+new[end:],old)
 def test_optional_client_debug_name_delta_is_explicit_and_excluded_initially(self):
  p=json.loads((D/'client-reuse/debug-delta.json').read_text());h=json.loads((D/'client-reuse/hold-review.json').read_text())
  self.assertEqual(p['scope'],'existing CV matches preserved; original whole-object placement remains held')
  self.assertTrue(p['loaded_CODE996_raw_chunks_identical']);self.assertEqual(p['DEBSYM_lengths'],[557,545]);self.assertEqual(p['sole_debug_record_change']['byte_delta'],-12)
  self.assertFalse(p['selected_for_initial_provider_batch']);self.assertFalse(h['eligible_for_current_admission'])
 def test_optional_keyboard_client_is_byte_neutral_but_no_layout_claim(self):
  p=json.loads((D/'client-reuse/proof.json').read_text());self.assertEqual(p['fresh_compiles'],1);self.assertEqual(len(p['normal_results']),2);self.assertEqual(p['credited_CV_bytes'],995);self.assertEqual(p['whole_CODE_bytes'],996);self.assertEqual(p['all_CODE_field_count'],86);self.assertEqual(len(p['native_MZ']),12);self.assertFalse(p['whole_native_source_link_layout_claim'])
  self.assertEqual(p['compiler_tail_hex'],'90');self.assertEqual(p['tail_original_next_byte'],85);self.assertEqual(p['retired_client_name_if_later_applied'],'_pending_input_988e');self.assertEqual(p['provided_COMMON_name'],'_paused')

if __name__=='__main__':unittest.main(verbosity=2)
