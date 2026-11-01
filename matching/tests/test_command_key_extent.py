"""Isolated fixedFD6A extent controls; no canonical test/core mutation."""
import copy,dataclasses,hashlib,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
PROJECT=Path(__file__).resolve().parents[1];STAGE=PROJECT/'build/command-key-fd6a'
sys.path.insert(0,str(PROJECT))
import command_key_extent as policy
assert Path(policy.__file__).resolve()==PROJECT/'command_key_extent.py'
from command_key_extent import validate_command_key_extent,TARGET_SHA256
from omf import read_omf
from msc import compile_c
class CommandKeyTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.template=json.loads((STAGE/'proposed-unit.json').read_text());cls.obj=read_omf((STAGE/'positive.obj').read_bytes());cls.good=bytes.fromhex(json.loads((STAGE/'complete-proof.json').read_text())['records'][0]['whole_linked_CODE'])[:135]
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.project=Path(self.tmp.name);self.unit=copy.deepcopy(self.template);self.object=copy.deepcopy(self.obj);self.info=self.object.function_info(self.unit['symbol']);self.linked=self.good
  m=self.unit['extended_extent'];paths=[self.unit['rea_evidence'],m['raw_span_evidence'],m['next_entry_evidence'],m['gap_decoder_evidence'],m['preceding_jump_evidence'],m['alignment_observation_evidence']]+m['gap_xref_evidence']+m['context_prefix_evidence']
  for relative in paths:
   p=self.project/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((PROJECT/relative).read_bytes())
 def call(self):return validate_command_key_extent(self.unit,self.project,TARGET_SHA256,self.info,self.linked,source_object=self.object)
 def reject(self):
  with self.assertRaises((ValueError,KeyError,TypeError)):self.call()
 def edit(self,path,fn):
  p=self.project/path;d=json.loads(p.read_text());fn(d);p.write_text(json.dumps(d))
 def test_positive136(self):self.assertEqual(self.call()['whole_CODE_SEGDEF'],136)
 def test_positive_named_AM508(self):
  self.unit=json.loads((STAGE/'named-context-proposed-units.json').read_text())[-1];self.object=read_omf((PROJECT/'build/display-named-context-508/DISPLAY.OBJ').read_bytes());self.info=self.object.function_info(self.unit['symbol']);self.assertEqual(self.call()['whole_CODE_SEGDEF'],508)
 def test_AM_rejects136(self):
  self.unit['flags']=['/AM','/Gs','/Zi'];self.unit['compiler_source_name']='DISPLAY.C';self.reject()
 def test_wrong_named_basename(self):
  self.unit['flags']=['/AM','/Gs','/Zi'];self.unit['compiler_source_name']='OTHER.C';self.reject()
 def test_AS_cannot_masquerade_named(self):self.unit['compiler_source_name']='DISPLAY.C';self.reject()
 def test_fresh_named_generation_excludes_targets(self):
  unit=json.loads((STAGE/'named-context-proposed-units.json').read_text())[-1];old=Path.read_bytes;targets={(PROJECT.parent/'CHESS.EXE').resolve(),(PROJECT/'build/exepack/TRIM5_UNPACK.EXE').resolve()}
  def read(p,*a,**k):
   if p.resolve()in targets:raise AssertionError('target read during generation')
   return old(p,*a,**k)
  with patch.object(Path,'read_bytes',read):c=compile_c(PROJECT/unit['source'],unit['flags'],compiler='msc500',source_name=unit['compiler_source_name'])
  self.assertEqual(c.object_bytes,(PROJECT/'build/display-named-context-508/DISPLAY.OBJ').read_bytes())
 def test_positive508(self):
  self.object=read_omf((STAGE/'context508.obj').read_bytes());self.info=self.object.function_info(self.unit['symbol']);self.assertEqual(self.call()['whole_CODE_SEGDEF'],508)
 def test_fresh_generation_excludes_targets(self):
  old=Path.read_bytes;targets={(PROJECT.parent/'CHESS.EXE').resolve(),(PROJECT/'build/exepack/TRIM5_UNPACK.EXE').resolve()}
  def read(p,*a,**k):
   if p.resolve()in targets:raise AssertionError('target read during generation')
   return old(p,*a,**k)
  with patch.object(Path,'read_bytes',read):c=compile_c(PROJECT/self.unit['source'],self.unit['flags'],compiler='msc500')
  self.assertEqual(c.object_bytes,(STAGE/'positive.obj').read_bytes())
 def test_every135_body_byte_required(self):
  for i in range(135):
   with self.subTest(offset=i):self.linked=self.good[:i]+bytes([self.good[i]^1])+self.good[i+1:];self.reject()
 def test_semantic_wrong_key(self):self.linked=bytes.fromhex(json.loads((STAGE/'complete-proof.json').read_text())['records'][1]['whole_linked_CODE'])[:135];self.reject()
 def test_identity(self):self.unit['id']='foreign';self.reject()
 def test_extent(self):self.unit['size']=133;self.reject()
 def test_wrong_flags(self):self.unit['flags']=['/AS','/Zi'];self.reject()
 def test_wrong_far_alias(self):self.unit['code_address']['segment']=0;self.reject()
 def test_extra_bindings(self):self.unit['externals']['_extra']=0;self.reject()
 def test_metadata(self):self.unit['extended_extent']['override']=135;self.reject()
 def test_wrong_kind(self):self.unit['extended_extent']['kind']='unreachable_forward_jump_gap_v1';self.reject()
 def test_missing_object(self):self.object=None;self.reject()
 def test_tail_must_be_native90(self):
  at,b=self.object.segments[1].chunks[-1];self.object.segments[1].chunks[-1]=(at,b[:-1]+b'\xcc');self.reject()
 def test_CODE_hole(self):
  at,b=self.object.segments[1].chunks[0];self.object.segments[1].chunks[0]=(at+1,b);self.reject()
 def test_other_allocation(self):self.object.segments[2].length=1;self.reject()
 def test_foreign_public(self):self.object.publics['_foreign']=next(iter(self.object.publics.values()));self.reject()
 def test_wrong_CV(self):self.info['size']=133;self.reject()
 def test_field_name(self):
  f=self.info['fixups'][0];self.object.externals[f.target[1]]='_foreign';self.reject()
 def test_field_frame(self):
  self.info['fixups'][0]=dataclasses.replace(self.info['fixups'][0],frame=(0,1));self.reject()
 def test_field_missing(self):self.info['fixups'].pop();self.reject()
 def test_wrong_subject(self):self.edit(self.unit['rea_evidence'],lambda d:d['subject'].update(format='elf'));self.reject()
 def test_wrong_provider(self):self.edit(self.unit['rea_evidence'],lambda d:d['provider'].update(id='other'));self.reject()
 def test_wrong_profile(self):self.edit(self.unit['rea_evidence'],lambda d:d['analysis_profile']['parameters'].update(loader='other'));self.reject()
 def test_wrong_parameters(self):self.edit(self.unit['rea_evidence'],lambda d:d['parameters'].update(procedure='0x1fd6b'));self.reject()
 def test_duplicate_ID(self):
  body=json.loads((self.project/self.unit['rea_evidence']).read_text());self.edit(self.unit['extended_extent']['gap_decoder_evidence'],lambda d:d.update(evidence_id=body['evidence_id']));self.reject()
 def test_gap_xref(self):self.edit(self.unit['extended_extent']['gap_xref_evidence'][0],lambda d:d.update(normalized_result=['0x1234']));self.reject()
 def test_provider_gap_knowledge(self):self.edit(self.unit['extended_extent']['gap_decoder_evidence'],lambda d:d['normalized_result'].update(status='decoded'));self.reject()
 def test_provider_alignment_knowledge(self):self.edit(self.unit['extended_extent']['alignment_observation_evidence'],lambda d:d['normalized_result'].update(status='decoded'));self.reject()
 def test_predecessor_destination(self):self.edit(self.unit['extended_extent']['preceding_jump_evidence'],lambda d:d['normalized_result']['flow'].update(direct_destinations=['0x1fde9']));self.reject()
 def test_CFG_open(self):self.edit(self.unit['rea_evidence'],lambda d:d['normalized_result']['basic_blocks'][0]['successors'].append('0x1fdd1'));self.reject()
 def test_wrong_live_ranges(self):self.edit(self.unit['rea_evidence'],lambda d:d['normalized_result']['procedure']['body']['ranges'][0].update(end='0x1fdd2'));self.reject()
 def test_raw_short(self):self.edit(self.unit['extended_extent']['raw_span_evidence'],lambda d:d['normalized_result'].update(returned_bytes=161));self.reject()
 def raw_change(self,path,offset):
  def change(d):
   b=bytearray.fromhex(d['normalized_result']['bytes_hex']);b[offset]^=1;d['normalized_result']['bytes_hex']=b.hex()
  self.edit(path,change)
 def test_raw_alignment_byte(self):self.raw_change(self.unit['extended_extent']['raw_span_evidence'],135);self.reject()
 def test_raw_next_body(self):self.raw_change(self.unit['extended_extent']['raw_span_evidence'],-1);self.reject()
 def test_raw_prefix(self):self.raw_change(self.unit['extended_extent']['context_prefix_evidence'][0],0);self.reject()
 def test_next_boundary(self):self.edit(self.unit['extended_extent']['next_entry_evidence'],lambda d:d['normalized_result']['procedure'].update(address='0x1fdf1'));self.reject()
 def test_context_foreign_prefix(self):
  self.object=read_omf((STAGE/'context508.obj').read_bytes());self.info=self.object.function_info(self.unit['symbol']);at,b=self.object.segments[1].chunks[0];self.object.segments[1].chunks[0]=(at,bytes([b[0]^1])+b[1:]);self.reject()
if __name__=='__main__':unittest.main()
