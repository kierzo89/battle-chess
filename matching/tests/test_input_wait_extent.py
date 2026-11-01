"""Fixed607 native extent plus actual source-owned2322 and37-field board context."""
import copy,dataclasses,json,sys,tempfile,unittest
from pathlib import Path
STAGE=Path(__file__).resolve().parent;PROJECT=STAGE.parent if STAGE.name=='tests'else STAGE.parents[2]
sys.path.insert(0,str(PROJECT));sys.path.insert(0,str(STAGE))
from msc import compile_c
from omf import read_omf
from link16 import link_function
from extent import validate_extended_extent
from input_wait_context import validate_source_context
from input_wait_context_specs import BINDINGS,LAYOUT
from reference import ORIGINAL_SHA256,build_reference
class InputWaitExtentTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.units=json.loads((PROJECT/'config/units.json').read_text())
  if not any(x['id']=='input_wait_1da9'for x in cls.units):cls.units=json.loads((PROJECT/'build/input-wait-1da9/reviewed-coupled-units.json').read_text())
  cls.input=next(x for x in cls.units if x['id']=='input_wait_1da9');cls.board=next(x for x in cls.units if x['id']=='board_action_20d5')
  r=compile_c(PROJECT/cls.input['source'],['/AS','/Zi'],compiler='msc500');cls.built=r;cls.original_obj=read_omf(r.object_bytes);cls.ref=build_reference((PROJECT.parent/'CHESS.EXE').read_bytes())
  cls.evidence_paths={'evidence/rea_low_control_refresh_panel_1d51.json','evidence/rea_input_wait_command_full_2322_original.json','evidence/rea_input_wait_command_full_2322_expanded.json'}
  for u in [cls.input,cls.board]:
   cls.evidence_paths.add(u['rea_evidence'])
   for k,v in u['extended_extent'].items():
    if k!='kind':cls.evidence_paths.update(v if isinstance(v,list)else[v])
  cls.original_evidence={p:json.loads((PROJECT/p).read_text())for p in cls.evidence_paths}
  for e in cls.original_evidence.values():
   e.pop('raw_result',None)
   if e['operation']=='analyze_function':
    n=e['normalized_result'];e['normalized_result']={k:n[k]for k in ['procedure','basic_blocks','incoming_references']}
 @classmethod
 def tearDownClass(cls):pass
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.project=Path(self.tmp.name)/'matching';self.project.mkdir();(self.project.parent/'CHESS.EXE').write_bytes((PROJECT.parent/'CHESS.EXE').read_bytes())
  self.unit=copy.deepcopy(self.input);self.obj=copy.deepcopy(self.original_obj);self.es=copy.deepcopy(self.original_evidence);self.written={};self.linked_override=None;self.info_override=None;self.object_override=False
 def validate(self,board=False):
  if board:self.unit=copy.deepcopy(self.board)
  for path,e in self.es.items():
   s=json.dumps(e)
   if self.written.get(path)!=s:p=self.project/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s);self.written[path]=s
  info=self.obj.function_info(self.unit['symbol'])if self.info_override is None else self.info_override
  linked,_=link_function(self.original_obj,self.unit['symbol'],int(self.unit['image_offset'],0),self.unit['externals'])
  if self.linked_override is not None:linked=self.linked_override
  obj=None if self.object_override else self.obj
  return validate_extended_extent(self.unit,self.project,ORIGINAL_SHA256,info,linked,source_object=obj)
 def test_fresh_coupled607_51_and_board496_37_whole2322(self):
  p=self.validate();self.assertEqual((p['span_bytes'],p['reachable_body_bytes'],p['closed_cfg_blocks']),(607,605,40));self.assertEqual(p['compiler_fixups'],51);ctx=p['source_owned_context'];self.assertEqual(ctx['whole_source_CODE_bytes'],2322);self.assertEqual(ctx['actual_raw_fixups'],199);self.assertEqual(len(ctx['real_internal_CALLs']),4)
  p=self.validate(board=True);self.assertEqual(p['compiler_fixups'],37);self.assertEqual(p['source_owned_context']['actual_refresh_PUBLIC'],87)
 def test_no_fresh_object_no_51_or37_field_exception(self):
  self.object_override=True
  with self.assertRaises(ValueError):self.validate()
  with self.assertRaises(ValueError):self.validate(board=True)
 def test_every_inputwait_byte_including_dead_break_and_epilogue_is_fixed(self):
  base=self.ref['image'][0x1da9:0x2008]
  for at in range(607):
   b=bytearray(base);b[at]^=1;self.linked_override=bytes(b)
   with self.subTest(at=at),self.assertRaises(ValueError):self.validate()
 def test_raw_original_and_loaded_expanded_all720_plus_context_bytes(self):
  for key in ['original_raw_evidence','expanded_raw_evidence']:
   path=self.unit['extended_extent'][key];old=copy.deepcopy(self.es[path])
   for field,value in [('complete',False),('returned_bytes',719),('requested_bytes',719),('address','0x11daa')]:
    self.es[path]=copy.deepcopy(old);self.es[path]['normalized_result'][field]=value
    with self.subTest(key=key,field=field),self.assertRaises(ValueError):self.validate()
   self.es[path]=copy.deepcopy(old)
   for at in [0,50,85,248,605,606,607,719]:
    b=bytearray.fromhex(old['normalized_result']['bytes_hex']);b[at]^=1;self.es[path]['normalized_result']['bytes_hex']=b.hex()
    with self.subTest(key=key,byte=at),self.assertRaises(ValueError):self.validate()
   self.es[path]=old
  path='evidence/rea_input_wait_command_full_2322_expanded.json';old=copy.deepcopy(self.es[path]);b=bytearray.fromhex(old['normalized_result']['bytes_hex']);b[0]^=1;self.es[path]['normalized_result']['bytes_hex']=b.hex()
  with self.assertRaises(ValueError):self.validate()
 def test_every_evidence_target_profile_operation_and_duplicate_id_rejected(self):
  old=copy.deepcopy(self.es)
  active={self.unit['rea_evidence'],'evidence/rea_low_control_refresh_panel_1d51.json','evidence/rea_input_wait_command_full_2322_original.json','evidence/rea_input_wait_command_full_2322_expanded.json'}
  for k,v in self.unit['extended_extent'].items():
   if k!='kind':active.update(v if isinstance(v,list)else[v])
  for path in active:
   for field in ['subject','operation','digest','load_segment','language_id','target_format','identity']:
    self.es=copy.deepcopy(old);e=self.es[path]
    if field=='subject':e['subject']['digest']['sha256']='0'*64
    elif field=='operation':e['operation']='other'
    elif field=='digest':e['analysis_profile']['digest']='other'
    elif field=='identity':
     # Primary/every metadata set must be distinct; shared-context extras
     # also have independently pinned raw/refresh identities by operation.
     peer=self.unit['rea_evidence']if path!=self.unit['rea_evidence']else self.unit['extended_extent']['expanded_body_evidence'];e['evidence_id']=old[peer]['evidence_id']
    else:e['analysis_profile']['parameters'][field]='other'
    with self.subTest(path=path,field=field),self.assertRaises(ValueError):self.validate()
 def test_original_partial_and_full_next_native_bodies_cannot_be_reinterpreted(self):
  old=copy.deepcopy(self.es);paths=[self.unit['rea_evidence'],self.unit['extended_extent']['expanded_body_evidence'],*self.unit['extended_extent']['original_partial_evidence'],self.unit['extended_extent']['original_next_evidence'],self.unit['extended_extent']['expanded_next_evidence']]
  for path in paths:
   for field in ['ranges','total_bytes','span_bytes','contains_entry','available','non_contiguous']:
    self.es=copy.deepcopy(old);b=self.es[path]['normalized_result']['procedure']['body'];b[field]=[]if field=='ranges'else not b[field]if isinstance(b[field],bool)else 1
    with self.subTest(path=path,field=field),self.assertRaises(ValueError):self.validate()
 def test_each_expanded40block_successor_and_external_gap_entry_rejected(self):
  path=self.unit['extended_extent']['expanded_body_evidence'];old=copy.deepcopy(self.es[path]);n=old['normalized_result']
  for at,block in enumerate(n['basic_blocks']):
   for field in ['start','end','successors']:
    self.es[path]=copy.deepcopy(old);b=self.es[path]['normalized_result']['basic_blocks'][at];b[field]=['0x11eb8']if field=='successors'else hex(int(block[field],0)+1)
    with self.subTest(block=at,field=field),self.assertRaises(ValueError):self.validate()
  self.es[path]=copy.deepcopy(old);self.es[path]['normalized_result']['incoming_references'].append({'source_address':'0x15000','target_address':'0x11eb8'})
  with self.assertRaises(ValueError):self.validate()
 def test_all_false_far_sources_gap_xrefs_and_decoders_are_independent(self):
  old=copy.deepcopy(self.es)
  for key in ['original_false_xrefs_evidence','expanded_false_xrefs_evidence','original_gap_xrefs_evidence','expanded_gap_xrefs_evidence']:
   for path in self.unit['extended_extent'][key]:
    self.es=copy.deepcopy(old);n=self.es[path]['normalized_result'];self.es[path]['normalized_result']=n[1:]if n else['0x15000']
    with self.subTest(path=path),self.assertRaises(ValueError):self.validate()
  for key in ['expanded_instruction_evidence','original_instruction_evidence']:
   for path in self.unit['extended_extent'][key]:
    for field,value in [('status','decoded-other'),('bytes','90'),('length',99),('procedure','0x12002')]:
     self.es=copy.deepcopy(old);self.es[path]['normalized_result'][field]=value
     with self.subTest(path=path,field=field),self.assertRaises(ValueError):self.validate()
 def test_every199_real_context_field_shape_and_name_and_raw_fixupp_is_fixed(self):
  original=copy.deepcopy(self.original_obj)
  positions=[at for at,f in enumerate(original.fixups)if f.segment==1];self.assertEqual(len(positions),199)
  for at in positions:
   f=original.fixups[at]
   for changes in [{'target':(0,1)},{'frame':(0,1)},{'width':1},{'location_type':0},{'segment_relative':not f.segment_relative},{'displacement':1},{'raw':b'bad'},{'record_offset':-1}]:
    self.obj=copy.deepcopy(original);self.obj.fixups[at]=dataclasses.replace(f,**changes)
    with self.subTest(field=at,changes=changes),self.assertRaises(ValueError):self.validate()
 def test_four_actual_internal_calls_cannot_gain_fake_fixups_or_change_target(self):
  original=copy.deepcopy(self.original_obj);one=next(f for f in original.fixups if f.segment==1)
  for symbol,relative in [('_input_wait_1da9',120),('_input_wait_1da9',266),('_board_action_20d5',274),('_board_action_20d5',411)]:
   offset=original.function_info(symbol)['offset']+relative;self.obj=copy.deepcopy(original);self.obj.fixups.append(dataclasses.replace(one,offset=offset))
   with self.subTest(symbol=symbol,mode='fakefixup'),self.assertRaises(ValueError):self.validate()
   self.obj=copy.deepcopy(original);seg=self.obj.segments[1]
   # Alter actual raw displacement without changing the reference or public.
   seg.chunks=[(at,bytes((byte^1)if at+i==offset else byte for i,byte in enumerate(data)))for at,data in seg.chunks]
   with self.subTest(symbol=symbol,mode='wrongtarget'),self.assertRaises(ValueError):self.validate()
 def test_source_public_cv_storage_and_chunk_malformations_rejected(self):
  original=copy.deepcopy(self.original_obj)
  for change in ['missingPUBLIC','wrongPUBLIC','extraPUBLIC','shortCODE','alignment','hole','otherstorage','refreshbytes','wrongbinding','foreignemptyseg','extraCV','groupPUBLIC']:
   self.obj=copy.deepcopy(original);seg=self.obj.segments[1]
   if change=='missingPUBLIC':del self.obj.publics['_refresh_panel_1d51']
   elif change=='wrongPUBLIC':p=self.obj.publics['_refresh_panel_1d51'];self.obj.publics[p.name]=dataclasses.replace(p,offset=88)
   elif change=='extraPUBLIC':p=self.obj.publics['_refresh_panel_1d51'];self.obj.publics['_fake']=dataclasses.replace(p,name='_fake')
   elif change=='shortCODE':seg.length-=1
   elif change=='alignment':seg.attributes=0x68
   elif change=='hole':seg.chunks=[(a+1,b)for a,b in seg.chunks]
   elif change=='otherstorage':next(s for s in self.obj.segments.values()if s.name=='_BSS').length=2
   elif change=='foreignemptyseg':s=copy.deepcopy(self.obj.segments[2]);s.index=7;s.name='EVIL';self.obj.segments[7]=s
   elif change=='extraCV':self.obj.procedures['_hidden']=copy.deepcopy(self.obj.procedures['_refresh_panel_1d51'])
   elif change=='groupPUBLIC':p=self.obj.publics['_refresh_panel_1d51'];self.obj.publics[p.name]=dataclasses.replace(p,group=1)
   elif change=='refreshbytes':seg.chunks=[(at,bytes((byte^1)if at+i==90 else byte for i,byte in enumerate(data)))for at,data in seg.chunks]
   else:self.unit['externals']['__chkstk']=0xecab
   with self.subTest(change=change),self.assertRaises(ValueError):self.validate()
 def test_no_detached_emitted_info_and_no_standalone53_or_unreviewed_offset(self):
  old=self.original_obj.function_info('_input_wait_1da9')
  for field,value in [('symbol','_x'),('offset',0),('size',605),('end',781),('boundary','next_public'),('segment',2)]:
   self.info_override=copy.deepcopy(old);self.info_override[field]=value
   with self.subTest(field=field),self.assertRaises(ValueError):self.validate()
  standalone=compile_c(PROJECT/'src/probes/input_wait_1da9_match.c',['/AS','/Zi'],compiler='msc500');self.obj=read_omf(standalone.object_bytes);self.info_override=None
  with self.assertRaises(ValueError):self.validate()
 def test_original_binary_pin_required(self):
  p=self.project.parent/'CHESS.EXE';b=bytearray(p.read_bytes());b[8]^=1;p.write_bytes(b)
  with self.assertRaises(ValueError):self.validate()
if __name__=='__main__':unittest.main()
