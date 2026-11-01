"""Canonical-ready closed wrapper78 tests; no global regression or hardware execution."""
from pathlib import Path
import copy,dataclasses,json,os,sys,tempfile,unittest,io
from contextlib import redirect_stdout
from unittest.mock import patch,MagicMock
R=Path(os.environ.get('WRAPPER_TEST_PROJECT',Path(__file__).resolve().parents[1])).resolve();ROOT=R.parent;sys.path.insert(0,str(R))
import graphics_wrapper_code16 as s,check
from omf import read_omf,Public
from reference import build_reference
from library16 import link_segment,LibraryError
class WrapperTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  assert Path(s.__file__).resolve()==R/'graphics_wrapper_code16.py'and Path(check.__file__).resolve()==R/'check.py'
  cls.unit=json.loads((R/'build/graphics-wrapper78-backend-stage/proposed-unit.json').read_text())
  cls.built=s.assemble(R/s.SOURCE,R);cls.obj=read_omf(cls.built.object_bytes);cls.ref=build_reference((ROOT/'CHESS.EXE').read_bytes())
  cls.ex={n:(v['segment'],v['offset'])for n,v in s.BINDINGS.items()};cls.seg={1:(0x5cc2,0),2:(0x11ef,0)};cls.groups={1:0x5cc2}
 def bad_object(self,change,pattern):
  o=copy.deepcopy(self.obj);change(o)
  with self.assertRaisesRegex(ValueError,pattern):s.extract_code(o)
 def bad_unit(self,change,pattern):
  u=copy.deepcopy(self.unit);change(u)
  with self.assertRaisesRegex(ValueError,pattern):s.validate_unit(u)
 def test_fresh_complete_allocation(self):
  self.assertEqual(len(self.built.code),78);self.assertEqual(len(self.obj.fixups),15)
  self.assertEqual([p['offset']for p in self.built.metadata['publics']],[0,30,48]);self.assertEqual(self.built.metadata['segment']['attributes'],72)
 def test_full_compare_four_bases_and_qualified_CFG(self):
  b,p=s.validate_comparison(self.unit,self.built,self.ref['image'],R,self.ref['relocations'])
  self.assertEqual(b,self.ref['image'][s.BASE:s.BASE+78]);self.assertEqual(p['emitted_mz_sites'],s.MZ_SITES)
  self.assertEqual(len(p['four_load_bases']),4);self.assertFalse(p['first_entry_ordinary_REA_function_claim']);self.assertFalse(p['preceding_zero_gap_allocated']);self.assertEqual(p['DATA_byte_credit'],0)
 def test_link_has_no_target_reads(self):
  with patch.object(Path,'read_bytes',side_effect=AssertionError('pure link')),patch.object(Path,'read_text',side_effect=AssertionError('pure link')):
   b,l=s.link(self.obj,self.seg,self.groups,self.ex)
  self.assertEqual(b,self.ref['image'][s.BASE:s.BASE+78]);self.assertEqual(len(l),15)
 def test_default_runtime_linker_stays_restricted(self):
  with self.assertRaisesRegex(LibraryError,'only OFFSET16 and BASE16'):link_segment(self.obj,2,self.seg,self.groups,self.ex)
 def test_zero_C_and_function_credit(self):
  for key in ['authored_c_function_credit','authored_asm_function_credit','DATA_byte_credit']:self.assertEqual(self.built.metadata[key],0)
 def test_checksum(self):
  b=bytearray(self.built.object_bytes);b[4]^=1
  with self.assertRaisesRegex(ValueError,'checksum'):read_omf(bytes(b))
 def test_every_unlinked_code_byte_protected(self):
  for i in range(78):
   def mutate(o):at,b=o.segments[2].chunks[0];o.segments[2].chunks[0]=(at,b[:i]+bytes([b[i]^1])+b[i+1:])
   with self.subTest(offset=i):self.bad_object(mutate,'instructions/addends')
 def test_extra_segment(self):self.bad_object(lambda o:o.segments.update({3:copy.deepcopy(o.segments[1])}),'emptyDATA')
 def test_DATA_alloc(self):self.bad_object(lambda o:setattr(o.segments[1],'length',2),'DATA0')
 def test_DATA_bytes(self):self.bad_object(lambda o:o.segments[1].chunks.append((0,b'X')),'DATA0')
 def test_CODE_length_no_slices(self):
  for n in [18,30,48,77,79,3616]:
   with self.subTest(size=n):self.bad_object(lambda o:setattr(o.segments[2],'length',n),'CODE78')
 def test_WORD_attributes(self):self.bad_object(lambda o:setattr(o.segments[2],'attributes',40),'WORD')
 def test_names(self):self.bad_object(lambda o:o.names.append('FAKE'),'names')
 def test_hole(self):self.bad_object(lambda o:o.segments[2].chunks.__setitem__(0,(1,o.segments[2].chunks[0][1])),'hole')
 def test_overlap(self):self.bad_object(lambda o:o.segments[2].chunks.append((0,b'X')),'overlap')
 def test_omitted_tail(self):
  def change(o):at,b=o.segments[2].chunks[0];o.segments[2].chunks[0]=(at,b[:-1])
  self.bad_object(change,'tail')
 def test_LIDATA(self):self.bad_object(lambda o:setattr(o.segments[2],'unsupported_data',True),'CODE78')
 def test_alias_PUBLIC(self):self.bad_object(lambda o:o.publics.update({'_input_init_11ef_0000':Public('_input_init_11ef_0000',2,0,0,0)}),'PUBLIC')
 def test_wrong_PUBLIC_frame(self):self.bad_object(lambda o:o.publics.__setitem__('_graphics_end',Public('_graphics_end',1,0,0,0)),'PUBLIC')
 def test_foreign_external(self):self.bad_object(lambda o:o.externals.update({7:'_fake'}),'external')
 def test_no_CV(self):self.bad_object(lambda o:o.procedures.update({'_fake':{}}),'procedure')
 def test_missing_field(self):self.bad_object(lambda o:o.fixups.pop(),'15 authentic')
 def test_wrong_raw_field_shape(self):
  for changes in [{'frame':(0,2)},{'frame':(5,None)},{'target':(2,4)},{'width':2},{'location_type':1},{'segment_relative':False},{'displacement':1},{'offset':77},{'segment':1}]:
   with self.subTest(changes=changes):self.bad_object(lambda o:o.fixups.__setitem__(5,dataclasses.replace(o.fixups[5],**changes)),'15 authentic')
 def test_foreign_records(self):self.bad_object(lambda o:o.records.insert(-1,(0xb0,0,b'X')),'records')
 def test_wrong_group(self):
  def change(o):i=next(i for i,q in enumerate(o.records)if q[0]==0x9a);k,a,b=o.records[i];o.records[i]=(k,a,b'\x02')
  self.bad_object(change,'group')
 def test_raw_record_payloads_are_pinned(self):
  def mutate(o):
   i=next(i for i,q in enumerate(o.records)if q[0]==0x8c);k,a,b=o.records[i];o.records[i]=(k,a,b[:-1]+bytes([b[-1]^1]))
  self.bad_object(mutate,'record payload hashes')
 def test_unknown_metadata(self):
  for key in ['capacity','slice','aliases','owned_data','code_address','symbol','flags']:
   self.bad_unit(lambda u:u.update({key:None}),'metadata')
 def test_closed_unit_source_size_bindings(self):
  for key,value in [('language','c'),('backend','masm510-code-contribution-omf'),('object_profile','anything'),('source','fake.asm')]:self.bad_unit(lambda u:u.update({key:value}),'profile')
  for n in [30,48,77,79,3616]:self.bad_unit(lambda u:u.update(size=n),'Whole78')
  self.bad_unit(lambda u:u['externals']['_graphics_pointer_110d_0006'].update(offset=9),'bindings')
 def test_wrong_unit_pins(self):
  for key in ['source_sha256','assembler_sha256']:self.bad_unit(lambda u:u.update({key:'0'*64}),'Pinned')
 def test_wrong_public_list(self):self.bad_unit(lambda u:u.update(public_symbols=['_graphics_end']),'PUBLIC')
 def test_reference_region(self):self.bad_unit(lambda u:u.update(reference_region='unchanged-prefix'),'bindings')
 def test_changed_source_operand(self):
  p=(R/s.SOURCE).resolve();real=Path.read_bytes;changed=p.read_bytes().replace(b'cmp al, 1',b'cmp al, 2')
  with patch.object(Path,'read_bytes',lambda q:changed if q.resolve()==p else real(q)):
   with self.assertRaisesRegex(ValueError,'Source pin'):s.assemble(p,R)
 def test_wrong_path(self):
  with self.assertRaisesRegex(ValueError,'source path'):s.assemble(R/'fake.asm',R)
 def test_source_symlink(self):
  with tempfile.TemporaryDirectory()as tmp:
   p=Path(tmp)/'source.asm';p.symlink_to(R/s.SOURCE)
   with self.assertRaisesRegex(ValueError,'symlink'):s.assemble(p,R)
 def test_unsafe_project_path(self):
  for c in ['"',chr(10),chr(13)]:
   p=Path('/tmp/wrapper'+c)
   with patch.object(Path,'read_bytes',side_effect=AssertionError('No read')),patch.object(s.subprocess,'run',side_effect=AssertionError('No DOSBox')):
    with self.assertRaisesRegex(ValueError,'Unsafe assembler project'):s.assemble(p/s.SOURCE,p)
 def test_unsafe_scratch_path(self):
  for c in ['"',chr(10),chr(13)]:
   context=MagicMock();context.__enter__.return_value='/tmp/wrapper'+c
   with patch.object(s.tempfile,'TemporaryDirectory',return_value=context),patch.object(Path,'write_bytes',side_effect=AssertionError('No scratch write')),patch.object(s.subprocess,'run',side_effect=AssertionError('No DOSBox')):
    with self.assertRaisesRegex(ValueError,'Unsafe assembler scratch'):s.assemble(R/s.SOURCE,R)
 def test_tools_and_config_pins(self):
  real=Path.read_bytes
  for rel in ['toolchains/msc510/MASM.EXE','toolchains/msc510/manifest.json','toolchains/msc510/LICENSE','config/msc510.json']:
   with self.subTest(rel=rel),patch.object(Path,'read_bytes',lambda p:b'bad'if p.resolve()==(R/rel).resolve()else real(p)):
    with self.assertRaisesRegex(ValueError,'pin mismatch'):s.assemble(R/s.SOURCE,R)
 def test_generation_read_guard(self):
  rb,rt=Path.read_bytes,Path.read_text;allowed={(R/s.SOURCE).resolve(),(R/'config/msc510.json').resolve(),*((R/'toolchains/msc510'/n).resolve()for n in ['MASM.EXE','manifest.json','LICENSE'])}
  good=lambda p:p.resolve()in allowed or(p.parent.name.startswith('wrapper-masm-')and p.name in ['RESULT.TXT','MASM.LOG','UNIT.OBJ','UNIT.LST'])
  def b(p):
   if not good(p):raise AssertionError('generation read forbidden')
   return rb(p)
  def t(p,*a,**k):
   if not good(p):raise AssertionError('generation read forbidden')
   return rt(p,*a,**k)
  with patch.object(Path,'read_bytes',b),patch.object(Path,'read_text',t):
   for p in [ROOT/'CHESS.EXE',R/'build/graphics-wrapper78-followup/analysis-entry78.COM']:
    with self.assertRaises(AssertionError):p.read_bytes()
   built=s.assemble(R/s.SOURCE,R)
  self.assertEqual(built.object_bytes,self.built.object_bytes)
 def test_semantic_source_negative_rejected(self):
  o=read_omf((R/'build/graphics-wrapper78-followup/negative/UNIT.OBJ').read_bytes())
  with self.assertRaisesRegex(ValueError,'instructions/addends'):s.extract_code(o)
 def test_all_evidence_pins_fail_closed(self):
  real=Path.read_bytes
  for rel in s.EVIDENCE_PINS:
   p=(R/rel).resolve();wrong=real(p)+b'X'
   with self.subTest(rel=rel),patch.object(Path,'read_bytes',lambda q:wrong if q.resolve()==p else real(q)):
    with self.assertRaisesRegex(ValueError,'evidence pin'):s._evidence(R)
 def test_primary_and_COM_qualification(self):
  loaded,ids=s._evidence(R);self.assertEqual(len(loaded),96);self.assertEqual(len(ids),4)
  self.assertEqual(loaded[:78],(R/'build/graphics-wrapper78-followup/analysis-entry78.COM').read_bytes())
 def test_original_target_and_profile_context(self):
  with self.assertRaisesRegex(ValueError,'Wrong original'):s.validate_evidence(self.unit,R,'bad',self.ref)
  for bad in [None,self.ref|{'carrier_sha256':'bad'},self.ref|{'original_sha256':'bad'}]:
   with self.assertRaisesRegex(ValueError,'Pinned expanded'):s.validate_evidence(self.unit,R,s.ORIGINAL_SHA256,bad)
 def test_missing_extra_crossing_MZ(self):
  for sites in [[],s.MZ_SITES[:-1],s.MZ_SITES+[s.BASE-1],s.MZ_SITES+[s.BASE+77],s.MZ_SITES+[s.BASE+80],s.MZ_SITES+[s.MZ_SITES[0]]]:
   with self.subTest(sites=sites),self.assertRaisesRegex(ValueError,'MZ'):s.validate_comparison(self.unit,self.built,self.ref['image'],R,sites)
 def test_reference_full_bytes_no_mask(self):
  for at in [s.BASE,s.BASE+77,s.BASE+80]:
   b=bytearray(self.ref['image']);b[at]^=1
   with self.subTest(at=at),self.assertRaisesRegex(ValueError,'Whole78/native96'):s.validate_comparison(self.unit,self.built,b,R,self.ref['relocations'])
 def test_corrupted_build_metadata(self):
  built=dataclasses.replace(self.built,metadata=self.built.metadata|{'fake':True})
  with self.assertRaisesRegex(ValueError,'Build differs'):s.validate_comparison(self.unit,built,self.ref['image'],R,self.ref['relocations'])
 def test_no_function_boundary_slicing(self):
  with patch.object(type(self.obj),'function_info',side_effect=AssertionError('No C metadata slicing')):s.validate_comparison(self.unit,self.built,self.ref['image'],R,self.ref['relocations'])
 def test_missing_placement_sets(self):
  for seg,groups,ex in [{2:(0x11ef,0)},self.groups,self.ex], [self.seg,{},self.ex],[self.seg,self.groups,self.ex|{'_fake':(0,0)}]:
   with self.assertRaisesRegex(ValueError,'placements'):s.link(self.obj,seg,groups,ex)
 def test_wrong_DGROUP_or_extent(self):
  for seg,groups,ex in [[self.seg|{1:(0,0)},self.groups,self.ex],[self.seg|{2:(0x11ef,65530)},self.groups,self.ex],[self.seg,self.groups,self.ex|{'_input_x_005c':(0,92)}]]:
   with self.assertRaises(ValueError):s.link(self.obj,seg,groups,ex)
 def test_placement_scalar_validation(self):
  for value in [True,-1,65536,'0x11ef']:
   with self.assertRaises(ValueError):s.link(self.obj,self.seg|{2:(value,0)},self.groups,self.ex)
 def test_wrong_far_target_changes_actual_fields(self):
  b,l=s.link(self.obj,self.seg,self.groups,self.ex|{'_graphics_pointer_110d_0006':(0x110d,9)})
  self.assertNotEqual(b,self.ref['image'][s.BASE:s.BASE+78]);self.assertEqual([i for i,(x,y)in enumerate(zip(b,self.ref['image'][s.BASE:s.BASE+78]))if x!=y],[25,73])
 def test_normal_production(self):
  with tempfile.TemporaryDirectory()as tmp:r=check.build_unit(self.unit,self.ref['image'],R,'nasm',{},Path(tmp),reference=self.ref)
  self.assertEqual(r.get('status'),'asm_code_matched',r);self.assertEqual(r['actual_size'],78);self.assertEqual(len(r['relocations']),15)
  check.validate_emitted_mz_sites(r,self.ref['relocations']);self.assertEqual(r['authored_c_function_credit'],0)
 def test_old_asm_routes_unchanged(self):
  for backend,name in [(check.huff_allocation16,'nasm-code-contribution-omf'),(check.serial_code16,check.serial_code16.BACKEND),(check.blit_code16,check.blit_code16.BACKEND)]:
   with patch.object(backend,'validate_evidence',return_value='old')as mock:
    self.assertEqual(check.validate_rea_extent({'language':'asm-code','backend':name},R,s.ORIGINAL_SHA256,self.ref),'old');mock.assert_called_once()
 def test_expanded_CODE_exception_is_closed(self):
  check.validate_units([self.unit],self.ref['prefix_size'],len(self.ref['image']))
  for key,value in [('id','other_wrapper'),('object_profile','other_profile'),('size',76)]:
   u=copy.deepcopy(self.unit);u[key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):check.validate_units([u],self.ref['prefix_size'],len(self.ref['image']))
 def test_no_other_ASM_expanded_admission(self):
  u=copy.deepcopy(self.unit);u['backend']=check.serial_code16.BACKEND
  with self.assertRaisesRegex(ValueError,'Expanded references'):check.validate_units([u],self.ref['prefix_size'],len(self.ref['image']))
 def test_region_is_required_not_defaulted_to_file_credit(self):
  u=copy.deepcopy(self.unit);del u['reference_region']
  with self.assertRaises(ValueError):check.validate_units([u],self.ref['prefix_size'],len(self.ref['image']))
  with self.assertRaisesRegex(ValueError,'metadata'):s.validate_unit(u)
 def test_minimal_report_and_incomplete_exit(self):
  real=Path.read_text
  def read(p,*a,**k):
   if p.resolve()==(R/'config/units.json').resolve():return json.dumps([self.unit])
   if p.resolve()==(R/'config/source-inputs.json').resolve():return json.dumps({'schema_version':1,'source_allocations':[]})
   return real(p,*a,**k)
  with patch.object(Path,'read_text',read),tempfile.TemporaryDirectory()as tmp,patch.object(check,'ROOT',ROOT),patch.object(check,'HERE',R),patch.object(sys,'argv',['check.py','--target',str(ROOT/'CHESS.EXE'),'--output',tmp,'--require-complete']),redirect_stdout(io.StringIO()):
   exitcode=check.main();r=json.loads((Path(tmp)/'report.json').read_text())
  self.assertEqual(exitcode,1);q=r['summary'];self.assertEqual(q['failed_units'],0,r);self.assertEqual(q['asm_code_matched_units'],1);self.assertEqual(q['asm_code_matched_bytes'],78)
  self.assertEqual(q['asm_code_emitted_mz_relocations'],4);self.assertEqual(q['c_matched_functions'],0);self.assertEqual(q['asm_matched_functions'],0);self.assertEqual(q['source_data_bytes'],0);self.assertFalse(q['full_executable_match']);self.assertEqual(q['verified_file_span_bytes'],0);self.assertEqual(q['verified_image_span_bytes'],78)
if __name__=='__main__':unittest.main()
