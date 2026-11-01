"""Closed BIOS pixel33 backend tests; staged isolated imports, immutable fixtures."""
from pathlib import Path
import sys,json,copy,dataclasses,hashlib,inspect,unittest,importlib.util
from unittest.mock import patch
TEST=Path(__file__).resolve();M=TEST.parents[1];D=M/'build/bios-pixel-word33-backend-stage'
sys.path.insert(0,str(M))
import bios_pixel_word_code16 as b
import check
EXPECTED_MODULE=M/'bios_pixel_word_code16.py';EXPECTED_CHECK=M/'check.py'
TARGET=D.resolve().parents[1].parent/'CHESS.EXE'
from omf import read_omf
from reference import build_reference
H=lambda d:hashlib.sha256(d).hexdigest()
class BiosPixelWordTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.unit=json.loads((D/'proposed-unit.json').read_text());cls.object=(D/'positive-initial.obj').read_bytes();cls.obj=read_omf(cls.object);cls.raw,cls.meta=b.extract_code(cls.obj);cls.ref=build_reference(TARGET.read_bytes())
 def reject(self,f,*a):
  with self.assertRaises((ValueError,KeyError)):f(*a)
 def badunit(self,**kw):
  u=copy.deepcopy(self.unit);u.update(kw);self.reject(b.validate_unit,u)
 def badobj(self,edit):
  o=copy.deepcopy(self.obj);edit(o);self.reject(b.extract_code,o)
 def primary(self,name,edit):
  rel='build/bios-pixel-ea64/'+name;e=json.loads((M/rel).read_text());edit(e);data=(json.dumps(e)+'\n').encode();old=Path.read_bytes;pins=dict(b.EVIDENCE_PINS);pins[rel]=H(data)
  def read(p):return data if p.resolve()==(M/rel).resolve()else old(p)
  with patch.object(Path,'read_bytes',read),patch.object(b,'EVIDENCE_PINS',pins):self.reject(b._evidence,M)
 def test_actual_module_paths(self):
  self.assertEqual(Path(b.__file__).resolve(),EXPECTED_MODULE.resolve());self.assertEqual(Path(check.__file__).resolve(),EXPECTED_CHECK.resolve())
 def test_source_only_generation_signature(self):self.assertEqual(list(inspect.signature(b.assemble).parameters),['source','project'])
 def test_profile_positive(self):b.validate_unit(self.unit)
 def test_wrong_backend(self):self.badunit(backend='nasm-code-contribution-omf')
 def test_wrong_profile(self):self.badunit(object_profile='bios_pixel_alias')
 def test_wrong_source(self):self.badunit(source='asm/link/other.asm')
 def test_wrong_source_pin(self):self.badunit(source_sha256='0'*64)
 def test_wrong_tool_pin(self):self.badunit(assembler_sha256='0'*64)
 def test_no_ordinary_function_credit(self):self.badunit(language='asm')
 def test_no_crop_or_followzero(self):
  for n in [32,34]:self.badunit(size=n)
 def test_exact_origin(self):self.badunit(image_offset='0xea65')
 def test_no_expanded_exception(self):self.badunit(reference_region='exepack-expanded')
 def test_no_alias_public(self):self.badunit(public_symbols=list(b.PUBLICS)+['_alias'])
 def test_no_ownership_metadata(self):
  for k in ['symbol','owned_data','owned_bss','owned_const','extended_extent','data_address','code_address']:self.badunit(**{k:None})
 def test_exact_byte_external_binding(self):
  ex=copy.deepcopy(b.BINDINGS);ex['_graphics_driver_colour_110dc']['offset']=13;self.badunit(externals=ex)
 def test_no_fake_driver_backing(self):self.badunit(driver_backing_capacity=16)
 def test_no_foreign_primary(self):self.badunit(rea_evidence='other.json')
 def test_source_has_no_emission_directives(self):b.source_policy((D/'implementation/bios_pixel_word_ea64_omf.asm').read_bytes())
 def test_source_no_opcode_blob_padding_origin(self):
  for op in ['DB 90h','DW 0','DD 0','ORG 0','ALIGN 16','EVEN','INCLUDE other.asm','INCBIN raw.bin','REPT 2']:
   self.reject(b.source_policy,op.encode())
 def test_whole_raw33_and_single_public(self):self.assertEqual(len(self.raw),33);self.assertEqual(len(self.obj.publics),1);self.assertEqual(self.meta['authored_asm_function_credit'],0)
 def test_wrong_attribute(self):self.badobj(lambda o:setattr(o.segments[1],'attributes',104))
 def test_wrong_segment_class(self):self.badobj(lambda o:setattr(o.segments[1],'class_name','DATA'))
 def test_no_extra_allocation(self):self.badobj(lambda o:o.segments.update({2:copy.deepcopy(o.segments[1])}))
 def test_exact_segment_length(self):self.badobj(lambda o:setattr(o.segments[1],'length',34))
 def test_no_public_alias(self):self.badobj(lambda o:o.publics.update({'_alias':next(iter(o.publics.values()))}))
 def test_correct_public_address(self):self.badobj(lambda o:o.publics.update({'_bios_plot_pixel_ea64':dataclasses.replace(o.publics['_bios_plot_pixel_ea64'],offset=1)}))
 def test_no_other_external(self):self.badobj(lambda o:o.externals.update({2:'_fake_driver'}))
 def test_no_debug_or_common_records(self):
  for k in [0xb0,0x8e,0xa2]:self.badobj(lambda o,k=k:o.records.append((k,181,b'\0')))
 def test_exact_module_name(self):self.badobj(lambda o:o.records.__setitem__(0,(0x80,0,b'\x07ALT.ASM')))
 def test_no_code_hole(self):self.badobj(lambda o:setattr(o.segments[1],'chunks',[(1,self.raw)]))
 def test_no_code_overlap(self):self.badobj(lambda o:setattr(o.segments[1],'chunks',[(0,self.raw),(32,b'\0')]))
 def test_every_code_byte_pinned(self):
  for i in range(33):
   raw=bytearray(self.raw);raw[i]^=1;self.badobj(lambda o,v=bytes(raw):setattr(o.segments[1],'chunks',[(0,v)]))
 def test_both_actual_fields_required(self):self.badobj(lambda o:o.fixups.pop())
 def test_segment_field_location(self):self.badobj(lambda o:o.fixups.__setitem__(0,dataclasses.replace(o.fixups[0],location_type=1)))
 def test_same_external_frame(self):self.badobj(lambda o:o.fixups.__setitem__(0,dataclasses.replace(o.fixups[0],frame=(5,None))))
 def test_same_external_target(self):self.badobj(lambda o:o.fixups.__setitem__(1,dataclasses.replace(o.fixups[1],target=(2,2))))
 def test_no_displacement(self):self.badobj(lambda o:o.fixups.__setitem__(1,dataclasses.replace(o.fixups[1],displacement=1)))
 def test_no_self_relative_fields(self):self.badobj(lambda o:o.fixups.__setitem__(1,dataclasses.replace(o.fixups[1],segment_relative=False)))
 def test_native_four_bases_full33_and_mz(self):
  linked,p=b.validate_comparison(self.unit,b.Build(self.object,self.raw,self.meta,{}),self.ref['image'],M,self.ref['relocations']);self.assertEqual(linked,self.ref['image'][b.BASE:b.BASE+33]);self.assertTrue(all(r['all33_native_equal']for r in p['four_load_bases']));self.assertEqual(p['emitted_mz_sites'],[0xea6b])
 def test_complete_original_prefix_evidence(self):b.validate_evidence(self.unit,M,b.ORIGINAL_SHA256,self.ref)
 def test_wrong_original_target(self):self.reject(b.validate_evidence,self.unit,M,'0'*64,self.ref)
 def test_short_prefix(self):self.reject(b.validate_evidence,self.unit,M,b.ORIGINAL_SHA256,dict(self.ref,prefix_size=b.BASE+32))
 def test_mz_missing_extra_crossing(self):
  for sites in [[],[0xea6b,b.BASE-1],[0xea6b,b.BASE+32],[0xea6b,b.BASE+2],[0xea6b,0xea6b]]:self.reject(b._sites,sites)
 def test_wrong_native_kind(self):self.primary('rea-bytes34.json',lambda e:e['subject'].update(format='raw'))
 def test_wrong_native_provider(self):self.primary('rea-bytes34.json',lambda e:e['provider'].update(id='r2'))
 def test_wrong_loader_profile(self):self.primary('rea-bytes34.json',lambda e:e['analysis_profile']['parameters'].update(load_segment='0'))
 def test_wrong_native_operation(self):self.primary('rea-bytes34.json',lambda e:e.update(operation='analyze_function'))
 def test_partial_raw(self):self.primary('rea-bytes34.json',lambda e:e['normalized_result'].update(complete=False))
 def test_exact_native_parameters(self):self.primary('rea-bytes34.json',lambda e:e['parameters'].update(length=33))
 def test_wrong_native_extent(self):self.primary('rea-current.json',lambda e:e['normalized_result']['procedure']['body'].update(span_bytes=34))
 def test_native_disjoint_rejected(self):self.primary('rea-current.json',lambda e:e['normalized_result']['procedure']['body'].update(non_contiguous=True))
 def test_duplicate_native_ids(self):
  eid=json.loads((M/b.RAW_EVIDENCE).read_text())['evidence_id'];self.primary('rea-current.json',lambda e:e.update(evidence_id=eid))
 def test_native_mov_ES_AX_raw_over_provider_erratum(self):self.assertEqual(bytes.fromhex(json.loads((M/b.RAW_EVIDENCE).read_text())['normalized_result']['bytes_hex'])[9:11],bytes.fromhex('8ec0'))
 def test_no_placement_aliases(self):self.reject(b.link,self.obj,{'_other':(0x110d,12)})
 def test_invalid_external_placement(self):
  for value in [(65536,12),(0x110d,-1),(True,12),(0x110d,12,1)]:self.reject(b.link,self.obj,{'_graphics_driver_colour_110dc':value})
 def test_mz_field_is_external_segment_not_offset(self):
  a,logs=b.link(self.obj,{'_graphics_driver_colour_110dc':(0x2345,0x6789)});self.assertEqual(a[7:9],bytes.fromhex('4523'));self.assertEqual(a[15:17],bytes.fromhex('8967'));self.assertEqual([l['mz_segment_relocation_image_offset']for l in logs if 'mz_segment_relocation_image_offset'in l],[b.BASE+7])
 def test_fresh_source_tools_scratch_only_generation(self):
  P=D/'mirror';old=Path.read_bytes;oldtext=Path.read_text;reads=[]
  allowed={(P/b.SOURCE).resolve(),*(p.resolve()for p in [P/'toolchains/msc510/MASM.EXE',P/'toolchains/msc510/manifest.json',P/'toolchains/msc510/LICENSE',P/'config/msc510.json'])}
  def allow(p):
   q=p.resolve()
   if q not in allowed and not any(x.startswith('bios-pixel-word-masm-')for x in q.parts):raise PermissionError('Generation target/foreign read blocked')
   reads.append(str(q))
  def rb(p):allow(p);return old(p)
  def rt(p,*a,**kw):allow(p);return oldtext(p,*a,**kw)
  with patch.object(Path,'read_bytes',rb),patch.object(Path,'read_text',rt):
   for forbidden in [TARGET,M/'build/exepack/TRIM5_UNPACK.EXE']:
    with self.assertRaises(PermissionError):forbidden.read_bytes()
   built=b.assemble(P/b.SOURCE,P)
  self.assertEqual(built.object_bytes,self.object);self.assertTrue(reads)
 def test_real_AH0D_negative_normal_mismatch(self):
  n=json.loads((D/'negative-proof.json').read_text());self.assertEqual(n['status'],'mismatch');self.assertEqual(n['first_difference'],12);self.assertEqual(n['difference_count'],1);self.assertTrue(n['fresh_actual_generation'])
 def test_normal_report_no_C_function_DATA_credit(self):
  p=json.loads((D/'normal-report-proof.json').read_text());s=p['summary'];self.assertEqual(s['asm_code_matched_bytes'],33);self.assertEqual(s['asm_code_matched_units'],1);self.assertEqual(s['c_matched_functions'],0);self.assertEqual(s['asm_matched_functions'],0);self.assertEqual(s['source_data_units'],0);self.assertEqual(p['actual_normal_main_require_complete_returncode'],1)
 def test_old_PARA_object_rejected(self):self.reject(b.extract_code,read_omf((M/'build/bios-pixel-ea64/guarded-positive.obj').read_bytes()))
 def test_old_PARA_profile_rejected(self):self.reject(b.validate_unit,json.loads((M/'build/bios-pixel33-backend-stage/proposed-unit.json').read_text()))
 def test_WORD_source_supersedes_only_alignment_directive(self):
  old=(M/'build/bios-pixel-ea64/bios_pixel.asm').read_bytes();new=(D/'bios_pixel_word.asm').read_bytes();self.assertEqual(old.replace(b'SEGMENT PARA',b'SEGMENT WORD'),new)
 def alignment_records(self):
  return {rel:json.loads((M/rel).read_text())for rel in b.EVIDENCE_PINS if rel.endswith('.json')}
 def test_real200LINK_MAP_native_even_compatible(self):
  proof=b._alignment(M,self.alignment_records());self.assertEqual(proof['alignment_bytes'],2);self.assertEqual(proof['actual_LINK_PUBLIC'],[0xf27,4]);self.assertTrue(proof['native_even_compatible']);self.assertFalse(proof['final_native_placement_proven'])
 def test_alignment_rejects_extra_object(self):
  records=self.alignment_records();records['build/bios-pixel-word33-backend-stage/actual-LINK-proof.json']['physical_source_objects']=201;self.reject(b._alignment,M,records)
 def test_alignment_rejects_wrong_linked_object(self):
  records=self.alignment_records();records['build/bios-pixel-word33-backend-stage/actual-LINK-proof.json']['input_objects'][-1]['sha256']='0'*64;self.reject(b._alignment,M,records)
 def test_alignment_rejects_colour_backing_or_prefix(self):
  for field in ['new_stub_prefix_colour_backing','forced_offset4_or_padding_ORG']:
   records=self.alignment_records();records['build/bios-pixel-word33-backend-stage/actual-LINK-proof.json'][field]=True;self.reject(b._alignment,M,records)
 def test_alignment_requires_WORD_not_PARA(self):
  records=self.alignment_records();records['build/bios-pixel-word33-backend-stage/actual-LINK-proof.json']['source_SEGDEF_alignment_bytes']=16;self.reject(b._alignment,M,records)
if __name__=='__main__':unittest.main()
