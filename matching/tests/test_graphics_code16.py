"""Canonical-ready complete graphics1488 tests; real module path guards.
The staged mirror is selected explicitly; no fake compiler/cache objects.
"""
from pathlib import Path
import ast,copy,dataclasses,hashlib,inspect,io,json,os,sys,tempfile,unittest
from contextlib import redirect_stdout
from unittest.mock import patch
R=Path(os.environ.get('GRAPHICS_TEST_PROJECT',Path(__file__).resolve().parents[1])).resolve()
ROOT=Path(os.environ.get('GRAPHICS_TEST_ORIGINAL_ROOT',R.parent)).resolve()
sys.path.insert(0,str(R))
import graphics_code16 as g,graphics1488_link16 as adapter,blit_code16 as prefix,check,library16
from omf import read_omf,OMFObject,Public
from reference import build_reference

class GraphicsCodeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  for module,name in[(g,'graphics_code16.py'),(adapter,'graphics1488_link16.py'),(prefix,'blit_code16.py'),(check,'check.py')]:assert Path(module.__file__).resolve()==R/name
  cls.unit=json.loads((R/'build/graphics1488-code-backend-stage/proposed-unit.json').read_text())
  cls.built=g.assemble(R/g.SOURCE,R);cls.obj=read_omf(cls.built.object_bytes)
  cls.reference=build_reference((ROOT/'CHESS.EXE').read_bytes());cls.image=cls.reference['image']
 def objbad(self,edit,message):
  o=copy.deepcopy(self.obj);edit(o)
  with self.assertRaisesRegex(ValueError,message):g.extract_code(o)
 def unitbad(self,edit,message):
  u=copy.deepcopy(self.unit);edit(u)
  with self.assertRaisesRegex(ValueError,message):g.validate_unit(u)
 def semanticbad(self,path,edit,message):
  e=json.loads((R/path).read_text());edit(e);b=json.dumps(e).encode();real=Path.read_bytes
  owner=g if path in g.EVIDENCE_PINS else prefix;pins=dict(owner.EVIDENCE_PINS);pins[path]=hashlib.sha256(b).hexdigest()
  with patch.object(owner,'EVIDENCE_PINS',pins),patch.object(Path,'read_bytes',lambda p:b if p.resolve()==(R/path).resolve()else real(p)):
   with self.assertRaisesRegex(ValueError,message):g._evidence(R)
 def test_actual_complete_CODE_and_empty_DATA(self):
  self.assertEqual(len(self.built.code),1488);self.assertEqual(self.obj.segments[1].length,0);self.assertEqual(self.obj.segments[2].attributes,72)
  self.assertEqual([p['offset']for p in self.built.metadata['publics']],[280,1129,1203]);self.assertEqual(len(self.obj.fixups),84);self.assertFalse(self.obj.procedures)
 def test_pinned_adapter_is_exact_reviewed_source(self):
  self.assertEqual(hashlib.sha256((R/'graphics1488_link16.py').read_bytes()).hexdigest(),'8f06e8d41078d3b9c2f86a4aa0ea4ca9ee8476cc1c6c258c0b2a59b1e0467cac')
  self.assertEqual(hashlib.sha256(self.built.object_bytes).hexdigest(),adapter.OBJECT_SHA256)
 def test_source_only_generation_signature(self):self.assertEqual(list(inspect.signature(g.assemble).parameters),['source','project'])
 def test_source_tool_scratch_guard_actively_blocks_both_targets(self):
  rb,rt=Path.read_bytes,Path.read_text
  allowed={(R/g.SOURCE).resolve(),(R/'config/msc510.json').resolve(),*((R/'toolchains/msc510'/n).resolve()for n in['MASM.EXE','manifest.json','LICENSE'])}
  def valid(p):return p.resolve()in allowed or(p.parent.name.startswith('graphics-masm-')and p.name in['UNIT.OBJ','UNIT.LST','MASM.LOG','RESULT.TXT'])
  def readb(p):
   if not valid(p):raise AssertionError('Unexpected generation read '+str(p))
   return rb(p)
  def readt(p,*a,**k):
   if not valid(p):raise AssertionError('Unexpected generation read '+str(p))
   return rt(p,*a,**k)
  with patch.object(Path,'read_bytes',readb),patch.object(Path,'read_text',readt):
   for p in[ROOT/'CHESS.EXE',R/'build/exepack/TRIM5_UNPACK.EXE']:
    with self.assertRaises(AssertionError):p.read_bytes()
   b=g.assemble(R/g.SOURCE,R)
  self.assertEqual(b.object_bytes,self.built.object_bytes)
 def test_source_actual_operand_mutation(self):
  p=(R/g.SOURCE).resolve();real=Path.read_bytes;changed=real(p).replace(b'OR 4',b'OR 5',1);self.assertNotEqual(changed,real(p))
  with patch.object(Path,'read_bytes',lambda q:changed if q.resolve()==p else real(q)):
   with self.assertRaisesRegex(ValueError,'Source pin'):g.assemble(p,R)
 def test_tool_pin(self):
  p=(R/'toolchains/msc510/MASM.EXE').resolve();real=Path.read_bytes
  with patch.object(Path,'read_bytes',lambda q:b'wrong'if q.resolve()==p else real(q)):
   with self.assertRaisesRegex(ValueError,'assembler pin'):g.assemble(R/g.SOURCE,R)
 def test_manifest_license_configuration_pins(self):
  real=Path.read_bytes
  for rel in['toolchains/msc510/manifest.json','toolchains/msc510/LICENSE','config/msc510.json']:
   with self.subTest(rel=rel),patch.object(Path,'read_bytes',lambda p:b'bad'if p.resolve()==(R/rel).resolve()else real(p)):
    with self.assertRaisesRegex(ValueError,'pin mismatch'):g.assemble(R/g.SOURCE,R)
 def test_wrong_source_path(self):
  with self.assertRaisesRegex(ValueError,'source path'):g.assemble(R/'fake.asm',R)
 def test_mount_metacharacters(self):
  for name in['unsafe"project','unsafe\nproject']:
   p=R/name
   with self.assertRaisesRegex(ValueError,'Unsafe assembler project'):g.assemble(p/g.SOURCE,p)
 def test_wrong_metadata_profiles(self):
  for k,v in[('id','blit_e57a_code873'),('language','c'),('language','asm'),('backend','nasm-code-contribution-omf'),('object_profile','blit_dependency873'),('source','asm/link/blit_e57a_omf.asm')]:
   with self.subTest(k=k,v=v):self.unitbad(lambda u:u.update({k:v}),'profile')
 def test_no_slicing_or_old873_envelope(self):
  for n in[873,74,285,1487,1489,True]:self.unitbad(lambda u:u.update(size=n),'Complete1488')
  self.unitbad(lambda u:u.update(image_offset='0xe7cb'),'Complete1488')
 def test_public_metadata_and_sourcepins(self):
  for edit in[lambda u:u.update(public_symbols=['_blit_e57a']),lambda u:u.update(source_sha256='0'*64),lambda u:u.update(assembler_sha256='0'*64)]:self.unitbad(edit,'Complete1488|Pinned')
 def test_no_foreign_metadata_capacity_aliases(self):
  for k in['symbol','flags','code_address','slice','owned_const','owned_bss','font_capacity','end_symbol','alternate_binding']:
   self.unitbad(lambda u:u.update({k:None}),'Foreign')
 def test_each_real_binding_and_reference_metadata(self):
  for name in g.BINDINGS:self.unitbad(lambda u:u['externals'][name].update(offset=u['externals'][name]['offset']+1),'bindings')
  self.unitbad(lambda u:u.update(rea_evidence=prefix.RAW_EVIDENCE),'bindings')
  self.unitbad(lambda u:u.update(reference_region='exepack-expanded'),'bindings')
 def test_no_extra_allocation(self):self.objbad(lambda o:o.segments.update({3:copy.deepcopy(o.segments[1])}),'emptyDATA')
 def test_no_DATA_allocation_or_chunks(self):
  self.objbad(lambda o:setattr(o.segments[1],'length',32),'DATA0');self.objbad(lambda o:o.segments[1].chunks.append((0,b'\0')),'DATA0')
 def test_WORD_CODE_size_and_overlay(self):
  self.objbad(lambda o:setattr(o.segments[2],'attributes',40),'WORD');self.objbad(lambda o:setattr(o.segments[2],'length',873),'CODE1488');self.objbad(lambda o:setattr(o.segments[2],'overlay_index',2),'overlay')
 def test_CODE_hole(self):self.objbad(lambda o:o.segments[2].chunks.__setitem__(0,(1,o.segments[2].chunks[0][1])),'hole')
 def test_CODE_overlap(self):self.objbad(lambda o:o.segments[2].chunks.append((0,b'\0')),'overlap')
 def test_CODE_tail(self):
  def edit(o):at,b=o.segments[2].chunks[-1];o.segments[2].chunks[-1]=(at,b[:-1])
  self.objbad(edit,'tail')
 def test_no_LIDATA(self):self.objbad(lambda o:setattr(o.segments[2],'unsupported_data',True),'CODE1488')
 def test_every_source_CODE_byte_is_guarded(self):
  for i in range(1488):
   def edit(o):
    for j,(at,b)in enumerate(o.segments[2].chunks):
     if at<=i<at+len(b):o.segments[2].chunks[j]=(at,b[:i-at]+bytes([b[i-at]^1])+b[i-at+1:]);return
   with self.subTest(i=i):self.objbad(edit,'instructions/addends')
 def test_no_extra_PUBLIC_or_alias(self):self.objbad(lambda o:o.publics.update({'_fake':Public('_fake',2,1129,0,0)}),'PUBLIC')
 def test_each_PUBLIC_offset(self):
  for n in g.PUBLICS:self.objbad(lambda o:o.publics.__setitem__(n,dataclasses.replace(o.publics[n],offset=o.publics[n].offset+1)),'PUBLIC')
 def test_no_missing_PUBLIC(self):self.objbad(lambda o:o.publics.pop('_prepare_pixels_e8cb'),'PUBLIC')
 def test_no_foreign_external(self):self.objbad(lambda o:o.externals.update({10:'_fake'}),'external')
 def test_no_debug_CV(self):self.objbad(lambda o:o.procedures.update({'_fake':{}}),'procedure')
 def test_exact_field_count(self):self.objbad(lambda o:o.fixups.pop(),'Exact84')
 def test_each_actual_field_shape(self):
  for i in range(84):
   with self.subTest(i=i):self.objbad(lambda o:o.fixups.__setitem__(i,dataclasses.replace(o.fixups[i],displacement=65535)),'Exact84')
 def test_external_SEG_OFFSET_FAR_shapes(self):
  for i in[67,68,70,74,82]:
   for change in[dict(frame=(5,None)),dict(target=(2,1)),dict(width=1),dict(location_type=0),dict(segment_relative=False),dict(offset=1),dict(segment=1),dict(raw=b'bad'),dict(record_offset=0)]:
    with self.subTest(i=i,change=change):self.objbad(lambda o:o.fixups.__setitem__(i,dataclasses.replace(o.fixups[i],**change)),'Exact84')
 def test_no_COMMON_iterated_debug_records(self):
  for k in[0xb0,0xb2,0xa2,0x94]:self.objbad(lambda o:o.records.insert(1,(k,0,b'')),'Closed records')
 def test_THEADR_DGROUP_directive_entry(self):
  for kind in[0x80,0x9a,0x88,0x8a]:
   def edit(o):o.records=[(k,a,b'bad'if k==kind else b)for k,a,b in o.records]
   with self.subTest(kind=kind):self.objbad(edit,'THEADR/DGROUP')
 def test_unmodified_adapter_rejects_every_object_byte_mutation(self):
  for i in range(len(self.built.object_bytes)):
   b=bytearray(self.built.object_bytes);b[i]^=1
   with self.subTest(i=i),self.assertRaises(ValueError):adapter.validate_object(bytes(b))
 def test_genuine_semantic_negative_object(self):
  raw=(R/'build/graphics-following-e8cb-e915/wrong-colour/UNIT.OBJ').read_bytes();o=read_omf(raw)
  self.assertEqual(o.segments[2].length,1488);self.assertEqual(len(o.fixups),84)
  with self.assertRaisesRegex(ValueError,'instructions/addends'):g.extract_code(o)
  with self.assertRaises(ValueError):adapter.validate_object(raw)
 def test_default_library_external_BASE_reject_unchanged(self):
  ex={k:(v['segment'],v['offset'])for k,v in g.BINDINGS.items()}
  with self.assertRaisesRegex(ValueError,'matching explicit group frame'):library16.link_segment(self.obj,2,{1:(0x5cc2,0),2:(0,g.BASE)},{1:0x5cc2},ex)
 def test_all_primary_and_dependency_pins(self):
  real=Path.read_bytes
  for rel in g.EVIDENCE_PINS:
   with self.subTest(rel=rel),patch.object(Path,'read_bytes',lambda p:b'wrong'if p.resolve()==(R/rel).resolve()else real(p)):
    with self.assertRaisesRegex(ValueError,'evidence pin'):g._evidence(R)
 def test_primary_subject_provider_profile_operation(self):
  original=json.loads((R/g.RAW_EVIDENCE).read_text())
  for edit in[lambda e:e['subject'].update(format='elf'),lambda e:e['subject'].update(architecture='x86_64'),lambda e:e['subject']['digest'].update(sha256='0'*64),lambda e:e.update(provider={'id':'ida'}),lambda e:e.update(operation='analyze_function'),lambda e:e['analysis_profile'].update(digest='0'*64),lambda e:e['analysis_profile']['parameters'].update(load_segment='0x2000'),lambda e:e['analysis_profile']['parameters'].update(target_kind='library'),lambda e:e.update(evidence_id='invalid')]:
   e=copy.deepcopy(original);edit(e)
   with self.assertRaises(ValueError):g._subject(e,g.ORIGINAL_SHA256,'read_bytes')
 def test_raw_exact_parameters(self):self.semanticbad(g.RAW_EVIDENCE,lambda e:e['parameters'].update(length=615),'Complete656')
 def test_raw_incomplete(self):self.semanticbad(g.RAW_EVIDENCE,lambda e:e['normalized_result'].update(complete=False),'Complete656')
 def test_prepare_complete_native_body(self):self.semanticbad(g.PREPARE_EVIDENCE,lambda e:e['normalized_result']['procedure']['body'].update(total_bytes=73),'complete native boundary')
 def test_draw_complete_native_body(self):self.semanticbad(g.DRAW_EVIDENCE,lambda e:e['normalized_result']['procedure']['body'].update(non_contiguous=True),'complete native boundary')
 def test_complete_native_CFG_edges(self):
  for rel in[g.PREPARE_EVIDENCE,g.DRAW_EVIDENCE]:self.semanticbad(rel,lambda e:e['normalized_result']['basic_blocks'][0].update(successors=[]),'complete native CFG')
 def test_wrong_native_entry_parameter(self):self.semanticbad(g.DRAW_EVIDENCE,lambda e:e['parameters'].update(procedure='0x1e914'),'native procedure entry')
 def test_distinct_evidence_IDs(self):
  identity=json.loads((R/g.DRAW_EVIDENCE).read_text())['evidence_id'];self.semanticbad(g.PREPARE_EVIDENCE,lambda e:e.update(evidence_id=identity),'Distinct')
 def test_next_full41_boundary(self):self.semanticbad(g.NEXT_EVIDENCE,lambda e:e['normalized_result']['procedure']['body'].update(span_bytes=40),'complete native boundary')
 def test_real_functional_table(self):
  def edit(e):b=bytearray.fromhex(e['normalized_result']['bytes_hex']);b[100]^=1;e['normalized_result']['bytes_hex']=b.hex()
  self.semanticbad(g.RAW_EVIDENCE,edit,'Functional')
 def test_primary_overlap(self):
  def edit(e):b=bytearray.fromhex(e['normalized_result']['bytes_hex']);b[0]^=1;e['normalized_result']['bytes_hex']=b.hex()
  self.semanticbad(g.RAW_EVIDENCE,edit,'Overlapping')
 def test_actual_FAR_identity_not_provider_aliases(self):
  def edit(e):b=bytearray.fromhex(e['normalized_result']['bytes_hex']);b[1204-873]^=1;e['normalized_result']['bytes_hex']=b.hex()
  self.semanticbad(g.RAW_EVIDENCE,edit,'Raw external')
 def test_partial_blitter_native_limit_is_not_promoted(self):self.semanticbad(prefix.NATIVE_EVIDENCE,lambda e:e['normalized_result']['procedure']['body'].update(total_bytes=593),'partial ordinary')
 def test_75_native_replay_scope_is_preserved(self):self.semanticbad(prefix.REPLAY_EVIDENCE,lambda e:e.update(instruction_or_decoder_hooks_substituted=True),'native75')
 def test_conditional592_rawCFG_is_preserved(self):self.semanticbad(prefix.CFG_EVIDENCE,lambda e:e['secondary_CFG'].update(conditionally_reachable_bytes=593),'CFG completeness')
 def test_full_evidence_reference_and_target(self):
  self.assertTrue(g.validate_evidence(self.unit,R,g.ORIGINAL_SHA256,self.reference).startswith('ev_'))
  with self.assertRaisesRegex(ValueError,'original target'):g.validate_evidence(self.unit,R,'0'*64,self.reference)
  with self.assertRaisesRegex(ValueError,'Pinned expanded'):g.validate_evidence(self.unit,R,g.ORIGINAL_SHA256,None)
 def test_complete1488_comparison(self):
  b,p=g.validate_comparison(self.unit,self.built,self.image,R,self.reference['relocations']);self.assertEqual(b,self.image[g.BASE:g.BASE+1488]);self.assertEqual(len(p['relocations']),84);self.assertEqual(p['emitted_mz_sites'],g.MZ_SITES);self.assertFalse(p['function_partition_claim']);self.assertFalse(p['font_or_scratch_backing_supplied'])
 def test_forward_four_actual_load_bases(self):
  _,p=g.validate_comparison(self.unit,self.built,self.image,R,self.reference['relocations']);self.assertEqual([x['load_paragraph']for x in p['four_load_bases']],[0,1,0x1000,0xffff]);self.assertTrue(all(x['original_mz']==x['emitted_mz']==g.MZ_SITES for x in p['four_load_bases']))
 def test_original_instruction_byte_negative(self):
  image=bytearray(self.image);image[g.BASE+1300]^=1
  with self.assertRaisesRegex(ValueError,'Complete1488'):g.validate_comparison(self.unit,self.built,image,R,self.reference['relocations'])
 def test_missing_extra_crossing_MZ(self):
  for sites in[[],g.MZ_SITES[:-1],g.MZ_SITES+[g.BASE-1],g.MZ_SITES+[g.BASE+1487],g.MZ_SITES+[g.BASE+900]]:
   with self.assertRaisesRegex(ValueError,'MZ sites'):g.validate_comparison(self.unit,self.built,self.image,R,sites)
 def test_build_metadata_or_code_tampering(self):
  for b in[dataclasses.replace(self.built,metadata=self.built.metadata|{'forged':True}),dataclasses.replace(self.built,code=self.built.code[:-1])]:
   with self.assertRaisesRegex(ValueError,'Build differs'):g.validate_comparison(self.unit,b,self.image,R,self.reference['relocations'])
 def test_no_function_info_slicing(self):
  with patch.object(OMFObject,'function_info',side_effect=AssertionError('no slices')):g.validate_comparison(self.unit,self.built,self.image,R,self.reference['relocations'])
 def test_actual_MZ_ONLY_BASE_and_FAR_segment_halves(self):
  _,p=g.validate_comparison(self.unit,self.built,self.image,R,self.reference['relocations']);marked=[f for f in p['relocations']if f['mz_relocation_image_offset']is not None]
  self.assertEqual([f['location_type']for f in marked],[2,3,3,3]);self.assertEqual([f['object_offset']for f in marked],[1135,1204,1355,1473])
 def test_natural_NOP_and_transparency_table_retained(self):
  self.assertEqual(self.built.code[778:781],bytes.fromhex('eb5890'));self.assertIn('EB 58 90',self.built.provenance['assembler_listing']);self.assertNotIn('    nop',(R/g.SOURCE).read_text().lower())
 def test_meaningful_complete_translation_formula(self):
  def m(v):return 4 if v==1 else 12 if v==9 else v
  self.assertEqual(self.built.code[873:1129],bytes((m(x>>4)<<4)|m(x&15)for x in range(256)))
 def test_fresh_standard_build_unit_no_fake_cache(self):
  with tempfile.TemporaryDirectory()as d:
   r=check.build_unit(self.unit,self.image,R,'nasm',{},Path(d),reference=self.reference)
   self.assertEqual(r.get('status'),'asm_code_matched',r);self.assertEqual(r['actual_size'],1488);self.assertEqual(len(r['relocations']),84);self.assertEqual(r['authored_c_function_credit'],0);self.assertEqual(r['authored_asm_function_credit'],0)
 def test_normal_minimal_report_and_require_complete_failure(self):
  real=Path.read_text
  def read(p,*a,**k):
   if p.resolve()==(R/'config/units.json').resolve():return json.dumps([self.unit])
   if p.resolve()==(R/'config/source-inputs.json').resolve():return '{"schema_version":1,"source_allocations":[]}'
   return real(p,*a,**k)
  with patch.object(Path,'read_text',read),tempfile.TemporaryDirectory()as d,patch.object(check,'ROOT',ROOT),patch.object(check,'HERE',R),patch.object(sys,'argv',['check.py','--target',str(ROOT/'CHESS.EXE'),'--output',d,'--require-complete']),redirect_stdout(io.StringIO()):
   code=check.main();q=json.loads((Path(d)/'report.json').read_text())['summary']
  self.assertEqual(code,1);self.assertEqual(q['failed_units'],0);self.assertEqual(q['asm_code_matched_units'],1);self.assertEqual(q['asm_code_matched_bytes'],1488);self.assertEqual(q['c_matched_functions'],0);self.assertEqual(q['asm_matched_functions'],0);self.assertEqual(q['source_data_bytes'],0);self.assertFalse(q['full_executable_match'])
 def test_huff_route_preserved(self):
  old={'language':'asm-code','backend':check.huff_allocation16.BACKEND if hasattr(check.huff_allocation16,'BACKEND')else'nasm-code-contribution-omf'}
  with patch.object(check.huff_allocation16,'validate_evidence',return_value='huff')as f:self.assertEqual(check.validate_rea_extent(old,R,g.ORIGINAL_SHA256,self.reference),'huff');f.assert_called_once()
 def test_serial_route_preserved(self):
  old={'language':'asm-code','backend':check.serial_code16.BACKEND}
  with patch.object(check.serial_code16,'validate_evidence',return_value='serial')as f:self.assertEqual(check.validate_rea_extent(old,R,g.ORIGINAL_SHA256,self.reference),'serial');f.assert_called_once()
 def test_old873_route_preserved(self):
  old={'language':'asm-code','backend':check.blit_code16.BACKEND}
  with patch.object(check.blit_code16,'validate_evidence',return_value='old873')as f:self.assertEqual(check.validate_rea_extent(old,R,g.ORIGINAL_SHA256,self.reference),'old873');f.assert_called_once()
 def test_only_real_MZ_keys_reach_canonical_report(self):
  _,p=g.validate_comparison(self.unit,self.built,self.image,R,self.reference['relocations'])
  self.assertEqual(len(p['raw_adapter_field_logs']),84);self.assertEqual(len(p['relocations']),84)
  self.assertEqual(sum('mz_segment_relocation_image_offset'in q for q in p['relocations']),4)
  unit=dict(self.unit,relocations=p['relocations']);check.validate_emitted_mz_sites(unit,self.reference['relocations'])
  unit['relocations']=[q for q in p['relocations']if q['object_offset']!=1135]
  with self.assertRaisesRegex(ValueError,'MZ relocation set'):check.validate_emitted_mz_sites(unit,self.reference['relocations'])
 def test_next41_complete_reference_not_ignored(self):
  ref=copy.deepcopy(self.reference);b=bytearray(ref['image']);b[g.BASE+1488]^=1;ref['image']=bytes(b)
  with self.assertRaisesRegex(ValueError,'next41 reference'):g.validate_evidence(self.unit,R,g.ORIGINAL_SHA256,ref)
 def test_actual873_and1488_cannot_both_be_selected(self):
  old=json.loads((R/'build/blit-code-backend-stage/proposed-unit.json').read_text())
  with self.assertRaisesRegex(ValueError,'extents overlap'):check.validate_units([old,self.unit],len(self.image),len(self.image))
 def test_new_near_API_and_caller_binding_guards(self):
  def edit(e):
   for a in e['source_AST_declarations']:
    for d in a['declarations']:
     if d['name']=='prepare_pixels_e8cb':d['expanded_type']='int (char *, int, int)'
  self.semanticbad(g.API_EVIDENCE,edit,'New near API type')
  def binding(e):
   row=next(r for r in e['actual_current_external_bindings']if '_draw_text_e915'in r['bindings']);row['bindings']['_draw_text_e915']+=1
  self.semanticbad(g.API_EVIDENCE,binding,'binding identity')
 def test_no_font_capacity_or_scratch_provider_fabricated(self):
  self.semanticbad(g.API_EVIDENCE,lambda e:e['new_external_views']['_font_glyphs'].update(capacity=128),'invented storage')
  self.semanticbad(g.API_EVIDENCE,lambda e:e['new_external_views']['_text_glyph_pixels'].update(source_allocated=True),'invented storage')
 def test_compiler_or_public_partition_not_claimed(self):
  _,m=g.extract_code(self.obj);self.assertEqual((m['authored_c_function_credit'],m['authored_asm_function_credit'],m['DATA_byte_credit']),(0,0,0));self.assertEqual(m['CODE_contributions'],1)

if __name__=='__main__':unittest.main()
