"""Prepared inert focused controls. No C5, LINK or emitted/fill positive fixtures."""
from pathlib import Path
from types import SimpleNamespace
import copy,json,os,sys,tempfile,unittest
M=Path(os.environ.get('BC_LABELS15_PROJECT',Path(__file__).resolve().parents[1])).resolve();CORE=next(p for p in Path(__file__).resolve().parents if(p/'config/msc500.json').is_file());sys.path[:0]=[str(M),str(CORE)];sys.dont_write_bytecode=True
import animation_labels_data16 as h
from animation_labels15_pins import TOOLS
from omf import read_omf
from cdata import extract_data,CDataError
F=Path(__file__).resolve().parent/'fixtures/animation_labels';RAW=(F/'labels.obj').read_bytes();SOURCE=(F/'labels.c').read_bytes();UNIT=json.loads((F/'unit-labels.json').read_text())
def record(k,p):
 b=bytes([k])+(len(p)+1).to_bytes(2,'little')+p;return b+bytes([-sum(b)&255])
def rewrite(k,fn):
 out=[];at=0;done=False
 while at<len(RAW):
  kind=RAW[at];n=int.from_bytes(RAW[at+1:at+3],'little');p=RAW[at+3:at+2+n]
  if kind==k and not done:
   x=fn(p)
   if x!=p:p=x;done=True
  out.append(record(kind,p));at+=3+n
 assert done;return b''.join(out)
def insert(k,p):
 at=read_omf(RAW).records[-1][1];return RAW[:at]+record(k,p)+RAW[at:]
class AnimationLabelDataControls(unittest.TestCase):
 def reject(self,b):
  with self.assertRaises(ValueError):h.validate_raw(b)
 def test_actual_raw_literal14_single_hole1(self):
  r=h.validate_raw(RAW);self.assertEqual(r['source_literal_bytes'],14);self.assertEqual(r['raw_uninitialized_alignment'],{'offset':7,'length':1});self.assertEqual(sum(x['length']for x in r['literal_writes']),14)
 def test_old_generic_parser_still_rejects_hole(self):
  with self.assertRaisesRegex(CDataError,'hole'):extract_data(read_omf(RAW),h.NAMES[0])
 def test_unsized_exact_source(self):
  self.assertEqual(h.sha(SOURCE),h.SOURCE_SHA);self.assertIn(b'[] = "Black:";',SOURCE);self.assertIn(b'[] = "White:";',SOURCE);self.assertNotIn(b'[8]',SOURCE)
 def test_complete_segment_must_be15(self):self.reject(rewrite(0x98,lambda p:p[:1]+b'\x10\0'+p[3:]if p[1:3]==b'\x0f\0'else p))
 def test_public_white_offset8(self):self.reject(rewrite(0x90,lambda p:p.replace(b'_animation_white_label_4d9e\x08\0',b'_animation_white_label_4d9e\x07\0')))
 def test_wrong_literal_byte(self):self.reject(rewrite(0xa0,lambda p:p.replace(b'Black:',b'black:')))
 def test_synthetic_hole_fill_is_rejected_negative_only(self):self.reject(rewrite(0xa0,lambda p:p+b'\0'if p[:3]==bytes.fromhex('020000')else p))
 def test_missing_terminator(self):self.reject(rewrite(0xa0,lambda p:p[:-1]+b'X'if b'Black:'in p else p))
 def test_other_loaded_allocation(self):self.reject(rewrite(0x98,lambda p:p[:1]+b'\x01\0'+p[3:]if p[1:3]==b'\0\0'else p))
 def test_unused_marker_is_preserved(self):self.assertEqual(read_omf(RAW).externals,{1:'__acrtused'})
 def test_marker_targeting_field_forbidden(self):self.reject(insert(0x9c,bytes.fromhex('c4005601')))
 def test_foreign_record(self):self.reject(insert(0xbc,b'\0'))
 def test_checksum(self):
  b=bytearray(RAW);b[-1]^=1;self.reject(bytes(b))
 def test_data16_unit_forbidden(self):
  u=copy.deepcopy(UNIT);u['size']=16
  with self.assertRaises(ValueError):h.validate_unit(u)
 def test_wrong_source_rejects_before_LINK(self):
  c=SimpleNamespace(source_sha256='0'*64,compiler='msc500',flags=h.FLAGS,source_name='UNIT.C',toolchain_manifest_sha256=h.MANIFEST_SHA,tool_hashes=TOOLS,object_bytes=RAW)
  with self.assertRaises(ValueError):h.validate_compiled(c,SOURCE,UNIT,project=M,output=M/'NO_OUTPUT',link_emitter=lambda*a:(_ for _ in()).throw(AssertionError('LINK forbidden')))
 def test_no_link_output_is_HELD_not_filled(self):
  with self.assertRaises(ValueError):h.validate_link_component(RAW,b'','', '', 'link_failed')
 def actual_component(self,**changes):
  v={'raw':RAW,'exe':(F/'LABELS.EXE').read_bytes(),'map_text':(F/'LABELS.MAP').read_text(),'log_text':(F/'LINK.LOG').read_text(),'link_status':(F/'RESULT.TXT').read_text().strip()};v.update(changes);return h.validate_link_component(**v)
 def test_actual_LINK_data15_excludes16_prefix(self):
  actual,p=self.actual_component();self.assertEqual(actual,b'Black:\0\0White:\0');self.assertEqual(len(actual),15);self.assertEqual(p['LINK_zero_prefix_credit'],0);self.assertEqual(p['source_literal_bytes'],14);self.assertEqual(p['LINK_initialized_alignment_bytes'],1)
 def test_changed_LINK_prefix_is_rejected(self):
  b=bytearray((F/'LABELS.EXE').read_bytes());b[512]=1
  with self.assertRaises(ValueError):self.actual_component(exe=bytes(b))
 def test_MAP_extra_loaded_segment_is_rejected(self):
  with self.assertRaises(ValueError):self.actual_component(map_text=(F/'LABELS.MAP').read_text()+'\n 00020H 00020H 00001H EXTRA DATA\n')
 def test_changed_public_is_rejected(self):
  with self.assertRaises(ValueError):self.actual_component(map_text=(F/'LABELS.MAP').read_text().replace('0001:0008','0001:0007'))
 def test_unexpected_undefined_is_rejected(self):
  with self.assertRaises(ValueError):self.actual_component(log_text=(F/'LINK.LOG').read_text().replace('__acrtused','_other'))
 def test_stream_stays_generic_complete309(self):
  b,p=extract_data(read_omf((F/'stream.obj').read_bytes()),'_animation_initial_stream_0f08');self.assertEqual(len(b),309);self.assertEqual(b.count(255),72);self.assertEqual(len(p['data_writes']),1)
if __name__=='__main__':unittest.main()
