"""Real352B positive and pure integrity/type/dispatch negatives. Never compiles."""
from pathlib import Path
import sys,json,copy,tempfile,importlib.util,unittest
from unittest.mock import patch
I=Path(__file__).resolve().parents[1];BASE=next(p for p in Path(__file__).resolve().parents if(p/'config/target.json').is_file());sys.path[:0]=[str(I),str(BASE)]
import square_coordinate_pointers_source_inputs as s
from omf import read_omf,OMFError
RAW=(I/'tests/fixtures/square_coordinate_pointers/actual.obj').read_bytes()
def item():return{'id':'square-coordinate-pointers-common','backend':s.BACKEND,'source':s.SOURCE,'source_sha256':s.SOURCE_SHA,'compiler':'msc500','flags':s.FLAGS[:],'toolchain_manifest_sha256':s.MANIFEST_SHA,'objects':[{'symbol':n,'size':2,'storage':'near-common'}for n in s.NAMES],'evidence':copy.deepcopy(s.PINS)}
class ObjectIntegrity(unittest.TestCase):
 def test_actual352whole_positive(self):self.assertEqual([(d['symbol'],d['type_index'],d['datatype'],d['size'])for d in s.validate_object(RAW)],[('_square_x',515,98,2),('_square_y',161,98,2)])
 def test_wrong_checksum_rejected(self):
  b=bytearray(RAW);b[-1]^=1
  with self.assertRaises((ValueError,OMFError)):s.validate_object(bytes(b))
 def test_truncated_or_appended_object_rejected(self):
  for b in[RAW[:-1],RAW+b'\0']:
   with self.assertRaises((ValueError,OMFError)):s.validate_object(b)
 def test_row9_complete_graph_positive(self):self.assertEqual(s.graph({515:bytes.fromhex('7a748304028200'),516:bytes.fromhex('78859000838100')},515),s.EXPECTED['_square_x'])
 def test_wrong_row_element_extent_pointer_kind_rejected(self):
  for ptr,arr in[('7a758304028200','78859000838100'),('7a748304028200','78858000838100'),('7a748304028200','78859000838000'),('7a74830402820000','78859000838100')]:
   with self.assertRaises(ValueError):s.graph({515:bytes.fromhex(ptr),516:bytes.fromhex(arr)},515)
 def test_missing_or_cyclic_graph_rejected(self):
  for ts in[{}, {515:bytes.fromhex('7a748303028200')}]:
   with self.assertRaises(ValueError):s.graph(ts,515)
 def test_far_pointer_or_integer_builtin_rejected(self):
  for typ in[0x81,0xc1]:
   with self.assertRaises(ValueError):s.graph({},typ)
 def test_parsed_loaded_BSS_or_PUBLIC_rejected(self):
  a=copy.deepcopy(read_omf(RAW));a.segments[4].length=1
  with self.assertRaises(ValueError):s.validate_provider_structure(a)
  a=copy.deepcopy(read_omf(RAW));a.publics['_square_x']=None
  with self.assertRaises(ValueError):s.validate_provider_structure(a)
 def test_parsed_COMMON_size_not_pointer_width_rejected(self):
  o=copy.deepcopy(read_omf(RAW));o.records=[(k,at,p[:-1]+b'\x04'if k==0xb0 else p)for k,at,p in o.records]
  with self.assertRaises(ValueError):s.validate_provider_structure(o)
 def test_missing_or_extra_debug_FAR_rejected(self):
  for mode in['missing','extra']:
   o=copy.deepcopy(read_omf(RAW));o.fixups=o.fixups[:-1]if mode=='missing'else o.fixups+[o.fixups[0]]
   with self.assertRaises(ValueError):s.validate_provider_structure(o)
class SourceEvidence(unittest.TestCase):
 def test_exact_item_positive(self):s.validate_item(item())
 def test_wrong_source_flags_id_or_storage_rejected(self):
  for key,value in[('source','src/link/other.c'),('source_sha256','0'*64),('id','other'),('flags',['/AS']),('compiler','msc600'),('objects',[{'symbol':'_square_x','size':4,'storage':'far-common'}])]:
   x=item();x[key]=value
   with self.assertRaises(ValueError):s.validate_item(x)
 def test_wrong_evidence_selection_rejected_before_reads(self):
  p=copy.deepcopy(s.PINS);p['producer_object']['sha256']='0'*64
  with self.assertRaises(ValueError):s.validate_evidence(I,p,BASE.parent/'CHESS.EXE')
 def test_owned_evidence_and_native_DATA8_positive(self):self.assertEqual(len(s.validate_evidence(I,s.PINS,BASE.parent/'CHESS.EXE')),2)
 def test_owned_file_corruption_rejected(self):
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp)
   for row in s.PINS.values():
    p=root/row['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((I/row['path']).read_bytes())
   p=root/s.PINS['producer_object']['path'];p.write_bytes(p.read_bytes()[:-1]+b'\0')
   with self.assertRaises(ValueError):s.validate_evidence(root,s.PINS,BASE.parent/'CHESS.EXE')
class Routing(unittest.TestCase):
 def setUp(self):
  spec=importlib.util.spec_from_file_location('square_candidate_dispatch',I/'source_inputs.py');self.dispatch=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.dispatch)
 def call(self,rows,defined=()):
  with tempfile.TemporaryDirectory()as tmp:
   p=Path(tmp)/'inputs.json';p.write_text(json.dumps({'schema_version':1,'source_allocations':rows}));return self.dispatch.build_source_inputs(BASE,BASE.parent/'CHESS.EXE',Path(tmp)/'out',config_path=p,defined_symbols=defined)
 def test_existing_named_definition_rejected_before_backend(self):
  with patch.object(s,'build_input',side_effect=AssertionError('backend mustnotrun'))as fn:
   with self.assertRaises(ValueError):self.call([item()],['_square_y'])
   self.assertEqual(fn.call_count,0)
 def test_duplicate_id_source_symbol_rejected_before_second_route(self):
  # Fixture-only route stub, never a fakefreshcompiler/provenance claim.
  with patch.object(s,'build_input',return_value={'fixture_routing_only':True})as fn:
   with self.assertRaises(ValueError):self.call([item(),item()])
   self.assertEqual(fn.call_count,1)
 def test_unknown_backend_rejected_without_compile(self):
  x=item();x['backend']='msc500-near-common-square-coordinate-pointers-v99'
  with patch.object(self.dispatch,'compile_c',side_effect=AssertionError('nocompiler')):
   with self.assertRaises(ValueError):self.call([x])
if __name__=='__main__':unittest.main()
