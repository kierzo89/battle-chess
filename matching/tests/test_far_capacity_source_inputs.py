"""Adopted-module conditional FAR model controls; no compiler/LINK execution."""
from pathlib import Path
import copy,json,sys,tempfile,unittest
from unittest.mock import patch
PROJECT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(PROJECT))
import far_capacity_source_inputs as profile
import source_inputs
from omf import read_omf
class FarCapacitySourceTests(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  assert Path(profile.__file__).resolve()==PROJECT/'far_capacity_source_inputs.py'and Path(source_inputs.__file__).resolve()==PROJECT/'source_inputs.py'
  c.item=next(x for x in json.loads((PROJECT/'config/source-inputs.json').read_text())['source_allocations']if x['backend']==profile.BACKEND);c.raw=(PROJECT/profile.PINS['producer_object']['path']).read_bytes()
 def mutate(self,choose,change):
  out=[];done=False
  for k,at,p in read_omf(self.raw).records:
   if not done and choose(k,p):p=change(p);done=True
   b=bytes([k])+(len(p)+1).to_bytes(2,'little')+p;out.append(b+bytes([-sum(b)&255]))
  self.assertTrue(done);return b''.join(out)
 def test_actual_far61_counts_times_one(self):
  d=profile.validate_object(self.raw);self.assertEqual([(x['communal_kind'],x['element_count'],x['element_bytes'],x['size'])for x in d],[(0x61,70000,1,70000),(0x61,150000,1,150000)])
 def test_checksum_rejected(self):
  b=bytearray(self.raw);b[-1]^=1
  with self.assertRaises(ValueError):profile.validate_object(bytes(b))
 def test_count_or_element_width_rejected(self):
  for old,new in [('84701101','846f1101'),('8470110101','8470110102')]:
   b=self.mutate(lambda k,p:k==0xb0,lambda p:p.replace(bytes.fromhex(old),bytes.fromhex(new),1))
   with self.assertRaises(ValueError):profile.validate_object(b)
 def test_array_type_or_near_storage_rejected(self):
  for choose,change in [(lambda k,p:k==0xa0 and p[0]==6,lambda p:p.replace(bytes.fromhex('86808b0800'),bytes.fromhex('86788b0800'),1)),(lambda k,p:k==0xb0,lambda p:p.replace(bytes.fromhex('820361'),bytes.fromhex('820362'),1))]:
   with self.assertRaises(ValueError):profile.validate_object(self.mutate(choose,change))
 def test_duplicate_symbol_rejected_before_generation(self):
  with tempfile.TemporaryDirectory()as t:
   q=Path(t);cfg=q/'inputs.json';cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[self.item]}))
   with patch.object(source_inputs,'compile_c',side_effect=AssertionError('must not compile')),self.assertRaises(ValueError):source_inputs.build_source_inputs(PROJECT,PROJECT.parent/'CHESS.EXE',q/'out',cfg,defined_symbols=['_asset_buffer'])
 def test_evidence_tamper_rejected(self):
  with tempfile.TemporaryDirectory()as t:
   q=Path(t);p=q/profile.PINS['model']['path'];p.parent.mkdir(parents=True);p.write_text('{}\n')
   with self.assertRaises(ValueError):profile.validate_evidence(q,profile.PINS,PROJECT.parent/'CHESS.EXE')
 def test_explicit_near_far_accounting_and_report(self):
  far={'id':'far','source':'f.c','object':'f.obj','object_sha256':'fixture','COMMON_kind':'far','definitions':profile.validate_object(self.raw)};near={'id':'near','source':'n.c','object':'n.obj','object_sha256':'fixture','definitions':[{'symbol':'_one','size':2}]};totals=source_inputs.COMMON_totals([near,far]);self.assertEqual(totals,{'near':{'contributions':1,'definitions':1,'bytes':2},'far':{'contributions':1,'definitions':2,'bytes':220000}});r=source_inputs.report_inputs({'objects':[near,far],'COMMON_totals':totals});self.assertEqual(r[0]['definitions'][0]['communal_kind'],0x62);self.assertEqual(r[1]['definitions'][0]['element_count'],70000);self.assertTrue(r[1]['conditional_native_capacity_model'])
  bad=copy.deepcopy(far);bad['definitions'][0]['element_bytes']=2
  with self.assertRaises(ValueError):source_inputs.COMMON_totals([bad])
 def test_old_near_only_report_and_unknown_kind(self):
  row={'id':'n','source':'n.c','object':'n.obj','object_sha256':'fixture','definitions':[{'symbol':'_one','size':2}]};self.assertEqual(source_inputs.report_inputs({'objects':[row]}),[row]);bad=copy.deepcopy(row);bad['definitions'][0]['communal_kind']=0x60
  with self.assertRaises(ValueError):source_inputs.COMMON_totals([bad])
 def test_actual_adopted_dispatch_routes_to_far_profile(self):
  # Routing fixture only, not an object/compiler cache or source-generation result.
  with tempfile.TemporaryDirectory()as t:
   q=Path(t);cfg=q/'inputs.json';cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[self.item]}));sentinel={'COMMON_kind':'far','definitions':profile.validate_object(self.raw)}
   with patch.object(profile,'build_input',return_value=sentinel)as route:r=source_inputs.build_source_inputs(PROJECT,PROJECT.parent/'CHESS.EXE',q/'out',cfg)
   self.assertIs(r['objects'][0],sentinel);self.assertEqual(route.call_count,1);self.assertEqual(r['COMMON_totals']['far']['definitions'],2);self.assertIs(route.call_args.kwargs['compiler_fn'],source_inputs.compile_c)
