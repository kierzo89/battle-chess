"""Prepared comparison controls; no compiler, process, LINK or fixture injection."""
from pathlib import Path
import sys,json,copy,dataclasses,unittest
from unittest.mock import patch
M=Path(__file__).resolve().parents[1];sys.path.insert(0,str(M))
import shared_turn_book_selector2418 as shared
import owned_selector_const16 as dispatch
from omf import read_omf
from reference import build_reference
from link16 import link_function
F=M/'tests/fixtures/shared_turn_book2418'
class SharedTurnBook2418Tests(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.raw=(F/'actual.obj').read_bytes();c.units=json.loads((F/'units17.json').read_text());c.unit=next(x for x in c.units if x['symbol']=='_setup_state');c.legacy=json.loads((F/'legacy-book-unit.json').read_text());c.reference=build_reference((M.parent/'CHESS.EXE').read_bytes())
 def obj(self):return read_omf(self.raw)
 def layout(self,o=None,d=None,e=None):return shared.validate_layout(self.obj()if o is None else o,self.unit['owned_selector_const']if d is None else d,self.unit['externals']if e is None else e)
 def bad(self,mutate):
  o=self.obj();mutate(o)
  with self.assertRaises(ValueError):self.layout(o)
 def context(self):
  obj=self.obj();p=shared.validate_shared_object(obj);code=bytearray();fields=[]
  for n,(at,size)in p['procedures'].items():
   b,f=link_function(obj,n,0x7c52+at,self.unit['externals'],**({'owned_selector_const':self.unit['owned_selector_const']}if n in shared.OWNERS else{}));code.extend(b);fields.extend(f)
  return bytes(code),fields,p
 def test_snapshot_integer_JSON_keys_compare_in_same_closed_view(self):
  a={1:'one',2:'two',10:'ten'};self.assertEqual(shared.canonical(a),shared.canonical(json.loads(json.dumps(a))))
 def test_duplicate_normalized_snapshot_key_rejected(self):
  self.bad(lambda o:o.externals.update({'1':o.externals[1]}))
 def test_positive_complete18_CV_CODE2418_CONST2_456fields(self):
  o=self.obj();p=shared.validate_shared_object(o);self.assertEqual(self.layout(o),0x4da6);self.assertEqual(len(o.fixups),456);self.assertEqual(len(p['procedures']),18)
 def test_full17_native_matches_commit408_negative_fourbases(self):
  _,b,p=dispatch.validate(self.unit,self.obj(),M,self.reference);self.assertEqual(b,b'\x09\x1f');self.assertFalse(p['whole_CODE_exact_native']);self.assertEqual((p['matched_complete_procedure_count'],p['matched_complete_procedure_bytes']),(17,2010));self.assertEqual([r['shared_offset']for r in p['held_commit_differences']],[1215,1539,1594]);self.assertEqual([r['load_paragraph']for r in p['four_load_bases']],[0,1,4096,65535]);self.assertEqual((p['authored_c_function_credit'],p['source_data_credit']),(0,0))
 def test_all_six_real_owners_only(self):
  owners=[u for u in self.units if u.get('owned_selector_const')]
  self.assertEqual({u['symbol']for u in owners},shared.OWNERS)
  for u in owners:dispatch.validate_unit_metadata(u)
  for n in ['_shift_state','_commit_turn_810c','_prepare_hint_8384']:
   with self.assertRaises(ValueError):shared.validate_unit_metadata(dict(self.unit,symbol=n))
 def test_exact_source_flags_extent_and_id(self):
  for change in [{'source':'src/book_context_match.c'},{'id':'fake'},{'flags':['/AS','/Zi']},{'image_offset':'0x7c9a'},{'size':140},{'size':141.0},{'object_profile':'alias'},{'owned_const':{}}]:
   with self.assertRaises(ValueError):shared.validate_unit_metadata(dict(self.unit,**change))
 def test_native_descriptor_boolean_extra_key_and_relocation_target(self):
  for change in [{'group':True},{'size':2.0},{'segment':2},{'image_offset':'0x619c8'},{'target_symbol':'_graphics_copy'},{'fake':1},{'data_address':{'segment':0x5cc2,'offset':0x4da8}}]:
   with self.assertRaises(ValueError):self.layout(d=dict(self.unit['owned_selector_const'],**change))
 def test_exact_binding_type_missing_extra_and_value(self):
  for name,value in [('_current_side',True),('_current_side',38982.0),('_splash_buffer',{'segment':0x1f0a,'offset':0})]:
   e=copy.deepcopy(self.unit['externals']);e[name]=value
   with self.assertRaises(ValueError):self.layout(e=e)
  for operation in ['missing','extra']:
   e=copy.deepcopy(self.unit['externals']);e.pop('_current_side')if operation=='missing'else e.update(_alias=0)
   with self.assertRaises(ValueError):self.layout(e=e)
 def test_skip_owner_requires_new_strict_extent(self):
  u=copy.deepcopy(next(u for u in self.units if u['symbol']=='_skip_book_8577'))
  for change in [None,{},dict(u['extended_extent'],kind='book_skip_8577_v1')]:
   with self.assertRaises(ValueError):shared.validate_unit_metadata(dict(u,extended_extent=change))
 def test_other_owners_cannot_gain_extent_or_storage(self):
  for k in ['extended_extent','owned_data','owned_bss','code_address']:
   with self.assertRaises(ValueError):shared.validate_unit_metadata(dict(self.unit,**{k:{'kind':'fake'}}))
 def test_old800_positive_gate_intact_and_new_rejected(self):
  o=read_omf((F/'legacy-book.obj').read_bytes());u=self.legacy;self.assertEqual(dispatch.validate_layout(o,u['owned_selector_const'],u['externals']),0x4da6)
  with self.assertRaises(ValueError):dispatch.validate_layout(self.obj(),u['owned_selector_const'],u['externals'])
  with self.assertRaises(ValueError):self.layout(o)
 def test_missing_or_alias_PUBLIC_and_public_frame(self):
  self.bad(lambda o:o.publics.pop('_setup_state'));self.bad(lambda o:o.publics.update(_alias=next(iter(o.publics.values()))));self.bad(lambda o:o.publics.__setitem__('_setup_state',dataclasses.replace(o.publics['_setup_state'],group=1)))
 def test_changed_CV_length_hidden_proc_and_typegraph(self):
  self.bad(lambda o:o.procedures['_setup_state'].update(length=140));self.bad(lambda o:o.procedures.update(_hidden=copy.deepcopy(o.procedures['_setup_state'])));self.bad(lambda o:setattr(o.segments[6],'chunks',[(0,b'\0'*o.segments[6].length)]))
 def test_CODE_tail_hole_overlap_no_trimming(self):
  self.bad(lambda o:setattr(o.segments[1],'length',2419));self.bad(lambda o:o.segments[1].chunks.pop());self.bad(lambda o:o.segments[1].chunks.append(o.segments[1].chunks[0]))
 def test_no_extra_DATA_BSS_COMMON_or_unknown_record(self):
  self.bad(lambda o:setattr(o.segments[2],'length',2));self.bad(lambda o:setattr(o.segments[4],'length',4));self.bad(lambda o:o.records.append((0xb0,0,b'\0')));self.bad(lambda o:o.records.append((0xc2,0,b'\0')))
 def test_CONST_word_and_BASE_field_target_strict(self):
  self.bad(lambda o:setattr(o.segments[3],'chunks',[(0,b'\1\0')]))
  def change(o):
   i=next(i for i,f in enumerate(o.fixups)if f.segment==3);o.fixups[i]=dataclasses.replace(o.fixups[i],frame=(1,1))
  self.bad(change)
 def test_all_eight_owner_offsets_frames_accounted(self):
  self.bad(lambda o:setattr(o,'fixups',[f for f in o.fixups if not(f.segment==1 and f.offset==97)]))
  def change(o):
   i=next(i for i,f in enumerate(o.fixups)if f.segment==1 and f.offset==97);o.fixups[i]=dataclasses.replace(o.fixups[i],target=(0,2))
  self.bad(change)
 def test_debug_ordered_patch_real18_shadowed_not_runtime(self):
  p=shared.validate_shared_object(self.obj());self.assertEqual(len(p['shadowed_debug_offsets']),18)
  self.bad(lambda o:setattr(o.segments[5],'chunks',list(reversed(o.segments[5].chunks))));self.bad(lambda o:o.data_writes.pop())
 def test_profile_or_retained_evidence_tamper_rejected(self):
  original=Path.read_bytes
  for filename in ['shared_turn_book_selector2418_profile.json','comparison.json','generation.json']:
   def changed(p,*a,**k):
    b=original(p,*a,**k);return b+b' 'if p.name==filename else b
   with patch.object(Path,'read_bytes',changed),self.assertRaises(ValueError):dispatch.validate(self.unit,self.obj(),M,self.reference)
 def test_comparison_source_hash_rejected(self):
  original=Path.read_bytes
  def changed(p,*a,**k):
   b=original(p,*a,**k);return b+b' 'if p.name=='shared_turn_book_context_match.c'else b
  with patch.object(Path,'read_bytes',changed),self.assertRaises(ValueError):dispatch.validate(self.unit,self.obj(),M,self.reference)
 def test_descriptor_primary_escape_cannot_switch_evidence(self):
  for key in ['rea_evidence','code_evidence']:
   u=copy.deepcopy(self.unit);u['owned_selector_const'][key]='../CHESS.EXE'
   with self.assertRaises(ValueError):dispatch.validate(u,self.obj(),M,self.reference)
 def test_native_context_mutation_rejected_including_held_site(self):
  code,fields,p=self.context()
  for offset in [0x7c99,0x8111]:
   ref=dict(self.reference);b=bytearray(ref['image']);b[offset]^=1;ref['image']=bytes(b)
   with self.assertRaises(ValueError):shared.compare_context(code,b'\x09\x1f',fields,ref,p)
 def test_source_commit_correction_is_not_allowed(self):
  code,fields,p=self.context();b=bytearray(code);b[1215]=4
  with self.assertRaises(ValueError):shared.compare_context(bytes(b),b'\x09\x1f',fields,self.reference,p)
 def test_raw_chronology_retained_but_generic_runtime_logs_sorted(self):
  code,fields,p=self.context();raw=[(f['offset'],f['record_offset'])for f in p['object_snapshot']['fixups']if f['segment']==1];self.assertNotEqual(raw,sorted(raw));self.assertEqual([(f['object_offset'],f['record_offset'])for f in fields],sorted(raw));shared.compare_context(code,b'\x09\x1f',fields,self.reference,p)
 def test_all362_CODE_logs_required_not_just_MZ(self):
  code,fields,p=self.context();self.assertEqual(len(fields),362)
  with self.assertRaises(ValueError):shared.compare_context(code,b'\x09\x1f',fields[1:],self.reference,p)
 def test_wrong_MZ_scope_and_no_forged_site(self):
  code,fields,p=self.context();changed=copy.deepcopy(fields);i=next(i for i,f in enumerate(changed)if'mz_segment_relocation_image_offset'in f);changed[i]['mz_segment_relocation_image_offset']+=2
  with self.assertRaises(ValueError):shared.compare_context(code,b'\x09\x1f',changed,self.reference,p)
 def test_readonly_structural_helper_has_no_target_or_positive_reads(self):
  o=self.obj();before=copy.deepcopy(shared.snapshot(o));original=Path.read_bytes
  def guarded(p,*a,**k):
   if p.name!='shared_turn_book_selector2418_profile.json':raise AssertionError('Unexpected structural helper read')
   return original(p,*a,**k)
  with patch.object(Path,'read_bytes',guarded):shared.validate_shared_object(o)
  self.assertEqual(shared.snapshot(o),before)
 def test_alternate_extent_existing_assertions_accept_new_context(self):
  from extent import validate_extended_extent
  u=next(u for u in self.units if u['symbol']=='_alternate_view');o=self.obj();b,_=link_function(o,u['symbol'],int(u['image_offset'],0),u['externals']);proof=validate_extended_extent(u,M,self.reference['original_sha256'],o.function_info(u['symbol']),b,o);self.assertTrue(proof)
 def test_owned_context_collector_reauthenticates_six_owners_once(self):
  from owned_context_mz import collect_owned_context_mz
  rows=[]
  for u in self.units:
   if not u.get('owned_selector_const'):continue
   _,_,proof=dispatch.validate(u,self.obj(),M,self.reference);rows.append(dict(u,status='c_matched',source_sha256=shared.pins.SOURCE_SHA256,object_sha256=shared.pins.OBJECT_SHA256,object_artifact=str((F/'actual.obj').resolve()),owned_selector_const_proof=proof))
  accepted=collect_owned_context_mz(rows,M,self.reference,self.reference['relocations']);self.assertEqual(accepted['sites'],[0x619c6]);self.assertEqual(len(accepted['matched_owner_units']),6)
  with self.assertRaises(ValueError):collect_owned_context_mz(rows+[rows[0]],M,self.reference,self.reference['relocations'])
  rows[0]['owned_selector_const_proof']['held_commit_bytes']=0
  with self.assertRaises(ValueError):collect_owned_context_mz(rows,M,self.reference,self.reference['relocations'])
 def test_source_guard_and_actual_prior_single_compile_closure(self):
  g=json.loads((M/'evidence/shared_turn_book2418/generation.json').read_text());self.assertTrue(g['source_tool_scratch_only']);self.assertEqual(g['actual_compiler_calls'],1);self.assertEqual(len(g['blocked_probes']),5);self.assertEqual(g['source_generation']['source_sha256'],shared.pins.SOURCE_SHA256)
if __name__=='__main__':unittest.main()
