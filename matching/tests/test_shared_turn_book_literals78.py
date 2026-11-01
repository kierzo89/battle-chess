"""Focused mixed selector/literal comparison controls. No generators or LINK."""
from pathlib import Path
import sys,json,copy,unittest,dataclasses
from unittest.mock import patch
M=Path(__file__).resolve().parents[1];sys.path.insert(0,str(M));F=M/'tests/fixtures/shared_turn_book_literals78'
from omf import read_omf
from reference import build_reference
from link16 import link_function
import shared_turn_book_literals78 as mixed
import owned_selector_const16 as dispatch
class SharedTurnBookLiterals78Tests(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.raw=(F/'actual.obj').read_bytes();c.units=json.loads((F/'units17.json').read_text());c.unit=next(x for x in c.units if x['symbol']=='_setup_state');c.reference=build_reference((M.parent/'CHESS.EXE').read_bytes())
 def obj(self):return read_omf(self.raw)
 def layout(self,o=None,d=None,e=None):return mixed.validate_layout(self.obj()if o is None else o,self.unit['owned_selector_const']if d is None else d,self.unit['externals']if e is None else e)
 def bad(self,fn):
  o=self.obj();fn(o)
  with self.assertRaises(ValueError):self.layout(o)
 def linked(self):
  o=self.obj();code=bytearray();fields=[]
  procs=sorted(((o.function_info(n)['offset'],n)for n in o.procedures))
  for at,n in procs:
   self.assertEqual(at,len(code));b,f=link_function(o,n,0x7c52+at,self.unit['externals'],**({'owned_selector_const':self.unit['owned_selector_const']}if n in mixed.OWNERS else{}));code.extend(b);fields.extend(f)
  return bytes(code),fields
 def test_whole18_CODE2418_CONST78_451_rawfields(self):
  o=self.obj();mixed.validate_shared_object(o);self.assertEqual(self.layout(o),0x4da6);self.assertEqual(len(o.publics),18);self.assertEqual(len(o.procedures),18);self.assertEqual(len(o.fixups),451);self.assertEqual([sum(f.segment==n for f in o.fixups)for n in [1,3,5]],[362,1,88])
 def test_complete_native_pool78_not_literal_padding(self):
  _,blob,p=dispatch.validate(self.unit,self.obj(),M,self.reference);self.assertEqual(len(blob),78);self.assertEqual(blob,self.reference['image'][0x619c6:0x61a14]);self.assertEqual(blob[:2],b'\x09\x1f');self.assertEqual(p['complete_CONST_bytes'],78);self.assertEqual(p['complete_MZ_sites'],[0x619c6]);self.assertEqual((p['authored_c_function_credit'],p['source_data_credit']),(0,0))
 def test_chronological_CONST_two_writes_reverse_address_order(self):
  o=self.obj();self.assertEqual([(at,len(b))for at,b in o.segments[3].chunks],[(2,76),(0,2)]);self.assertFalse(any(p.segment==3 for p in o.publics.values()));self.assertEqual(sum(len(b)for at,b in o.segments[3].chunks),78)
 def test_all13_own_CONST_fields_exactaddresses(self):
  o=self.obj();refs=[f for f in o.fixups if f.target==(0,3)];self.assertEqual(len(refs),13);self.assertEqual(sorted(f.offset for f in refs),[97,581,1431,1448,1460,1477,1752,2115,2140,2255,2276,2352,2384])
 def test_five_real_literal_addends_and_no_removed_externs(self):
  o=self.obj();code=bytearray(2418)
  for at,b in o.segments[1].chunks:code[at:at+len(b)]=b
  self.assertEqual({f.offset:int.from_bytes(code[f.offset:f.offset+2],'little')for f in o.fixups if f.segment==1 and f.offset in [581,1431,1448,1460,1477]},{581:2,1431:26,1448:39,1460:53,1477:65});self.assertTrue({'_alternate_prompt','_auto_white_text_4dc0','_auto_white_packet_4dcd','_auto_black_text_4ddb','_auto_black_packet_4de7'}.isdisjoint(o.externals.values()))
 def test_seven_registered_owners_eight_linkowners_no_commitunit(self):
  self.assertEqual(len(mixed.OWNERS),8);self.assertIn('_commit_turn_810c',mixed.OWNERS);self.assertEqual(len(mixed.REGISTERED_OWNERS),7);self.assertNotIn('_commit_turn_810c',mixed.REGISTERED_OWNERS);self.assertEqual({u['symbol']for u in self.units if u.get('owned_selector_const')},mixed.REGISTERED_OWNERS)
  for u in self.units:
   if u.get('owned_selector_const'):dispatch.validate_unit_metadata(u)
  with self.assertRaises(ValueError):mixed.validate_unit_metadata(dict(self.unit,symbol='_commit_turn_810c',id='commit_turn_810c',image_offset='0x810c',size=408))
 def test_full17_native_CODE_and_held_commit_three(self):
  code,fields=self.linked();self.assertEqual(len(code),2418);self.assertEqual(len(fields),362);native=self.reference['image'][0x7c52:0x85c4];self.assertEqual([i for i,(a,b)in enumerate(zip(code,native))if a!=b],[1215,1539,1594]);o=self.obj();matched=[]
  for n in o.procedures:
   info=o.function_info(n);at=info['offset'];size=info['size'];equal=code[at:at+size]==native[at:at+size];self.assertEqual(equal,n!='_commit_turn_810c')
   if equal:matched.append(size)
  self.assertEqual((len(matched),sum(matched)),(17,2010))
 def test_all_five_MZ_four_loadbases_keep_same_three_differences(self):
  code,fields=self.linked();sites=[r['mz_segment_relocation_image_offset']for r in fields if'mz_segment_relocation_image_offset'in r];self.assertEqual(sorted(sites),[0x7e22,0x82d0,0x82e6,0x837c])
  for base in [0,1,4096,65535]:
   a=bytearray(code);b=bytearray(self.reference['image'][0x7c52:0x85c4])
   for site in sites:
    at=site-0x7c52
    for buf in (a,b):buf[at:at+2]=((int.from_bytes(buf[at:at+2],'little')+base)&65535).to_bytes(2,'little')
   self.assertEqual([i for i,(x,y)in enumerate(zip(a,b))if x!=y],[1215,1539,1594])
 def test_wrong_source_flags_owner_or_extent_rejected(self):
  for c in [{'source':'src/shared_turn_book_context_match.c'},{'flags':['/AS','/Zi']},{'size':140},{'size':141.0},{'symbol':'_shift_state'},{'image_offset':'0x7c9a'},{'owned_data':{}}]:
   with self.assertRaises(ValueError):mixed.validate_unit_metadata(dict(self.unit,**c))
 def test_wrong_pool_size_placement_bool_or_target(self):
  for c in [{'size':2},{'size':78.0},{'group':True},{'image_offset':'0x619c8'},{'target_symbol':'_graphics_copy'},{'fake':0}]:
   with self.assertRaises(ValueError):self.layout(d=dict(self.unit['owned_selector_const'],**c))
 def test_exact_binding_map_no_removed_alias_reintroduced(self):
  for c in [{'key':'_alternate_prompt','value':0x4da8},{'key':'_splash_buffer','value':{'segment':0x1f0a,'offset':0}},{'key':'_current_side','value':True}]:
   e=copy.deepcopy(self.unit['externals']);e[c['key']]=c['value']
   with self.assertRaises(ValueError):self.layout(e=e)
 def test_literal_missing_extra_or_wrong_written_byte(self):
  self.bad(lambda o:setattr(o.segments[3],'length',80));self.bad(lambda o:o.segments[3].chunks.pop());self.bad(lambda o:o.segments[3].chunks.append((78,b'\0')))
  def wrong(o):at,b=o.segments[3].chunks[0];o.segments[3].chunks[0]=(at,bytes([b[0]^1])+b[1:])
  self.bad(wrong)
 def test_raw_chunk_order_not_sorted_away(self):self.bad(lambda o:setattr(o.segments[3],'chunks',list(reversed(o.segments[3].chunks))))
 def test_literal_field_target_frame_or_addend_changed(self):
  for c in [{'frame':(5,None)},{'target':(0,2)},{'width':4}]:
   def wrong(o):i=next(i for i,f in enumerate(o.fixups)if f.offset==581 and f.segment==1);o.fixups[i]=dataclasses.replace(o.fixups[i],**c)
   self.bad(wrong)
 def test_CODE_tail_and_foreign_loaded_DATA_or_COMMON_rejected(self):
  self.bad(lambda o:setattr(o.segments[1],'length',2419));self.bad(lambda o:setattr(o.segments[2],'length',2));self.bad(lambda o:o.records.append((0xb0,0,b'\0')))
 def test_all_PUBLIC_CV_and_debug_records_rejected_on_mutation(self):
  self.bad(lambda o:o.publics.update(_alias=next(iter(o.publics.values()))));self.bad(lambda o:o.procedures['_setup_state'].update(length=140));self.bad(lambda o:o.data_writes.pop())
 def test_previous_selector2_context_still_positive_newcross_rejected(self):
  import shared_turn_book_selector2418 as old
  u=json.loads((F/'previous-unit.json').read_text());o=read_omf((F/'previous2418.obj').read_bytes());self.assertEqual(old.validate_layout(o,u['owned_selector_const'],u['externals']),0x4da6)
  with self.assertRaises(ValueError):self.layout(o)
  with self.assertRaises(ValueError):old.validate_layout(self.obj(),u['owned_selector_const'],u['externals'])
 def test_skip_new_kind_oldkind_notaccepted(self):
  u=copy.deepcopy(next(u for u in self.units if u['symbol']=='_skip_book_8577'));u['extended_extent']['kind']='shared_book_skip_8577_v1'
  with self.assertRaises(ValueError):mixed.validate_unit_metadata(u)
 def test_alternate_view_preserves_existing_native_switch_extent(self):
  from extent import validate_extended_extent
  u=next(u for u in self.units if u['symbol']=='_alternate_view');o=self.obj();b,_=link_function(o,u['symbol'],int(u['image_offset'],0),u['externals'],owned_selector_const=u['owned_selector_const']);p=validate_extended_extent(u,M,self.reference['original_sha256'],o.function_info(u['symbol']),b,o);self.assertTrue(p)
 def test_new_skip_dispatch_complete22_and_four_fields(self):
  from extent import validate_extended_extent
  u=next(u for u in self.units if u['symbol']=='_skip_book_8577');o=self.obj();b,_=link_function(o,u['symbol'],int(u['image_offset'],0),u['externals'],owned_selector_const=u['owned_selector_const']);p=validate_extended_extent(u,M,self.reference['original_sha256'],o.function_info(u['symbol']),b,o);self.assertEqual(p['kind'],'shared_book_skip_literals78_8577_v1');self.assertEqual(sorted(f.offset-2341 for f in o.function_info(u['symbol'])['fixups']),[3,7,11,16])
 def test_collector_full78_accounts_only_selector_site_zero_DATAcredit(self):
  from owned_context_mz import collect_owned_context_mz
  rows=[]
  for u in self.units:
   if not u.get('owned_selector_const'):continue
   _,_,proof=dispatch.validate(u,self.obj(),M,self.reference);rows.append(dict(u,status='c_matched',source_sha256='8647747ee40d0778b16a74618dc6a9556db8192e766031d7a875d37e81ad60db',object_sha256='1163a5c8e4e05e565805bda572a771b63e61343f9bc6bbcb68c8ff9512768c50',object_artifact=str((F/'actual.obj').resolve()),owned_selector_const_proof=proof))
  p=collect_owned_context_mz(rows,M,self.reference,self.reference['relocations']);self.assertEqual(p['sites'],[0x619c6]);self.assertEqual((p['byte_credit'],p['function_credit']),(0,0));self.assertEqual(len(p['matched_owner_units']),7)
  with self.assertRaises(ValueError):collect_owned_context_mz(rows+[rows[0]],M,self.reference,self.reference['relocations'])
  rows[0]['owned_selector_const_proof']['source_data_credit']=76
  with self.assertRaises(ValueError):collect_owned_context_mz(rows,M,self.reference,self.reference['relocations'])
 def test_no_generation_or_sourceobject_mutation_in_structural_helper(self):
  o=self.obj();before=copy.deepcopy(o.__dict__);mixed.validate_shared_object(o);self.assertEqual(o.__dict__,before)
 def test_new_genuine_source_hash_checked_postgeneration(self):
  original=Path.read_bytes
  def change(p,*a,**k):
   b=original(p,*a,**k);return b+b' 'if p.name=='shared_turn_book_literals_match.c'else b
  with patch.object(Path,'read_bytes',change),self.assertRaises(ValueError):dispatch.validate(self.unit,self.obj(),M,self.reference)
 def test_actual_source_generation_one_call_twenty_denials(self):
  g=json.loads((M/'evidence/shared_turn_book_literals78/generation-receipt.json').read_text());self.assertEqual(g['actual_C5_calls'],1);self.assertEqual(len(g['blocked_probes']),20);self.assertTrue(g['guard_closed']);self.assertTrue(g['source_tools_new_scratch_only']);self.assertFalse(g['native_original_oldOBJ_comparison_inputs_inside_GEN']);self.assertEqual(g['raw_whole_object_sha256'],'1163a5c8e4e05e565805bda572a771b63e61343f9bc6bbcb68c8ff9512768c50');self.assertTrue(all(c['terminal']and c['reaped']and c['returncode']==0 for c in g['calls']))
 def test_changed_reference_pool_literal_or_held_byte_rejected(self):
  for at in [0x619c8,0x619ff,0x8111]:
   r=dict(self.reference);b=bytearray(r['image']);b[at]^=1;r['image']=bytes(b)
   with self.assertRaises(ValueError):dispatch.validate(self.unit,self.obj(),M,r)
if __name__=='__main__':unittest.main()
