"""Permanent component-test proposal; no compiler or LINK is executed."""
from pathlib import Path
from unittest.mock import patch
import copy,json,os,sys,tempfile,unittest
M=Path(os.environ.get('BC_ASSET_FOUR_PROJECT',Path(__file__).resolve().parents[1])).resolve();sys.path.insert(0,str(M));sys.dont_write_bytecode=True
import asset_fixed_arrays_source_inputs as h
import source_inputs
FIXTURE=Path(__file__).resolve().parent/'fixtures/asset_fixed_arrays'
RAW=(FIXTURE/'common.obj').read_bytes();ITEM=json.loads((FIXTURE/'item.json').read_text())
def rewrite(kind,change,segment=None):
 out=bytearray();at=0;done=False
 while at<len(RAW):
  k=RAW[at];n=int.from_bytes(RAW[at+1:at+3],'little');p=RAW[at+3:at+2+n]
  if not done and k==kind and (segment is None or p[0]==segment):
   changed=change(p)
   if changed!=p:p=changed;done=True
  b=bytes([k])+(len(p)+1).to_bytes(2,'little')+p;out.extend(b+bytes([-sum(b)&255]));at+=3+n
 assert done;return bytes(out)
def type_change(old,new):
 def change(p):
  a=bytes.fromhex(old);b=bytes.fromhex(new);assert p.count(a)==1;return p.replace(a,b,1)
 return rewrite(0xa0,change,6)
class AssetFixedArraysTests(unittest.TestCase):
 def reject(self,raw):
  with self.assertRaises(ValueError):h.validate_object(raw)
 def test_real_whole_object(self):
  r=h.validate_object(RAW);self.assertEqual(sum(x['size']for x in r),64);self.assertEqual([x['symbol']for x in r],h.NAMES)
 def test_bad_checksum(self):
  b=bytearray(RAW);b[-1]^=1;self.reject(bytes(b))
 def test_unknown_record(self):
  at=h.read_omf(RAW).records[-1][1];self.reject(RAW[:at]+bytes.fromhex('8e010071')+RAW[at:])
 def test_trailing_module(self):self.reject(RAW+b'\0')
 def test_wrong_near_common_extent(self):self.reject(rewrite(0xb0,lambda p:p.replace(bytes.fromhex('6210'),bytes.fromhex('620c'),1)))
 def test_far_common_forbidden(self):self.reject(rewrite(0xb0,lambda p:p.replace(bytes.fromhex('6210'),bytes.fromhex('6110'),1)))
 def test_renamed_definition(self):self.reject(rewrite(0xb0,lambda p:p.replace(b'metadata_records',b'metadata_recordx',1)))
 def test_metadata_array_count(self):self.reject(type_change('7885800083e000','7885600083e000'))
 def test_metadata_pointer_view(self):self.reject(type_change('7885800083e000','7885800083c000'))
 def test_frame_array_count(self):self.reject(type_change('78850001830402','7885c000830402'))
 def test_frame_member_count(self):self.reject(type_change('794005830502830602820069','794004830502830602820069'))
 def test_frame_member_pointer(self):self.reject(type_change('7f83840083840083800083800083e400','7f83840083840083800083800083c400'))
 def test_frame_member_signedness(self):self.reject(type_change('7f83840083840083800083800083e400','7f83840083840083840083800083e400'))
 def test_frame_member_offset(self):self.reject(type_change('8206706978656c738804','8206706978656c738805'))
 def test_values_signed_type(self):self.reject(type_change('7840838100','7840838500'))
 def test_task_pointer_distance(self):self.reject(type_change('7a74830802820d416e696d6174696f6e5461736b','7a75830802820d416e696d6174696f6e5461736b'))
 def test_recursive_type_rejected(self):self.reject(type_change('7885800083e000','78858000830a02'))
 def test_wrong_debug_far_target(self):self.reject(rewrite(0x9c,lambda p:p.replace(bytes.fromhex('cc445605'),bytes.fromhex('cc445604'),1)))
 def test_unknown_comment(self):self.reject(rewrite(0x88,lambda p:p[:-1]+bytes([p[-1]^1])))
 def test_nonempty_loaded_segment(self):self.reject(rewrite(0x98,lambda p:p[:1]+b'\x01\x00'+p[3:]))
 def test_wrong_memory_model(self):
  item=copy.deepcopy(ITEM);item['flags']=['/AM','/Zl','/Zi']
  with self.assertRaisesRegex(ValueError,'source/compiler'):h.validate_item(item)
 def test_wrong_registry_extent(self):
  item=copy.deepcopy(ITEM);item['objects'][0]['size']=12
  with self.assertRaisesRegex(ValueError,'logical extents'):h.validate_item(item)
 def test_wrong_source_before_compiler(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);s=p/h.SOURCE;s.parent.mkdir(parents=True);s.write_text('int values[3];\n')
   with patch.object(h,'compile_c',side_effect=AssertionError('compiler forbidden')):
    with self.assertRaisesRegex(ValueError,'source hash'):h.build_input(ITEM,p,p/'CHESS.EXE',p/'out')
 def test_bad_evidence_before_target(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);pin=next(iter(h.PINS.values()));q=p/pin['path'];q.parent.mkdir(parents=True);q.write_text('{}\n')
   with self.assertRaisesRegex(ValueError,'evidence pin'):h.validate_evidence(p,h.PINS,p/'CHESS.EXE')
 def test_evidence_selection_closed(self):
  p=copy.deepcopy(h.PINS);p['ownership']['sha256']='0'*64
  with self.assertRaisesRegex(ValueError,'evidence selection'):h.validate_evidence(M,p,M.parent/'CHESS.EXE')
 def test_all_four_existing_definitions_reject_before_generation(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);(p/'config').mkdir();(p/'config/source-inputs.json').write_text(json.dumps({'schema_version':1,'source_allocations':[ITEM]}))
   for name in h.NAMES:
    with self.subTest(name=name),patch.object(source_inputs,'compile_c',side_effect=AssertionError('compiler forbidden')):
     with self.assertRaisesRegex(ValueError,'already matched definition'):source_inputs.build_source_inputs(p,p/'CHESS.EXE',p/'out',defined_symbols=[name])
 def test_unrecognized_backend_does_not_route(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);(p/'config').mkdir();item=copy.deepcopy(ITEM);item['backend']='msc500-near-common-asset-fixed-arrays-v2';(p/'config/source-inputs.json').write_text(json.dumps({'schema_version':1,'source_allocations':[item]}))
   with patch.object(source_inputs,'compile_c',side_effect=AssertionError('compiler forbidden')):
    with self.assertRaisesRegex(ValueError,'unreviewed source allocation'):source_inputs.build_source_inputs(p,p/'CHESS.EXE',p/'out')
 def test_path_escape(self):
  with self.assertRaisesRegex(ValueError,'path escape'):h.local(M,'../forbidden')
if __name__=='__main__':unittest.main()
