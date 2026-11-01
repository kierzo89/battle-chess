"""Prepared permanent controls. No compiler runs in these tests."""
from pathlib import Path
from unittest.mock import patch
import copy,json,os,sys,tempfile,unittest
M=Path(os.environ.get('BC_SCREEN_POINTER_PROJECT',Path(__file__).resolve().parents[1])).resolve();sys.path.insert(0,str(M));sys.dont_write_bytecode=True
import screen_coordinate_pointers_source_inputs as h
import source_inputs
F=Path(__file__).resolve().parent/'fixtures/screen_coordinate_pointers';RAW=(F/'common.obj').read_bytes();ITEM=json.loads((F/'item.json').read_text())
def rewrite(kind,change):
 out=bytearray();at=0;done=False
 while at<len(RAW):
  k=RAW[at];n=int.from_bytes(RAW[at+1:at+3],'little');p=RAW[at+3:at+2+n]
  if not done and k==kind:
   changed=change(p)
   if changed!=p:p=changed;done=True
  b=bytes([k])+(len(p)+1).to_bytes(2,'little')+p;out.extend(b+bytes([-sum(b)&255]));at+=3+n
 assert done;return bytes(out)
class ScreenCoordinatePointerTests(unittest.TestCase):
 def reject(self,b):
  with self.assertRaises(ValueError):h.validate_object(b)
 def test_actual_whole_object_A1_two_cells(self):
  ds=h.validate_object(RAW);self.assertEqual([(x['symbol'],x['size'],x['type_index'])for x in ds],[('_screen_x',2,161),('_screen_y',2,161)])
 def test_checksum(self):
  b=bytearray(RAW);b[-1]^=1;self.reject(bytes(b))
 def test_trailing_module(self):self.reject(RAW+b'\0')
 def test_unsupported_record(self):
  at=h.read_omf(RAW).records[-1][1];self.reject(RAW[:at]+bytes.fromhex('8e010071')+RAW[at:])
 def test_cell_extent(self):self.reject(rewrite(0xb0,lambda p:p.replace(bytes.fromhex('6202'),bytes.fromhex('6204'),1)))
 def test_far_storage(self):self.reject(rewrite(0xb0,lambda p:p.replace(bytes.fromhex('6202'),bytes.fromhex('6102'),1)))
 def test_far_pointer_builtin(self):self.reject(rewrite(0xb0,lambda p:p.replace(bytes.fromhex('80a1'),bytes.fromhex('80c1'),1)))
 def test_definition_name(self):self.reject(rewrite(0xb0,lambda p:p.replace(b'screen_x',b'screen_z',1)))
 def test_debug_global_type(self):self.reject(rewrite(0xa0,lambda p:p.replace(bytes.fromhex('a100'),bytes.fromhex('c100'),1)))
 def test_debug_fixup_target(self):self.reject(rewrite(0x9c,lambda p:p.replace(bytes.fromhex('cc135603'),bytes.fromhex('cc135602'),1)))
 def test_unknown_comment(self):self.reject(rewrite(0x88,lambda p:p[:-1]+bytes([p[-1]^1])))
 def test_loaded_segment(self):self.reject(rewrite(0x98,lambda p:p[:1]+b'\x02\x00'+p[3:]))
 def test_wrong_memory_model(self):
  item=copy.deepcopy(ITEM);item['flags']=['/AM','/Zl','/Zi']
  with self.assertRaisesRegex(ValueError,'source/compiler'):h.validate_item(item)
 def test_wrong_registry_extent(self):
  item=copy.deepcopy(ITEM);item['objects'][0]['size']=4
  with self.assertRaisesRegex(ValueError,'logical extents'):h.validate_item(item)
 def test_wrong_evidence_selection(self):
  p=copy.deepcopy(h.PINS);p['identity']['sha256']='0'*64
  with self.assertRaisesRegex(ValueError,'evidence selection'):h.validate_evidence(M,p,M/'NO_TARGET')
 def test_wrong_source_before_compiler(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);s=p/h.SOURCE;s.parent.mkdir(parents=True);s.write_text('int screen_x;\nint screen_y;\n')
   with patch.object(h,'compile_c',side_effect=AssertionError('compiler forbidden')):
    with self.assertRaisesRegex(ValueError,'source hash'):h.build_input(ITEM,p,p/'NO_TARGET',p/'out')
 def test_path_escape(self):
  with self.assertRaisesRegex(ValueError,'path escape'):h.local(M,'../forbidden')
 def test_existing_definition_rejects_before_generation(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);(p/'config').mkdir();(p/'config/source-inputs.json').write_text(json.dumps({'schema_version':1,'source_allocations':[ITEM]}))
   for n in h.NAMES:
    with self.subTest(symbol=n),patch.object(source_inputs,'compile_c',side_effect=AssertionError('compiler forbidden')):
     with self.assertRaisesRegex(ValueError,'already matched definition'):source_inputs.build_source_inputs(p,p/'NO_TARGET',p/'out',defined_symbols=[n])
 def test_unrecognized_backend(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);(p/'config').mkdir();item=copy.deepcopy(ITEM);item['backend']+='-unreviewed';(p/'config/source-inputs.json').write_text(json.dumps({'schema_version':1,'source_allocations':[item]}))
   with patch.object(source_inputs,'compile_c',side_effect=AssertionError('compiler forbidden')):
    with self.assertRaisesRegex(ValueError,'unreviewed source allocation'):source_inputs.build_source_inputs(p,p/'NO_TARGET',p/'out')
if __name__=='__main__':unittest.main()
