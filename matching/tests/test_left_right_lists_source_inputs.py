"""Prepared permanent controls; no compiler, assembler or LINK is run by this suite."""
from pathlib import Path
from unittest.mock import patch
import copy,json,os,sys,tempfile,unittest
M=Path(os.environ.get('BC_LIST_GRIDS_PROJECT',Path(__file__).resolve().parents[1])).resolve();sys.path.insert(0,str(M));sys.dont_write_bytecode=True
import left_right_lists_source_inputs as h
import source_inputs
FIXTURE=Path(__file__).resolve().parent/'fixtures/left_right_lists'
RAW=(FIXTURE/'common.obj').read_bytes();ITEM=json.loads((FIXTURE/'item.json').read_text())
def rewrite(kind,change,segment=None):
 out=bytearray();at=0;done=False
 while at<len(RAW):
  k=RAW[at];n=int.from_bytes(RAW[at+1:at+3],'little');p=RAW[at+3:at+2+n]
  if not done and k==kind and(segment is None or p[0]==segment):
   q=change(p)
   if q!=p:p=q;done=True
  b=bytes([k])+(len(p)+1).to_bytes(2,'little')+p;out.extend(b+bytes([-sum(b)&255]));at+=n+3
 assert done;return bytes(out)
def type_change(old,new):
 def change(p):
  a,b=bytes.fromhex(old),bytes.fromhex(new);assert p.count(a)==1;return p.replace(a,b,1)
 return rewrite(0xa0,change,6)
def registry(p,rows):
 (p/'config').mkdir(exist_ok=True);(p/'config/source-inputs.json').write_text(json.dumps({'schema_version':1,'source_allocations':rows}))
class LeftRightListsTests(unittest.TestCase):
 def reject(self,b):
  with self.assertRaises(ValueError):h.validate_object(b)
 def test_actual_complete_common144(self):
  r=h.validate_object(RAW);self.assertEqual([(x['symbol'],x['size'],x['communal_kind'])for x in r],[(n,72,0x62)for n in h.NAMES])
 def test_actual_complete_two_dimension_pointer_graphs(self):
  o=h.read_omf(RAW);ts=h.types(o);gs=h.globals(o);self.assertEqual({n:h.graph(ts,v['type'])for n,v in gs.items()},dict.fromkeys(h.NAMES,['array',576,['array',96,['builtin',160]]]))
 def test_only_two_debug_far_no_runtime_fixups(self):
  o=h.read_omf(RAW);self.assertEqual(len(o.fixups),2);self.assertTrue(all(f.segment==5 and f.width==4 for f in o.fixups));self.assertFalse(o.publics or o.procedures)
 def test_bad_checksum(self):
  b=bytearray(RAW);b[-1]^=1;self.reject(bytes(b))
 def test_truncated_record(self):self.reject(RAW[:-2])
 def test_trailing_module(self):self.reject(RAW+b'\0')
 def test_unknown_raw_record(self):
  at=h.read_omf(RAW).records[-1][1];self.reject(RAW[:at]+bytes.fromhex('8e010071')+RAW[at:])
 def test_wrong_common_extent(self):self.reject(rewrite(0xb0,lambda p:p.replace(b'\x62\x48',b'\x62\x46',1)))
 def test_far_common_forbidden(self):self.reject(rewrite(0xb0,lambda p:p.replace(b'\x62\x48',b'\x61\x48',1)))
 def test_renamed_definition(self):self.reject(rewrite(0xb0,lambda p:p.replace(b'left_lists',b'left_listx',1)))
 def test_wrong_outer_array_dimension(self):self.reject(type_change('78854002830502','7885e001830502'))
 def test_wrong_inner_array_dimension(self):self.reject(type_change('786083a000','785083a000'))
 def test_changed_pointer_builtin(self):self.reject(type_change('786083a000','786083c000'))
 def test_recursive_array_type(self):self.reject(type_change('78854002830502','78854002830402'))
 def test_wrong_debug_global_target(self):self.reject(rewrite(0x9c,lambda p:p.replace(bytes.fromhex('cc155603'),bytes.fromhex('cc155602'),1)))
 def test_unknown_comment(self):self.reject(rewrite(0x88,lambda p:p[:-1]+bytes([p[-1]^1])))
 def test_extra_loaded_storage(self):self.reject(rewrite(0x98,lambda p:p[:1]+b'\x01\x00'+p[3:]))
 def test_wrong_memory_model(self):
  item=copy.deepcopy(ITEM);item['flags']=['/AM','/Zl','/Zi']
  with self.assertRaisesRegex(ValueError,'source/compiler'):h.validate_item(item)
 def test_wrong_registry_extent(self):
  item=copy.deepcopy(ITEM);item['objects'][0]['size']=70
  with self.assertRaisesRegex(ValueError,'logical extents'):h.validate_item(item)
 def test_evidence_selection_closed(self):
  pins=copy.deepcopy(h.PINS);pins['ownership']['sha256']='0'*64
  with self.assertRaisesRegex(ValueError,'evidence selection'):h.validate_evidence(M,pins,M.parent/'CHESS.EXE')
 def test_bad_evidence_before_target_or_compiler(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);row=h.PINS['ownership'];q=p/row['path'];q.parent.mkdir(parents=True);q.write_text('{}\n')
   with patch.object(h,'compile_c',side_effect=AssertionError('compiler forbidden')):
    with self.assertRaisesRegex(ValueError,'evidence pin'):h.validate_evidence(p,h.PINS,p/'CHESS.EXE')
 def test_wrong_source_before_compiler(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);s=p/h.SOURCE;s.parent.mkdir(parents=True);s.write_text('int left_lists[35];\n')
   with patch.object(h,'compile_c',side_effect=AssertionError('compiler forbidden')):
    with self.assertRaisesRegex(ValueError,'source hash'):h.build_input(ITEM,p,p/'CHESS.EXE',p/'out')
 def test_source_symlink_forbidden_before_compiler(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);s=p/h.SOURCE;s.parent.mkdir(parents=True);real=s.parent/'copy.c';real.write_bytes((M/h.SOURCE).read_bytes());s.symlink_to(real)
   with patch.object(h,'compile_c',side_effect=AssertionError('compiler forbidden')):
    with self.assertRaisesRegex(ValueError,'regular source'):h.build_input(ITEM,p,p/'CHESS.EXE',p/'out')
 def test_each_already_defined_name_rejects_before_generation(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);registry(p,[ITEM])
   for n in h.NAMES:
    with self.subTest(name=n),patch.object(h,'build_input',side_effect=AssertionError('generation forbidden')):
     with self.assertRaisesRegex(ValueError,'already matched definition'):source_inputs.build_source_inputs(p,p/'CHESS.EXE',p/'out',defined_symbols=[n])
 def test_duplicate_id_rejected_before_second_dispatch(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);second=copy.deepcopy(ITEM);second['source']='src/link/other.c';registry(p,[ITEM,second])
   with patch.object(h,'build_input',return_value={'id':'dispatch-only-test'})as call:
    with self.assertRaisesRegex(ValueError,'duplicate source allocation'):source_inputs.build_source_inputs(p,p/'CHESS.EXE',p/'out')
   self.assertEqual(call.call_count,1)
 def test_duplicate_source_rejected_before_second_dispatch(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);second=copy.deepcopy(ITEM);second['id']='other';registry(p,[ITEM,second])
   with patch.object(h,'build_input',return_value={'id':'dispatch-only-test'})as call:
    with self.assertRaisesRegex(ValueError,'duplicate source allocation'):source_inputs.build_source_inputs(p,p/'CHESS.EXE',p/'out')
   self.assertEqual(call.call_count,1)
 def test_duplicate_symbols_rejected_before_second_dispatch(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);second=copy.deepcopy(ITEM);second['id']='other';second['source']='src/link/other.c';registry(p,[ITEM,second])
   with patch.object(h,'build_input',return_value={'id':'dispatch-only-test'})as call:
    with self.assertRaisesRegex(ValueError,'duplicate allocation symbol'):source_inputs.build_source_inputs(p,p/'CHESS.EXE',p/'out')
   self.assertEqual(call.call_count,1)
 def test_exact_backend_routes_once_without_real_compiler(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);registry(p,[ITEM])
   with patch.object(h,'build_input',return_value={'id':'dispatch-only-test'})as call,patch.object(source_inputs,'compile_c',side_effect=AssertionError('compiler forbidden')):
    passed=source_inputs.compile_c;r=source_inputs.build_source_inputs(p,p/'CHESS.EXE',p/'out')
   self.assertEqual(call.call_count,1);self.assertEqual(len(r['objects']),1);self.assertIs(call.call_args.kwargs['compiler_fn'],passed)
 def test_unknown_backend_not_routed(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);item=copy.deepcopy(ITEM);item['backend']=h.BACKEND+'-unknown';registry(p,[item])
   with patch.object(h,'build_input',side_effect=AssertionError('generation forbidden')):
    with self.assertRaisesRegex(ValueError,'unreviewed source allocation'):source_inputs.build_source_inputs(p,p/'CHESS.EXE',p/'out')
 def test_not_implicitly_enabled(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);registry(p,[])
   with patch.object(h,'build_input',side_effect=AssertionError('generation forbidden')):self.assertEqual(source_inputs.build_source_inputs(p,p/'CHESS.EXE',p/'out')['objects'],[])
 def test_generation_scope_source_and_fresh_output_only(self):
  # Capability control only: bytes here are not a fake compiler/provenance result.
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);s=p/h.SOURCE;s.parent.mkdir(parents=True);s.write_bytes(b'source-capability-control')
   with h.source_generation_scope(p,s,p/'CHESS.EXE')as(reads,denied,roots):
    self.assertEqual(s.read_bytes(),b'source-capability-control')
    with tempfile.TemporaryDirectory(prefix='battlechess-msc-')as scratch:
     q=Path(scratch)/'UNIT.OBJ';q.write_bytes(b'capability-only');self.assertEqual(q.read_bytes(),b'capability-only')
   self.assertEqual(len(denied),5);self.assertEqual(len(roots),1);self.assertTrue(any('provider.obj'in n for n in denied));self.assertTrue(any('proof'in n for n in denied))
 def test_generation_scope_rejects_unlisted_tool_file(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t);s=p/h.SOURCE;s.parent.mkdir(parents=True);s.write_bytes(b'source')
   with self.assertRaisesRegex(ValueError,'forbidden generation read'):
    with h.source_generation_scope(p,s,p/'CHESS.EXE'):(p/'toolchains/msc500/OLD.OBJ').read_bytes()
 def test_retained_native_type_layout_evidence(self):
  constraints=h.validate_evidence(M,h.PINS,M.parent/'CHESS.EXE');self.assertEqual([(r['symbol'],r['size'],r['dgroup_offset'])for r in constraints],[(n,72,hex(a))for n,a in zip(h.NAMES,h.OFFSETS)])
 def test_path_escape_rejected(self):
  with self.assertRaisesRegex(ValueError,'path escape'):h.local(M,'../forbidden')
if __name__=='__main__':unittest.main()
