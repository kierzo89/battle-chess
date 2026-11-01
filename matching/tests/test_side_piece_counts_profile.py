"""Prepared focused profile controls; no compiler call or aggregate execution."""
from pathlib import Path
from unittest.mock import patch
import copy,json,os,sys,tempfile,unittest
M=Path(os.environ.get('BC_COUNTS_PROFILE_PROJECT',Path(__file__).resolve().parents[1])).resolve();sys.path[:0]=[str(M)];sys.dont_write_bytecode=True
import side_piece_counts_source_inputs as h
F=Path(__file__).resolve().parent/'fixtures/side_piece_counts';RAW=(F/'provider.obj').read_bytes();ITEM=json.loads((F/'item.json').read_text())
def rewrite(kind,fn):
 at=0;out=[];done=False
 while at<len(RAW):
  k=RAW[at];n=int.from_bytes(RAW[at+1:at+3],'little');p=RAW[at+3:at+2+n]
  if k==kind and not done:
   x=fn(p)
   if x!=p:p=x;done=True
  b=bytes([k])+(len(p)+1).to_bytes(2,'little')+p;out.append(b+bytes([-sum(b)&255]));at+=3+n
 assert done;return b''.join(out)
class ConditionalSideCountsTests(unittest.TestCase):
 def reject(self,b):
  with self.assertRaises(ValueError):h.validate_object(b)
 def test_actual_whole_int2_common4(self):self.assertEqual(h.validate_object(RAW),[{'symbol':'_side_piece_counts','type_index':515,'datatype':98,'size':4}])
 def test_wrong_common_extent(self):self.reject(rewrite(0xb0,lambda p:p[:-1]+b'\x08'))
 def test_far_common_forbidden(self):self.reject(rewrite(0xb0,lambda p:p.replace(bytes.fromhex('6204'),bytes.fromhex('6104'),1)))
 def test_wrong_array_count(self):self.reject(rewrite(0xa0,lambda p:p.replace(bytes.fromhex('7820838100'),bytes.fromhex('7830838100'))))
 def test_incomplete_provider_array_forbidden(self):self.reject(rewrite(0xa0,lambda p:p.replace(bytes.fromhex('7820838100'),bytes.fromhex('7800838100'))))
 def test_wrong_signed_array_element(self):self.reject(rewrite(0xa0,lambda p:p.replace(bytes.fromhex('7820838100'),bytes.fromhex('7820838500'))))
 def test_wrong_global_type(self):self.reject(rewrite(0xa0,lambda p:p.replace(bytes.fromhex('0302'),bytes.fromhex('0202'),1)if p[0]==5 else p))
 def test_wrong_debug_target(self):self.reject(rewrite(0x9c,lambda p:p.replace(bytes.fromhex('cc025602'),bytes.fromhex('cc025601'))))
 def test_wrong_name(self):self.reject(rewrite(0xb0,lambda p:p.replace(b'side_piece_counts',b'side_piece_countz')))
 def test_checksum(self):
  b=bytearray(RAW);b[-1]^=1;self.reject(bytes(b))
 def test_wrong_memory_model(self):
  item=copy.deepcopy(ITEM);item['flags']=['/AM','/Zl','/Zi']
  with self.assertRaisesRegex(ValueError,'source/compiler'):h.validate_item(item)
 def test_evidence_selection_cannot_remove_conditional_model(self):
  p=copy.deepcopy(h.PINS);p.pop('model')
  with self.assertRaisesRegex(ValueError,'evidence selection'):h.validate_evidence(M,p,M/'NO_TARGET')
 def test_wrong_source_rejects_before_compiler(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);s=p/h.SOURCE;s.parent.mkdir(parents=True);s.write_text('int side_piece_counts[4];\n')
   with patch.object(h,'compile_c',side_effect=AssertionError('compiler forbidden')):
    with self.assertRaisesRegex(ValueError,'source hash'):h.build_input(ITEM,p,p/'NO_TARGET',p/'out')
if __name__=='__main__':unittest.main()
