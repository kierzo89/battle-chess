"""Closed typed Blit24 profile, canonical-ready paths; ordinary gates remain strict."""
from pathlib import Path
from dataclasses import replace
import copy,json,struct,sys,tempfile,unittest
from unittest.mock import patch
PROJECT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(PROJECT))
import blit_prefix_data16 as d,check,buffer_data16
from cdata import extract_data as ordinary,CDataError
from omf import read_omf,OMFError
from msc import compile_c
from reference import build_reference,validate_expanded_read
assert Path(d.__file__).resolve()==PROJECT/'blit_prefix_data16.py'
assert Path(check.__file__).resolve()==PROJECT/'check.py'
STAGE=PROJECT/'build/blit-prefix-data-backend-stage';UP=PROJECT/'build/blit-data-owner-followup'
SOURCE=PROJECT/'src/data/blit_prefix.c'

def record(kind,p):
 h=bytes([kind])+struct.pack('<H',len(p)+1)+p;return h+bytes([-sum(h)&255])
def mutate(raw,index,p=None,kind=None):
 rows=list(read_omf(raw).records);k,_,old=rows[index];rows[index]=(k if kind is None else kind,0,old if p is None else p)
 return b''.join(record(k,p)for k,_,p in rows)

class BlitPrefixDataTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.raw=(UP/'prefix.obj').read_bytes();cls.rows=read_omf(cls.raw).records;cls.reference=build_reference((PROJECT.parent/'CHESS.EXE').read_bytes())
  cls.units=json.loads((STAGE/'proposed-data-units.json').read_text());cls.unit=cls.units[0];cls.evidence=json.loads((PROJECT/cls.unit['rea_evidence']).read_text())
 def reject(self,raw):
  with self.assertRaises((OMFError,ValueError)):d.extract_data(raw)
 def test_full_struct24_raw_leaf_and_10_meaningful_members(self):
  before=bytes(self.raw);b,m=d.extract_data(self.raw)
  self.assertEqual(b,bytes(24));self.assertEqual(before,self.raw);self.assertEqual(m['segment']['length'],24)
  self.assertEqual(m['public']['type_index'],0x203);self.assertEqual(m['cv']['struct_bit_size'],192)
  self.assertEqual([r['name']for r in m['cv']['members']],d.NAMES)
  self.assertEqual([r['offset']for r in m['cv']['members']],d.OFFSETS)
  self.assertEqual([r['type']for r in m['cv']['members']],['int']*8+['char huge *']*2)
  self.assertEqual(len(bytes.fromhex(m['cv']['raw_hex'])),183);self.assertEqual(m['data_writes'][1]['raw_payload'],'0202000b000000020000')
  self.assertTrue(m['all_segments'][1]['unsupported_data_retained']);self.assertEqual(m['emitted_mz_sites'],[])
  self.assertFalse(m['historical_aggregate_boundary_proven']);self.assertTrue(m['larger_historical_capacity_unknown']);self.assertFalse(m['six_gap_bytes_allocated'])
 def test_ordinary_and_buffer_gates_not_generalized(self):
  with self.assertRaisesRegex(CDataError,'LIDATA'):ordinary(read_omf(self.raw),'_blit')
  with self.assertRaises(ValueError):buffer_data16.extract_data(self.raw)
  self.reject((PROJECT/'build/huff-data-state/input512.obj').read_bytes())
  self.reject(read_omf(self.raw))
 def test_every_object_byte_and_checksum(self):
  for i in range(len(self.raw)):
   b=bytearray(self.raw);b[i]^=1
   with self.subTest(i=i):self.reject(bytes(b))
 def test_truncated_extra_modend_and_lengths(self):
  for raw in [self.raw[:-1],self.raw+b'\0',self.raw[:250],self.raw[:-5]]:self.reject(raw)
 def test_leaf_repeat_short_long_zero(self):
  for n in [0,1,10,12,65535]:
   p=bytearray(self.rows[16][2]);p[3:5]=struct.pack('<H',n);self.reject(mutate(self.raw,16,bytes(p)))
 def test_leaf_nested_malformed_literals(self):
  for at,value in [(5,1),(6,1),(7,0),(7,1),(7,3),(8,1),(9,1)]:
   p=bytearray(self.rows[16][2]);p[at]=value;self.reject(mutate(self.raw,16,bytes(p)))
 def test_leaf_trailing_truncated(self):
  p=self.rows[16][2]
  for q in [p+b'\0',p[:-1],p[:3]]:self.reject(mutate(self.raw,16,q))
 def test_foreign_leaf_holes_overlap(self):
  for segment,offset in [(1,2),(3,2),(2,0),(2,1),(2,3)]:
   p=bytearray(self.rows[16][2]);p[0]=segment;p[1:3]=struct.pack('<H',offset);self.reject(mutate(self.raw,16,bytes(p)))
 def test_real_first_word_required_no_filler(self):
  for p in [b'\x02\0\0',b'\x02\0\0\0',b'\x02\0\0\x01\0',b'\x02\x01\0\0\0',b'\x02\0\0\0\0\0\0']:self.reject(mutate(self.raw,15,p))
 def test_SEGDEF_whole_struct_not_expected_slice(self):
  for n in [0,22,26,32]:
   p=bytearray(self.rows[5][2]);p[1:3]=struct.pack('<H',n);self.reject(mutate(self.raw,5,bytes(p)))
  for at in [0,4,5]:
   p=bytearray(self.rows[5][2]);p[at]^=1;self.reject(mutate(self.raw,5,bytes(p)))
 def test_extra_CODE_CONST_BSS_and_debug_allocations(self):
  for index in [4,6,7,8]:
   p=bytearray(self.rows[index][2]);p[1:3]=b'\x02\0';self.reject(mutate(self.raw,index,bytes(p)))
 def test_CV_member_names_offsets_huge_pointer_and_structsize(self):
  for at in [17,19,33,60,74,84,161,182]:
   p=bytearray(self.rows[17][2]);p[3+at]^=1;self.reject(mutate(self.raw,17,bytes(p)))
 def test_PUBLIC_offset_group_type_name(self):
  for at in [0,1,3,8,10]:
   p=bytearray(self.rows[13][2]);p[at]^=1;self.reject(mutate(self.raw,13,bytes(p)))
  with self.assertRaises(ValueError):d.extract_data(self.raw,'_other')
 def test_extra_PUBLIC_COMMON_SEGDEF_group_or_data_record(self):
  for k,p in [(0xb0,b'\x05_fake\0\x62\x02'),(0x90,self.rows[13][2]),(0x98,self.rows[5][2]),(0x9a,self.rows[10][2]),(0xa0,b'\x02\x18\0\0')]:self.reject(self.raw[:-5]+record(k,p)+self.raw[-5:])
 def test_forbidden_fixups_external_directives_entry(self):
  for i,p in [(11,bytes.fromhex('c4005601')),(12,b'\x05_other\x01'),(1,b'\0\x9e'),(18,b'\x80'),(10,b'\x02\xff\x02')]:self.reject(mutate(self.raw,i,p))
 def test_closed_unit_no_ownership_or_placement_aliases(self):
  d.validate_unit(self.unit)
  for k,v in [('symbol','_other'),('size',22),('image_offset','0x61546'),('language','c'),('backend','msc500-data-omf'),('flags',['/AS']),('reference_region','unchanged-prefix'),('externals',{'x':1}),('owned_const',{}),('owned_data',{}),('owned_bss',{}),('owned_selector_const',{}),('extended_extent',{}),('data_address',{}),('compiler_source_name','OTHER.C')]:
   u=copy.deepcopy(self.unit);u[k]=v
   with self.subTest(key=k),self.assertRaises(ValueError):d.validate_unit(u)
 def test_source_change_rejected_before_generation(self):
  with tempfile.TemporaryDirectory()as td:
   p=Path(td)/'changed.c';p.write_bytes(SOURCE.read_bytes()+b' ')
   with patch.object(d,'compile_c',side_effect=AssertionError('must not compile')):
    with self.assertRaisesRegex(ValueError,'source fingerprint'):d.build(p)
 def test_source_symlink_rejected(self):
  with tempfile.TemporaryDirectory()as td:
   p=Path(td)/'alias.c';p.symlink_to(SOURCE)
   with self.assertRaisesRegex(ValueError,'symlink'):d.build(p)
 def test_tool_change_rejected_before_generation(self):
  with patch.object(d,'validate_toolchain',return_value=('0'*64,d.TOOL_HASHES)),patch.object(d,'compile_c',side_effect=AssertionError('must not compile')):
   with self.assertRaisesRegex(ValueError,'tool pins'):d.build(SOURCE)
 def test_fresh_source_only_generation_exact_wholeobject(self):
  b=d.build(SOURCE);self.assertEqual(b.object_bytes,self.raw);self.assertEqual(b.data,bytes(24));self.assertEqual(b.provenance['source_sha256'],d.SOURCE_SHA256)
 def test_fresh_provenance_rejects_all_profile_changes(self):
  c=compile_c(SOURCE,d.FLAGS,compiler='msc500')
  for changed in [replace(c,compiler='msc510'),replace(c,flags=('/AS','/Zi')),replace(c,source_sha256='0'*64),replace(c,toolchain_manifest_sha256='0'*64),replace(c,tool_hashes={}),replace(c,command=()),replace(c,source_name='OTHER.C')]:
   with self.assertRaises(ValueError):d.validate_compiled(changed,SOURCE.read_bytes())
 def test_primary_raw_complete_reference_and_each_byte(self):
  raw,_=d.extract_data(self.raw);validate_expanded_read(self.evidence,self.unit,raw,self.reference,emitted_mz_sites=[])
  at=int(self.unit['image_offset'],0);self.assertEqual(raw,self.reference['image'][at:at+24]);self.assertFalse(any(x<at+24 and x+2>at for x in self.reference['relocations']))
  for base in [0,1,0x1000,0xffff]:self.assertEqual(raw,self.reference['image'][at:at+24])
  for i in range(24):
   b=bytearray(raw);b[i]=1
   with self.assertRaises(ValueError):validate_expanded_read(self.evidence,self.unit,bytes(b),self.reference,emitted_mz_sites=[])
 def test_primary_wrong_subject_profile_extent_or_MZ(self):
  raw,_=d.extract_data(self.raw)
  for k in ['subject','profile','extent']:
   e=copy.deepcopy(self.evidence)
   if k=='subject':e['subject']['digest']['sha256']='0'*64
   elif k=='profile':e['analysis_profile']['parameters']['load_segment']='0x1001'
   else:e['parameters']['length']=23
   with self.assertRaises(ValueError):validate_expanded_read(e,self.unit,raw,self.reference,emitted_mz_sites=[])
  with self.assertRaises(ValueError):validate_expanded_read(self.evidence,self.unit,raw,self.reference,emitted_mz_sites=[int(self.unit['image_offset'],0)])
 def test_normal_production_prefix_and_saved_word(self):
  with tempfile.TemporaryDirectory()as td:
   cache={}
   for u in self.units:
    r=check.build_unit(u,self.reference['image'],PROJECT,'nasm',cache,Path(td),reference=self.reference)
    self.assertEqual(r['status'],'c_data_matched');self.assertEqual(r['relocations'],[]);check.validate_emitted_mz_sites(r,self.reference['relocations'])
 def test_coherent15_current_C_bodies_allfields_MZ_and_bindings(self):
  units=json.loads((STAGE/'proposed-code-units.json').read_text());check.validate_shared_external_bindings(json.loads((STAGE/'prospective-units.json').read_text()))
  text=(PROJECT/units[0]['source']).read_text();self.assertNotIn('reserved[3]',text);self.assertNotIn('blit.saved_word',text);self.assertIn('extern int blit_saved_word_4942;',text)
  with tempfile.TemporaryDirectory()as td:
   cache={};total=0
   for u in units:
    check.validate_rea_extent(u,PROJECT,self.reference['original_sha256'],self.reference)
    r=check.build_unit(u,self.reference['image'],PROJECT,'nasm',cache,Path(td),reference=self.reference)
    # The coherent int pen prototype changes debug types; its complete loaded
    # CODE/CONST and fields stay unchanged. These 15 native comparisons stay strict.
    # Before/after whole objects: pen-selector-560-root-review/compile-02/03.obj.
    self.assertEqual(r['status'],'c_matched');self.assertEqual(r['object_sha256'],'bbf21cc9175467d80a2fbc3ed8471b94a7893c11f27d2cac46f3a563d2022dc3');check.validate_emitted_mz_sites(r,self.reference['relocations']);total+=r['actual_size']
   self.assertEqual(total,2761);self.assertEqual(len(cache),1)
 def test_unknown_backend_still_rejected(self):
  u=copy.deepcopy(self.unit);u['backend']='msc500-any-lidata-omf'
  with self.assertRaises(ValueError):check.validate_units([u],self.reference['prefix_size'],len(self.reference['image']))

if __name__=='__main__':unittest.main()
