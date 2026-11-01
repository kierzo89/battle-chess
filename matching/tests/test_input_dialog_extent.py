"""Fixed260C canonical policy tests with retained immutable native/codegen fixture."""
import copy,dataclasses,hashlib,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
PROJECT=Path(__file__).resolve().parents[1]
STAGE=PROJECT/'build/input-dialog-260c'
sys.path.insert(0,str(PROJECT))
import input_dialog_extent as policy
assert Path(policy.__file__).resolve()==PROJECT/'input_dialog_extent.py'
from input_dialog_extent import validate_input_dialog_extent,TARGET_SHA256
from omf import read_omf
from msc import compile_c
class InputDialogExtentTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.template=json.loads((STAGE/'proposed-unit.json').read_text());cls.obj=read_omf((STAGE/'positive.obj').read_bytes());cls.good=bytes.fromhex(json.loads((STAGE/'complete-proof.json').read_text())['records'][0]['whole_linked_CODE'])
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.project=Path(self.tmp.name).resolve();self.unit=copy.deepcopy(self.template);self.object=copy.deepcopy(self.obj);self.linked=self.good;self.info=self.object.function_info('_input_dialog_260c')
  m=self.unit['extended_extent'];paths=[self.unit['rea_evidence'],m['raw_span_evidence'],m['next_entry_evidence'],m['gap_decoder_evidence'],m['preceding_jump_evidence']]+m['gap_xref_evidence']
  for relative in paths:
   p=self.project/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((PROJECT/relative).read_bytes())
 def call(self):return validate_input_dialog_extent(self.unit,self.project,TARGET_SHA256,self.info,self.linked,source_object=self.object)
 def reject(self):
  with self.assertRaises((ValueError,KeyError,TypeError)):self.call()
 def edit(self,path,fn):
  p=self.project/path;d=json.loads(p.read_text());fn(d);p.write_text(json.dumps(d))
 def test_positive_complete(self):
  p=self.call();self.assertEqual((p['span_bytes'],p['reachable_body_bytes'],p['compiler_fields'],p['FAR16_fields']),(242,240,17,3))
 def test_fresh_source_generation_excludes_target(self):
  original=Path.read_bytes;targets={(PROJECT.parent/'CHESS.EXE').resolve(),(PROJECT/'build/exepack/TRIM5_UNPACK.EXE').resolve()}
  def read(p,*a,**k):
   if p.resolve()in targets:raise AssertionError('target read during generation')
   return original(p,*a,**k)
  with patch.object(Path,'read_bytes',read):c=compile_c(PROJECT/self.unit['source'],self.unit['flags'],compiler='msc500')
  self.assertEqual(c.object_bytes,(STAGE/'positive.obj').read_bytes());self.assertEqual(c.source_sha256,hashlib.sha256((PROJECT/self.unit['source']).read_bytes()).hexdigest())
 def test_every_output_byte_required(self):
  for i in range(242):
   with self.subTest(offset=i):self.linked=self.good[:i]+bytes([self.good[i]^1])+self.good[i+1:];self.reject()
 def test_semantic_wrong_wrap_rejected(self):
  self.linked=bytes.fromhex(json.loads((STAGE/'complete-proof.json').read_text())['records'][1]['whole_linked_CODE']);self.reject()
 def test_wrong_identity(self):self.unit['id']='another';self.reject()
 def test_wrong_extent(self):self.unit['size']=240;self.reject()
 def test_wrong_flags(self):self.unit['flags']=['/AS','/Os','/Zi'];self.reject()
 def test_extra_metadata(self):self.unit['extended_extent']['override']=242;self.reject()
 def test_wrong_kind(self):self.unit['extended_extent']['kind']='unreachable_forward_jump_gap_v1';self.reject()
 def test_far_alias_wrong(self):self.unit['externals']['_write_command_fd4e']={'offset':0xfd4e,'segment':0};self.reject()
 def test_extra_binding(self):self.unit['externals']['_invented']=0;self.reject()
 def test_missing_object(self):self.object=None;self.reject()
 def test_extra_allocation(self):self.object.segments[2].length=1;self.reject()
 def test_foreign_public(self):self.object.publics['_extra']=next(iter(self.object.publics.values()));self.reject()
 def test_CODE_hole(self):
  at,b=self.object.segments[1].chunks[0];self.object.segments[1].chunks[0]=(at+1,b);self.reject()
 def test_far_field_changed(self):
  f=next(q for q in self.info['fixups']if q.width==4);self.info['fixups'][self.info['fixups'].index(f)]=dataclasses.replace(f,width=2);self.reject()
 def test_wrong_field_name(self):
  f=self.info['fixups'][0];self.object.externals[f.target[1]]='_foreign';self.reject()
 def test_wrong_subject_format(self):self.edit(self.unit['rea_evidence'],lambda d:d['subject'].update(format='elf'));self.reject()
 def test_wrong_arch(self):self.edit(self.unit['rea_evidence'],lambda d:d['subject'].update(architecture='x86_64'));self.reject()
 def test_wrong_provider(self):self.edit(self.unit['rea_evidence'],lambda d:d['provider'].update(id='other'));self.reject()
 def test_wrong_profile_parameters(self):self.edit(self.unit['rea_evidence'],lambda d:d['analysis_profile']['parameters'].update(loader='other'));self.reject()
 def test_wrong_query_parameters(self):self.edit(self.unit['rea_evidence'],lambda d:d['parameters'].update(procedure='0x1260d'));self.reject()
 def test_duplicate_ID(self):
  body=json.loads((self.project/self.unit['rea_evidence']).read_text());self.edit(self.unit['extended_extent']['gap_decoder_evidence'],lambda d:d.update(evidence_id=body['evidence_id']));self.reject()
 def test_gap_xref_not_empty(self):self.edit(self.unit['extended_extent']['gap_xref_evidence'][0],lambda d:d.update(normalized_result=['0x12345']));self.reject()
 def test_live_predecessor_target(self):self.edit(self.unit['extended_extent']['preceding_jump_evidence'],lambda d:d['normalized_result']['flow'].update(direct_destinations=['0x12673']));self.reject()
 def test_gap_provider_knowledge_not_invented(self):self.edit(self.unit['extended_extent']['gap_decoder_evidence'],lambda d:d['normalized_result'].update(status='decoded'));self.reject()
 def test_open_CFG(self):self.edit(self.unit['rea_evidence'],lambda d:d['normalized_result']['basic_blocks'][0]['successors'].append('0x12673'));self.reject()
 def test_bad_live_ranges(self):self.edit(self.unit['rea_evidence'],lambda d:d['normalized_result']['procedure']['body']['ranges'][0].update(end='0x12674'));self.reject()
 def test_next_entry_shift(self):self.edit(self.unit['extended_extent']['next_entry_evidence'],lambda d:d['normalized_result']['procedure'].update(address='0x126ff'));self.reject()
 def test_raw_short(self):self.edit(self.unit['extended_extent']['raw_span_evidence'],lambda d:d['normalized_result'].update(returned_bytes=308));self.reject()
 def test_next_raw_byte_changed(self):
  def change(d):
   b=bytearray.fromhex(d['normalized_result']['bytes_hex']);b[-1]^=1;d['normalized_result']['bytes_hex']=b.hex()
  self.edit(self.unit['extended_extent']['raw_span_evidence'],change);self.reject()
if __name__=='__main__':unittest.main()
