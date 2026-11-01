"""Staged fixed packet714/856 extent tests; no canonical mutations."""
import copy,dataclasses,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
PROJECT=Path(__file__).resolve().parents[1];STAGE=PROJECT/'build/packet-receiver-extent-stage'
sys.path.insert(0,str(PROJECT))
import packet_receive_extent as policy
assert Path(policy.__file__).resolve()==PROJECT/'packet_receive_extent.py'
from packet_receive_extent import validate_packet_receive_extent,TARGET_SHA256
from omf import read_omf
from msc import compile_c
class PacketReceiveTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.template=json.loads((STAGE/'proposed-856-units.json').read_text())[1];cls.good=bytes.fromhex(json.loads((PROJECT/'build/packet-context-856-root/proof.json').read_text())['whole_original_native'])[241:655];cls.obj=read_omf((PROJECT/'build/packet-context-856-root/packet_context856.obj').read_bytes())
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.project=Path(self.tmp.name);self.unit=copy.deepcopy(self.template);self.object=copy.deepcopy(self.obj);self.info=self.object.function_info(self.unit['symbol']);self.linked=self.good
  paths=[self.unit['rea_evidence']]
  for k,v in self.unit['extended_extent'].items():
   if k.endswith('_evidence'):paths.extend(v if isinstance(v,list)else[v])
  for relative in paths:
   p=self.project/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((PROJECT/relative).read_bytes())
 def call(self):return validate_packet_receive_extent(self.unit,self.project,TARGET_SHA256,self.info,self.linked,source_object=self.object)
 def reject(self):
  with self.assertRaises((ValueError,KeyError,TypeError)):self.call()
 def edit(self,path,fn):
  p=self.project/path;d=json.loads(p.read_text());fn(d);p.write_text(json.dumps(d))
 def byte(self,path,offset):
  def change(d):
   b=bytearray.fromhex(d['normalized_result']['bytes_hex']);b[offset]^=1;d['normalized_result']['bytes_hex']=b.hex()
  self.edit(path,change)
 def object_byte(self,offset):
  s=self.object.segments[1]
  for k,(at,b)in enumerate(s.chunks):
   if at<=offset<at+len(b):v=bytearray(b);v[offset-at]^=1;s.chunks[k]=(at,bytes(v));return
  raise AssertionError('missing byte')
 def test_positive856(self):self.assertEqual((self.call()['whole_CODE_SEGDEF'],self.call()['all_compiler_fields']),(856,36))
 def test_positive714(self):
  self.unit=json.loads((STAGE/'proposed-units.json').read_text())[1];self.object=read_omf((PROJECT/'build/packet-context-714/packet_context714.obj').read_bytes());self.info=self.object.function_info(self.unit['symbol']);self.assertEqual(self.call()['procedure_field_counts'],[11,16,4])
 def test_fresh856_source_excludes_target(self):
  old=Path.read_bytes;targets={(PROJECT.parent/'CHESS.EXE').resolve(),(PROJECT/'build/exepack/TRIM5_UNPACK.EXE').resolve()}
  def read(p,*a,**kw):
   if p.resolve()in targets:raise AssertionError('target read during generation')
   return old(p,*a,**kw)
  with patch.object(Path,'read_bytes',read):c=compile_c(PROJECT/self.unit['source'],self.unit['flags'],compiler='msc500')
  self.assertEqual(c.object_bytes,(PROJECT/'build/packet-context-856-root/packet_context856.obj').read_bytes())
 def test_every414_body_byte_required(self):
  for i in range(414):
   with self.subTest(offset=i):self.linked=self.good[:i]+bytes([self.good[i]^1])+self.good[i+1:];self.reject()
 def test_semantic_length_bound_wrong(self):self.linked=self.good[:81]+b'\x29'+self.good[82:];self.reject()
 def test_identity(self):self.unit['id']='another';self.reject()
 def test_size(self):self.unit['size']=412;self.reject()
 def test_flags(self):self.unit['flags']=['/AS','/Gs','/Zi'];self.reject()
 def test_source_name_override(self):self.unit['compiler_source_name']='PACKET.C';self.reject()
 def test_far_alias(self):self.unit['code_address']={'segment':0xddd,'offset':3};self.reject()
 def test_extra_binding(self):self.unit['externals']['_extra']=0;self.reject()
 def test_wrong_binding(self):self.unit['externals']['_read_bytes_dbe3']=0;self.reject()
 def test_metadata_extra(self):self.unit['extended_extent']['override']=856;self.reject()
 def test_wrong_kind(self):self.unit['extended_extent']['kind']='unreachable_return_gap_v1';self.reject()
 def test_wrong_context_kind(self):self.unit['extended_extent']['context_kind']='packet857_v1';self.reject()
 def test_856_object_cannot_claim714(self):self.unit=json.loads((STAGE/'proposed-units.json').read_text())[1];self.reject()
 def test_standalone_odd414_forbidden(self):self.object=read_omf((PROJECT/'build/receive-packet-ddd3/positive.obj').read_bytes());self.info=self.object.function_info(self.unit['symbol']);self.reject()
 def test_missing_object(self):self.object=None;self.reject()
 def test_hidden_COMMON(self):self.object.records.append((0xb0,0,b''));self.reject()
 def test_iterated_allocation(self):self.object.records.append((0xa2,0,b''));self.reject()
 def test_extra_allocation(self):self.object.segments[2].length=1;self.reject()
 def test_foreign_PUBLIC(self):self.object.publics['_extra']=next(iter(self.object.publics.values()));self.reject()
 def test_prefix_sender_must_match(self):self.object_byte(0);self.reject()
 def test_reset_must_match(self):self.object_byte(660);self.reject()
 def test_wrapper_must_match(self):self.object_byte(730);self.reject()
 def test_inputreset_must_match(self):self.object_byte(838);self.reject()
 def test_native90_must_match(self):self.object_byte(855);self.reject()
 def test_no_padding_added(self):self.object.segments[1].length=858;self.reject()
 def test_no_tail_crop(self):self.object.segments[1].length=855;self.reject()
 def test_CODE_hole(self):
  at,b=self.object.segments[1].chunks[0];self.object.segments[1].chunks[0]=(at+1,b);self.reject()
 def test_wrong_CV(self):self.info['size']=412;self.reject()
 def test_wrong_field_name(self):
  f=self.info['fixups'][0];self.object.externals[f.target[1]]='_foreign';self.reject()
 def test_wrong_field_shape(self):self.info['fixups'][0]=dataclasses.replace(self.info['fixups'][0],width=4);self.reject()
 def test_field_missing(self):self.object.fixups.pop(next(i for i,f in enumerate(self.object.fixups)if f.segment==1));self.reject()
 def test_fake_FIXUPP_for_resolved_call(self):self.object.fixups.append(dataclasses.replace(self.info['fixups'][0],offset=704));self.reject()
 def test_compiler_resolved_call_mutated(self):self.object_byte(704);self.reject()
 def test_wrapper_resolved_call_mutated(self):self.object_byte(759);self.reject()
 def test_duplicate_ID(self):
  body=json.loads((self.project/self.unit['rea_evidence']).read_text());self.edit(self.unit['extended_extent']['gap_decoder_evidence'],lambda d:d.update(evidence_id=body['evidence_id']));self.reject()
 def test_wrong_provider(self):self.edit(self.unit['rea_evidence'],lambda d:d['provider'].update(id='other'));self.reject()
 def test_wrong_subject(self):self.edit(self.unit['rea_evidence'],lambda d:d['subject'].update(format='elf'));self.reject()
 def test_wrong_profile(self):self.edit(self.unit['rea_evidence'],lambda d:d['analysis_profile']['parameters'].update(loader='other'));self.reject()
 def test_wrong_parameters(self):self.edit(self.unit['rea_evidence'],lambda d:d['parameters'].update(procedure='0x1ddd4'));self.reject()
 def test_native_ranges(self):self.edit(self.unit['rea_evidence'],lambda d:d['normalized_result']['procedure']['body']['ranges'][0].update(end='0x1dec1'));self.reject()
 def test_open_CFG(self):self.edit(self.unit['rea_evidence'],lambda d:d['normalized_result']['basic_blocks'][0]['successors'].append('0x1dec0'));self.reject()
 def test_gap_xref(self):self.edit(self.unit['extended_extent']['gap_xref_evidence'][0],lambda d:d.update(normalized_result=['0x12345']));self.reject()
 def test_gap_knowledge_not_invented(self):self.edit(self.unit['extended_extent']['gap_decoder_evidence'],lambda d:d['normalized_result'].update(status='decoded'));self.reject()
 def test_live_bypass_target(self):self.edit(self.unit['extended_extent']['preceding_jump_evidence'],lambda d:d['normalized_result']['flow'].update(direct_destinations=['0x1dece']));self.reject()
 def test_short_raw(self):self.edit(self.unit['extended_extent']['raw_span_evidence'],lambda d:d['normalized_result'].update(returned_bytes=472));self.reject()
 def test_raw_reset(self):self.byte(self.unit['extended_extent']['raw_span_evidence'],-1);self.reject()
 def test_raw_sender(self):self.byte(self.unit['extended_extent']['context_span_evidence'],0);self.reject()
 def test_raw_following(self):self.byte(self.unit['extended_extent']['following_span_evidence'],-1);self.reject()
 def test_raw_extended(self):self.byte(self.unit['extended_extent']['extended_context_evidence'],1);self.reject()
 def test_raw_huff_next(self):self.byte(self.unit['extended_extent']['extended_context_evidence'],-1);self.reject()
 def test_wrong_following_boundary(self):self.edit(self.unit['extended_extent']['following_entry_evidence'],lambda d:d['normalized_result']['procedure'].update(address='0x1dfad'));self.reject()
 def test_wrong_wrapper_boundary(self):self.edit(self.unit['extended_extent']['kind_wrapper_evidence'],lambda d:d['normalized_result']['procedure']['body'].update(span_bytes=43));self.reject()
 def test_wrong_inputreset_boundary(self):self.edit(self.unit['extended_extent']['input_reset_evidence'],lambda d:d['normalized_result']['procedure'].update(address='0x1e010'));self.reject()
 def test_wrong_huff_boundary(self):self.edit(self.unit['extended_extent']['huff_next_evidence'],lambda d:d['normalized_result']['procedure']['body'].update(total_bytes=60));self.reject()
if __name__=='__main__':unittest.main()
