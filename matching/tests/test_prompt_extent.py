"""Original432 prompt boundary: full native/bytes/fields and rejected mutations."""
import copy,dataclasses,json,sys,tempfile,unittest
from pathlib import Path
PROJECT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(PROJECT))
from prompt_extent import validate_prompt_extent,ORIGINAL_SHA256
from msc import compile_c
from omf import read_omf
from link16 import link_function
class PromptExtentTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.unit=next((u for u in json.loads((PROJECT/'config/units.json').read_text())if u['id']=='prompt_1296'),None)or json.loads((PROJECT/'evidence/prompt-extent-unit.json').read_text())
  r=compile_c(PROJECT/cls.unit['source'],cls.unit['flags'],compiler='msc500');o=read_omf(r.object_bytes);cls.info=o.function_info(cls.unit['symbol']);cls.linked,_=link_function(o,cls.unit['symbol'],0x1296,cls.unit['externals']);validate_prompt_extent(cls.unit,PROJECT,ORIGINAL_SHA256,cls.info,cls.linked)
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.project=Path(self.tmp.name)/'matching';self.project.mkdir();(self.project.parent/'CHESS.EXE').write_bytes((PROJECT.parent/'CHESS.EXE').read_bytes());self.unit=copy.deepcopy(type(self).unit);self.info=copy.deepcopy(type(self).info);self.linked=type(self).linked;self.paths=[self.unit['rea_evidence']]
  for k,v in self.unit['extended_extent'].items():
   if k!='kind':self.paths.extend(v if isinstance(v,list)else[v])
  self.es={p:json.loads((PROJECT/p).read_text())for p in self.paths};self.written={}
  for e in self.es.values():
   e.pop('raw_result',None)
   if e['operation']=='analyze_function':
    n=e['normalized_result'];e['normalized_result']={k:n[k]for k in['procedure','basic_blocks','incoming_references']}
 def e(self,k):return self.es[self.unit['extended_extent'][k]]
 def validate(self):
  for p,e in self.es.items():
   s=json.dumps(e)
   if self.written.get(p)!=s:q=self.project/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(s);self.written[p]=s
  return validate_prompt_extent(self.unit,self.project,ORIGINAL_SHA256,self.info,self.linked)
 def test_fresh_full_C432_CFG38_next123(self):
  r=self.validate();self.assertEqual(r['span_bytes'],432);self.assertEqual(r['closed_cfg_blocks'],38);self.assertEqual(r['gap_bytes'],4);self.assertEqual(r['mz_relocations'],[])
 def test_each_linked_byte_rejected_including_all_dead_bytes(self):
  for at in range(432):
   b=bytearray(type(self).linked);b[at]^=1;self.linked=bytes(b)
   with self.subTest(at=at),self.assertRaises(ValueError):self.validate()
 def test_every_original_context_byte_rejected_even_if_compiler_agrees(self):
  n=self.e('raw_span_evidence')['normalized_result'];old=bytes.fromhex(n['bytes_hex'])
  for at in range(555):
   b=bytearray(old);b[at]^=1;n['bytes_hex']=b.hex();self.linked=bytes(b[:432])
   with self.subTest(at=at),self.assertRaises(ValueError):self.validate()
 def test_identity_flags_metadata(self):
  old=copy.deepcopy(self.unit)
  for d in[{'id':'x'},{'symbol':'_x'},{'size':428},{'image_offset':'0x1297'},{'flags':['/AS','/Os','/Zi']},{'language':'asm'},{'backend':'msc400-omf'},{'code_address':{'segment':0,'offset':0x1296}}]:
   self.unit=copy.deepcopy(old);self.unit.update(d)
   with self.subTest(d=d),self.assertRaises(ValueError):self.validate()
  self.unit=copy.deepcopy(old);self.unit['extended_extent']['extra']=1
  with self.assertRaises(ValueError):self.validate()
 def test_each_evidence_pin_profile_operation_identity(self):
  old=copy.deepcopy(self.es)
  for p in self.paths:
   for k in['subject','operation','digest','load_segment','language_id','target_format','identity']:
    self.es=copy.deepcopy(old);e=self.es[p]
    if k=='subject':e['subject']['digest']['sha256']='0'*64
    elif k=='operation':e['operation']='other'
    elif k=='digest':e['analysis_profile']['digest']='other'
    elif k=='identity':e['evidence_id']=old[self.paths[(self.paths.index(p)+1)%len(self.paths)]]['evidence_id']
    else:e['analysis_profile']['parameters'][k]='other'
    with self.subTest(p=p,k=k),self.assertRaises(ValueError):self.validate()
 def test_complete_original_binary_pin(self):
  p=self.project.parent/'CHESS.EXE';b=bytearray(p.read_bytes());b[10]^=1;p.write_bytes(b)
  with self.assertRaises(ValueError):self.validate()
 def test_native_body_and_next_queries_ranges_counts(self):
  old=copy.deepcopy(self.es)
  for p in[self.unit['rea_evidence'],self.unit['extended_extent']['next_entry_evidence']]:
   for k in['query','ranges','total_bytes','span_bytes','contains_entry','available','non_contiguous']:
    self.es=copy.deepcopy(old)
    if k=='query':self.es[p]['parameters']['procedure']='0x10000'
    else:
     b=self.es[p]['normalized_result']['procedure']['body'];b[k]=[]if k=='ranges'else not b[k]if isinstance(b[k],bool)else 1
    with self.subTest(p=p,k=k),self.assertRaises(ValueError):self.validate()
 def test_each_CFG_block_and_successor_body_and_next(self):
  old=copy.deepcopy(self.es)
  for p in[self.unit['rea_evidence'],self.unit['extended_extent']['next_entry_evidence']]:
   for at,block in enumerate(old[p]['normalized_result']['basic_blocks']):
    for field in['start','end','successors']:
     self.es=copy.deepcopy(old);b=self.es[p]['normalized_result']['basic_blocks'][at];b[field]=['0x11370']if field=='successors'else hex(int(block[field],0)+1)
     with self.subTest(p=p,at=at,field=field),self.assertRaises(ValueError):self.validate()
 def test_external_interior_entry_rejected_body_and_next(self):
  old=copy.deepcopy(self.es)
  for p,target in[(self.unit['rea_evidence'],'0x11370'),(self.unit['extended_extent']['next_entry_evidence'],'0x11448')]:
   self.es=copy.deepcopy(old);self.es[p]['normalized_result']['incoming_references'].append({'source_address':'0x13000','target_address':target})
   with self.subTest(p=p),self.assertRaises(ValueError):self.validate()
 def test_each_global_gap_xref_required_empty_and_at_exact_address(self):
  old=copy.deepcopy(self.es)
  for p in self.unit['extended_extent']['gap_xref_evidence']:
   for k in['query','refs']:
    self.es=copy.deepcopy(old)
    if k=='query':self.es[p]['parameters']['address']='0x11372'
    else:self.es[p]['normalized_result']=['0x12000']
    with self.subTest(p=p,k=k),self.assertRaises(ValueError):self.validate()
 def test_live_predecessors_decoded_and_gap_unknowns_preserved(self):
  old=copy.deepcopy(self.es)
  for k in['preceding_jump_evidence','gap_decoder_evidence']:
   for p in self.unit['extended_extent'][k]:
    for field,val in[('status','other'),('bytes','90'),('length',1),('procedure','0x11372')]:
     self.es=copy.deepcopy(old);self.es[p]['normalized_result'][field]=val
     with self.subTest(p=p,field=field),self.assertRaises(ValueError):self.validate()
 def test_raw_complete_counts_and_queries(self):
  old=copy.deepcopy(self.es)
  for field,val in[('complete',False),('address','0x11297'),('requested_bytes',554),('returned_bytes',554)]:
   self.es=copy.deepcopy(old);self.e('raw_span_evidence')['normalized_result'][field]=val
   with self.subTest(field=field),self.assertRaises(ValueError):self.validate()
 def test_full_CV_identity_offset_size(self):
  old=copy.deepcopy(self.info)
  for k,v in[('symbol','_x'),('boundary','other'),('size',428),('offset',1),('end',431),('segment',0)]:
   self.info=copy.deepcopy(old);self.info[k]=v
   with self.subTest(k=k),self.assertRaises(ValueError):self.validate()
 def test_all34_actual_external_OFFSET16_fields(self):
  old=copy.deepcopy(self.info)
  for at in range(34):
   for changes in[{'frame':(0,1)},{'target':(0,1)},{'width':4},{'location_type':3},{'segment_relative':not old['fixups'][at].segment_relative},{'displacement':1},{'segment':2},{'offset':999}]:
    self.info=copy.deepcopy(old);self.info['fixups'][at]=dataclasses.replace(self.info['fixups'][at],**changes)
    with self.subTest(at=at,changes=changes),self.assertRaises(ValueError):self.validate()
  for fs in[old['fixups'][:-1],old['fixups'][:-1]+old['fixups'][:1]]:
   self.info=copy.deepcopy(old);self.info['fixups']=fs
   with self.assertRaises(ValueError):self.validate()
if __name__=='__main__':unittest.main()
