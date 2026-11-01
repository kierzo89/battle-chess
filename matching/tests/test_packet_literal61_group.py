"""Pure finite-group controls. Real fixtures are calibration, never fresh SOURCE."""
from pathlib import Path
import sys,json,copy,tempfile,unittest,types
sys.dont_write_bytecode=True
M=Path(__file__).resolve().parents[1];sys.path[:0]=[str(M),str(M/'build_pipeline/engine_v1')]
import packet_literal61 as p
from reference import build_reference
from omf import read_omf
from library16 import link_segment,LibraryError
from msc import CompileResult
from cohort import validate_descriptor,select_source_phase
from fresh_lifecycle import FreshLifecycle
from source_phase import SourceObserver
F=Path(__file__).parent/'fixtures/packet_literal61';REALROOT=Path('/home/kierzo/chess')
class PacketGroup(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.raw=(F/'actual-natural-packet.obj').read_bytes();c.old=(F/'actual-old-packet.obj').read_bytes();c.pool=(F/'actual-retained-LINK-pool62.bin').read_bytes();c.ref=build_reference((REALROOT/'CHESS.EXE').read_bytes());c.units=json.loads((M/'config/units.json').read_text());c.d=json.loads((M/'build_pipeline/engine_v1/descriptor.json').read_text())
 def fresh_context(self):
  t=tempfile.TemporaryDirectory(prefix='packet-pure-only-');self.addCleanup(t.cleanup);out=Path(t.name)/'new';components=out/'components';components.mkdir(parents=True);observer=SourceObserver(M,copy.deepcopy(self.d));life=FreshLifecycle(copy.deepcopy(self.d),M,out,components,observer,lambda *a:None,lambda *a:(_ for _ in()).throw(AssertionError('NO LINK IN PURE TEST')));ctx=p.new_run_context(life,self.units);life.packet_context=ctx;life.phase='PARTITIONED_PENDING_CRT88';return ctx
 def test_real_raw_and_exact_hole(self):
  o=p.validate_raw(self.raw);self.assertEqual([(a,len(b))for a,b in o.segments[3].chunks],[(0,37),(38,24)]);self.assertEqual(len(o.fixups),57)
 def test_old_raw_not_new_profile(self):
  with self.assertRaises(p.PacketError):p.validate_raw(self.old)
 def test_raw_corruption_rejected(self):
  b=bytearray(self.raw);b[20]^=1
  with self.assertRaises(p.PacketError):p.validate_raw(bytes(b))
 def test_parsed_object_is_not_byte_factory(self):
  with self.assertRaises(p.PacketError):p.validate_raw(read_omf(self.raw))
 def test_generic_raw_hole_rejection_unchanged(self):
  with self.assertRaisesRegex(LibraryError,'hole'):link_segment(read_omf(self.raw),3,{3:(0x5cc2,0x51b4)},{1:0x5cc2},{})
 def test_real_retained_payload_validation_not_capability(self):
  q=p.validate_materialized_payload(self.raw,self.pool);self.assertFalse(q['fresh_capability']);self.assertEqual(q['credit'],0)
 def test_missing_alignment_byte_rejected(self):
  with self.assertRaises(p.PacketError):p.validate_materialized_payload(self.raw,self.pool[:37]+self.pool[38:])
 def test_truncated_materialized_allocation_rejected(self):
  with self.assertRaises(p.PacketError):p.validate_materialized_payload(self.raw,self.pool[:-1])
 def test_nonzero_alignment_rejected(self):
  b=bytearray(self.pool);b[37]=1
  with self.assertRaises(p.PacketError):p.validate_materialized_payload(self.raw,bytes(b))
 def test_wrong_literal_payload_rejected(self):
  b=bytearray(self.pool);b[38]^=1
  with self.assertRaises(p.PacketError):p.validate_materialized_payload(self.raw,bytes(b))
 def test_extra_allocation_byte_rejected(self):
  with self.assertRaises(p.PacketError):p.validate_materialized_payload(self.raw,self.pool+b'\0')
 def test_native_core_all856_and15receiver_primaries(self):
  q=p.native_core(self.raw,self.ref,M);self.assertEqual(len(q['code']),856);self.assertEqual([len(b)for b in q['arrays']],[37,24]);self.assertEqual(len(q['receiver_native_extent']['evidence_ids']),15);self.assertFalse(q['allocation_complete'])
 def test_wrong_native_code_context_rejected(self):
  r=dict(self.ref);b=bytearray(r['image']);b[0xdce2]^=1;r['image']=bytes(b)
  with self.assertRaises(p.PacketError):p.native_core(self.raw,r,M)
 def test_wrong_native_literal_context_rejected(self):
  r=dict(self.ref);b=bytearray(r['image']);b[0x61dd4]^=1;r['image']=bytes(b)
  with self.assertRaises(p.PacketError):p.native_core(self.raw,r,M)
 def test_eight_exact_contracts(self):
  self.assertEqual(len(p.contracts()),8)
  for u in p.contracts().values():p.validate_unit(u)
 def test_literal_array_view_offset_mutation_rejected(self):
  u=copy.deepcopy(p.contracts()['packet_error_51b4']);u['literal_array_view']['offset']=37
  with self.assertRaises(p.PacketError):p.validate_unit(u)
 def test_literal_type_bound_mutation_rejected(self):
  u=copy.deepcopy(p.contracts()['packet_error_51b4']);u['literal_array_view']['array_bits']=304
  with self.assertRaises(p.PacketError):p.validate_unit(u)
 def test_fake_PUBLIC_alias_contract_rejected(self):
  u=copy.deepcopy(p.contracts()['packet_error_51b4']);u['literal_array_view']['anonymous_no_PUBLIC_alias']=False
  with self.assertRaises(p.PacketError):p.validate_unit(u)
 def test_foreign_source_contract_rejected(self):
  u=copy.deepcopy(p.contracts()['send_packet_dce2']);u['source']='src/packet_context_match.c'
  with self.assertRaises(p.PacketError):p.validate_unit(u)
 def test_valid_descriptor_exact_group(self):
  validate_descriptor(copy.deepcopy(self.d));self.assertEqual(len(p.registration(self.d)['owners']),8)
 def test_missing_group_registration_rejected(self):
  d=copy.deepcopy(self.d);d['source_allocation_jobs']=[]
  with self.assertRaises(p.PacketError):validate_descriptor(d)
 def test_wrong_group_rejected(self):
  d=copy.deepcopy(self.d);d['source_allocation_jobs'][0]['policy']='any-hole'
  with self.assertRaises(p.PacketError):p.registration(d)
 def test_wrong_group_owner_rejected(self):
  d=copy.deepcopy(self.d);d['source_allocation_jobs'][0]['owners']=d['source_allocation_jobs'][0]['owners'][:-1]
  with self.assertRaises(p.PacketError):p.registration(d)
 def test_wrong_group_source_RAW_rejected(self):
  d=copy.deepcopy(self.d);d['source_allocation_jobs'][0]['raw_sha256']='0'*64
  with self.assertRaises(p.PacketError):p.registration(d)
 def test_fake_lifecycle_context_rejected(self):
  with self.assertRaises(p.PacketError):p.new_run_context(types.SimpleNamespace(phase='NEW',descriptor=self.d),self.units)
 def test_public_context_constructor_denied(self):
  with self.assertRaises(p.PacketError):p.RunContext(object(),None,M,M/'build')
 def test_pending_token_wrong_capability_rejected_before_selection(self):
  ctx=self.fresh_context()
  with self.assertRaises(p.PacketError):p.split_source_results([p.PendingOwner(object(),None,'{}')],ctx)
 def test_source_ready_dict_is_not_pending_token(self):
  ctx=self.fresh_context()
  with self.assertRaises(p.PacketError):p.split_source_results([{'id':n,'status':'source_ready_pending_packet_alignment'}for n in p.contracts()],ctx)
 def test_standalone_route_does_not_compile(self):
  calls=[]
  with self.assertRaises(p.PacketError):p.stage_owner(p.contracts()['send_packet_dce2'],M,{},M/'build',self.ref,lambda *a,**k:calls.append(True),None)
  self.assertEqual(calls,[])
 def test_one_failed_callback_poison_no_eight_retry(self):
  ctx=self.fresh_context();calls=[]
  def fail(*a,**k):calls.append(1);raise OSError('inert pure callback, no process')
  cache={}
  for u in p.contracts().values():
   with self.assertRaises((p.PacketError,OSError)):p.stage_owner(u,M,cache,ctx.output,self.ref,fail,ctx)
  self.assertEqual(len(calls),1);self.assertEqual(ctx.state,'POISONED_NO_RETRY')
 def test_actual_calibration_Fa_is_not_standard_compile_witness(self):
  ctx=self.fresh_context();g=json.loads((F/'calibration-generation.json').read_text());calls=[]
  result=CompileResult(self.raw,'CALIBRATION ONLY',(),g['source_sha256'],g['toolchain_manifest_sha256'],g['tool_hashes'],tuple(g['flags']),'msc500','UNIT.C')
  def replay(*a,**k):calls.append(1);return result
  cache={}
  for u in p.contracts().values():
   with self.assertRaises(p.PacketError):p.stage_owner(u,M,cache,ctx.output,self.ref,replay,ctx)
  self.assertEqual(len(calls),1);self.assertEqual(ctx.state,'VALIDATING_ONE_SOURCE');self.assertIsNone(ctx.group)
 def test_injected_cache_refused_without_callback(self):
  ctx=self.fresh_context();calls=[];key=('packet61-private',id(ctx),p.profile()['source_SHA256'],tuple(p.FLAGS),'UNIT.C')
  with self.assertRaises(p.PacketError):p.stage_owner(p.contracts()['send_packet_dce2'],M,{key:object()},ctx.output,self.ref,lambda *a,**k:calls.append(1),ctx)
  self.assertEqual(calls,[])
 def test_fake_group_cache_type_rejected(self):
  ctx=self.fresh_context();ctx.group=types.SimpleNamespace(valid=lambda:True)
  with self.assertRaises(p.PacketError):ctx.valid()
 def test_retained_aggregate_JSON_not_fresh_capability(self):
  with self.assertRaises(p.PacketError):p._materialized_allocation(None,{'run_id':'retained','SOURCE_digest':'0'*64,'LINK':'success'})
 def test_ducktyped_aggregate_not_fresh_capability(self):
  with self.assertRaises(p.PacketError):p._materialized_allocation(None,types.SimpleNamespace(valid=lambda:True))
 def test_complete_requires_private_context(self):
  with self.assertRaises(p.PacketError):p.complete(types.SimpleNamespace(state='SOURCE_BOUND'),[],{},self.ref)
 def test_old_receiver_gate_positive_on_old_object(self):
  import packet_receive_extent as old
  u=next(u for u in p.profile()['old8_unit_contracts']if u['id']=='receive_packet_ddd3');o=read_omf(self.old);info=o.function_info(u['symbol']);q=old.validate_packet_receive_extent(u,M,self.ref['original_sha256'],info,self.ref['image'][0xddd3:0xdf71],o);self.assertEqual(q['whole_CODE_SEGDEF'],856)
 def test_old_receiver_gate_still_rejects_new_extra_allocation(self):
  import packet_receive_extent as old
  u=next(u for u in p.profile()['old8_unit_contracts']if u['id']=='receive_packet_ddd3');o=read_omf(self.raw)
  with self.assertRaisesRegex(ValueError,'complete WORD'):old.validate_packet_receive_extent(u,M,self.ref['original_sha256'],o.function_info(u['symbol']),self.ref['image'][0xddd3:0xdf71],o)
 def test_all_other514_unit_contracts_retained(self):
  base=json.loads((F/'baseline522-units.json').read_text());now={u['id']:u for u in self.units};self.assertEqual(len(base),522)
  for u in base:
   if u['id']not in p.contracts():self.assertEqual(u,now[u['id']])
 def test_no_uncredited_alignment_into_literal_rows(self):
  views=[u for u in p.contracts().values()if u['language']=='c-data'];self.assertEqual(sum(u['size']for u in views),61);self.assertTrue(all(u['literal_array_view']['anonymous_no_PUBLIC_alias']for u in views))
if __name__=='__main__':unittest.main()
