"""Focused comparison-only controls for genuine asset drive literal158."""
from pathlib import Path
import sys,json,copy,dataclasses,unittest
from unittest.mock import patch
M=Path(__file__).resolve().parents[1];sys.path.insert(0,str(M));F=M/'tests/fixtures/asset_drive_literals158'
from omf import read_omf
from reference import build_reference
from link16 import link_function
import owned_asset_drive_literal_const16 as asset
import owned_literal_const16 as dispatch
class AssetDriveLiteral158Tests(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.raw=(F/'actual.obj').read_bytes();c.units=json.loads((F/'units9.json').read_text());c.unit=next(u for u in c.units if u['symbol']=='_load_asset_index');c.reference=build_reference((M.parent/'CHESS.EXE').read_bytes())
 def obj(self):return read_omf(self.raw)
 def layout(self,o=None,u=None):return asset.validate_layout(self.unit if u is None else u,self.obj()if o is None else o)
 def bad(self,fn):
  o=self.obj();fn(o)
  with self.assertRaises(ValueError):self.layout(o)
 def test_complete_nine_CV_CODE1036_CONST158_fields121(self):
  o=self.obj();p=asset.validate_shared_object(o);self.assertEqual(len(o.publics),9);self.assertEqual(len(o.procedures),9);self.assertEqual([sum(f.segment==s for f in o.fixups)for s in [1,3,5]],[89,0,32]);self.assertEqual(sum(u['size']for u in self.units),1036)
 def test_full158_native_pool_and_all9_CODE_zero_contextcredit(self):
  d,b,p=dispatch.validate(self.unit,self.obj(),M,self.reference);self.assertEqual(len(b),158);self.assertEqual(b,self.reference['image'][0x61cde:0x61d7c]);self.assertEqual(p['whole_CODE_size'],1036);self.assertEqual(p['whole_CODE_fields'],89);self.assertEqual(p['whole_CODE_MZ_sites'],[51483,51654,52257]);self.assertEqual(p['four_forward_load_bases'],[0,1,4096,65535]);self.assertEqual((p['source_data_credit'],p['authored_c_function_count']),(0,0))
 def test_three_consuming_owners_including_new_load(self):
  owners=[u for u in self.units if u.get('owned_const')];self.assertEqual({u['symbol']for u in owners},asset.OWNERS)
  for u in owners:dispatch.validate_unit_metadata(u)
  for n in ['_dispatch_c83a','_read_asset','_probe_asset_file']:
   with self.assertRaises(ValueError):asset.validate_unit_metadata(dict(self.unit,symbol=n))
 def test_prefix46_and_old112_no_padding_or_alias_PUBLIC(self):
  d,b,refs=self.layout();self.assertEqual(len(b[:46]),46);self.assertEqual(len(b[46:]),112);self.assertEqual(b[46:],self.reference['image'][0x61d0c:0x61d7c]);self.assertEqual(self.obj().segments[3].chunks,[(0,b)]);self.assertFalse(any(p.segment==3 for p in self.obj().publics.values()))
 def test_all_nine_consumed_offsets_and_raw_chronology(self):
  o=self.obj();d,b,refs=self.layout(o);self.assertEqual(refs,[(416,0),(439,9),(472,37),(582,46),(602,55),(681,64),(733,88),(752,115),(839,144)]);self.assertEqual([f.offset for f in o.fixups if f.target==(0,3)],[472,439,416,752,733,681,602,582,839])
 def test_three_old_externs_absent_from_RAW_and_bindings(self):
  names={'_asset_drive_file','_asset_drive_error','_asset_drive_second_file'};self.assertTrue(names.isdisjoint(self.obj().externals.values()))
  for u in self.units:self.assertTrue(names.isdisjoint(u['externals']))
 def test_all9_registered_native_hashes_and_exact89_logs(self):
  o=self.obj();code=bytearray();fields=[]
  for u in self.units:
   b,f=link_function(o,u['symbol'],int(u['image_offset'],0),u['externals'],**({'owned_const':u['owned_const']}if u.get('owned_const')else{}));self.assertEqual(b,self.reference['image'][int(u['image_offset'],0):int(u['image_offset'],0)+u['size']]);code.extend(b);fields.extend(f)
  self.assertEqual((len(code),len(fields)),(1036,89))
 def test_old112_gate_and_fixture_unchanged_crossrejected(self):
  u=json.loads((F/'legacy-unit.json').read_text());o=read_omf((F/'legacy112.obj').read_bytes());d,b,_=dispatch.validate_layout(u,o);self.assertEqual(len(b),112)
  with self.assertRaises(ValueError):self.layout(o)
  with self.assertRaises(ValueError):dispatch.validate_layout(u,self.obj())
 def test_metadata_source_flags_identity_and_foreign_profile(self):
  for c in [{'source':'src/asset_dispatch_file_context_match.c'},{'flags':['/AS','/Gs','/Os','/Zi']},{'owned_const_profile':'asset_messages_1036_v1'},{'id':'alias'},{'size':133},{'size':134.0},{'owned_selector_const':{}},{'extended_extent':{}}]:
   with self.assertRaises(ValueError):asset.validate_unit_metadata(dict(self.unit,**c))
 def test_descriptor_size112_shifted_placement_bool_or_extra(self):
  for c in [{'size':112},{'size':158.0},{'group':True},{'image_offset':'0x61d0c'},{'data_address':{'segment':0x5cc2,'offset':0x50ec}},{'fake':1}]:
   u=copy.deepcopy(self.unit);u['owned_const'].update(c)
   with self.assertRaises(ValueError):self.layout(u=u)
 def test_external_numeric_type_or_reintroduced_alias(self):
  for operation in ['change','extra']:
   u=copy.deepcopy(self.unit)
   if operation=='extra':u['externals']['_asset_drive_file']=0x50be
   else:
    k=next(k for k,v in u['externals'].items()if type(v)is int);u['externals'][k]=float(u['externals'][k])
   with self.assertRaises(ValueError):self.layout(u=u)
 def test_whole_CODE_tail_missing_or_foreign_storage(self):
  self.bad(lambda o:setattr(o.segments[1],'length',1037));self.bad(lambda o:o.segments[1].chunks.pop());self.bad(lambda o:setattr(o.segments[2],'length',2));self.bad(lambda o:setattr(o.segments[4],'length',2))
 def test_prefix_literal_and_old_pool_bytes_not_masked(self):
  for at in [0,9,37,46,157]:
   def change(o):a,b=o.segments[3].chunks[0];o.segments[3].chunks[0]=(a,b[:at]+bytes([b[at]^1])+b[at+1:])
   self.bad(change)
 def test_no_holes_overlaps_trimming_or_CONST_fixups(self):
  self.bad(lambda o:setattr(o.segments[3],'length',160));self.bad(lambda o:setattr(o.segments[3],'chunks',[(2,b'\0'*156)]));self.bad(lambda o:o.segments[3].chunks.append((0,b'\0')))
  def change(o):o.fixups.append(dataclasses.replace(o.fixups[0],segment=3,offset=0))
  self.bad(change)
 def test_own_reference_target_frame_width_addend(self):
  for c in [{'frame':(5,None)},{'target':(0,2)},{'width':4}]:
   def change(o):i=next(i for i,f in enumerate(o.fixups)if f.segment==1 and f.offset==416);o.fixups[i]=dataclasses.replace(o.fixups[i],**c)
   self.bad(change)
 def test_raw_record_order_PUBLIC_CV_and_type_graph_bound(self):
  self.bad(lambda o:setattr(o,'records',list(reversed(o.records))));self.bad(lambda o:o.publics.update(_alias=next(iter(o.publics.values()))));self.bad(lambda o:o.procedures['_load_asset_index'].update(length=133));self.bad(lambda o:setattr(o.segments[6],'chunks',[(0,b'\0'*o.segments[6].length)]))
 def test_debug_patch_and_raw121_fields_not_discarded(self):
  self.bad(lambda o:o.data_writes.pop());self.bad(lambda o:o.fixups.pop());self.bad(lambda o:setattr(o.segments[5],'chunks',list(reversed(o.segments[5].chunks))))
 def test_source_profile_and_native_primary_hash_checked(self):
  original=Path.read_bytes
  for name in ['asset_dispatch_drive_literals_match.c','asset_drive_literal158_profile.json','pool158.json']:
   def change(p,*a,**k):b=original(p,*a,**k);return b+b' 'if p.name==name else b
   with patch.object(Path,'read_bytes',change),self.assertRaises(ValueError):dispatch.validate(self.unit,self.obj(),M,self.reference)
 def test_reference_wrong_literal_or_CODE_rejected(self):
  for at in [0x61cde,0x61d0c,0xc83a]:
   r=dict(self.reference);b=bytearray(r['image']);b[at]^=1;r['image']=bytes(b)
   with self.assertRaises(ValueError):dispatch.validate(self.unit,self.obj(),M,r)
 def test_structural_no_target_fixture_reads_or_object_mutation(self):
  o=self.obj();before=copy.deepcopy(o.__dict__);original=Path.read_bytes
  def guard(p,*a,**k):
   if p.name!='asset_drive_literal158_profile.json':raise AssertionError('Unexpected structural read')
   return original(p,*a,**k)
  with patch.object(Path,'read_bytes',guard):asset.validate_shared_object(o)
  self.assertEqual(o.__dict__,before)
 def test_json_key_view_and_duplicate_key_rejection(self):
  v={1:0,2:2,10:9};self.assertEqual(asset.canonical(v),asset.canonical(json.loads(json.dumps(v))));self.bad(lambda o:o.externals.update({'1':o.externals[1]}))
 def test_actual_one_C5_twenty_denials_closed_sourceonly(self):
  g=json.loads((M/'evidence/asset_drive_literals158/generation-receipt.json').read_text());self.assertEqual(g['actual_C5_calls'],1);self.assertEqual(len(g['blocked_probes']),20);self.assertTrue(g['guard_closed']);self.assertTrue(g['source_tools_new_scratch_only']);self.assertFalse(g['native_original_oldOBJ_comparison_inputs_inside_GEN']);self.assertEqual(g['raw_whole_object_sha256'],'2c51681185a687e74828f4f38031d4a94ee674c7c5c40e564283a80840cb91d0')
if __name__=='__main__':unittest.main()
