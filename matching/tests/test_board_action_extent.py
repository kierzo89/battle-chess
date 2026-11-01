"""Fixed496 board action: native gaps, real dead cleanup and compiler ownership."""
import copy,dataclasses,json,sys,tempfile,unittest
from pathlib import Path
PROJECT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(PROJECT))
from board_action_extent import validate_board_action_extent,ORIGINAL_SHA256
from msc import compile_c
from omf import read_omf
from link16 import link_function
class BoardActionExtentTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  # Keep the classic39-field policy exercised independently of the new37-field source context.
  cls.unit=next(u for u in json.loads((PROJECT/'evidence/checkpoints/203-input-archive/config/units.json').read_text())if u['id']=='board_action_20d5')
  r=compile_c(PROJECT/cls.unit['source'],cls.unit['flags'],compiler='msc500');o=read_omf(r.object_bytes);cls.info=o.function_info(cls.unit['symbol']);cls.linked,_=link_function(o,cls.unit['symbol'],0x20d5,cls.unit['externals']);validate_board_action_extent(cls.unit,PROJECT,ORIGINAL_SHA256,cls.info,cls.linked)
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
  return validate_board_action_extent(self.unit,self.project,ORIGINAL_SHA256,self.info,self.linked)
 def test_fresh_full_C496_CFG49_next60(self):
  r=self.validate();self.assertEqual(r['span_bytes'],496);self.assertEqual(r['closed_cfg_blocks'],49);self.assertEqual(r['gap_bytes'],9);self.assertEqual(r['mz_relocations'],[0x2267])
 def test_each_linked_byte_rejected_including_all_dead_bytes(self):
  for at in range(496):
   b=bytearray(type(self).linked);b[at]^=1;self.linked=bytes(b)
   with self.subTest(at=at),self.assertRaises(ValueError):self.validate()
 def test_every_original_context_byte_rejected_even_if_compiler_agrees(self):
  n=self.e('raw_span_evidence')['normalized_result'];old=bytes.fromhex(n['bytes_hex'])
  for at in range(648):
   b=bytearray(old);b[at]^=1;n['bytes_hex']=b.hex();self.linked=bytes(b[92:588])
   with self.subTest(at=at),self.assertRaises(ValueError):self.validate()
 def test_identity_flags_metadata(self):
  old=copy.deepcopy(self.unit)
  for d in[{'id':'x'},{'symbol':'_x'},{'size':487},{'image_offset':'0x20d6'},{'flags':['/AS','/Os','/Zi']},{'language':'asm'},{'backend':'msc400-omf'},{'code_address':{'segment':0,'offset':0x20d5}}]:
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
     self.es=copy.deepcopy(old);b=self.es[p]['normalized_result']['basic_blocks'][at];b[field]=['0x121f7']if field=='successors'else hex(int(block[field],0)+1)
     with self.subTest(p=p,at=at,field=field),self.assertRaises(ValueError):self.validate()
 def test_external_interior_entry_rejected_body_and_next(self):
  old=copy.deepcopy(self.es)
  for p,target in[(self.unit['rea_evidence'],'0x121f7'),(self.unit['extended_extent']['next_entry_evidence'],'0x122c7')]:
   self.es=copy.deepcopy(old);self.es[p]['normalized_result']['incoming_references'].append({'source_address':'0x13000','target_address':target})
   with self.subTest(p=p),self.assertRaises(ValueError):self.validate()
 def test_each_global_gap_xref_required_empty_and_at_exact_address(self):
  old=copy.deepcopy(self.es)
  for p in self.unit['extended_extent']['gap_xref_evidence']:
   for k in['query','refs']:
    self.es=copy.deepcopy(old)
    if k=='query':self.es[p]['parameters']['address']='0x121f9'
    else:self.es[p]['normalized_result']=['0x12000']
    with self.subTest(p=p,k=k),self.assertRaises(ValueError):self.validate()
 def test_live_predecessors_decoded_and_gap_unknowns_preserved(self):
  old=copy.deepcopy(self.es)
  for k in['preceding_jump_evidence','gap_decoder_evidence','live_cleanup_evidence']:
   for p in self.unit['extended_extent'][k]:
    for field,val in[('status','other'),('bytes','90'),('length',1),('procedure','0x121f9')]:
     self.es=copy.deepcopy(old);self.es[p]['normalized_result'][field]=val
     with self.subTest(p=p,field=field),self.assertRaises(ValueError):self.validate()
 def test_raw_complete_counts_and_queries(self):
  old=copy.deepcopy(self.es)
  for field,val in[('complete',False),('address','0x1207a'),('requested_bytes',647),('returned_bytes',647)]:
   self.es=copy.deepcopy(old);self.e('raw_span_evidence')['normalized_result'][field]=val
   with self.subTest(field=field),self.assertRaises(ValueError):self.validate()
 def test_full_CV_identity_offset_size(self):
  old=copy.deepcopy(self.info)
  for k,v in[('symbol','_x'),('boundary','other'),('size',487),('offset',1),('end',495),('segment',0)]:
   self.info=copy.deepcopy(old);self.info[k]=v
   with self.subTest(k=k),self.assertRaises(ValueError):self.validate()
 def test_all39_actual_external_compiler_fields(self):
  old=copy.deepcopy(self.info)
  for at in range(39):
   for changes in[{'frame':(0,1)},{'target':(0,1)},{'width':1},{'location_type':0},{'segment_relative':not old['fixups'][at].segment_relative},{'displacement':1},{'segment':2},{'offset':999}]:
    self.info=copy.deepcopy(old);self.info['fixups'][at]=dataclasses.replace(self.info['fixups'][at],**changes)
    with self.subTest(at=at,changes=changes),self.assertRaises(ValueError):self.validate()
  for fs in[old['fixups'][:-1],old['fixups'][:-1]+old['fixups'][:1]]:
   self.info=copy.deepcopy(old);self.info['fixups']=fs
   with self.assertRaises(ValueError):self.validate()
 def test_CV_reviewed_contexts_zero_92_and205_only(self):
  old=copy.deepcopy(self.info)
  for pos in[0,92,205]:
   self.info=copy.deepcopy(old);d=pos-old['offset'];self.info.update(offset=pos,end=pos+496);self.info['fixups']=[dataclasses.replace(f,offset=f.offset+d)for f in old['fixups']];self.validate()
 def test_fresh_natural_six_function_context_offset205(self):
  units=json.loads((PROJECT/'build/pump-input-2301/group-units.json').read_text())
  unit=next(u for u in units if u['id']=='board_action_20d5')
  r=compile_c(PROJECT/unit['source'],unit['flags'],compiler='msc500');o=read_omf(r.object_bytes)
  info=o.function_info(unit['symbol']);linked,_=link_function(o,unit['symbol'],0x20d5,unit['externals'])
  self.assertEqual(info['offset'],205);self.assertEqual(info['end'],701)
  segment=o.segments[info['segment']]
  self.assertEqual(segment.length,1540)
  result=validate_board_action_extent(unit,PROJECT,ORIGINAL_SHA256,info,linked)
  self.assertEqual(result['compiler_fixups'],39);self.assertEqual(linked,type(self).linked)
 def test_unreviewed_adjacent_CV_offsets_rejected(self):
  old=copy.deepcopy(self.info)
  for pos in[1,91,93,204,206,496,1540]:
   self.info=copy.deepcopy(old);d=pos-old['offset'];self.info.update(offset=pos,end=pos+496)
   self.info['fixups']=[dataclasses.replace(f,offset=f.offset+d)for f in old['fixups']]
   with self.subTest(pos=pos),self.assertRaises(ValueError):self.validate()
 def test_real_cleanup_all_three_relocations_must_share_external_symbol(self):
  old=copy.deepcopy(self.info)
  for rel in[284,421,487]:
   self.info=copy.deepcopy(old)
   for at,f in enumerate(self.info['fixups']):
    if f.offset-self.info['offset']==rel:self.info['fixups'][at]=dataclasses.replace(f,target=(2,999))
   with self.subTest(rel=rel),self.assertRaises(ValueError):self.validate()
 def test_state_clear_actual_binding_fixed(self):
  self.unit['externals']['_board_action_active_0056']=0x57
  with self.assertRaises(ValueError):self.validate()
if __name__=='__main__':unittest.main()
