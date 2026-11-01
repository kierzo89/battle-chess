"""Closed huge-char pointer DATA and unchanged near-pointer compatibility."""
import copy
import dataclasses
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
PROJECT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT))
import check
import screen_far_pointer_data16 as far
import cdata_pointer
import library16
from cdata import extract_data
from msc import compile_c
from omf import read_omf
from reference import build_reference,validate_expanded_read
FIXTURE=PROJECT/'build/screen-far-pointer-data-stage'

# Checksum-valid adversarial object construction is test input only. Production
# accepts unchanged compiler bytes, and never calls this mutation function.
def replace_record(data,kind,ordinal,transform):
 obj=read_omf(data);count=0;out=bytearray()
 for k,at,p in obj.records:
  raw=data[at:at+3+int.from_bytes(data[at+1:at+3],'little')]
  if k==kind:
   if count==ordinal:
    p=transform(p);prefix=bytes([k])+(len(p)+1).to_bytes(2,'little')+p;raw=prefix+bytes([-sum(prefix)&255])
   count+=1
  out.extend(raw)
 return bytes(out)

class ScreenFarPointerDataTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  assert Path(check.__file__).resolve()==PROJECT/'check.py'
  assert Path(far.__file__).resolve()==PROJECT/'screen_far_pointer_data16.py'
  cls.raw=(FIXTURE/'generated-0.obj').read_bytes()
  cls.ref=build_reference((PROJECT.parent/'CHESS.EXE').read_bytes())
  cls.primary=json.loads((PROJECT/'build/actor-text-screen-data/rea-screen.json').read_text())
  cls.unit=json.loads((FIXTURE/'proposed-unit.json').read_text())
  cls.production=json.loads((FIXTURE/'production-proof.json').read_text())
 def setUp(self):
  self.data=self.raw;self.bindings=copy.deepcopy(self.unit['externals']);self.origin=0x5d1ee
 def link(self):return far.link_data(self.data,'_screen',self.origin,0x5cc2,self.bindings)
 def test_complete_DATA4_PUBLIC0_huge_type_no_pointee(self):
  b,m=self.link();self.assertEqual(b.hex(),'404c0d12');self.assertEqual(m['segment']['length'],4)
  self.assertEqual(m['public']['type_index'],224);self.assertEqual(set(m['publics']),{'_screen'})
  self.assertFalse(m['pointee_allocated']);self.assertFalse(m['pointee_capacity_proved']);self.assertFalse(m['net_LINK_closure_claim'])
  self.assertEqual(m['debug']['validated_debug_fixups'],1);self.assertEqual(len(m['all_raw_fixups']),2);json.dumps(m)
 def test_native_MZ_scope_and_all_four_load_bases(self):
  b,m=self.link();validate_expanded_read(self.primary,self.unit,b,self.ref,emitted_mz_sites=m['emitted_mz_sites'])
  check.validate_emitted_mz_sites(dict(self.unit,relocations=m['relocations']),self.ref['relocations'])
  for base in [0,1,0x1000,0xffff]:
   a=bytearray(b);expected=bytearray(self.ref['image'][self.origin:self.origin+4])
   for raw in [a,expected]:raw[2:]=((int.from_bytes(raw[2:],'little')+base)&65535).to_bytes(2,'little')
   self.assertEqual(a,expected)
 def test_fresh_normal_positive_and_real_source_offset_negative(self):
  p=self.production;self.assertEqual(p['fresh_compiles'],2);self.assertTrue(p['no_handcrafted_cache'])
  self.assertEqual([r['status']for r in p['normal_production']],['c_data_matched','build_error'])
  self.assertEqual(p['normal_production'][0]['object_sha256'],hashlib.sha256(self.raw).hexdigest())
  self.assertEqual(len(p['blocked_target_carrier_reads']),4)
  self.assertNotEqual((FIXTURE/'generated-1.obj').read_bytes(),self.raw)
 def test_generation_and_decoder_have_no_target_reads(self):
  with patch.object(Path,'read_bytes',side_effect=AssertionError('unexpected filesystem read')),patch.object(Path,'read_text',side_effect=AssertionError('unexpected filesystem read')):
   b,m=self.link()
  self.assertEqual(b.hex(),'404c0d12')
 def test_wrong_offset_and_selector_each_fail_native_comparison(self):
  for key in ['offset','segment']:
   self.bindings=copy.deepcopy(self.unit['externals']);self.bindings['_screen_pixels'][key]+=1
   b,m=self.link()
   with self.subTest(key=key),self.assertRaises(ValueError):validate_expanded_read(self.primary,self.unit,b,self.ref,emitted_mz_sites=m['emitted_mz_sites'])
 def test_missing_wrong_duplicate_crossing_native_MZ_rejected(self):
  b,m=self.link()
  for sites in [[],[self.origin],[self.origin+2,self.origin+2],[self.origin+3]]:
   with self.subTest(sites=sites),self.assertRaises(ValueError):validate_expanded_read(self.primary,self.unit,b,self.ref,emitted_mz_sites=sites)
  with self.assertRaises(ValueError):check.validate_emitted_mz_sites(dict(self.unit,relocations=[]),self.ref['relocations'])
 def test_native_MZ_extra_or_omitted_reference_sites_fail(self):
  b,m=self.link()
  for sites in [set(self.ref['relocations'])-{self.origin+2},set(self.ref['relocations'])|{self.origin}]:
   r=dict(self.ref,relocations=sites)
   with self.assertRaises(ValueError):validate_expanded_read(self.primary,self.unit,b,r,emitted_mz_sites=m['emitted_mz_sites'])
 def test_bindings_are_exact_explicit_unsigned_words(self):
  for bindings in [{},{'_other':{'segment':1,'offset':2}},dict(self.bindings,extra={'segment':0,'offset':0}),{'_screen_pixels':0}, {'_screen_pixels':{'segment':True,'offset':1}},{'_screen_pixels':{'segment':65536,'offset':1}},{'_screen_pixels':{'segment':1,'offset':-1}},{'_screen_pixels':{'segment':1,'offset':2,'capacity':32000}}]:
   self.bindings=bindings
   with self.subTest(bindings=bindings),self.assertRaises(ValueError):self.link()
 def test_natural_WORD_origin_and_frame_bounds(self):
  for origin,frame in [(True,0x5cc2),(self.origin+1,0x5cc2),(self.origin,True),(0x5cc20-2,0x5cc2),(0x5cc20+65534,0x5cc2)]:
   with self.subTest(origin=origin,frame=frame),self.assertRaises(ValueError):far.link_data(self.data,'_screen',origin,frame,self.bindings)
 def test_resolver_shape_width_location_mode_frame_target_disp(self):
  f=read_omf(self.raw).fixups[0]
  for change in [{'width':2},{'location_type':1},{'location_type':2},{'segment_relative':False},{'frame':(1,1)},{'frame':(2,2)},{'target':(0,2)},{'target':(2,0)},{'displacement':0}]:
   with self.subTest(change=change),self.assertRaises(ValueError):far.resolve_external_far16(dataclasses.replace(f,**change),bytes(4),self.bindings['_screen_pixels'],self.origin)
 def test_real_offset_addend_preserved_and_overflow_rejected(self):
  self.data=(FIXTURE/'generated-1.obj').read_bytes();b,m=self.link();self.assertEqual(b.hex(),'414c0d12');self.assertEqual(m['relocations'][0]['original_addend'],1)
  self.bindings['_screen_pixels']['offset']=65535
  with self.assertRaisesRegex(ValueError,'overflow'):self.link()
 def test_selector_addend_is_not_ignored_or_normalized(self):
  self.data=replace_record(self.raw,0xa0,0,lambda p:p[:5]+b'\x01\0')
  with self.assertRaisesRegex(ValueError,'selector addend'):self.link()
 def test_every_initialized_byte_affects_output_or_rejects(self):
  baseline,_=self.link()
  for i in range(4):
   def mutate(p):
    b=bytearray(p);b[3+i]^=1;return bytes(b)
   self.data=replace_record(self.raw,0xa0,0,mutate)
   if i<2:self.assertNotEqual(self.link()[0],baseline)
   else:
    with self.assertRaises(ValueError):self.link()
 def test_checksum_bad_and_truncated_objects_reject(self):
  for data in [self.raw[:-1],self.raw+b'\0',bytes([self.raw[0]^1])+self.raw[1:]]:
   self.data=data
   with self.assertRaises(ValueError):self.link()
 def test_hole_overlap_and_uninitialized_tail_reject(self):
  controls=[(0xa0,0,lambda p:p[:1]+b'\x01\0'+p[3:]),(0xa0,0,lambda p:p[:-1]),(0xa0,0,lambda p:p+b'\0'),(0x98,1,lambda p:p[:1]+b'\x06\0'+p[3:])]
  for kind,n,fn in controls:
   self.data=replace_record(self.raw,kind,n,fn)
   with self.subTest(kind=kind),self.assertRaises(ValueError):self.link()
 def test_extra_CODE_CONST_BSS_allocation_rejects(self):
  for index in [0,2,3]:
   self.data=replace_record(self.raw,0x98,index,lambda p:p[:1]+b'\x02\0'+p[3:])
   with self.subTest(index=index),self.assertRaises(ValueError):self.link()
 def test_wrong_PUBLIC_extent_group_type_or_name_rejects(self):
  for transform in [lambda p:p[:10]+b'\x01\0'+p[12:],lambda p:p[:-2]+b'\x80\xa0',lambda p:b'\0'+p[1:],lambda p:p.replace(b'screen',b'SCREEN')]:
   self.data=replace_record(self.raw,0x90,0,transform)
   with self.assertRaises(ValueError):self.link()
 def test_duplicate_PUBLIC_alias_is_not_accepted(self):
  self.data=replace_record(self.raw,0x90,0,lambda p:p+p[2:])
  with self.assertRaises(ValueError):self.link()
 def test_foreign_or_extra_EXTDEF_and_debug_types_reject(self):
  for kind,n,fn in [(0x8c,0,lambda p:p.replace(b'screen_pixels',b'SCREEN_PIXELS')),(0x8c,0,lambda p:p[:-1]+b'\x02'),(0xa0,2,lambda p:p[:-1]+b'\x01')]:
   self.data=replace_record(self.raw,kind,n,fn)
   with self.assertRaises(ValueError):self.link()
 def test_wrong_or_overlapping_DATA_fields_reject(self):
  for fn in [lambda p:p[:1]+b'\x01'+p[2:],lambda p:p+p,lambda p:bytes.fromhex('c4005602'),lambda p:bytes.fromhex('cc005402'),lambda p:bytes.fromhex('cc005603')]:
   self.data=replace_record(self.raw,0x9c,1,fn)
   with self.assertRaises(ValueError):self.link()
 def test_foreign_debug_field_is_not_image_MZ(self):
  self.data=replace_record(self.raw,0x9c,2,lambda p:bytes.fromhex('cc025601'))
  with self.assertRaises(ValueError):self.link()
 def test_complete_DGROUP_and_RECORD_contract_rejects(self):
  for kind,n,fn in [(0x9a,0,lambda p:p[:-1]+b'\x01'),(0x88,0,lambda p:p+b'\0'),(0x80,0,lambda p:p.replace(b'UNIT.C',b'OTHERX')),(0x8a,0,lambda p:b'\x01')]:
   self.data=replace_record(self.raw,kind,n,fn)
   with self.assertRaises(ValueError):self.link()
 def test_unknown_unit_profile_alias_capacity_and_slice_reject(self):
  for patching in [{'object_profile':'other'},{'size':2},{'symbol':'_alias'},{'capacity':32000},{'slice':4},{'owned_const':None},{'code_address':None},{'flags':['/AM','/Zl','/Zi']}]:
   with self.subTest(patching=patching),self.assertRaises(ValueError):far.validate_unit(dict(self.unit,**patching))
 def test_registry_and_REA_routes_accept_only_actual_complete_profile(self):
  check.validate_units([self.unit],83415,len(self.ref['image']))
  self.assertTrue(check.validate_rea_extent(self.unit,PROJECT,self.ref['original_sha256'],self.ref))
  for patching in [{'data_address':{'segment':0x5cc1,'offset':0x5de}},{'externals':{'_screen_pixels':{'segment':1,'offset':2,'capacity':3}}}]:
   u=dict(self.unit,**patching)
   with self.assertRaises(ValueError):
    check.validate_units([u],83415,len(self.ref['image']));check.validate_rea_extent(u,PROJECT,self.ref['original_sha256'],self.ref)
 def test_compiler_source_tools_flags_identity_are_mandatory(self):
  p=self.production['normal_production'][0]
  from msc import CompileResult
  c=CompileResult(self.raw,p['compiler_log'],tuple(p['build_command']),p['source_sha256'],p['toolchain_manifest_sha256'],p['compiler_tool_hashes'],tuple(p['compiler_flags']),'msc500','UNIT.C')
  source=(FIXTURE/'implementation/screen.c').read_bytes();far.validate_compiled(c,source,self.unit)
  for change in [{'source_sha256':'0'*64},{'toolchain_manifest_sha256':'0'*64},{'tool_hashes':{}},{'flags':('/AS',)},{'source_name':'OTHER.C'},{'command':('fake',)}]:
   with self.subTest(change=change),self.assertRaises(ValueError):far.validate_compiled(dataclasses.replace(c,**change),source,self.unit)
  with self.assertRaises(ValueError):far.validate_compiled(c,source+b' ',self.unit)
 def test_original_near_pointer_and_library_gates_still_reject_FAR16(self):
  obj=read_omf(self.raw)
  with self.assertRaises(ValueError):extract_data(obj,'_screen')
  with self.assertRaisesRegex(ValueError,'OFFSET16'):cdata_pointer.link_pointer_data(obj,'_screen',self.origin,0x5cc2,{'_screen_pixels':0x4c40})
  with self.assertRaisesRegex(ValueError,'only OFFSET16 and BASE16'):library16.link_segment(obj,2,{2:(0x5cc2,0x5ce)},{1:0x5cc2},{'_screen_pixels':(0x120d,0x4c40)})

if __name__=='__main__':unittest.main(verbosity=2)
