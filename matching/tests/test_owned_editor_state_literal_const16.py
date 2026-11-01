"""Closed editor/state264 full-object controls; no source generation from target."""
from pathlib import Path
import sys,json,copy,dataclasses,unittest
M=Path(__file__).resolve().parents[1];D=M/'build/editor-state-literal-ownership-stage';sys.path.insert(0,str(M))
import owned_editor_state_literal_const16 as gate,owned_arena_literal_const16,owned_literal_const16 as dispatch
import owned_const16
from omf import read_omf,OMFError,Public
from reference import build_reference,validate_expanded_read
from link16 import link_function
assert Path(dispatch.__file__).resolve()==M/'owned_literal_const16.py'
assert Path(gate.__file__).resolve()==M/'owned_editor_state_literal_const16.py'
assert Path(owned_const16.__file__).resolve()==M/'owned_const16.py'
class EditorStateControls(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.raw=(M/'build/editor-state-literal264-context/positive-final.obj').read_bytes();c.obj=read_omf(c.raw)
  c.units=json.loads((D/'proposed-units.json').read_text());c.owners=[u for u in c.units if u.get('owned_const')];c.unit=c.owners[0]
  c.reference=build_reference((M.parent/'CHESS.EXE').read_bytes());c.primary=json.loads((M/'build/editor-state-literal264-context/rea-whole-code1554.json').read_text())
 def test_two_owners_14_CVs_complete1554_native90_264_uncredited(self):
  before=copy.deepcopy(self.obj)
  for u in self.owners:
   desc,pool,p=owned_const16.validate(u,self.obj,M,self.reference)
   self.assertEqual(len(pool),264);self.assertEqual(len(p['whole_CODE_scopes']),14)
   self.assertEqual((p['whole_CODE_size'],p['whole_CODE_CV_bytes'],p['whole_CODE_fields']),(1554,1553,174))
   self.assertEqual(p['whole_CODE_MZ_sites'],[]);self.assertEqual(p['source_data_credit'],0)
   self.assertEqual(p['uncredited_source_CODE_tail'],{'offset':1553,'size':1,'bytes_hex':'90','original_primary_exact':True,'matching_credit':0})
   self.assertFalse(p['standalone_source_link_layout_proved']);self.assertEqual(p['four_forward_load_bases'],[0,1,0x1000,0xffff])
  self.assertEqual(self.obj,before)
 def test_ordinary_missing_profile_and_lowlevel_default_reject(self):
  u=dict(self.unit);u.pop('owned_const_profile')
  with self.assertRaises(OMFError):owned_const16.validate(u,self.obj,M,self.reference)
  with self.assertRaises(OMFError):link_function(self.obj,self.unit['symbol'],int(self.unit['image_offset'],0),self.unit['externals'])
 def test_unknown_nonowner_size_flags_ownership_combinations_reject(self):
  for changes in [{'owned_const_profile':'editor_state_messages_1554_v2'},{'symbol':'_reset_state'},{'size':339},{'flags':['/AS','/Os','/Zi']},{'code_address':{'segment':0,'offset':0}},{'owned_data':{}},{'owned_bss':{}},{'extended_extent':{}},{'owned_selector_const':{}}]:
   with self.subTest(changes=changes),self.assertRaises(OMFError):dispatch.validate_unit_metadata(dict(self.unit,**changes))
 def test_descriptor_exact_closed_identity(self):
  for key,value in [('segment',True),('size',263),('image_offset','0x61a23'),('group',2),('extra',0),('rea_evidence','wrong.json')]:
   u=copy.deepcopy(self.unit);u['owned_const'][key]=value
   with self.subTest(key=key),self.assertRaises(OMFError):gate.validate_unit_metadata(u)
 def test_external_union_no_missing_alias_or_binding_drift(self):
  for label in ['missing','literal','drift']:
   u=copy.deepcopy(self.unit)
   if label=='missing':u['externals'].pop(next(iter(u['externals'])))
   elif label=='literal':u['externals']['_check_text']=0x4ed7
   else:u['externals']['_setup_state']+=1
   with self.subTest(label=label),self.assertRaises(OMFError):gate.validate_unit_metadata(u)
 def test_all264_pool_bytes_closed(self):
  for i in range(264):
   o=copy.deepcopy(self.obj);b=bytearray(o.segments[3].chunks[0][1]);b[i]^=1;o.segments[3].chunks=[(0,bytes(b))]
   with self.subTest(i=i),self.assertRaises(OMFError):gate.validate_layout(self.unit,o)
 def test_all237_raw_fields_closed(self):
  for i,f in enumerate(self.obj.fixups):
   o=copy.deepcopy(self.obj);o.fixups[i]=dataclasses.replace(f,offset=f.offset+1)
   with self.subTest(i=i),self.assertRaises(OMFError):gate.validate_layout(self.unit,o)
 def test_12_owner_addends_not_reassigned_between_owners(self):
  d,p,fields=gate.validate_layout(self.unit,self.obj)
  self.assertEqual(fields,[(123,0),(135,25),(147,51),(159,75),(171,100),(183,118),(236,137),(278,157),(322,178),(327,196),(621,213),(636,241)])
 def test_tail_change_remove_extend_and_CV_slice_reject(self):
  for label in ['change','remove','extend','CV']:
   o=copy.deepcopy(self.obj)
   if label=='change':o.segments[1].chunks[-1]=(1553,b'\x91')
   elif label=='remove':o.segments[1].chunks.pop();o.segments[1].length-=1
   elif label=='extend':o.segments[1].chunks.append((1554,b'\x90'));o.segments[1].length+=1
   else:o.procedures.clear()
   with self.subTest(label=label),self.assertRaises(OMFError):gate.validate_layout(self.unit,o)
 def test_extra_allocation_public_CONSTfixup_reserved_data_holes_record_fail(self):
  for label in ['DATA','BSS','alias','fixup','iterated','hole','overlap','record']:
   o=copy.deepcopy(self.obj)
   if label=='DATA':o.segments[2].length=1
   elif label=='BSS':o.segments[4].length=2
   elif label=='alias':o.publics['_fake']=Public('_fake',3,0,1,0)
   elif label=='fixup':o.fixups.append(dataclasses.replace(o.fixups[0],segment=3,offset=0))
   elif label=='iterated':o.segments[3].unsupported_data=True
   elif label=='hole':o.segments[3].chunks=[(1,o.segments[3].chunks[0][1][1:])]
   elif label=='overlap':o.segments[3].chunks.append((263,b'\0'))
   else:o.records.pop()
   with self.subTest(label=label),self.assertRaises(OMFError):gate.validate_layout(self.unit,o)
 def test_genuine_wrong_letter_CODEsame_pool_reject(self):
  wrong=read_omf((M/'build/editor-state-literal264-context/wrong-literal.obj').read_bytes())
  self.assertEqual(wrong.segments[1].chunks,self.obj.segments[1].chunks)
  with self.assertRaises(OMFError):gate.validate_layout(self.unit,wrong)
  desc=self.unit['owned_const'];e=json.loads((M/desc['rea_evidence']).read_text())
  with self.assertRaises(ValueError):validate_expanded_read(e,dict(desc,reference_region='exepack-expanded'),wrong.segments[3].chunks[0][1],self.reference)
 def test_full_primary_wrong_tail_length_load_address_subject_fail(self):
  native=self.reference['image'][0x8e36:0x9448]
  for label in ['tail','length','address','load','subject']:
   e=copy.deepcopy(self.primary)
   if label=='tail':e['normalized_result']['bytes_hex']=e['normalized_result']['bytes_hex'][:-2]+'91'
   elif label=='length':e['normalized_result']['returned_bytes']=1553
   elif label=='address':e['parameters']['address']='0x18e37'
   elif label=='load':e['analysis_profile']['parameters']['load_segment']='0x1001'
   else:e['subject']['digest']['sha256']='0'*64
   with self.subTest(label=label),self.assertRaises(OMFError):gate._primary_code(e,native,self.reference)
 def test_extra_MZ_and_corrupt_wholeCODE_reference_reject(self):
  for label in ['extra','code']:
   r=copy.deepcopy(self.reference)
   if label=='extra':r['relocations']=tuple(r['relocations'])+(0x8e38,)
   else:b=bytearray(r['image']);b[0x9447]^=1;r['image']=bytes(b)
   with self.subTest(label=label),self.assertRaises(OMFError):gate.validate(self.unit,self.obj,M,r)
 def test_nonowner_cannot_gain_pool(self):
  u=copy.deepcopy(next(u for u in self.units if u['symbol']=='_reset_state'));u.update(owned_const_profile=gate.PROFILE,owned_const=self.unit['owned_const'])
  with self.assertRaises(OMFError):dispatch.validate_unit_metadata(u)
 def test_editor213_descriptor_cannot_be_reused_or_duplicated(self):
  u=copy.deepcopy(self.unit);u['owned_const']['size']=213
  with self.assertRaises(OMFError):dispatch.validate_unit_metadata(u)
 def test_raw_checksum_corruption(self):
  raw=bytearray(self.raw);raw[-1]^=1
  with self.assertRaises(OMFError):read_omf(bytes(raw))
if __name__=='__main__':unittest.main()
