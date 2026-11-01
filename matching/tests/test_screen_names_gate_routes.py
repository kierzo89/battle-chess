"""Prepared gate controls use untouched actual objects, no compilation."""
from pathlib import Path
import copy,hashlib,json,os,sys,unittest
M=Path(os.environ.get('BC_SCREEN_POINTER_PROJECT',Path(__file__).resolve().parents[1])).resolve();sys.path.insert(0,str(M));sys.dont_write_bytecode=True
from omf import read_omf
from link16 import link_function
from reference import ORIGINAL_SHA256
from extent import validate_extended_extent
import input_wait_extent,board_action_extent,input_wait_extent_screen_names,board_action_extent_screen_names
F=Path(__file__).resolve().parent/'fixtures/screen_coordinate_pointers'
BEFORE=json.loads((F/'metadata-before.json').read_text());AFTER=json.loads((F/'metadata-v2.json').read_text());OLD=read_omf((F/'context-old.obj').read_bytes());NEW=read_omf((F/'context-new.obj').read_bytes())
class ScreenNamesGateRouteTests(unittest.TestCase):
 def rows(self,ident):return next(x for x in BEFORE if x['id']==ident),next(x for x in AFTER if x['id']==ident)
 def validate(self,row,obj,fn):
  body,_=link_function(obj,row['symbol'],int(row['image_offset'],0),row['externals']);return fn(row,M,ORIGINAL_SHA256,obj.function_info(row['symbol']),body,source_object=obj)
 def test_old_kind_old_object_preserved(self):
  for ident in ['input_wait_1da9','board_action_20d5']:
   a,b=self.rows(ident);self.assertEqual(self.validate(a,OLD,validate_extended_extent)['kind'],a['extended_extent']['kind'])
 def test_new_kind_actual_new_object(self):
  for ident in ['input_wait_1da9','board_action_20d5']:
   a,b=self.rows(ident);self.assertEqual(self.validate(b,NEW,validate_extended_extent)['kind'],b['extended_extent']['kind'])
 def test_old_kind_actual_new_object_rejected(self):
  for ident in ['input_wait_1da9','board_action_20d5']:
   a,b=self.rows(ident);b=copy.deepcopy(b);b['extended_extent']['kind']=a['extended_extent']['kind']
   with self.assertRaisesRegex(ValueError,'actual compiler field ownership'):self.validate(b,NEW,validate_extended_extent)
 def test_new_kind_old_object_rejected(self):
  for ident in ['input_wait_1da9','board_action_20d5']:
   a,b=self.rows(ident);a=copy.deepcopy(a);a['extended_extent']['kind']=b['extended_extent']['kind']
   with self.assertRaisesRegex(ValueError,'actual compiler field ownership'):self.validate(a,OLD,validate_extended_extent)
 def test_cross_kind_identity_rejected(self):
  a,b=self.rows('input_wait_1da9');b=copy.deepcopy(b);b['extended_extent']['kind']='board_action_screen_names_20d5_v2'
  with self.assertRaises(ValueError):self.validate(b,NEW,validate_extended_extent)
 def test_missing_actual_object_rejected(self):
  a,b=self.rows('input_wait_1da9');body,_=link_function(NEW,b['symbol'],int(b['image_offset'],0),b['externals'])
  with self.assertRaises(ValueError):validate_extended_extent(b,M,ORIGINAL_SHA256,NEW.function_info(b['symbol']),body,source_object=None)
 def test_actual_code_mutation_rejected(self):
  a,b=self.rows('input_wait_1da9');body,_=link_function(NEW,b['symbol'],int(b['image_offset'],0),b['externals']);body=bytes([body[0]^1])+body[1:]
  with self.assertRaises(ValueError):validate_extended_extent(b,M,ORIGINAL_SHA256,NEW.function_info(b['symbol']),body,source_object=NEW)
 def test_unknown_kind_rejected(self):
  a,b=self.rows('input_wait_1da9');b=copy.deepcopy(b);b['extended_extent']['kind']='input_wait_screen_names_1da9_v3'
  with self.assertRaises(ValueError):self.validate(b,NEW,validate_extended_extent)
if __name__=='__main__':unittest.main()
