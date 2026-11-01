"""Closed arena context mutations; actual source-produced objects only."""
from pathlib import Path
import sys,json,copy,dataclasses,unittest
M=Path(__file__).resolve().parents[1];D=M/'build/arena-literal-ownership-stage';sys.path.insert(0,str(M))
import owned_arena_literal_const16 as arena,owned_literal_const16 as dispatch
import owned_const16
from omf import read_omf,OMFError,Public
from reference import build_reference,validate_expanded_read
from link16 import link_function
assert Path(dispatch.__file__).resolve()==M/'owned_literal_const16.py'
assert Path(arena.__file__).resolve()==M/'owned_arena_literal_const16.py'
assert Path(owned_const16.__file__).resolve()==M/'owned_const16.py'
class ArenaControls(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.raw=(M/'build/arena-literal65-context/positive-final.obj').read_bytes();c.obj=read_omf(c.raw)
  c.units=json.loads((D/'proposed-units.json').read_text());c.owners=[u for u in c.units if u.get('owned_const')];c.unit=c.owners[0]
  c.reference=build_reference((M.parent/'CHESS.EXE').read_bytes());c.primary=json.loads((M/'build/arena-literal65-context/rea-whole-code1244.json').read_text())
 def test_five_owners_six_procedures_full1244_tail65_no_mutation_credit(self):
  before=copy.deepcopy(self.obj)
  for u in self.owners:
   desc,pool,p=owned_const16.validate(u,self.obj,M,self.reference)
   self.assertEqual(len(pool),65);self.assertEqual(len(p['whole_CODE_scopes']),6);self.assertEqual(p['whole_CODE_size'],1244)
   self.assertEqual(p['whole_CODE_CV_bytes'],1243);self.assertEqual(p['whole_CODE_fields'],137)
   self.assertEqual(p['whole_CODE_MZ_sites'],[14008,14111,14586,14962]);self.assertEqual(p['source_data_credit'],0)
   self.assertEqual(p['uncredited_source_CODE_tail'],{'offset':1243,'size':1,'bytes_hex':'90','original_primary_exact':True,'matching_credit':0})
   self.assertFalse(p['standalone_source_link_layout_proved']);self.assertEqual(p['four_forward_load_bases'],[0,1,0x1000,0xffff])
  self.assertEqual(self.obj,before)
 def test_missing_profile_still_ordinary_rejects_other_owners(self):
  u=dict(self.unit);u.pop('owned_const_profile')
  with self.assertRaises(OMFError):owned_const16.validate(u,self.obj,M,self.reference)
 def test_default_lowlevel_rejects_without_optin(self):
  with self.assertRaises(OMFError):link_function(self.obj,self.unit['symbol'],int(self.unit['image_offset'],0),self.unit['externals'])
 def test_unknown_profile_nonowner_and_wrong_extent_flags_fail(self):
  for changes in [{'owned_const_profile':'arena_messages_1244_v2'},{'symbol':'_cache_asset_frame'},{'size':34},{'flags':['/AS','/Os','/Zi']},{'code_address':{'segment':0,'offset':0}},{'owned_data':{}},{'owned_bss':{}},{'extended_extent':{}},{'owned_selector_const':{}}]:
   with self.subTest(changes=changes),self.assertRaises(OMFError):dispatch.validate_unit_metadata(dict(self.unit,**changes))
 def test_descriptor_boolean_size_origin_group_alias_rejected(self):
  for key,value in [('segment',True),('size',64),('image_offset','0x61969'),('group',2),('extra',0),('rea_evidence','wrong.json')]:
   u=copy.deepcopy(self.unit);u['owned_const'][key]=value
   with self.subTest(key=key),self.assertRaises(OMFError):arena.validate_unit_metadata(u)
 def test_external_union_missing_extra_literal_or_BASE16_segment_drift_rejected(self):
  for label in ['missing','literal','drift','absolute']:
   u=copy.deepcopy(self.unit)
   if label=='missing':u['externals'].pop(next(iter(u['externals'])))
   elif label=='literal':u['externals']['_arena_exhausted_message']=0x4d48
   elif label=='absolute':u['externals']['__AHSHIFT']={'absolute':13}
   else:
    name=next(n for n,v in u['externals'].items()if isinstance(v,dict)and 'segment'in v);u['externals'][name]['segment']+=1
   with self.subTest(label=label),self.assertRaises(OMFError):arena.validate_unit_metadata(u)
 def test_all65_pool_byte_mutations_rejected(self):
  for i in range(65):
   o=copy.deepcopy(self.obj);b=bytearray(o.segments[3].chunks[0][1]);b[i]^=1;o.segments[3].chunks=[(0,bytes(b))]
   with self.subTest(i=i),self.assertRaises(OMFError):arena.validate_layout(self.unit,o)
 def test_all181_raw_fields_rejected_when_parsed_model_changed(self):
  for i,f in enumerate(self.obj.fixups):
   o=copy.deepcopy(self.obj);o.fixups[i]=dataclasses.replace(f,offset=f.offset+1)
   with self.subTest(i=i),self.assertRaises(OMFError):arena.validate_layout(self.unit,o)
 def test_actual_tail90_changed_removed_extended_or_slice_size_fails(self):
  for label in ['change','remove','extend','CV']:
   o=copy.deepcopy(self.obj)
   if label=='change':o.segments[1].chunks[-1]=(1243,b'\x91')
   elif label=='remove':o.segments[1].chunks.pop();o.segments[1].length-=1
   elif label=='extend':o.segments[1].chunks.append((1244,b'\x90'));o.segments[1].length+=1
   else:o.procedures.clear()
   with self.subTest(label=label),self.assertRaises(OMFError):arena.validate_layout(self.unit,o)
 def test_foreign_allocations_CONST_alias_fixup_LIDATA_and_holes_fail(self):
  for label in ['DATA','BSS','alias','fixup','iterated','hole','overlap','record']:
   o=copy.deepcopy(self.obj)
   if label=='DATA':o.segments[2].length=1
   elif label=='BSS':o.segments[4].length=2
   elif label=='alias':o.publics['_fake']=Public('_fake',3,0,1,0)
   elif label=='fixup':o.fixups.append(dataclasses.replace(o.fixups[0],segment=3,offset=0))
   elif label=='iterated':o.segments[3].unsupported_data=True
   elif label=='hole':o.segments[3].chunks=[(1,o.segments[3].chunks[0][1][1:])]
   elif label=='overlap':o.segments[3].chunks.append((64,b'\0'))
   else:o.records.pop()
   with self.subTest(label=label),self.assertRaises(OMFError):arena.validate_layout(self.unit,o)
 def test_genuine_wrong_literal_same_fullCODE_and_pool_reject(self):
  wrong=read_omf((M/'build/arena-literal65-context/wrong-literal-final.obj').read_bytes())
  self.assertEqual(wrong.segments[1].chunks,self.obj.segments[1].chunks)
  with self.assertRaises(OMFError):arena.validate_layout(self.unit,wrong)
  desc=self.unit['owned_const'];e=json.loads((M/desc['rea_evidence']).read_text())
  with self.assertRaises(ValueError):validate_expanded_read(e,dict(desc,reference_region='exepack-expanded'),wrong.segments[3].chunks[0][1],self.reference)
 def test_original_static_read_must_NOT_be_rebased_as_inner_loaded(self):
  desc,pool,fields,raw=arena._layout(self.unit,self.obj);code=bytearray(raw)
  for u in self.units:
   i=self.obj.function_info(u['symbol']);body,_=link_function(self.obj,u['symbol'],int(u['image_offset'],0),u['externals'],owned_const=u.get('owned_const'));code[i['offset']:i['end']]=body
  self.assertTrue(arena._primary_code(self.primary,bytes(code),self.reference))
  loaded=copy.deepcopy(self.primary);b=bytearray.fromhex(loaded['normalized_result']['bytes_hex'])
  for site in [14008,14111,14586,14962]:
   at=site-0x3652;b[at:at+2]=((int.from_bytes(b[at:at+2],'little')+0x1000)&65535).to_bytes(2,'little')
  loaded['normalized_result']['bytes_hex']=b.hex()
  with self.assertRaises(OMFError):arena._primary_code(loaded,bytes(code),self.reference)
 def test_raw_full1244_primary_wrong_lastbyte_length_profile_and_subject_fail(self):
  native=self.reference['image'][0x3652:0x3b2e]
  for label in ['tail','length','address','load','subject']:
   e=copy.deepcopy(self.primary)
   if label=='tail':e['normalized_result']['bytes_hex']=e['normalized_result']['bytes_hex'][:-2]+'91'
   elif label=='length':e['normalized_result']['returned_bytes']=1243
   elif label=='address':e['parameters']['address']='0x13653'
   elif label=='load':e['analysis_profile']['parameters']['load_segment']='0x1001'
   else:e['subject']['digest']['sha256']='0'*64
   with self.subTest(label=label),self.assertRaises(OMFError):arena._primary_code(e,native,self.reference)
 def test_missing_extra_CODE_MZ_and_corrupt_wholeCODE_reject(self):
  for label in ['missing','extra','code']:
   r=copy.deepcopy(self.reference)
   if label=='missing':r['relocations']=tuple(s for s in r['relocations']if s!=14008)
   elif label=='extra':r['relocations']=tuple(r['relocations'])+(0x3654,)
   else:b=bytearray(r['image']);b[0x3b2d]^=1;r['image']=bytes(b)
   with self.subTest(label=label),self.assertRaises(OMFError):arena.validate(self.unit,self.obj,M,r)
 def test_nonreferencing_cache_cannot_gain_owned_pool_credit(self):
  u=copy.deepcopy(next(u for u in self.units if u['symbol']=='_cache_asset_frame'));u.update(owned_const_profile=arena.PROFILE,owned_const=self.unit['owned_const'])
  with self.assertRaises(OMFError):dispatch.validate_unit_metadata(u)
 def test_raw_checksum_corruption_rejects(self):
  raw=bytearray(self.raw);raw[-1]^=1
  with self.assertRaises(OMFError):read_omf(bytes(raw))
if __name__=='__main__':unittest.main()
