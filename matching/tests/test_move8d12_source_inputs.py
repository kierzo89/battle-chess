"""Permanent proposal: strict logical Move8 profile; no compiler or target reads.
Fixture OBJ is an unchanged genuine ordinary-route output, comparison only.
"""
from pathlib import Path
import copy,hashlib,json,tempfile,unittest
from unittest.mock import patch
import move8d12_source_inputs as p
import source_inputs as dispatch
F=Path(__file__).resolve().parent/'fixtures/move8d12'

def raw():return (F/'provider.obj').read_bytes()
def item():return {'id':'move8-state-common','backend':p.BACKEND,'source':p.SOURCE,'source_sha256':p.SOURCE_SHA,'compiler':'msc500','flags':p.FLAGS[:],'toolchain_manifest_sha256':p.MANIFEST_SHA,'objects':[{'symbol':'_state_8d12','size':8,'storage':'near-common'}],'evidence':copy.deepcopy(p.PINS)}
def change_record(data,kind,change):
 out=bytearray();at=0;done=False
 while at<len(data):
  k=data[at];n=int.from_bytes(data[at+1:at+3],'little');payload=data[at+3:at+2+n]
  if k==kind and not done:payload=change(payload);done=True
  prefix=bytes([k])+(len(payload)+1).to_bytes(2,'little')+payload;out.extend(prefix+bytes([(-sum(prefix))&255]));at+=n+3
 assert done and at==len(data);return bytes(out)
def alter_type(data,index,change):
 # Preserve record lengths and checksums; challenge semantic CV, not corruption.
 def body(v):
  if v[0]!=6:return v
  b=bytearray(v);at=3;ix=512
  while at<len(b):
   n=int.from_bytes(b[at+1:at+3],'little')
   if ix==index:b[at+3:at+3+n]=change(bytes(b[at+3:at+3+n]));return bytes(b)
   at+=3+n;ix+=1
  raise AssertionError('missing type')
 # Locate the DEBTYP LEDATA explicitly; earlier LEDATA records are unchanged.
 out=bytearray();at=0;done=False
 while at<len(data):
  k=data[at];n=int.from_bytes(data[at+1:at+3],'little');v=data[at+3:at+2+n]
  if k==0xa0 and v[0]==6:v=body(v);done=True
  prefix=bytes([k])+(len(v)+1).to_bytes(2,'little')+v;out.extend(prefix+bytes([(-sum(prefix))&255]));at+=n+3
 assert done;return bytes(out)
class Move8ProfileTests(unittest.TestCase):
 def rejected(self,b):
  with self.assertRaises(ValueError):p.validate_object(b)
 def test_genuine_whole_object(self):self.assertEqual(p.sha(raw()),p.OBJECT_SHA);p.validate_object(raw())
 def test_genuine_source(self):self.assertEqual(p.sha((F/'provider.c').read_bytes()),p.SOURCE_SHA)
 def test_single_near_eight(self):self.assertEqual(p.validate_object(raw()),[{'symbol':'_state_8d12','type_index':522,'datatype':98,'size':8}])
 def test_empty_loaded_no_publics(self):
  o=p.read_omf(raw());self.assertFalse(o.publics or o.procedures);self.assertEqual([s.length for s in o.segments.values()if s.class_name in ['CODE','DATA','CONST','BSS']],[0]*4)
 def test_debug_far_is_not_runtime_pointer(self):
  o=p.read_omf(raw());self.assertEqual([(f.segment,f.offset,f.width)for f in o.fixups],[(5,2,4)]);self.assertEqual(p.graph(p.types(o),522),p.EXPECTED_GRAPH)
 def test_complete_nine_record_graph(self):
  seen=set();self.assertEqual(p.graph(p.types(p.read_omf(raw())),522,seen),p.EXPECTED_GRAPH);self.assertEqual(len(seen),9)
 def test_checksum_corruption(self):
  b=bytearray(raw());b[4]^=1;self.rejected(bytes(b))
 def test_rechecksummed_wrong_extent(self):self.rejected(change_record(raw(),0xb0,lambda b:b[:-1]+bytes([10])))
 def test_rechecksummed_wrong_storage_class(self):self.rejected(change_record(raw(),0xb0,lambda b:b[:-2]+bytes([0x61])+b[-1:]))
 def test_rechecksummed_pointer_instead_of_value(self):self.rejected(alter_type(raw(),522,lambda b:bytes([0x7a])+b[1:]))
 def test_rechecksummed_wrong_composite_bits(self):self.rejected(alter_type(raw(),522,lambda b:b[:1]+bytes([56])+b[2:]))
 def test_reachable_types_unknown_leaf(self):
  ts=p.types(p.read_omf(raw()));seen=set();p.graph(ts,522,seen)
  for index in seen:
   with self.subTest(index=index):self.rejected(alter_type(raw(),index,lambda b:bytes([0])+b[1:]))
 def test_rechecksummed_wrong_signedness(self):self.rejected(alter_type(raw(),523,lambda b:b[:2]+bytes([0x85])+b[3:]))
 def test_rechecksummed_wrong_detail_offset(self):self.rejected(alter_type(raw(),524,lambda b:b[:-1]+bytes([5])))
 def test_rechecksummed_union_byte_overlap(self):self.rejected(alter_type(raw(),517,lambda b:b[:-1]+bytes([0])))
 def test_missing_graph_record(self):
  ts=p.types(p.read_omf(raw()));del ts[522]
  with self.assertRaises(ValueError):p.graph(ts,522)
 def test_cyclic_graph(self):
  ts=p.types(p.read_omf(raw()));ts[522]=bytes.fromhex('794004830a02831802820069')
  with self.assertRaises(ValueError):p.graph(ts,522)
 def test_wrong_source_path(self):
  x=item();x['source']='src/link/other.c'
  with self.assertRaises(ValueError):p.validate_item(x)
 def test_wrong_source_digest(self):
  x=item();x['source_sha256']='0'*64
  with self.assertRaises(ValueError):p.validate_item(x)
 def test_wrong_flags(self):
  x=item();x['flags']=['/AS','/Zi']
  with self.assertRaises(ValueError):p.validate_item(x)
 def test_unknown_profile_field(self):
  x=item();x['waive_native']=True
  with self.assertRaises(ValueError):p.validate_item(x)
 def test_wrong_evidence_before_target_or_compiler(self):
  pins=copy.deepcopy(p.PINS);pins['identity']['sha256']='0'*64
  with patch.object(p,'compile_c',side_effect=AssertionError('compiler forbidden')),patch.object(Path,'read_bytes',side_effect=AssertionError('target forbidden')):
   with self.assertRaises(ValueError):p.validate_evidence(Path('.'),pins,Path('CHESS.EXE'))
 def test_wrong_declaration(self):
  x=item();x['objects'][0]['symbol']='_candidate_move'
  with self.assertRaises(ValueError):p.validate_item(x)
 def route(self,rows,defined=()):
  calls=[]
  def stub(x,*a,**kw):
   p.validate_item(x);calls.append(x['id']);self.assertIs(kw['compiler_fn'],dispatch.compile_c)
   return {'id':x['id'],'source':x['source'],'object':'INERT-not-OBJ','object_sha256':p.OBJECT_SHA,'definitions':[{'symbol':'_state_8d12','size':8}],'matching_credit':0}
  with tempfile.TemporaryDirectory()as t,patch.object(p,'build_input',side_effect=stub),patch.object(dispatch,'compile_c',side_effect=AssertionError('compiler forbidden')):
   cfg=Path(t)/'cfg.json';cfg.write_text(json.dumps({'schema_version':1,'source_allocations':rows}))
   try:return dispatch.build_source_inputs(Path(t),Path(t)/'CHESS.EXE',Path(t)/'out',cfg,defined_symbols=defined),calls
   finally:self.last_calls=calls
 def test_dispatch_positive_no_compiler(self):self.assertEqual(self.route([item()])[1],['move8-state-common'])
 def test_dispatch_duplicate_id_source(self):
  with self.assertRaises(ValueError):self.route([item(),item()])
  self.assertEqual(self.last_calls,['move8-state-common'])
 def test_dispatch_preexisting_symbol(self):
  with self.assertRaises(ValueError):self.route([item()],['_state_8d12'])
  self.assertEqual(self.last_calls,[])
 def test_closed_ordinary_provenance_and_logical_boundary(self):
  r=json.loads((F/'ordinary-result.json').read_text());g=json.loads((F/'ordinary-guard.json').read_text());b=json.loads((F/'range-proof.json').read_text())
  self.assertEqual(r['objects'][0]['object_sha256'],p.OBJECT_SHA);self.assertEqual(g['actual_calls'],1);self.assertEqual(len(g['blocked_reads']),3);self.assertTrue(g['comparison_reads_separate']);self.assertEqual(b['logical_range'],[0x8d12,0x8d1a]);self.assertEqual(b['following_values'],[0x8d1a,0x8d22]);self.assertTrue(all(not(a<0x8d1a and z>0x8d12)for a,z,n in b['future26_near_ranges']))
if __name__=='__main__':unittest.main()
