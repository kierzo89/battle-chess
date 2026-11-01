import copy,dataclasses,json,shutil,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
O=Path(__file__).resolve().parent
R=next(p for p in O.parents if (p/'config/target.json').is_file())
sys.path[:0]=[str(R),str(O)]
import huff_allocation16 as h
if (O/'check_staged.py').is_file():
 import check_staged as check
else:
 import check
from omf import read_omf,Public,Segment,OMFObject
from reference import build_reference

class AllocationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  registry=json.loads((R/'config/units.json').read_text());selected=[u for u in registry if u.get('object_profile')=='huff_refill_trap'];cls.unit=selected[0]if selected else json.loads((O/'huff-refill-trap-95-fixture.json').read_text());cls.built=h.assemble(R/h.SOURCE,cls.unit);cls.obj=read_omf(cls.built.object_bytes);cls.reference=build_reference((R.parent/'CHESS.EXE').read_bytes());cls.image=cls.reference['image']
 def object_bad(self,edit,message):
  obj=copy.deepcopy(self.obj);edit(obj)
  with self.assertRaisesRegex(ValueError,message):h.extract_code(obj)
 def unit_bad(self,edit,message):
  u=copy.deepcopy(self.unit);edit(u)
  with self.assertRaisesRegex(ValueError,message):h.validate_unit(u)
 def primary_bad(self,path,edit,message):
  real=Path.read_text;record=json.loads((R/path).read_text());edit(record)
  def read(p,*a,**k):return json.dumps(record)if p.resolve()==(R/path).resolve()else real(p,*a,**k)
  with patch.object(Path,'read_text',read):
   with self.assertRaisesRegex(ValueError,message):h._native(R)
 def test_fresh_whole95(self):
  raw,m=h.extract_code(self.obj);self.assertEqual(len(raw),95);self.assertEqual(len(self.obj.fixups),10);self.assertEqual(raw[38:41],b'\xcc\x06\x1e');self.assertEqual(m['authored_asm_function_credit'],0)
 def test_full_primary_MZ_and_two_LINK_orders(self):
  code,p=h.validate_comparison(self.unit,self.built,self.image,R,self.reference['relocations']);self.assertEqual(len(code),95);self.assertEqual(p['emitted_mz_sites'],[0xe42a]);self.assertEqual(len(p['authentic_two_order_LINK']),2);self.assertEqual(len(p['four_load_bases']),4);self.assertFalse(p['function_partition_claim'])
 def test_no_function_info_slicing(self):
  with patch.object(OMFObject,'function_info',side_effect=AssertionError('no function extent')):
   code,p=h.validate_comparison(self.unit,self.built,self.image,R,self.reference['relocations'])
  self.assertEqual(len(code),95)
 def test_guarded_generation_inputs(self):
  source=(R/h.SOURCE).resolve();tool=Path(shutil.which('nasm')).resolve();real=Path.read_bytes;reads=[]
  def read(p):
   p=p.resolve();reads.append(p);generated=p.name=='UNIT.OBJ'and p.parent.name.startswith('huff-allocation-')and not p.is_relative_to(R)
   if p not in(source,tool)and not generated:raise AssertionError('unexpected generation input')
   return real(p)
  with patch.object(Path,'read_bytes',read):
   with self.assertRaises(AssertionError):(R.parent/'CHESS.EXE').read_bytes()
   reads.clear();h.assemble(source,self.unit)
  self.assertIn(source,reads);self.assertIn(tool,reads)
 def test_forbid_fake_38_byte_function(self):self.unit_bad(lambda u:u.update(size=38),'Whole95')
 def test_forbid_fake_57_byte_function(self):self.unit_bad(lambda u:u.update(size=57),'Whole95')
 def test_forbid_function_symbol_metadata(self):self.unit_bad(lambda u:u.update(symbol='_huff_refill_e3ea'),'function/ownership')
 def test_forbid_one_public_selection(self):self.unit_bad(lambda u:u.update(public_symbols=['_huff_refill_e3ea']),'Whole95')
 def test_forbid_ASM_function_model(self):self.unit_bad(lambda u:u.update(language='asm'),'profile')
 def test_source_pin(self):self.unit_bad(lambda u:u.update(source_sha256='0'*64),'pinned')
 def test_tool_pin(self):self.unit_bad(lambda u:u.update(assembler_sha256='0'*64),'pinned')
 def test_placement_context(self):self.unit_bad(lambda u:u['externals']['_huff_input_buffer'].update(offset=0x2ec4),'bindings')
 def test_extra_allocation(self):self.object_bad(lambda o:o.segments.update({2:Segment(2,0,0,0,0,0x48)}),'one complete')
 def test_wrong_size(self):self.object_bad(lambda o:setattr(o.segments[1],'length',94),'CODE95')
 def test_wrong_alignment(self):self.object_bad(lambda o:setattr(o.segments[1],'attributes',0x28),'CODE95')
 def test_foreign_public(self):self.object_bad(lambda o:o.publics.update({'_fake':Public('_fake',1,39,0,0)}),'unaliased')
 def test_false_resume_public(self):self.object_bad(lambda o:o.publics.update({'_huff_depth_trap_e410':Public('_huff_depth_trap_e410',1,39,0,0)}),'unaliased')
 def test_foreign_external(self):self.object_bad(lambda o:o.externals.update({5:'_fake'}),'external')
 def test_hole(self):self.object_bad(lambda o:o.segments[1].chunks.__setitem__(0,(1,o.segments[1].chunks[0][1])),'hole')
 def test_missing_tail(self):
  def edit(o):a,b=o.segments[1].chunks[-1];o.segments[1].chunks[-1]=(a,b[:-1])
  self.object_bad(edit,'tail')
 def test_changed_trap(self):
  def edit(o):a,b=o.segments[1].chunks[0];o.segments[1].chunks[0]=(a,b[:38]+b'\x90'+b[39:])
  self.object_bad(edit,'instruction/addend')
 def test_missing_fixup(self):self.object_bad(lambda o:o.fixups.pop(),'Exact10')
 def test_wrong_BASE16_target(self):self.object_bad(lambda o:o.fixups.__setitem__(5,dataclasses.replace(o.fixups[5],target=(2,2))),'Exact10')
 def test_wrong_BASE16_frame(self):self.object_bad(lambda o:o.fixups.__setitem__(5,dataclasses.replace(o.fixups[5],frame=(1,1))),'Exact10')
 def test_wrong_BASE16_location(self):self.object_bad(lambda o:o.fixups.__setitem__(5,dataclasses.replace(o.fixups[5],location_type=1)),'Exact10')
 def test_extra_BASE16(self):self.object_bad(lambda o:o.fixups.__setitem__(0,dataclasses.replace(o.fixups[0],location_type=2)),'Exact10')
 def test_wrong_relative_mode(self):self.object_bad(lambda o:o.fixups.__setitem__(2,dataclasses.replace(o.fixups[2],segment_relative=True)),'Exact10')
 def test_COMM_record(self):self.object_bad(lambda o:o.records.insert(1,(0xb0,0,b'')),'Foreign record')
 def test_changed_original_byte(self):
  image=bytearray(self.image);image[h.BASE+94]^=1
  with self.assertRaisesRegex(ValueError,'Complete95'):h.validate_comparison(self.unit,self.built,image,R,self.reference['relocations'])
 def test_missing_original_MZ(self):
  with self.assertRaisesRegex(ValueError,'MZ set'):h.validate_comparison(self.unit,self.built,self.image,R,[])
 def test_extra_original_MZ(self):
  with self.assertRaisesRegex(ValueError,'MZ set'):h.validate_comparison(self.unit,self.built,self.image,R,[h.BASE+64,h.BASE+90])
 def test_crossing_original_MZ(self):
  with self.assertRaisesRegex(ValueError,'MZ set'):h.validate_comparison(self.unit,self.built,self.image,R,[h.BASE-1,h.BASE+64])
 def test_wrong_native_profile(self):self.primary_bad(h.NATIVE['refill'],lambda e:e['analysis_profile']['parameters'].update(load_segment='0x2000'),'profile')
 def test_wrong_native_parameters(self):self.primary_bad(h.NATIVE['refill'],lambda e:e.update(parameters={'procedure':'0x1e3eb'}),'parameters')
 def test_false_contiguous_native_body(self):self.primary_bad(h.NATIVE['refill'],lambda e:e['normalized_result']['procedure']['body'].update(non_contiguous=False),'ownership')
 def test_native_wrong_live_count(self):self.primary_bad(h.NATIVE['refill'],lambda e:e['normalized_result']['procedure']['body'].update(total_bytes=95),'ownership')
 def test_native_trap_wrong_instruction(self):self.primary_bad(h.NATIVE['trap'],lambda e:e['normalized_result'].update(assembly=['0x1e410: RET']),'trap instruction')
 def test_native_CFG_changed(self):self.primary_bad(h.NATIVE['refill'],lambda e:e['normalized_result']['basic_blocks'][0].update(successors=[]),'CFG')
 def test_duplicate_primary_IDs(self):
  eid=json.loads((R/h.RAW_EVIDENCE).read_text())['evidence_id'];self.primary_bad(h.NATIVE['trap'],lambda e:e.update(evidence_id=eid),'Duplicate')
 def test_actual_LINK_artifact_pin(self):
  real=Path.read_bytes;target=(R/h.AUTHENTIC_LINK[0]['exe']).resolve()
  def read(p):
   data=real(p)
   return data[:-1]+bytes([data[-1]^1])if p.resolve()==target else data
  with patch.object(Path,'read_bytes',read):
   with self.assertRaisesRegex(ValueError,'EXE/MAP pin'):h._authenticate_links(R,self.obj)
 def test_generic_library_stays_fail_closed(self):
  from library16 import link_segment
  with self.assertRaisesRegex(ValueError,'BASE16'):
   link_segment(self.obj,1,{1:(0,h.BASE)},{},{n:(v['segment'],v['offset'])for n,v in h.BINDINGS.items()})
 def test_actual_DGROUP_not_individual_data_frame(self):
  bindings=copy.deepcopy(h.BINDINGS);bindings['_huff_input_buffer']['segment']+=1
  with self.assertRaisesRegex(ValueError,'common data frame'):h._link_fixed(self.obj,(0,h.BASE),bindings)
 def test_production_model_status_not_function(self):
  result=check.build_unit(self.unit,self.image,R,'nasm',reference=self.reference);self.assertEqual(result['status'],'asm_code_matched');self.assertEqual(result['authored_asm_function_credit'],0);self.assertEqual(result['authored_c_function_credit'],0);check.validate_emitted_mz_sites(result,self.reference['relocations'])
 def test_reporting_no_extra_ASM_functions(self):
  registry=json.loads((R/'config/units.json').read_text());old=[u for u in registry if u.get('object_profile')in('bios_input','huffman_core','huffman_core_dgroup1')];self.assertEqual(len(old),11);real=Path.read_text;reports=[]
  # Source-allocation inventory has separate zero-credit semantics, outside
  # this deliberately bounded12-unit status/reporting check.
  empty={'schema_version':1,'objects':[],'placement_proven':False,'matching_credit':0}
  with tempfile.TemporaryDirectory()as tmp:
   for name,units in[('old',old),('new',old+[self.unit])]:
    def read(path,*a,**k):return json.dumps(units)if path.resolve()==(R/'config/units.json').resolve()else real(path,*a,**k)
    with patch.object(Path,'read_text',read),patch.object(check,'build_source_inputs',return_value=empty):reports.append(check.run(R.parent,R,R.parent/'CHESS.EXE',Path(tmp)/name,'nasm'))
  a,b=[r['summary']for r in reports];self.assertEqual(a['asm_matched_functions'],11);self.assertEqual(b['asm_matched_functions'],11);self.assertEqual(a['asm_matched_bytes'],b['asm_matched_bytes']);self.assertEqual(b['asm_code_matched_units'],1);self.assertEqual(b['asm_code_matched_bytes'],95);self.assertEqual(b['asm_code_emitted_mz_relocations'],1);self.assertEqual(b['failed_units'],0);self.assertEqual(a['c_matched_functions'],b['c_matched_functions']);self.assertEqual(b['verified_image_span_bytes']-a['verified_image_span_bytes'],95)


if __name__=='__main__':unittest.main(verbosity=2)
