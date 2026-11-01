"""Canonical-ready strict serial248 tests; isolated mirror selected explicitly."""
from pathlib import Path
import copy,dataclasses,hashlib,io,json,os,sys,tempfile,unittest
from contextlib import redirect_stdout
from unittest.mock import patch
R=Path(os.environ.get('SERIAL_TEST_PROJECT',Path(__file__).resolve().parents[1])).resolve()
ROOT=Path(os.environ.get('SERIAL_TEST_ORIGINAL_ROOT',R.parent)).resolve()
sys.path.insert(0,str(R))
import serial248_code16 as s
import serial_code16 as dispatcher
import check
from omf import read_omf,Segment,Public
from reference import build_reference

class Serial248CodeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  assert Path(s.__file__).resolve()==R/'serial248_code16.py'
  assert Path(dispatcher.__file__).resolve()==R/'serial_code16.py'
  assert Path(check.__file__).resolve()==R/'check.py'
  cls.unit=json.loads((R/'tests/fixtures/serial248-unit.json').read_text())
  cls.built=s.assemble(R/s.SOURCE,R);cls.obj=read_omf(cls.built.object_bytes)
  cls.reference=build_reference((ROOT/'CHESS.EXE').read_bytes());cls.image=cls.reference['image']
 def object_bad(self,edit,message):
  o=copy.deepcopy(self.obj);edit(o)
  with self.assertRaisesRegex(ValueError,message):s.extract_code(o)
 def unit_bad(self,edit,message):
  u=copy.deepcopy(self.unit);edit(u)
  with self.assertRaisesRegex(ValueError,message):s.validate_unit(u)
 def evidence_bad(self,path,edit):
  original=Path.read_bytes;data=json.loads((R/path).read_text());edit(data)
  with patch.object(Path,'read_bytes',lambda p:json.dumps(data).encode()if p.resolve()==(R/path).resolve()else original(p)):
   with self.assertRaisesRegex(ValueError,'evidence pin'):s._evidence(R)
 def test_raw_checksum_tamper(self):
  bad=bytearray(self.built.object_bytes);bad[4]^=1
  with self.assertRaisesRegex(ValueError,'checksum'):read_omf(bytes(bad))
 def test_fresh_whole_allocation(self):
  self.assertEqual(len(self.built.code),248);self.assertEqual(len(self.obj.fixups),21)
  self.assertEqual(self.built.metadata['segment']['attributes'],72)
  self.assertEqual(sorted(p['offset']for p in self.built.metadata['publics']),[0,35,182,221])
  self.assertEqual(self.built.provenance['deterministic_source_name'],'UNIT.ASM')
 def test_exact_comparison_and_raw_handler_limits(self):
  b,p=s.validate_comparison(self.unit,self.built,self.image,R,self.reference['relocations'])
  self.assertEqual(b,self.image[s.BASE:s.BASE+248]);self.assertEqual(len(p['four_load_bases']),4)
  self.assertFalse(p['function_partition_claim']);self.assertEqual(p['DATA_byte_credit'],0)
  self.assertEqual(len(p['relocations']),21);self.assertEqual(p['emitted_mz_sites'],[])
 def test_source_only_generation_guard(self):
  real_bytes,real_text=Path.read_bytes,Path.read_text
  allowed={(R/s.SOURCE).resolve(),*(p.resolve()for p in [(R/'toolchains/msc510'/n)for n in ['MASM.EXE','manifest.json','LICENSE']]),(R/'config/msc510.json').resolve()}
  def permitted(p):return p.resolve()in allowed or(p.name in ['UNIT.OBJ','MASM.LOG','UNIT.LST','RESULT.TXT']and p.parent.name.startswith('serial-masm-'))
  def rb(p):
   if not permitted(p):raise AssertionError('Unexpected generation input '+str(p))
   return real_bytes(p)
  def rt(p,*a,**k):
   if not permitted(p):raise AssertionError('Unexpected generation input '+str(p))
   return real_text(p,*a,**k)
  with patch.object(Path,'read_bytes',rb),patch.object(Path,'read_text',rt):
   with self.assertRaises(AssertionError):(ROOT/'CHESS.EXE').read_bytes()
   built=s.assemble(R/s.SOURCE,R)
  self.assertEqual(built.code,self.built.code)
 def test_changed_actual_source_operand_rejected(self):
  p=(R/s.SOURCE).resolve();real=Path.read_bytes
  changed=real(p).replace(b'and al, 7fh',b'and al, 7eh');self.assertNotEqual(changed,real(p))
  with patch.object(Path,'read_bytes',lambda q:changed if q.resolve()==p else real(q)):
   with self.assertRaisesRegex(ValueError,'Source pin'):s.assemble(p,R)
 def test_tool_mutation_rejected(self):
  p=(R/'toolchains/msc510/MASM.EXE').resolve();real=Path.read_bytes
  with patch.object(Path,'read_bytes',lambda q:b'bad'if q.resolve()==p else real(q)):
   with self.assertRaisesRegex(ValueError,'assembler pin'):s.assemble(R/s.SOURCE,R)
 def test_manifest_license_config_mutations(self):
  real=Path.read_bytes
  for rel in ['toolchains/msc510/manifest.json','toolchains/msc510/LICENSE','config/msc510.json']:
   with self.subTest(rel=rel),patch.object(Path,'read_bytes',lambda q:b'bad'if q.resolve()==(R/rel).resolve()else real(q)):
    with self.assertRaisesRegex(ValueError,'pin mismatch'):s.assemble(R/s.SOURCE,R)
 def test_source_path_rejected(self):
  with self.assertRaisesRegex(ValueError,'source path'):s.assemble(R/'fake.asm',R)
 def test_closed_units(self):
  for edit in [lambda u:u.update(size=74),lambda u:u.update(size=180),lambda u:u.update(language='c'),lambda u:u.update(language='asm'),lambda u:u.update(public_symbols=['_enable_serial_irq_10d3_0023']),lambda u:u.update(image_offset='0x10d53')]:
   self.unit_bad(edit,'profile|Complete248')
 def test_foreign_function_metadata(self):
  for key in ['symbol','flags','owned_const','code_address','end_symbol']:
   self.unit_bad(lambda u:u.update({key:None}),'function/ownership')
 def test_binding_and_source_pins(self):
  self.unit_bad(lambda u:u['externals']['_serial_irq'].update(offset=3),'bindings')
  self.unit_bad(lambda u:u.update(source_sha256='0'*64),'Pinned')
  self.unit_bad(lambda u:u.update(assembler_sha256='0'*64),'Pinned')
 def test_extra_allocation(self):self.object_bad(lambda o:o.segments.update({3:copy.deepcopy(o.segments[1])}),'emptyDATA')
 def test_nonempty_DATA(self):self.object_bad(lambda o:setattr(o.segments[1],'length',2),'DATA0')
 def test_DATA_chunks(self):self.object_bad(lambda o:o.segments[1].chunks.append((0,b'\0\0')),'DATA0')
 def test_wrong_WORD_attributes(self):self.object_bad(lambda o:setattr(o.segments[2],'attributes',40),'WORD')
 def test_wrong_code_length(self):self.object_bad(lambda o:setattr(o.segments[2],'length',180),'CODE248')
 def test_hole(self):self.object_bad(lambda o:o.segments[2].chunks.__setitem__(0,(1,o.segments[2].chunks[0][1])),'hole')
 def test_overlap(self):self.object_bad(lambda o:o.segments[2].chunks.append((0,b'\0')),'overlap')
 def test_tail(self):
  def edit(o):at,b=o.segments[2].chunks[-1];o.segments[2].chunks[-1]=(at,b[:-1])
  self.object_bad(edit,'tail')
 def test_lidata(self):self.object_bad(lambda o:setattr(o.segments[2],'unsupported_data',True),'CODE248')
 def test_every_unlinked_byte_protected(self):
  for i in range(248):
   def edit(o):at,b=o.segments[2].chunks[0];o.segments[2].chunks[0]=(at,b[:i]+bytes([b[i]^1])+b[i+1:])
   with self.subTest(i=i):self.object_bad(edit,'instructions/addends')
 def test_wrong_public_identity(self):self.object_bad(lambda o:o.publics.update({'_fake':Public('_fake',2,109,0,0)}),'PUBLIC')
 def test_wrong_public_offset(self):self.object_bad(lambda o:o.publics.__setitem__('_enable_serial_irq_10d3_0023',Public('_enable_serial_irq_10d3_0023',2,36,0,0)),'PUBLIC')
 def test_foreign_external(self):self.object_bad(lambda o:o.externals.update({8:'_fake'}),'external')
 def test_no_fabricated_CV(self):self.object_bad(lambda o:o.procedures.update({'_fake':{}}),'procedure')
 def test_missing_field(self):self.object_bad(lambda o:o.fixups.pop(),'21 fields')
 def test_wrong_fixup_shapes(self):
  for change in [dict(frame=(5,None)),dict(target=(2,1)),dict(displacement=181),dict(location_type=2),dict(width=4),dict(segment_relative=False),dict(offset=180),dict(segment=1)]:
   self.object_bad(lambda o:o.fixups.__setitem__(2,dataclasses.replace(o.fixups[2],**change)),'21 fields')
 def test_foreign_records_and_group(self):
  for kind in [0xb0,0xb2,0xa2,0x94]:self.object_bad(lambda o:o.records.insert(1,(kind,0,b'')),'record sequence')
  def edit(o):o.records=[(k,at,b'bad'if k==0x9a else p)for k,at,p in o.records]
  self.object_bad(edit,'DGROUP')
 def test_wrong_overlay(self):self.object_bad(lambda o:setattr(o.segments[2],'overlay_index',2),'overlay')
 def test_wrong_THEADR(self):
  def edit(o):o.records=[(k,at,b'bad'if k==0x80 else p)for k,at,p in o.records]
  self.object_bad(edit,'THEADR')
 def test_linker_comment(self):
  def edit(o):o.records=[(k,at,b'bad'if k==0x88 else p)for k,at,p in o.records]
  self.object_bad(edit,'directive')
 def test_all_primary_pins(self):
  for rel in s.EVIDENCE_PINS:self.evidence_bad(rel,lambda e:e.update(fake=True))
 def test_subject_parameters_direct(self):
  e=json.loads((R/s.RAW_EVIDENCE).read_text());e['analysis_profile']['parameters']['load_segment']='0x2000'
  with self.assertRaisesRegex(ValueError,'loader parameters'):s._subject(e,s.ORIGINAL_SHA256,'read_bytes')
 def test_reference_context(self):
  self.assertTrue(s.validate_evidence(self.unit,R,s.ORIGINAL_SHA256,self.reference).startswith('ev_'))
  with self.assertRaisesRegex(ValueError,'original target'):s.validate_evidence(self.unit,R,'0'*64,self.reference)
  with self.assertRaisesRegex(ValueError,'Pinned expanded'):s.validate_evidence(self.unit,R,s.ORIGINAL_SHA256,None)
 def test_wrong_original_byte(self):
  b=bytearray(self.image);b[s.BASE+247]^=1
  with self.assertRaisesRegex(ValueError,'Complete248'):s.validate_comparison(self.unit,self.built,b,R,self.reference['relocations'])
 def test_extra_crossing_MZ(self):
  for at in [s.BASE-1,s.BASE,s.BASE+247]:
   with self.assertRaisesRegex(ValueError,'MZ'):s.validate_comparison(self.unit,self.built,self.image,R,[at])
 def test_no_public_extent_slicing(self):
  from omf import OMFObject
  with patch.object(OMFObject,'function_info',side_effect=AssertionError('no slicing')):
   s.validate_comparison(self.unit,self.built,self.image,R,self.reference['relocations'])
 def test_build_metadata_corruption(self):
  bad=dataclasses.replace(self.built,metadata=self.built.metadata|{'forged':True})
  with self.assertRaisesRegex(ValueError,'Build differs'):s.validate_comparison(self.unit,bad,self.image,R,[])
 def test_staged_production_fresh(self):
  with tempfile.TemporaryDirectory()as tmp:
   result=check.build_unit(self.unit,self.image,R,'nasm',{},Path(tmp),reference=self.reference)
   self.assertEqual(result.get('status'),'asm_code_matched',result)
   self.assertEqual(len(result['relocations']),21);self.assertEqual(result['authored_c_function_credit'],0)
   self.assertEqual(result['authored_asm_function_credit'],0);self.assertEqual(result['actual_size'],248)
 def test_real_minimal_report_and_require_complete(self):
  real=Path.read_text
  def read(p,*a,**k):
   if p.resolve()==(R/'config/units.json').resolve():return json.dumps([self.unit])
   if p.resolve()==(R/'config/source-inputs.json').resolve():return json.dumps({'schema_version':1,'source_allocations':[]})
   return real(p,*a,**k)
  with patch.object(Path,'read_text',read),tempfile.TemporaryDirectory()as tmp,patch.object(check,'ROOT',ROOT),patch.object(check,'HERE',R),patch.object(sys,'argv',['check.py','--target',str(ROOT/'CHESS.EXE'),'--output',tmp,'--require-complete']),redirect_stdout(io.StringIO()):
   code=check.main();report=json.loads((Path(tmp)/'report.json').read_text())
   self.assertEqual(code,1,report);summary=report['summary'];self.assertEqual(summary['failed_units'],0,report)
   self.assertEqual(summary['asm_code_matched_units'],1);self.assertEqual(summary['asm_code_matched_bytes'],248)
   self.assertEqual(summary['asm_matched_functions'],0);self.assertEqual(summary['c_matched_functions'],0)
   self.assertEqual(summary['source_data_bytes'],0);self.assertFalse(summary['full_executable_match'])
 def test_huff_dispatch_unchanged(self):
  old={'language':'asm-code','backend':'nasm-code-contribution-omf'}
  with patch.object(check.huff_allocation16,'validate_evidence',return_value='old-route')as guard:
   self.assertEqual(check.validate_rea_extent(old,R,s.ORIGINAL_SHA256,self.reference),'old-route');guard.assert_called_once()

 def test_unknown_metadata_keys_fail_closed(self):
  for key in ['slice','capacity','aliases','start','end','field_overrides','padding','symbol']:
   u=copy.deepcopy(self.unit);u[key]=0
   with self.subTest(key=key),self.assertRaisesRegex(ValueError,'metadata keys'):dispatcher.validate_unit(u)
  u=copy.deepcopy(self.unit);del u['boundary_evidence']
  with self.assertRaisesRegex(ValueError,'metadata keys'):dispatcher.validate_unit(u)
 def test_unsafe_project_mount_rejected_before_read_or_process(self):
  for char in ['"',chr(10),chr(13)]:
   project=Path('/tmp/unsafe'+char+'serial-project')
   with self.subTest(char=repr(char)),patch.object(Path,'read_bytes',side_effect=AssertionError('No file read')),patch.object(s.subprocess,'run',side_effect=AssertionError('No DOSBox')):
    with self.assertRaisesRegex(ValueError,'Unsafe assembler project path'):s.assemble(project/s.SOURCE,project)
 def test_unsafe_scratch_mount_rejected_before_write_or_process(self):
  from unittest.mock import MagicMock
  for char in ['"',chr(10),chr(13)]:
   cm=MagicMock();cm.__enter__.return_value='/tmp/unsafe'+char+'serial-scratch'
   with self.subTest(char=repr(char)),patch.object(s.tempfile,'TemporaryDirectory',return_value=cm),patch.object(Path,'write_bytes',side_effect=AssertionError('No scratch writes')),patch.object(s.subprocess,'run',side_effect=AssertionError('No DOSBox')):
    with self.assertRaisesRegex(ValueError,'Unsafe assembler scratch path'):s.assemble(R/s.SOURCE,R)
 def test_tail_evidence_all_pins_and_gap_limits(self):
  real=Path.read_bytes
  for rel in s.TAIL_EVIDENCE_PINS:
   content=(R/rel).read_bytes()
   with self.subTest(path=rel),patch.object(Path,'read_bytes',lambda p:content+b'X'if p.resolve()==(R/rel).resolve()else real(p)):
    with self.assertRaisesRegex(ValueError,'tail evidence pin'):s._evidence(R)
  raw,p=s._evidence(R);self.assertEqual(len(raw),248);self.assertEqual(p['tail_reachable_vs_span'],[38,39]);self.assertTrue(p['unowned_following8'])
 def test_old182_module_stays_closed_on_new248(self):
  oldunit=json.loads((R/'build/serial248-code-backend-stage/base-unit182.json').read_text())
  # The dispatcher opts by exact new profile; an old182 unit cannot select248.
  with self.assertRaises(ValueError):s.validate_unit(oldunit)
  unknown=copy.deepcopy(self.unit);unknown['object_profile']='serial_irq249'
  with self.assertRaises(ValueError):dispatcher.validate_unit(unknown)
  self.assertEqual(dispatcher.SOURCE_SHA256,'e3571172ef936c9adc81e8cb347ed84e0e656695bcbb5d21155d55adc61bbdb2')
 def test_dispatcher_new_profile_extract_and_source_generation(self):
  dispatcher.validate_unit(self.unit);raw,meta=dispatcher.extract_code(self.obj)
  self.assertEqual(raw,self.built.code);self.assertEqual(meta,self.built.metadata)
  built=dispatcher.assemble(R/s.SOURCE,R);self.assertEqual(built.object_bytes,self.built.object_bytes)
 def test_actual_semantic_timeout_source_negative(self):
  o=read_omf((R/'build/serial-tail-native-followup/negative/UNIT.OBJ').read_bytes())
  with self.assertRaisesRegex(ValueError,'instructions/addends'):s.extract_code(o)
 def test_no_zero_gap_or_single_entry_extent_admission(self):
  for size in [27,39,66,182,247,249,256]:
   u=copy.deepcopy(self.unit);u['size']=size
   with self.subTest(size=size),self.assertRaises(ValueError):dispatcher.validate_unit(u)
  self.assertEqual(self.built.metadata['segment']['length'],248)
 def test_no_parser_or_codeview_boundary_slicing(self):
  with patch.object(type(self.obj),'function_info',side_effect=AssertionError('PUB/CV slicing forbidden')):
   raw,proof=dispatcher.validate_comparison(self.unit,self.built,self.image,R,self.reference['relocations'])
  self.assertEqual(len(raw),248);self.assertFalse(proof['following8bytes_allocated']);self.assertTrue(proof['previous182_preserved'])

if __name__=='__main__':unittest.main()
