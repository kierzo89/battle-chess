"""Staged platform659 closed backend tests. No canonical or frozen fixture writes."""
from pathlib import Path
import sys,json,copy,hashlib,dataclasses,tempfile,unittest,importlib.util,inspect
from unittest.mock import patch
TEST=Path(__file__).resolve();M=TEST.parents[1];D=M/'build/platform-code659-backend-stage'
sys.path.insert(0,str(M))
import platform_code16 as b
import check
EXPECTED_MODULE=M/'platform_code16.py'
EXPECTED_CHECK=M/'check.py'
from omf import read_omf
from reference import build_reference
TARGET=D.resolve().parents[1].parent/'CHESS.EXE'
H=lambda v:hashlib.sha256(v).hexdigest()
class Platform659Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.unit=json.loads((D/'proposed-unit.json').read_text());cls.positive=(M/'build/platform-code-10e30/guarded-positive.obj').read_bytes();cls.obj=read_omf(cls.positive)
  cls.reference=build_reference(TARGET.read_bytes());cls.native=cls.reference['image'];cls.raw,cls.metadata=b.extract_code(cls.obj)
 def fail(self,f,*args):
  with self.assertRaises((b.PlatformCodeError,ValueError,KeyError)):f(*args)
 def badunit(self,**kw):
  u=copy.deepcopy(self.unit);u.update(kw);self.fail(b.validate_unit,u)
 def badobj(self,mutate):
  o=copy.deepcopy(self.obj);mutate(o);self.fail(b.extract_code,o)
 def mutate_primary(self,name,mutate):
  rel='build/platform-code-10e30/'+name;e=json.loads((M/rel).read_text());mutate(e);content=(json.dumps(e)+'\n').encode();old=Path.read_bytes;pins=dict(b.EVIDENCE_PINS);pins[rel]=H(content)
  def reads(p):return content if p.resolve()==(M/rel).resolve()else old(p)
  with patch.object(Path,'read_bytes',reads),patch.object(b,'EVIDENCE_PINS',pins):self.fail(b._evidence,M)
 def test_module_path_guard(self):
  self.assertEqual(Path(b.__file__).resolve(),EXPECTED_MODULE.resolve());self.assertEqual(Path(check.__file__).resolve(),EXPECTED_CHECK.resolve())
 def test_generation_signature(self):self.assertEqual(list(inspect.signature(b.assemble).parameters),['source','project'])
 def test_unit_positive(self):b.validate_unit(self.unit)
 def test_backend_identity(self):self.badunit(backend='masm510-code-contribution-omf')
 def test_profile_identity(self):self.badunit(object_profile='platform659_copy')
 def test_foreign_metadata(self):self.badunit(owned_selector_const={})
 def test_no_ordinary_function(self):self.badunit(language='asm')
 def test_source_path(self):self.badunit(source='asm/link/other.asm')
 def test_source_pin(self):self.badunit(source_sha256='0'*64)
 def test_tool_pin(self):self.badunit(assembler_sha256='0'*64)
 def test_no_crop(self):self.badunit(size=658)
 def test_no_following_zero(self):self.badunit(size=660)
 def test_exact_base(self):self.badunit(image_offset=hex(b.BASE+1))
 def test_no_expanded_exception(self):self.badunit(reference_region='exepack-expanded')
 def test_public_order_and_no_alias(self):self.badunit(public_symbols=list(b.PUBLICS)[::-1])
 def test_native_bindings(self):
  ex=copy.deepcopy(b.BINDINGS);ex['_speed_2eb3']['offset']+=1;self.badunit(externals=ex)
 def test_no_ownership_or_function_metadata(self):
  for k in ('symbol','flags','owned_const','owned_data','owned_bss','code_address','extended_extent','compiler_source_name'):self.badunit(**{k:None})
 def test_raw_evidence_identity(self):self.badunit(rea_evidence='other.json')
 def test_source_policy_only_real_retry_DB(self):b.source_policy((D/'implementation/platform_hardware_omf.asm').read_bytes())
 def test_source_policy_reject_opcode_blob(self):self.fail(b.source_policy,b'drive_attempts DB 0\nDB 90h\n')
 def test_source_policy_reject_padding(self):
  for op in ('ORG 0','ALIGN 16','EVEN','DW 0','DUP(0)','INCLUDE file','INCBIN file'):self.fail(b.source_policy,('drive_attempts DB 0\n'+op).encode())
 def test_source_policy_reject_missing_retry(self):self.fail(b.source_policy,b'NOP\n')
 def test_exact_whole_segment_and_no_debug(self):
  self.assertEqual(len(self.raw),659);self.assertFalse(self.obj.procedures);self.assertEqual(self.metadata['authored_asm_function_credit'],0)
 def test_wrong_code_attribute(self):self.badobj(lambda o:setattr(o.segments[2],'attributes',72))
 def test_code_tail(self):self.badobj(lambda o:setattr(o.segments[2],'length',660))
 def test_extra_data(self):self.badobj(lambda o:setattr(o.segments[1],'length',1))
 def test_extra_segment(self):self.badobj(lambda o:o.segments.update({3:copy.deepcopy(o.segments[1])}))
 def test_public_alias(self):self.badobj(lambda o:o.publics.update({'_alias':next(iter(o.publics.values()))}))
 def test_public_offset(self):self.badobj(lambda o:o.publics.update({'_initialize_video':dataclasses.replace(o.publics['_initialize_video'],offset=483)}))
 def test_external_name(self):self.badobj(lambda o:o.externals.update({1:'_fake_storage'}))
 def test_segment_names(self):self.badobj(lambda o:o.names.append('EXTRA'))
 def test_no_common_or_debug_records(self):
  for k in (0xb0,0xa2,0x8e):self.badobj(lambda o,k=k:o.records.append((k,1257,b'\0')))
 def test_code_hole(self):self.badobj(lambda o:setattr(o.segments[2],'chunks',[(1,self.raw)]))
 def test_code_overlap(self):self.badobj(lambda o:setattr(o.segments[2],'chunks',[(0,self.raw),(658,b'\0')]))
 def test_every_code_byte_is_pinned(self):
  for i in range(659):
   changed=bytearray(self.raw);changed[i]^=1;self.badobj(lambda o,c=bytes(changed):setattr(o.segments[2],'chunks',[(0,c)]))
 def test_missing_field(self):self.badobj(lambda o:o.fixups.pop())
 def test_wrong_field_frame(self):self.badobj(lambda o:o.fixups.__setitem__(0,dataclasses.replace(o.fixups[0],frame=(5,None))))
 def test_wrong_field_target(self):self.badobj(lambda o:o.fixups.__setitem__(0,dataclasses.replace(o.fixups[0],target=(2,2))))
 def test_wrong_field_width(self):self.badobj(lambda o:o.fixups.__setitem__(0,dataclasses.replace(o.fixups[0],width=4)))
 def test_wrong_selfrel_mode(self):self.badobj(lambda o:o.fixups.__setitem__(19,dataclasses.replace(o.fixups[19],segment_relative=True)))
 def test_wrong_far_displacement(self):self.badobj(lambda o:o.fixups.__setitem__(23,dataclasses.replace(o.fixups[23],displacement=360)))
 def test_complete_record_identity(self):self.badobj(lambda o:o.records.__setitem__(0,(0x80,0,b'\x07ALT.ASM')))
 def test_all_native_and_mz_four_bases(self):
  built=b.Build(self.positive,self.raw,self.metadata,{})
  linked,p=b.validate_comparison(self.unit,built,self.native,M,self.reference['relocations'])
  self.assertEqual(linked,self.native[b.BASE:b.BASE+659]);self.assertEqual(p['emitted_mz_sites'],[0x11020]);self.assertTrue(all(r['all659_native_bytes_equal']for r in p['four_load_bases']));self.assertEqual(len(p['relocations']),35)
 def test_exact_partition_native_evidence(self):self.assertEqual(len(b._evidence(M)[0]),660)
 def test_unchanged_prefix_evidence_gate(self):b.validate_evidence(self.unit,M,b.ORIGINAL_SHA256,self.reference)
 def test_wrong_original_subject(self):self.fail(b.validate_evidence,self.unit,M,'0'*64,self.reference)
 def test_wrong_carrier_reference(self):
  r=dict(self.reference,carrier_sha256='0'*64);self.fail(b.validate_evidence,self.unit,M,b.ORIGINAL_SHA256,r)
 def test_prefix_must_cover659(self):
  r=dict(self.reference,prefix_size=b.BASE+658);self.fail(b.validate_evidence,self.unit,M,b.ORIGINAL_SHA256,r)
 def test_omit_and_extra_and_crossing_mz(self):
  for sites in ([],[0x11020,b.BASE+1],[0x11020,b.BASE-1],[0x11020,b.BASE+658],[0x11020,0x11020]):self.fail(b._sites,sites)
 def test_wrong_native_kind(self):self.mutate_primary('rea-whole660.json',lambda e:e['subject'].update(format='raw'))
 def test_wrong_native_provider(self):self.mutate_primary('rea-whole660.json',lambda e:e['provider'].update(id='r2'))
 def test_wrong_native_profile_parameters(self):self.mutate_primary('rea-whole660.json',lambda e:e['analysis_profile']['parameters'].update(load_segment='0x2000'))
 def test_wrong_native_operation(self):self.mutate_primary('rea-whole660.json',lambda e:e.update(operation='analyze_function'))
 def test_wrong_read_parameters(self):self.mutate_primary('rea-whole660.json',lambda e:e['parameters'].update(length=659))
 def test_partial_native_read(self):self.mutate_primary('rea-whole660.json',lambda e:e['normalized_result'].update(complete=False))
 def test_wrong_native_procedure_bounds(self):self.mutate_primary('rea-sound-entry.json',lambda e:e['normalized_result']['procedure']['body'].update(span_bytes=129))
 def test_disjoint_native_procedure(self):self.mutate_primary('rea-sound-entry.json',lambda e:e['normalized_result']['procedure']['body'].update(non_contiguous=True))
 def test_duplicate_evidence_ids(self):
  eid=json.loads((M/b.RAW_EVIDENCE).read_text())['evidence_id'];self.mutate_primary('rea-sound-entry.json',lambda e:e.update(evidence_id=eid))
 def test_raw_interrupt_not_fabricated_procedure(self):
  e=json.loads((M/'build/platform-code-10e30/rea-timer-handler.json').read_text());self.assertIn('No procedure exists',str(e));self.assertEqual(self.raw[348],0x50)
 def test_link_closed_placement_domain(self):
  ex={k:(v['segment'],v['offset'])for k,v in b.BINDINGS.items()};self.fail(b.link,self.obj,{1:(0x5cc2,0),2:(0x10e3,0),3:(0,0)},{1:0x5cc2},ex)
 def test_near_external_frame_mismatch(self):
  ex={k:(v['segment'],v['offset'])for k,v in b.BINDINGS.items()};ex['_speed_2eb3']=(0x5cc3,0x2eb3);self.fail(b.link,self.obj,{1:(0x5cc2,0),2:(0x10e3,0)},{1:0x5cc2},ex)
 def test_whole_segment_fit(self):
  ex={k:(v['segment'],v['offset'])for k,v in b.BINDINGS.items()};self.fail(b.link,self.obj,{1:(0x5cc2,0),2:(0x10e3,65500)},{1:0x5cc2},ex)
 def test_native_partial_LINK_own8_fields(self):
  data=(M/'build/future-platform-input-data-LINK-252/LINK/PARTIAL.EXE').read_bytes();header=int.from_bytes(data[8:10],'little')*16;image=data[header:];maptext=(M/'build/future-platform-input-data-LINK-252/LINK/PARTIAL.MAP').read_text()
  import re
  for name,at in b.PUBLICS.items():self.assertRegex(maptext,rf'(?i)0EFE:{at:04X}\s+{name}\b')
  mzoff=int.from_bytes(data[24:26],'little');count=int.from_bytes(data[6:8],'little');sites={int.from_bytes(data[mzoff+4*i+2:mzoff+4*i+4],'little')*16+int.from_bytes(data[mzoff+4*i:mzoff+4*i+2],'little')for i in range(count)}
  for f in self.obj.fixups:
   if f.target!=(0,2):continue
   disp=f.displacement
   expected=(((disp-(f.offset+2))&65535).to_bytes(2,'little') if not f.segment_relative else disp.to_bytes(2,'little'))
   if f.width==4:expected+=bytes.fromhex('fe0e');self.assertIn(0xefe0+f.offset+2,sites)
   self.assertEqual(image[0xefe0+f.offset:0xefe0+f.offset+f.width],expected)
 def test_production_route_and_require_complete_status(self):
  p=json.loads((D/'production-proof.json').read_text());self.assertEqual(p['positive_status'],'asm_code_matched');self.assertTrue(p['actual_original_and_carrier_read_attempts_blocked'])
 def test_positive_object_source_tool_only_generation_proof(self):
  p=json.loads((D/'production-proof.json').read_text());self.assertTrue(all('CHESS.EXE'not in q and 'TRIM5_UNPACK.EXE'not in q for q in p['generation_reads']))
 def test_real_wrong_delay_reaches_normal_mismatch(self):
  p=json.loads((D/'negative-proof.json').read_text());self.assertEqual(p['status'],'mismatch');self.assertEqual(p['first_difference'],18);self.assertTrue(p['fresh_actual_generation']);self.assertEqual(p['difference_count'],1)
 def test_actual_fresh_generation_source_tools_scratch_guard(self):
  project=D/'mirror';old=Path.read_bytes;oldtext=Path.read_text;reads=[]
  allowed={(project/b.SOURCE).resolve(),*(p.resolve()for p in [project/'toolchains/msc510/MASM.EXE',project/'toolchains/msc510/manifest.json',project/'toolchains/msc510/LICENSE',project/'config/msc510.json'])}
  def allow(p):
   q=p.resolve()
   if q not in allowed and not any(x.startswith('platform-masm-')for x in q.parts):raise PermissionError('No target/foreign generation reads')
   reads.append(str(q))
  def binary(p):allow(p);return old(p)
  def text(p,*a,**kw):allow(p);return oldtext(p,*a,**kw)
  with patch.object(Path,'read_bytes',binary),patch.object(Path,'read_text',text):
   for forbidden in (TARGET,D.parents[1]/'build/exepack/TRIM5_UNPACK.EXE'):
    with self.assertRaises(PermissionError):forbidden.read_bytes()
   built=b.assemble(project/b.SOURCE,project)
  self.assertEqual(built.object_bytes,self.positive);self.assertTrue(reads);self.assertFalse(any('CHESS.EXE'in q or 'TRIM5_UNPACK.EXE'in q for q in reads))
 def test_normal_report_keeps_function_data_credit_zero(self):
  p=json.loads((D/'normal-report-proof.json').read_text());s=p['summary'];self.assertEqual(s['asm_code_matched_bytes'],659);self.assertEqual(s['c_matched_functions'],0);self.assertEqual(s['asm_matched_functions'],0);self.assertEqual(s['source_data_units'],0);self.assertEqual(p['require_complete_returncode'],1)
 def test_complete_source_object_pin(self):
  self.assertEqual(H(self.positive),b.OBJECT_SHA256);self.assertEqual(H((D/'implementation/platform_hardware_omf.asm').read_bytes()),b.SOURCE_SHA256)
 def test_wrong_far_source_frame(self):
  self.badobj(lambda o:o.fixups.__setitem__(23,dataclasses.replace(o.fixups[23],frame=(1,1))))
 def test_missing_retry_byte_primary(self):self.mutate_primary('rea-drive-attempt-byte1.json',lambda e:e['normalized_result'].update(bytes_hex='01'))
 def test_wrong_native_loaded_instruction(self):
  changed=bytearray(self.native);changed[b.BASE+18]^=1;self.fail(b.validate_comparison,self.unit,b.Build(self.positive,self.raw,self.metadata,{}),bytes(changed),M,self.reference['relocations'])
if __name__=='__main__':unittest.main()
