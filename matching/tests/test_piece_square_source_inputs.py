"""Adopted-module piece-square controls; fixtures are comparison inputs only."""
from pathlib import Path
import copy,json,sys,tempfile,unittest
from unittest.mock import patch
PROJECT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(PROJECT))
import piece_square_source_inputs as profile
import source_inputs
from omf import read_omf
class PieceSquareSourceTests(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  assert Path(profile.__file__).resolve()==PROJECT/'piece_square_source_inputs.py'and Path(source_inputs.__file__).resolve()==PROJECT/'source_inputs.py'
  c.item=next(x for x in json.loads((PROJECT/'config/source-inputs.json').read_text())['source_allocations']if x['backend']==profile.BACKEND);c.raw=(PROJECT/profile.PINS['producer_object']['path']).read_bytes()
 def mutate(self,choose,change):
  out=[];done=False
  for k,at,p in read_omf(self.raw).records:
   if not done and choose(k,p):p=change(p);done=True
   b=bytes([k])+(len(p)+1).to_bytes(2,'little')+p;out.append(b+bytes([-sum(b)&255]))
  self.assertTrue(done);return b''.join(out)
 def test_complete2880_near_shape_and_empty_loaded(self):
  self.assertEqual(profile.validate_object(self.raw)[0]['size'],2880);o=read_omf(self.raw);self.assertFalse(o.publics);self.assertFalse(o.procedures);self.assertTrue(all(not s.length for s in o.segments.values()if s.class_name not in ['DEBSYM','DEBTYP']))
 def test_checksum_rejected(self):
  b=bytearray(self.raw);b[-1]^=1
  with self.assertRaises(ValueError):profile.validate_object(bytes(b))
 def test_last_word_capacity_rejected(self):
  b=self.mutate(lambda k,p:k==0xb0,lambda p:p[:-2]+bytes.fromhex('3e0b'))
  with self.assertRaises(ValueError):profile.validate_object(b)
 def test_complete_array_type_change_rejected(self):
  b=self.mutate(lambda k,p:k==0xa0 and p[0]==6,lambda p:p.replace(bytes.fromhex('7885005a83'),bytes.fromhex('7885002d83'),1))
  with self.assertRaises(ValueError):profile.validate_object(b)
 def test_storage_class_or_registry_extent_rejected(self):
  b=self.mutate(lambda k,p:k==0xb0,lambda p:p.replace(bytes.fromhex('820362'),bytes.fromhex('820361'),1))
  with self.assertRaises(ValueError):profile.validate_object(b)
  x=copy.deepcopy(self.item);x['objects'][0]['storage']='far-common'
  with self.assertRaises(ValueError):profile.validate_item(x)
 def test_wrong_source_fails_before_generation(self):
  with tempfile.TemporaryDirectory()as t:
   q=Path(t);p=q/profile.SOURCE;p.parent.mkdir(parents=True);p.write_text('int piece_square[2][6][119];\n')
   with patch.object(profile,'compile_c',side_effect=AssertionError('must not compile')),self.assertRaises(ValueError):profile.build_input(self.item,q,PROJECT.parent/'CHESS.EXE',q/'out')
 def test_evidence_tamper_rejected(self):
  with tempfile.TemporaryDirectory()as t:
   q=Path(t);p=q/profile.PINS['ownership']['path'];p.parent.mkdir(parents=True);p.write_text('{}\n')
   with self.assertRaises(ValueError):profile.validate_evidence(q,profile.PINS,PROJECT.parent/'CHESS.EXE')
 def test_duplicate_symbol_prevents_generation(self):
  with tempfile.TemporaryDirectory()as t:
   q=Path(t);cfg=q/'inputs.json';cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[self.item]}))
   with patch.object(source_inputs,'compile_c',side_effect=AssertionError('must not compile')),self.assertRaises(ValueError):source_inputs.build_source_inputs(PROJECT,PROJECT.parent/'CHESS.EXE',q/'out',cfg,defined_symbols=['_piece_square'])
 def test_actual_adopted_dispatch_routes_to_profile(self):
  # Routing fixture only; never substitutes for the separately fresh normal build.
  with tempfile.TemporaryDirectory()as t:
   q=Path(t);cfg=q/'inputs.json';cfg.write_text(json.dumps({'schema_version':1,'source_allocations':[self.item]}));sentinel={'definitions':[]}
   with patch.object(profile,'build_input',return_value=sentinel)as route:
    r=source_inputs.build_source_inputs(PROJECT,PROJECT.parent/'CHESS.EXE',q/'out',cfg)
   self.assertIs(r['objects'][0],sentinel);self.assertEqual(route.call_count,1);self.assertIs(route.call_args.kwargs['compiler_fn'],source_inputs.compile_c)
