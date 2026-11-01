"""Finite strict TEXT33 profile controls; no real generator or child process in tests."""
from pathlib import Path
import sys,json,copy,dataclasses,hashlib,inspect,unittest
from unittest.mock import patch
M=Path(__file__).resolve().parents[1];F=M/'tests/fixtures/bios_TEXT33';sys.path.insert(0,str(M))
import bios_pixel_text_code16 as b
import bios_pixel_word_code16 as legacy
from omf import read_omf
from reference import build_reference
H=lambda x:hashlib.sha256(x).hexdigest()
class BiosTEXT33(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.unit=json.loads((F/'unit.json').read_text());cls.raw=(F/'TEXT33.obj').read_bytes();cls.obj=read_omf(cls.raw);cls.code,cls.meta=b.extract_code(cls.obj);cls.reference=build_reference((M.parent/'CHESS.EXE').read_bytes())
 def reject(self,fn,*args):
  with self.assertRaises((ValueError,KeyError,TypeError)):fn(*args)
 def badunit(self,**kwargs):
  u=copy.deepcopy(self.unit);u.update(kwargs);self.reject(b.validate_unit,u)
 def badobj(self,edit):
  o=copy.deepcopy(self.obj);edit(o);self.reject(b.extract_code,o)
 def test_actual_new_module(self):self.assertEqual(Path(b.__file__).resolve(),(M/'bios_pixel_text_code16.py').resolve())
 def test_source_tools_only_signature(self):self.assertEqual(list(inspect.signature(b.assemble).parameters),['source','project'])
 def test_exact_unit(self):b.validate_unit(self.unit)
 def test_legacy_profile_rejected(self):self.badunit(object_profile='bios_pixel_word33')
 def test_legacy_backend_rejected(self):self.badunit(backend=legacy.BACKEND)
 def test_legacy_source_rejected(self):self.badunit(source=legacy.SOURCE)
 def test_wrong_source_pin(self):self.badunit(source_sha256='0'*64)
 def test_wrong_assembler_pin(self):self.badunit(assembler_sha256='0'*64)
 def test_expanded_region_rejected(self):self.badunit(reference_region='exepack-expanded')
 def test_no_following_byte_credit(self):
  for size in [32,34]:self.badunit(size=size)
 def test_no_extra_unit_fields(self):
  for key in ['status','data_address','owned_data','owned_bss','historical_SEGDEF']:self.badunit(**{key:True})
 def test_wrong_native_origin(self):self.badunit(image_offset='0xea65')
 def test_no_driver_capacity(self):self.badunit(driver_capacity=1)
 def test_external_binding_exact(self):self.badunit(externals={'_graphics_driver_colour_110dc':{'segment':0x110d,'offset':13}})
 def test_whole171_and_CODE33(self):self.assertEqual(len(self.raw),171);self.assertEqual(len(self.code),33);self.assertEqual(H(self.raw),b.OBJECT_SHA256)
 def test_legacy_object_rejected(self):self.reject(b.extract_code,read_omf((F/'legacy_WORD33.obj').read_bytes()))
 def test_new_object_rejected_by_legacy(self):self.reject(legacy.extract_code,self.obj)
 def test_old_gate_still_positive(self):legacy.extract_code(read_omf((F/'legacy_WORD33.obj').read_bytes()))
 def test_TEXT_WORD_PUBLIC_shape(self):self.assertEqual((self.obj.segments[1].name,self.obj.segments[1].attributes),('_TEXT',72))
 def test_wrong_segment_name(self):self.badobj(lambda o:setattr(o.segments[1],'name','BIOS_PIXEL_TEXT'))
 def test_wrong_alignment(self):self.badobj(lambda o:setattr(o.segments[1],'attributes',40))
 def test_wrong_class(self):self.badobj(lambda o:setattr(o.segments[1],'class_name','DATA'))
 def test_extra_segment(self):self.badobj(lambda o:o.segments.update({2:copy.deepcopy(o.segments[1])}))
 def test_no_code_hole(self):self.badobj(lambda o:setattr(o.segments[1],'chunks',[(1,self.code)]))
 def test_no_code_overlap(self):self.badobj(lambda o:setattr(o.segments[1],'chunks',[(0,self.code),(32,b'\0')]))
 def test_all33_bytes_bound(self):
  for i in range(33):
   c=bytearray(self.code);c[i]^=1;self.badobj(lambda o,c=bytes(c):setattr(o.segments[1],'chunks',[(0,c)]))
 def test_no_public_alias(self):self.badobj(lambda o:o.publics.update({'_alias':next(iter(o.publics.values()))}))
 def test_public_exact_origin(self):self.badobj(lambda o:o.publics.update({'_bios_plot_pixel_ea64':dataclasses.replace(o.publics['_bios_plot_pixel_ea64'],offset=1)}))
 def test_no_new_external(self):self.badobj(lambda o:o.externals.update({2:'_fake'}))
 def test_whole_record_payloads(self):self.badobj(lambda o:o.records.__setitem__(0,(0x80,0,b'\x07ALT.ASM')))
 def test_no_common_or_debug_records(self):
  for k in [0xb0,0xb8,0x8e,0xa2]:self.badobj(lambda o,k=k:o.records.append((k,171,b'\0')))
 def test_both_typed_fields_required(self):self.badobj(lambda o:o.fixups.pop())
 def test_BASE_cannot_be_OFFSET(self):self.badobj(lambda o:o.fixups.__setitem__(0,dataclasses.replace(o.fixups[0],location_type=1)))
 def test_no_default_frame_fallback(self):self.badobj(lambda o:o.fixups.__setitem__(0,dataclasses.replace(o.fixups[0],frame=(5,None))))
 def test_no_GROUP_frame_fallback(self):self.badobj(lambda o:o.fixups.__setitem__(0,dataclasses.replace(o.fixups[0],frame=(1,1))))
 def test_no_alternate_target(self):self.badobj(lambda o:o.fixups.__setitem__(1,dataclasses.replace(o.fixups[1],target=(2,2))))
 def test_no_displacement(self):self.badobj(lambda o:o.fixups.__setitem__(1,dataclasses.replace(o.fixups[1],displacement=1)))
 def test_no_self_relative_OFFSET(self):self.badobj(lambda o:o.fixups.__setitem__(1,dataclasses.replace(o.fixups[1],segment_relative=False)))
 def test_source_policy_no_blobs_padding(self):
  b.source_policy((F/'source.asm').read_bytes())
  for op in ['DB 90h','DW 0','DD 0','ALIGN 16','EVEN','ORG 0','INCBIN raw','INCLUDE other','REPT 2']:self.reject(b.source_policy,op.encode())
 def test_complete_native_evidence(self):b.validate_evidence(self.unit,M,b.ORIGINAL_SHA256,self.reference)
 def test_native_four_bases_MZ(self):
  linked,p=b.validate_comparison(self.unit,b.Build(self.raw,self.code,self.meta,{}),self.reference['image'],M,self.reference['relocations']);self.assertEqual(linked,self.reference['image'][b.BASE:b.BASE+33]);self.assertTrue(all(x['all33_native_equal']for x in p['four_load_bases']));self.assertEqual(p['emitted_mz_sites'],[0xea6b])
 def test_wrong_original(self):self.reject(b.validate_evidence,self.unit,M,'0'*64,self.reference)
 def test_short_prefix(self):self.reject(b.validate_evidence,self.unit,M,b.ORIGINAL_SHA256,dict(self.reference,prefix_size=b.BASE+32))
 def test_complete_MZ_set(self):
  for sites in [[],[0xea6b,0xea63],[0xea6b,0xea84],[0xea6b,0xea6b]]:self.reject(b._sites,sites)
 def test_offset_vs_segment_distinct(self):
  linked,logs=b.link(self.obj,{'_graphics_driver_colour_110dc':(0x2345,0x6789)});self.assertEqual(linked[7:9],bytes.fromhex('4523'));self.assertEqual(linked[15:17],bytes.fromhex('8967'));self.assertEqual([x['mz_segment_relocation_image_offset']for x in logs if'mz_segment_relocation_image_offset'in x],[0xea6b])
 def test_no_placement_alias(self):self.reject(b.link,self.obj,{'_fake':(0x110d,12)})
 def test_invalid_placement(self):
  for x in [(True,12),(65536,12),(0x110d,-1),(0x110d,12,1)]:self.reject(b.link,self.obj,{'_graphics_driver_colour_110dc':x})
 def test_new_ordinary_requires_actual_raw(self):
  wrong=dataclasses.replace(b.Build(self.raw,self.code,self.meta,{}),object_bytes=(F/'legacy_WORD33.obj').read_bytes());self.reject(b.validate_comparison,self.unit,wrong,self.reference['image'],M,self.reference['relocations'])
 def test_calibration_is_not_placement(self):
  records={n:json.loads((M/n).read_text())for n in b.EVIDENCE_PINS};v=b._calibration(M,records);self.assertFalse(v['new_actual_LINK_placement_proven']);self.assertFalse(v['EA85_byte_allocated'])
 def test_calibration_malformed_not_accepted(self):
  original={n:json.loads((M/n).read_text())for n in b.EVIDENCE_PINS}
  for edit in [lambda r:r['evidence/bios_pixel_TEXT33/comparison.json'].update(new_segment_name='BIOS_PIXEL_TEXT'),lambda r:r['evidence/bios_pixel_TEXT33/generation-receipt.json'].update(actual_MASM_calls=0),lambda r:r['evidence/bios_pixel_TEXT33/generation-terminal.json'].update(exit_code=1)]:
   r=copy.deepcopy(original);edit(r);self.reject(b._calibration,M,r)
