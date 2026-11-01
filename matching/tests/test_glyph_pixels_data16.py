"""Closed-profile negative controls; mutations are test data, never production OMF."""
from pathlib import Path
import sys,unittest,json
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent;M=next(p for p in HERE.parents if(p/'config/msc500.json').is_file());sys.path[:0]=[str(HERE),str(M)]
import glyph_pixels_data16 as gate
assert Path(gate.__file__).resolve()==M/'glyph_pixels_data16.py' # canonical-ready: fail if a staged module is substituted
from omf import read_omf,OMFError
from cdata import extract_data as ordinary_data
P=M/'build/text-glyph-pixels-data-4500'
RAW=(M/'build/text-glyph-data-backend-stage/text_glyph_pixels.obj').read_bytes();NEG=(M/'build/text-glyph-data-backend-stage/wrong_glyph_pixels.obj').read_bytes()
def rec(kind,payload):
 body=bytes([kind])+(len(payload)+1).to_bytes(2,'little')+payload
 return body+bytes([-sum(body)&255])
def mutate(kind,func,nth=0):
 records=read_omf(RAW).records;seen=0;out=[]
 for k,_,payload in records:
  if k==kind:
   if seen==nth:payload=func(bytearray(payload))
   seen+=1
  out.append(rec(k,bytes(payload)))
 assert seen>nth, 'Test mutation selected a missing record'
 return b''.join(out)
def patchat(index,data):
 def f(p):p[index:index+len(data)]=data;return p
 return f
class GlyphPixelsTests(unittest.TestCase):
 def reject(self,raw):
  with self.assertRaises(OMFError):gate.extract_data(raw)
 def test_positive_whole32_and_typed16(self):
  raw,meta=gate.extract_data(RAW);self.assertEqual(raw,bytes(32));self.assertEqual(meta['cv']['array_elements'],16);self.assertEqual(meta['cv']['element_bits'],16);self.assertEqual(meta['segment']['length'],32);self.assertEqual(meta['data_writes'][1]['repeat_count'],15);self.assertEqual(meta['data_writes'][1]['offset'],2);self.assertTrue(meta['all_segments'][1]['unsupported_data_retained']);self.assertEqual(read_omf(RAW).segments[2].unsupported_data,True)
 def test_semantic_first_word_is_not_masked(self):
  raw,meta=gate.extract_data(NEG);self.assertEqual(raw,b'\x01\0'+bytes(30));self.assertNotEqual(raw,bytes(32));self.assertEqual(meta['data_writes'][0]['literal_hex'],'0100')
 def test_ordinary_validator_still_rejects(self):
  with self.assertRaisesRegex(OMFError,'iterated LIDATA'):ordinary_data(read_omf(RAW),gate.SYMBOL)
 def test_checksum_corruption(self):self.reject(RAW[:15]+bytes([RAW[15]^1])+RAW[16:])
 def test_trailing_object_bytes(self):self.reject(RAW+b'\0')
 def test_non_raw_input(self):self.reject(read_omf(RAW))
 def test_unreviewed_public(self):
  with self.assertRaises(OMFError):gate.extract_data(RAW,'_other')
 def test_segdef_short(self):self.reject(mutate(0x98,patchat(1,b'\x1e\0'),1))
 def test_segdef_long(self):self.reject(mutate(0x98,patchat(1,b'\x22\0'),1))
 def test_extra_bss_allocation(self):self.reject(mutate(0x98,patchat(1,b'\x02\0'),3))
 def test_foreign_empty_segment_identity(self):self.reject(mutate(0x98,patchat(3,b'\x03'),3))
 def test_segment_alignment(self):self.reject(mutate(0x98,patchat(0,b'\x68'),1))
 def test_cv_bit_capacity(self):self.reject(mutate(0xa0,patchat(3+17,b'\x02'),1))
 def test_cv_element_type(self):self.reject(mutate(0xa0,patchat(3+20,b'\x80'),1))
 def test_public_offset(self):self.reject(mutate(0x90,patchat(21,b'\x02')))
 def test_public_group(self):self.reject(mutate(0x90,patchat(0,b'\0')))
 def test_public_type(self):self.reject(mutate(0x90,patchat(23,b'\x04')))
 def test_group_membership(self):self.reject(mutate(0x9a,lambda p:p[:-2]))
 def test_extern_startup_marker(self):self.reject(mutate(0x8c,patchat(1,b'X')))
 def test_extra_record(self):self.reject(RAW[:-4]+rec(0xa0,bytes.fromhex('0200000000'))+RAW[-4:])
 def test_thread_metadata_changed(self):self.reject(mutate(0x9c,patchat(1,b'\x02')))
 def test_explicit_word_hole(self):self.reject(mutate(0xa0,patchat(1,b'\x01\0'),0))
 def test_explicit_word_short(self):self.reject(mutate(0xa0,lambda p:p[:-1],0))
 def test_lidata_overlap(self):self.reject(mutate(0xa2,patchat(1,b'\0\0')))
 def test_lidata_hole(self):self.reject(mutate(0xa2,patchat(1,b'\x04\0')))
 def test_lidata_foreign_segment(self):self.reject(mutate(0xa2,patchat(0,b'\x03')))
 def test_lidata_short_repeat(self):self.reject(mutate(0xa2,patchat(3,b'\x0e\0')))
 def test_lidata_long_repeat(self):self.reject(mutate(0xa2,patchat(3,b'\x10\0')))
 def test_lidata_nested(self):self.reject(mutate(0xa2,patchat(5,b'\x01\0')))
 def test_lidata_literal_length(self):self.reject(mutate(0xa2,patchat(7,b'\x01')))
 def test_lidata_literal_changed(self):self.reject(mutate(0xa2,patchat(8,b'\x01')))
 def test_lidata_trailing_payload(self):self.reject(mutate(0xa2,lambda p:p+b'\0'))
 def test_closed_unit(self):
  u=dict(language='c-data',backend=gate.BACKEND,symbol=gate.SYMBOL,flags=gate.FLAGS,size=32,reference_region='exepack-expanded',externals={});gate.validate_unit(u)
  for changes in [dict(size=30),dict(externals={'_x':1}),dict(owned_bss={}),dict(flags=['/AS'])]:
   with self.subTest(changes=changes),self.assertRaises(OMFError):gate.validate_unit(dict(u,**changes))
class CompilerProvenanceTests(unittest.TestCase):
 def candidate(self):
  proof=json.loads((M/'build/text-glyph-data-backend-stage/proof.json').read_text());c=proof['rows'][0]['compiler'];return SimpleNamespace(**c,object_bytes=RAW)
 def check_bad(self,**changes):
  c=self.candidate();c.__dict__.update(changes)
  with self.assertRaises(OMFError):gate.validate_compiled(c,(P/'text_glyph_pixels.c').read_bytes())
 def test_real_compiler_provenance(self):
  data,_=gate.validate_compiled(self.candidate(),(P/'text_glyph_pixels.c').read_bytes());self.assertEqual(data,bytes(32))
 def test_wrong_source_fingerprint(self):self.check_bad(source_sha256='0'*64)
 def test_unreviewed_source_bytes(self):
  with self.assertRaises(OMFError):gate.validate_compiled(self.candidate(),b'unsigned int other[16]={0};')
 def test_wrong_compiler(self):self.check_bad(compiler='msc510')
 def test_named_source_rejected(self):self.check_bad(source_name='COLOUR.C')
 def test_wrong_flags(self):self.check_bad(flags=['/AS','/Zi'])
 def test_wrong_manifest(self):self.check_bad(toolchain_manifest_sha256='0'*64)
 def test_wrong_tool(self):
  tools=dict(self.candidate().tool_hashes);tools['C2.EXE']='0'*64;self.check_bad(tool_hashes=tools)
 def test_wrong_command(self):self.check_bad(command=['T:\\CL.EXE','/c','/FoC:\\OTHER.OBJ'])
if __name__=='__main__':unittest.main(verbosity=2)
