"""Pure DW integrity and unchanged legacy DD controls; no generators."""
from pathlib import Path
from copy import deepcopy
from dataclasses import replace
import json,struct,unittest,importlib.util,sys
import asm_data16 as b
from omf import read_omf
ROOT=Path(__file__).resolve().parents[1]
FIX=ROOT/'tests/fixtures/asset_records_DW'
PRE=b'bits 16\nsegment _DATA public align=2 class=DATA use16\ngroup DGROUP _DATA\nglobal _a\n_a:\n'
class HomogeneousDataWidths(unittest.TestCase):
 def bad(self,tail):
  with self.assertRaises(b.ASMDataError):b.parse_source(PRE+tail+b'\n')
 def test_legacy_DD_model_exact(self):
  self.assertEqual(b.parse_source(PRE+b'dd -1,0xffffffff,0\n'),{'symbols':['_a'],'offsets':{'_a':0},'numeric_values':[0xffffffff,0xffffffff,0]})
 def test_legacy_DD_complete_fixture(self):
  o=read_omf((FIX/'archive-DD.obj').read_bytes());m=b.parse_source((FIX/'archive-DD.asm').read_bytes());d,meta=b.extract_data(o,m['symbols']);self.assertEqual(len(d),896);self.assertEqual(d,b''.join(struct.pack('<I',x)for x in m['numeric_values']));self.assertNotIn('element_width',m);self.assertEqual(meta['boundary'],'complete_asm_data_SEGDEF')
 def test_legacy_DD_entire_metadata_and_model_unchanged(self):
  spec=importlib.util.spec_from_file_location('legacy_asmdata_fixture',FIX/'legacy_asm_data16.py');old=importlib.util.module_from_spec(spec);sys.modules[spec.name]=old;spec.loader.exec_module(old)
  raw=(FIX/'archive-DD.obj').read_bytes();src=(FIX/'archive-DD.asm').read_bytes();m=old.parse_source(src);self.assertEqual(b.parse_source(src),m);self.assertEqual(b.extract_data(read_omf(raw),m['symbols']),old.extract_data(read_omf(raw),m['symbols']))
 def test_legacy_DD_CPU_remains_rejected(self):
  with self.assertRaises(b.ASMDataError):b.parse_source(PRE.replace(b'bits 16\n',b'bits 16\ncpu 8086\n')+b'dd 0\n')
 def test_DW_signed_unsigned_boundaries(self):
  self.assertEqual(b.parse_source(PRE+b'dw -32768,65535,0xffff,0\n')['numeric_values'],[32768,65535,65535,0])
 def test_DW_width_offsets(self):
  m=b.parse_source(PRE+b'dw 1\nglobal _b\n_b:\ndw 2,3\n');self.assertEqual(m['offsets'],{'_a':0,'_b':2});self.assertEqual(m['element_width'],2)
 def test_DW_CPU8086_exact_optional(self):
  self.assertEqual(b.parse_source(PRE+b'dw 0\n'),b.parse_source(PRE.replace(b'bits 16\n',b'bits 16\ncpu 8086\n')+b'dw 0\n'))
 def test_DW_overflow_positive(self):self.bad(b'dw 65536')
 def test_DW_overflow_negative(self):self.bad(b'dw -32769')
 def test_DW_mixed_DD_before(self):self.bad(b'dd 0\ndw 0')
 def test_DW_mixed_DD_after(self):self.bad(b'dw 0\ndd 0')
 def test_DW_unknown_opcode(self):self.bad(b'dw 0\nmov ax,1')
 def test_DW_no_reservation(self):self.bad(b'dw 0\nresw 1')
 def test_DW_no_repeat(self):self.bad(b'times 2 dw 0')
 def test_DW_no_expressions(self):self.bad(b'dw 1+2')
 def test_DW_no_symbol_initializer(self):self.bad(b'dw _a')
 def test_DW_no_include(self):self.bad(b'dw 0\n%include "x"')
 def test_DW_no_trailing_empty_label(self):self.bad(b'dw 0\nglobal _b\n_b:')
 def test_DW_no_alias_labels(self):self.bad(b'global _b\n_b:\ndw 0')
 def test_DW_no_missing_global(self):self.bad(b'dw 0\n_b:\ndw 1')
 def test_DW_no_duplicate_global(self):self.bad(b'global _a\ndw 1')
 def test_DW_no_arbitrary_CPU(self):
  with self.assertRaises(b.ASMDataError):b.parse_source(PRE.replace(b'bits 16',b'bits 16\ncpu 386')+b'dw 0')
 def test_DW_no_DATA_alignment_change(self):
  with self.assertRaises(b.ASMDataError):b.parse_source(PRE.replace(b'align=2',b'align=4')+b'dw 0')
 def test_DW_genuine_complete120_160(self):
  for name,n in [('groups120',120),('frames160',160)]:
   raw=(FIX/(name+'.obj')).read_bytes();o=read_omf(raw);before=deepcopy(o);m=b.parse_source((FIX/(name+'.asm')).read_bytes());d,meta=b._extract_data(o,m['symbols'],2);self.assertEqual(d,b''.join(struct.pack('<H',x)for x in m['numeric_values']));self.assertEqual(len(d),n);self.assertEqual(o,before);self.assertEqual(meta['emitted_mz_sites'],[])
 def test_DW_complete_PUBLIC_no_subset(self):
  o=read_omf((FIX/'groups120.obj').read_bytes())
  for syms in [[],['_other'],['_asset_groups','_extra']]:
   with self.assertRaises(b.ASMDataError):b._extract_data(o,syms,2)
 def test_DW_group0_rejected(self):
  o=read_omf((FIX/'groups120.obj').read_bytes());p=o.publics['_asset_groups'];o.publics[p.name]=replace(p,group=0)
  with self.assertRaises(b.ASMDataError):b._extract_data(o,[p.name],2)
 def test_DW_hole_rejected(self):
  o=read_omf((FIX/'groups120.obj').read_bytes());seg=next(iter(o.segments.values()));at,d=seg.chunks[0];seg.chunks[0]=(at+2,d[2:])
  with self.assertRaises(b.ASMDataError):b._extract_data(o,['_asset_groups'],2)
 def test_DW_unknown_record_rejected(self):
  o=read_omf((FIX/'groups120.obj').read_bytes());o.records.append((0xb0,0,b''))
  with self.assertRaises(b.ASMDataError):b._extract_data(o,['_asset_groups'],2)
 def test_DW_only_exact_internal_width(self):
  with self.assertRaises(b.ASMDataError):b._extract_data(read_omf((FIX/'groups120.obj').read_bytes()),['_asset_groups'],1)
