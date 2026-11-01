"""Canonical-ready tests for the two independent closed flags profiles."""
from pathlib import Path
import os,sys,json,hashlib,copy,dataclasses,tempfile,unittest
from unittest.mock import patch,MagicMock
R=Path(os.environ.get('FLAGS_TEST_PROJECT',Path(__file__).resolve().parents[1])).resolve();sys.path.insert(0,str(R))
import graphics_wrapper_flags_code16 as w,input_flags_code16 as n,graphics_wrapper_code16 as old,check
from omf import read_omf,OMFError
D=R/'build/input-flags-backend-migration-stage';F=R/'build/input-flags4952-coherent'
J=lambda p:json.loads(p.read_text());H=lambda b:hashlib.sha256(b).hexdigest()
WRAW=(F/'graphics_wrapper_flags.obj').read_bytes();NRAW=(F/'input_poll_flags.obj').read_bytes();WRONG=(F/'wrong_input_poll_flags.obj').read_bytes();UNITS=J(D/'proposed-code-units.json')
def rec(k,p):
 b=bytes([k])+(len(p)+1).to_bytes(2,'little')+p;return b+bytes([-sum(b)&255])
def mutate(kind,fn,nth=0):
 out=[];seen=0
 for k,_,p in read_omf(NRAW).records:
  if k==kind:
   if seen==nth:p=fn(bytearray(p))
   seen+=1
  out.append(rec(k,bytes(p)))
 assert seen>nth;return b''.join(out)
def at(i,b):
 def f(p):p[i:i+len(b)]=b;return p
 return f
class FlagsMigrationTests(unittest.TestCase):
 def reject(self,raw,shape=False):
  with patch.object(n,'OBJECT_HASHES',{H(raw)} if shape else n.OBJECT_HASHES):
   with self.assertRaises(OMFError):n.extract_code(raw)
 def test_actual_imports_and_minimal_routes(self):
  for module in [w,n,old,check]:self.assertEqual(Path(module.__file__).resolve(),R/(module.__name__+'.py'))
  for unit in UNITS:check.validate_units([unit],1,500000)
 def test_complete_allocations_actual_publics_fields(self):
  for module,raw,size,count in [(w,WRAW,78,15),(n,NRAW,388,34)]:
   code,meta=module.extract_code(read_omf(raw)if module is w else raw);self.assertEqual(len(code),size);self.assertEqual(len(read_omf(raw).fixups),count);self.assertFalse(read_omf(raw).procedures);self.assertEqual(len(read_omf(raw).publics),3)
 def test_true_latch_member_FIXUPPs(self):
  obj=read_omf(NRAW);fields=[f for f in obj.fixups if f.displacement==1];self.assertEqual([(f.offset,f.frame,f.target,f.raw.hex())for f in fields],[(252,(1,1),(2,6),'c4fc1201060100'),(257,(1,1),(2,6),'c5011201060100')]);self.assertEqual(obj.externals[6],'_input_flags_4952')
  code,logs=n.link(NRAW);self.assertEqual(code[252:254],b'\x53\x49');self.assertEqual(code[257:259],b'\x53\x49');self.assertEqual([(r['object_offset'],r['displacement'])for r in logs if r['target_symbol']=='_input_flags_4952'],[(252,1),(257,1)])
 def test_wrapper_true_aggregate_member0(self):
  o=read_omf(WRAW);self.assertEqual(o.externals[6],'_input_flags_4952');self.assertEqual([(f.offset,f.displacement)for f in o.fixups if f.target==(2,6)],[(1,None),(6,None),(31,None),(36,None),(50,None)])
 def test_wrong_member_rejected_precisely(self):
  with self.assertRaisesRegex(ValueError,'All34 actual raw fields'):n.extract_code(WRONG)
 def test_old_wrapper_rejects_new_profile(self):
  with self.assertRaises(ValueError):old.extract_code(read_omf(WRAW))
 def test_new_rejects_old_profile(self):
  with self.assertRaises(ValueError):w.extract_code(read_omf((R/'build/input-flags-backend-migration-stage/old-wrapper.obj').read_bytes()))
  self.reject((R/'build/input-neighbours-11f3e/input_poll_context_exact.obj').read_bytes())
 def test_no_target_reads_in_arithmetic(self):
  with patch.object(Path,'read_bytes',side_effect=AssertionError('pure arithmetic')),patch.object(Path,'read_text',side_effect=AssertionError('pure arithmetic')):
   code,logs=n.link(NRAW);ex={k:(v['segment'],v['offset'])for k,v in w.BINDINGS.items()};b,l=w.link(read_omf(WRAW),{1:(0x5cc2,0),2:(0x11ef,0)},{1:0x5cc2},ex)
  self.assertEqual(len(code+b),466);self.assertEqual(len(logs+l),49)
 def test_native_proofs_and_four_loader_bases(self):
  for module,raw in [(w,WRAW),(n,NRAW)]:
   loaded,_=module._evidence(R)
   if module is w:
    code,logs=module.link(read_omf(raw),{1:(0x5cc2,0),2:(0x11ef,0)},{1:0x5cc2},{k:(v['segment'],v['offset'])for k,v in module.BINDINGS.items()});sites=module.MZ_SITES
   else:code,logs=module.link(raw);sites=[r['mz_segment_relocation_image_offset']for r in logs if'mz_segment_relocation_image_offset'in r]
   self.assertEqual(module._forward(code,sites,4096),loaded[:len(code)])
   for base in [0,1,4096,65535]:
    if module is w:
     b,_=module.link(read_omf(raw),{1:((0x5cc2+base)&65535,0),2:((0x11ef+base)&65535,0)},{1:(0x5cc2+base)&65535},{k:((v['segment']+base)&65535,v['offset'])for k,v in module.BINDINGS.items()})
    else:b,_=module.link(raw,code_frame=(0x11ef+base)&65535,dgroup=(0x5cc2+base)&65535)
    self.assertEqual(b,module._forward(code,sites,base));self.assertEqual(b[252:254],b'\x53\x49')if module is n else None
 def test_checksum(self):self.reject(NRAW[:4]+bytes([NRAW[4]^1])+NRAW[5:])
 def test_extra_trailing(self):self.reject(NRAW+b'X')
 def test_hidden_DATA(self):self.reject(mutate(0x98,at(1,b'\x02\0')),True)
 def test_wrong_CODE_size(self):self.reject(mutate(0x98,at(1,b'\x83\x01'),1),True)
 def test_wrong_alignment(self):self.reject(mutate(0x98,at(0,b'\x68'),1),True)
 def test_own_group_wrong(self):self.reject(mutate(0x9a,at(2,b'\x02')),True)
 def test_foreign_external(self):self.reject(mutate(0x8c,at(1,b'X')),True)
 def test_real_FIXUPP_byte(self):self.reject(mutate(0x9c,at(1,b'\0')),True)
 def test_missing_LED_tail(self):self.reject(mutate(0xa0,lambda p:p[:-1]),True)
 def test_extra_LED_tail(self):self.reject(mutate(0xa0,lambda p:p+b'\x90'),True)
 def test_LED_hole(self):self.reject(mutate(0xa0,at(1,b'\x01\0')),True)
 def test_CODE_opcode_protection_even_without_wholehash(self):self.reject(mutate(0xa0,at(3,b'\x90')),True)
 def test_no_metadata_escape(self):
  for module,u in zip([w,n],UNITS):
   for key in ['capacity','alias','slice','owned_data','code_address','symbol']:
    with self.subTest(key=key),self.assertRaises(ValueError):module.validate_unit(u|{key:None})
 def test_no_small_slice_or_wrong_profile(self):
  for module,u in zip([w,n],UNITS):
   for key,value in [('size',u['size']-1),('object_profile','anything'),('backend',old.BACKEND),('source_sha256','0'*64)]:
    with self.subTest(key=key),self.assertRaises(ValueError):module.validate_unit(u|{key:value})
 def test_wrong_external_binding_rejected(self):
  for module,u in zip([w,n],UNITS):
   bad=copy.deepcopy(u);bad['externals']['_input_flags_4952']['offset']+=1
   with self.assertRaises(ValueError):module.validate_unit(bad)
 def test_MZ_missing_extra_crossing_rejected(self):
  for module,sites,size in [(w,w.MZ_SITES,78),(n,[n.BASE+f[1]+2 for f in n.FIELD_PROFILE if f[2]==4],388)]:
   fn=module._sites if module is w else module._native_sites
   for wrong in [sites[:-1],sites+[module.BASE-1],sites+[module.BASE+size-1],sites+[module.BASE]]:
    with self.subTest(wrong=wrong),self.assertRaises(ValueError):fn(wrong)
 def test_unsafe_project_no_reads(self):
  for module,source in [(w,w.SOURCE),(n,next(iter(n.SOURCES)))]:
   for c in ['"',chr(10),chr(13)]:
    p=Path('/tmp/flags'+c)
    with patch.object(Path,'read_bytes',side_effect=AssertionError('No read')),self.assertRaisesRegex(ValueError,'Unsafe assembler project'):module.assemble(p/source,p)
 def test_source_symlink_rejected(self):
  with tempfile.TemporaryDirectory()as temp:
   p=Path(temp)/'source.asm';p.symlink_to(R/w.SOURCE)
   for module in [w,n]:
    with self.assertRaisesRegex(ValueError,'symlink'):module.assemble(p,R)
 def test_tool_pins_fail_before_DOSBox(self):
  read=Path.read_bytes;bad=(R/'toolchains/msc510/MASM.EXE').resolve()
  for module,source in [(w,w.SOURCE),(n,next(iter(n.SOURCES)))]:
   with patch.object(Path,'read_bytes',lambda p:b'bad'if p.resolve()==bad else read(p)),patch.object(module.subprocess,'run',side_effect=AssertionError('No DOSBox')):
    with self.assertRaises((ValueError,AssertionError)):module.assemble(R/source,R)
 def test_unsafe_scratch_before_write(self):
  for module,source in [(w,w.SOURCE),(n,next(iter(n.SOURCES)))]:
   for c in ['"',chr(10),chr(13)]:
    context=MagicMock();context.__enter__.return_value='/tmp/flags'+c
    with patch.object(module.tempfile,'TemporaryDirectory',return_value=context),patch.object(Path,'write_bytes',side_effect=AssertionError('No scratch write')),patch.object(module.subprocess,'run',side_effect=AssertionError('No DOSBox')):
     with self.assertRaisesRegex(ValueError,'Unsafe assembler scratch'):module.assemble(R/source,R)
 def test_legacy_backend_routes_preserved(self):
  for module in [check.graphics_wrapper_code16,check.graphics_code16,check.blit_code16,check.serial_code16,check.huff_allocation16]:
   with patch.object(module,'validate_evidence',return_value='old')as mock:
    self.assertEqual(check.validate_rea_extent({'language':'asm-code','backend':getattr(module,'BACKEND','nasm-code-contribution-omf')},R,w.ORIGINAL_SHA256,{}),'old');mock.assert_called_once()
 def test_new_backend_routes_distinct(self):
  for module,u in zip([w,n],UNITS):
   with patch.object(module,'validate_evidence',return_value='new')as mock:
    self.assertEqual(check.validate_rea_extent(u,R,w.ORIGINAL_SHA256,{}),'new');mock.assert_called_once()
 def test_no_assembler_source_replacement(self):
  read=Path.read_bytes
  for module,source in [(w,w.SOURCE),(n,next(iter(n.SOURCES)))]:
   p=(R/source).resolve()
   with patch.object(Path,'read_bytes',lambda q:read(q)+b'\n;'if q.resolve()==p else read(q)),self.assertRaisesRegex(ValueError,'Source pin'):module.assemble(p,R)
if __name__=='__main__':unittest.main(verbosity=2)
