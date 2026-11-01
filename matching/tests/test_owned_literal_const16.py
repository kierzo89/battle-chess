"""Canonical fail-closed multi-owner literal gates; independent retained fixtures."""
import copy
import dataclasses
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
PROJECT=Path(__file__).resolve().parents[1]
M=PROJECT
D=M/'build/asset-literal-const-stage'
sys.path.insert(0,str(M))
import owned_literal_const16 as gate
import owned_const16
import check
for _module in (gate, owned_const16, check):
 assert Path(_module.__file__).resolve() == M/(_module.__name__+'.py'), \
  'Ownership tests require actual promoted canonical modules: '+str(_module.__file__)
from omf import read_omf,Public,OMFError
from reference import build_reference
from link16 import link_function,LinkError

class LiteralTests(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.raw=(M/'build/asset-message-data-context/literal-owner-final.obj').read_bytes();c.obj=read_omf(c.raw)
  c.units=json.loads((D/'proposed-units.json').read_text());c.owners=[u for u in c.units if u.get('owned_const')]
  c.unit=c.owners[0];c.reference=build_reference((M.parent/'CHESS.EXE').read_bytes())
 def test_complete_two_owners_nine_scopes_no_mutations_or_data_credit(self):
  before=copy.deepcopy(self.obj)
  for unit in self.owners:
   descriptor,data,p=owned_const16.validate(unit,self.obj,M,self.reference)
   self.assertEqual(len(data),112);self.assertEqual(p['whole_CODE_size'],1036)
   self.assertEqual(len(p['whole_CODE_scopes']),9);self.assertEqual(p['whole_CODE_fields'],89)
   self.assertEqual(p['whole_CODE_MZ_sites'],[0xc91b,0xc9c6,0xcc21]);self.assertEqual(p['source_data_credit'],0)
   self.assertEqual(p['four_forward_load_bases'],[0,1,0x1000,0xeeff]);self.assertFalse(p['standalone_source_link_layout_proved'])
  self.assertEqual(before,self.obj)
 def test_unknown_missing_or_nonreferencing_profile_owner_rejected(self):
  for changes in ({'owned_const_profile':'unknown'},{'owned_const':None},{'symbol':'_read_asset'},{'size':51},
    {'flags':['/AS','/Gs','/Os','/Zi']},{'code_address':{'segment':0,'offset':0}},
    {'owned_data':{}},{'extended_extent':{}},{'owned_bss':{}},{'owned_selector_const':{}}):
   with self.subTest(changes=changes),self.assertRaises(OMFError):gate.validate_unit_metadata(dict(self.unit,**changes))
 def test_descriptor_boolean_extra_wrong_placement_and_primary_rejected(self):
  for key,value in [('segment',True),('size',111),('image_offset','0x61d0d'),('group',2),('rea_evidence','other.json'),('data_address',{'segment':0x5cc2,'offset':0x50ed}),('extra',0)]:
   u=copy.deepcopy(self.unit);u['owned_const'][key]=value
   with self.subTest(key=key),self.assertRaises(OMFError):gate.validate_unit_metadata(u)
 def test_whole_external_dictionary_closed(self):
  for action in ('missing','extra','drift','absolute'):
   u=copy.deepcopy(self.unit)
   if action=='missing':u['externals'].pop('_read')
   if action=='extra':u['externals']['_asset_name_zero']=0x50ec
   if action=='drift':u['externals']['_read']+=1
   if action=='absolute':u['externals']['__AHSHIFT']={'absolute':13}
   with self.subTest(action=action),self.assertRaises(OMFError):gate.validate_unit_metadata(u)
 def test_each_const_byte_mutation_rejected(self):
  for at in range(112):
   o=copy.deepcopy(self.obj);b=bytearray(o.segments[3].chunks[0][1]);b[at]^=1;o.segments[3].chunks=[(0,bytes(b))]
   with self.subTest(at=at),self.assertRaises(OMFError):gate.validate_layout(self.unit,o)
 def test_every_raw_field_mutation_rejected(self):
  for at,f in enumerate(self.obj.fixups):
   o=copy.deepcopy(self.obj);o.fixups[at]=dataclasses.replace(f,offset=f.offset+1)
   with self.subTest(at=at),self.assertRaises(OMFError):gate.validate_layout(self.unit,o)
 def test_foreign_alloc_holes_tails_aliases_groups_communal_and_debug_tampering(self):
  for kind in ('hole','tail','overlap','BSS','DATA','alias','group','record','debug','CV','external','LIDATA'):
   o=copy.deepcopy(self.obj)
   if kind=='hole':o.segments[3].chunks=[(1,o.segments[3].chunks[0][1][1:])]
   elif kind=='tail':o.segments[3].length+=1
   elif kind=='overlap':o.segments[3].chunks.append((111,b'\0'))
   elif kind=='BSS':o.segments[4].length=2
   elif kind=='DATA':o.segments[2].length=2
   elif kind=='alias':o.publics['_alias']=Public('_alias',3,0,1,0)
   elif kind=='group':o.records=[(k,at,p[:-1]+b'\x01' if k==0x9a else p)for k,at,p in o.records]
   elif kind=='record':o.records.pop()
   elif kind=='debug':o.segments[6].chunks=[]
   elif kind=='CV':o.procedures.clear()
   elif kind=='external':o.externals[1]='_fake'
   elif kind=='LIDATA':o.segments[3].unsupported_data=True
   with self.subTest(kind=kind),self.assertRaises(OMFError):gate.validate_layout(self.unit,o)
 def test_record_checksum_authentication_rejects_raw_mutation(self):
  raw=bytearray(self.raw);raw[-1]^=1
  with self.assertRaises(OMFError):read_omf(bytes(raw))
 def test_no_opt_in_low_level_rejects_own_const(self):
  with self.assertRaises(LinkError):link_function(self.obj,self.unit['symbol'],int(self.unit['image_offset'],0),self.unit['externals'])
 def test_pure_layout_does_not_read_reference(self):
  with patch('reference.validate_expanded_read',side_effect=AssertionError('no target read')):
   self.assertEqual(len(gate.validate_layout(self.unit,self.obj)[1]),112)
 def test_full_code_reference_corruption_rejected(self):
  r=copy.deepcopy(self.reference);b=bytearray(r['image']);b[0xc83a]^=1;r['image']=bytes(b)
  with self.assertRaises(OMFError):gate.validate(self.unit,self.obj,M,r)
 def test_missing_or_extra_mz_rejected(self):
  for sites in ([s for s in self.reference['relocations'] if s!=0xc91b],list(self.reference['relocations'])+[0xc840]):
   with self.assertRaises(OMFError):gate.validate(self.unit,self.obj,M,dict(self.reference,relocations=sites))
 def test_wrong_original_carrier_or_const_bytes_rejected(self):
  for k in ('carrier_sha256','original_sha256'):
   with self.assertRaises(OMFError):gate.validate(self.unit,self.obj,M,dict(self.reference,**{k:'0'*64}))
  r=copy.deepcopy(self.reference);b=bytearray(r['image']);b[0x61d0c]^=1;r['image']=bytes(b)
  with self.assertRaises(OMFError):gate.validate(self.unit,self.obj,M,r)
 def test_ordinary_single_owner_fixture_unchanged(self):
  proposal=json.loads((M/'build/dialog-label-data/consumer-proposed-unit.json').read_text())['unit']
  proposal['owned_const']={'segment':3,'group':1,'size':24,'image_offset':'0x61dbb','data_address':{'segment':0x5cc2,'offset':0x519b},'rea_evidence':'evidence/rea-dialog-label-full24.json'}
  obj=read_omf((M/'build/dialog-label-data/literal-consumer-GsOs.obj').read_bytes())
  self.assertEqual(len(owned_const16.validate(proposal,obj,M,self.reference)[1]),24)
 def test_direct_build_unknown_profile_rejected_before_compile(self):
  import check
  with patch.object(check,'compile_c',side_effect=AssertionError('must fail before compiler')):
   with self.assertRaises(OMFError):check.build_unit(dict(self.unit,owned_const_profile='unknown'),self.reference['image'],M,'nasm',reference=self.reference)

if __name__=='__main__':unittest.main()
