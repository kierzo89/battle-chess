"""Full keyboard C extents and rejected forged native/compiler proofs."""
import copy,dataclasses,json,sys,tempfile,unittest
from pathlib import Path
PROJECT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(PROJECT))
from keyboard_extent import validate_keyboard_extent,ORIGINAL_SHA256
from msc import compile_c
from omf import read_omf
from link16 import link_function
class KeyboardExtentTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  canonical=json.loads((PROJECT/'config/units.json').read_text());p=json.loads((PROJECT/'evidence/keyboard-extent-units.json').read_text());cls.units=[next((u for u in canonical if u['id']==v['id']),v)for v in p]
  s=cls.units[0];r=compile_c(PROJECT/s['source'],s['flags'],compiler='msc500');o=read_omf(r.object_bytes);cls.infos={u['id']:o.function_info(u['symbol'])for u in cls.units};cls.linked={u['id']:link_function(o,u['symbol'],int(u['image_offset'],0),u['externals'])[0]for u in cls.units}
 def setUp(self):
  t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.project=Path(t.name)/'matching';self.project.mkdir();(self.project.parent/'CHESS.EXE').write_bytes((PROJECT.parent/'CHESS.EXE').read_bytes());self.unit=copy.deepcopy(self.units[0]);self.info=copy.deepcopy(self.infos[self.unit['id']]);self.b=self.linked[self.unit['id']];self.es={};self.written={}
  for u in self.units:
   paths=[u['rea_evidence']]
   for k,v in u['extended_extent'].items():
    if k!='kind':paths.extend(v if isinstance(v,list)else[v])
   for p in paths:
    e=json.loads((PROJECT/p).read_text());e.pop('raw_result',None)
    if e['operation']=='analyze_function':e['normalized_result']={k:e['normalized_result'][k]for k in ['procedure','basic_blocks','incoming_references']}
    self.es[p]=e
 def e(self,k):return self.es[self.unit['extended_extent'][k]]
 def select(self,u):self.unit=copy.deepcopy(u);self.info=copy.deepcopy(self.infos[u['id']]);self.b=self.linked[u['id']]
 def validate(self):
  for p,e in self.es.items():
   s=json.dumps(e)
   if self.written.get(p)!=s:q=self.project/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(s);self.written[p]=s
  return validate_keyboard_extent(self.unit,self.project,ORIGINAL_SHA256,self.info,self.b)
 def test_both_full_C_extents_and_actual_context_offsets(self):
  for u,n,f,mz in zip(self.units,[864,131],[79,7],[10,2]):
   self.select(u);p=self.validate();self.assertEqual(p['span_bytes'],n);self.assertEqual(p['compiler_fixups'],f);self.assertEqual(len(p['mz_relocations']),mz);self.assertFalse(p['source_context_alignment_proved'])
 def test_every_linked_byte_and_both_dead_breaks_rejected(self):
  for u in self.units:
   self.select(u);old=self.b
   for a in range(len(old)):
    b=bytearray(old);b[a]^=1;self.b=bytes(b)
    with self.subTest(id=u['id'],a=a),self.assertRaises(ValueError):self.validate()
 def test_every_context_byte_even_if_compiler_agrees_rejected(self):
  n=self.e('raw_span_evidence')['normalized_result'];old=bytes.fromhex(n['bytes_hex'])
  for a in range(len(old)):
   b=bytearray(old);b[a]^=1;n['bytes_hex']=b.hex();self.b=bytes(b[:864])
   with self.subTest(a=a),self.assertRaises(ValueError):self.validate()
 def test_unit_scope_flags_backend_and_source_offset_closed(self):
  old=copy.deepcopy(self.unit)
  for d in [{'id':'other'},{'symbol':'_other'},{'size':862},{'image_offset':'0x1918'},{'flags':['/AS','/Os','/Zi']},{'backend':'msc400-omf'},{'language':'asm'},{'code_address':{'segment':0,'offset':0x1917}},{'owned_data':{}},{'owned_bss':{}}]:
   self.unit=copy.deepcopy(old);self.unit.update(d)
   with self.subTest(d=d),self.assertRaises(ValueError):self.validate()
 def test_evidence_subject_profile_operation_and_distinct_identity(self):
  old=copy.deepcopy(self.es);paths=list(old)
  for p in paths:
   for k in ['subject','operation','digest','load_segment','language_id','target_format','identity']:
    self.es=copy.deepcopy(old);e=self.es[p]
    if k=='subject':e['subject']['digest']['sha256']='0'*64
    elif k=='operation':e['operation']='other'
    elif k=='digest':e['analysis_profile']['digest']='bad'
    elif k=='identity':e['evidence_id']=old[paths[(paths.index(p)+1)%len(paths)]]['evidence_id']
    else:e['analysis_profile']['parameters'][k]='bad'
    # Every observation is used by at least one of the two primary orientations.
    for u in self.units:
     self.select(u)
     with self.subTest(path=p,k=k,id=u['id']),self.assertRaises(ValueError):self.validate()
 def test_raw_query_complete_and_length_required(self):
  old=copy.deepcopy(self.es)
  for k,v in [('address','0x11918'),('complete',False),('requested_bytes',1081),('returned_bytes',1081)]:
   self.es=copy.deepcopy(old);self.e('raw_span_evidence')['normalized_result'][k]=v
   with self.subTest(k=k),self.assertRaises(ValueError):self.validate()
 def test_all_gap_xrefs_must_remain_empty(self):
  for p in self.unit['extended_extent']['gap_xref_evidence']:
   self.es[p]['normalized_result']=[{'source_address':'0x10010','target_address':'0x11c14'}]
   with self.assertRaises(ValueError):self.validate()
   self.es[p]['normalized_result']=[]
 def test_decoders_preserve_unknown_instead_of_fabricated_instruction(self):
  for p in self.unit['extended_extent']['gap_decoder_evidence']:
   self.es[p]['normalized_result']['status']='decoded'
   with self.assertRaises(ValueError):self.validate()
   self.es[p]['normalized_result']['status']='undecodable'
 def test_each_preceding_jump_flow_and_target(self):
  old=copy.deepcopy(self.es)
  for p in self.unit['extended_extent']['preceding_jump_evidence']:
   for k,v in [('kind','fallthrough'),('conditional',True),('computed',True),('direct_destinations',['0x11917'])]:
    self.es=copy.deepcopy(old);self.es[p]['normalized_result']['flow'][k]=v
    with self.subTest(k=k,p=p),self.assertRaises(ValueError):self.validate()
 def test_all_native_bodies_and_closed_CFGs(self):
  old=copy.deepcopy(self.es)
  for p,e in old.items():
   if e['operation']!='analyze_function':continue
   for k,v in [('available',False),('total_bytes',1),('span_bytes',1),('contains_entry',False),('ranges',[])]:
    self.es=copy.deepcopy(old);self.es[p]['normalized_result']['procedure']['body'][k]=v
    with self.subTest(p=p,k=k),self.assertRaises(ValueError):self.validate()
   self.es=copy.deepcopy(old);self.es[p]['normalized_result']['basic_blocks'][0]['successors'].append('0x11c14')
   with self.subTest(p=p),self.assertRaises(ValueError):self.validate()
 def test_incoming_external_interior_entry_rejected(self):
  for u in self.units:
   self.select(u);e=self.es[u['rea_evidence']];e['normalized_result']['incoming_references'].append({'source_address':'0x10010','target_address':hex(0x10000+int(u['image_offset'],0)+4)})
   with self.assertRaises(ValueError):self.validate()
 def test_entire_fresh_codeview_extent_and_reviewed_offset(self):
  for u in self.units:
   self.select(u);old=copy.deepcopy(self.info)
   for k,v in [('symbol','_x'),('boundary','next_public_or_segment_end'),('size',u['size']-2),('end',old['end']+1),('offset',old['offset']+1),('segment',0)]:
    self.info=copy.deepcopy(old);self.info[k]=v
    with self.subTest(id=u['id'],k=k),self.assertRaises(ValueError):self.validate()
 def test_missing_duplicate_or_extra_compiler_field_rejected(self):
  for u in self.units:
   self.select(u);old=copy.deepcopy(self.info)
   for fs in [old['fixups'][:-1],old['fixups']+[old['fixups'][0]],old['fixups'][:-1]+[old['fixups'][0]]]:
    self.info=copy.deepcopy(old);self.info['fixups']=fs
    with self.assertRaises(ValueError):self.validate()
 def test_every_actual_field_width_type_frame_target_and_displacement(self):
  for u in self.units:
   self.select(u);old=copy.deepcopy(self.info)
   for a,f in enumerate(old['fixups']):
    for k,v in [('width',1),('location_type',0),('segment_relative',not f.segment_relative),('frame',(1,1)),('target',(0,1)),('displacement',1),('offset',f.offset+1),('segment',f.segment+1)]:
     self.info=copy.deepcopy(old);self.info['fixups'][a]=dataclasses.replace(f,**{k:v})
     with self.subTest(id=u['id'],a=a,k=k),self.assertRaises(ValueError):self.validate()
 def test_metadata_count_unknown_fields_and_wrong_query_rejected(self):
  old=copy.deepcopy(self.unit)
  self.unit['extended_extent']['extra']=1
  with self.assertRaises(ValueError):self.validate()
  self.unit=copy.deepcopy(old);self.unit['extended_extent']['gap_xref_evidence'].pop()
  with self.assertRaises(ValueError):self.validate()
  self.unit=copy.deepcopy(old);self.e('next_entry_evidence')['parameters']['procedure']='0x11cfb'
  with self.assertRaises(ValueError):self.validate()
 def test_wrong_original_file_and_target_identity_rejected(self):
  with self.assertRaises(ValueError):validate_keyboard_extent(self.unit,self.project,'0'*64,self.info,self.b)
  p=self.project.parent/'CHESS.EXE';b=bytearray(p.read_bytes());b[-1]^=1;p.write_bytes(b)
  with self.assertRaises(ValueError):self.validate()
 def test_production_routes_and_full_fresh_compilation(self):
  from check import build_unit,validate_rea_extent
  from reference import build_reference
  ref=build_reference((PROJECT.parent/'CHESS.EXE').read_bytes());cache={}
  for u in self.units:
   validate_rea_extent(u,PROJECT,ORIGINAL_SHA256,ref);r=build_unit(u,ref['image'],PROJECT,'nasm',c_cache=cache,output=self.project/'compiled',reference=ref);self.assertEqual(r['status'],'c_matched',r);self.assertEqual(r['extended_extent_proof']['span_bytes'],u['size'])
if __name__=='__main__':unittest.main()
