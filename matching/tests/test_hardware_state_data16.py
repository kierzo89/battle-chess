from pathlib import Path
import sys,unittest,copy,dataclasses,json
M=next(p for p in Path(__file__).resolve().parents if(p/'config/msc500.json').is_file());sys.path[:0]=[str(Path(__file__).resolve().parent),str(M)]
import hardware_state_data16 as p
if Path(__file__).resolve().parent.name=='tests':assert Path(p.__file__).resolve()==M/'hardware_state_data16.py'
from omf import read_omf,Public
D=M/'build/platform-data-2eae'
class HardwareDataTests(unittest.TestCase):
 def setUp(self):self.raw=(D/'platform_state_grouped.obj').read_bytes();self.obj=read_omf(self.raw)
 def reject(self,o):
  with self.assertRaises(p.HardwareDataError):p.validate_object(o)
 def test_complete12_and_five_real_GROUP_publics(self):
  data,meta=p.extract_data(self.raw);self.assertEqual(data,b'\0'*12);self.assertEqual([x['offset']for x in meta['publics']],[0,1,5,7,11]);self.assertEqual(meta['authored_c_credit'],0)
 def test_semantic_initializer_same_profile_actual_difference(self):
  wrong,_=p.extract_data((D/'wrong_speed_grouped.obj').read_bytes());self.assertEqual([i for i,(a,b)in enumerate(zip(wrong,b'\0'*12))if a!=b],[5])
 def test_wrong_checksum_or_unreviewed_object(self):
  for raw in [self.raw[:-1],self.raw+b'\0',self.raw[:-1]+bytes([self.raw[-1]^1])]:
   with self.subTest(raw=raw[-4:]),self.assertRaises(p.HardwareDataError):p.extract_data(raw)
 def test_no_extra_SEGDEF(self):
  o=copy.deepcopy(self.obj);o.segments[2]=copy.deepcopy(o.segments[1]);self.reject(o)
 def test_exact_SEGDEF_shape(self):
  for k,v in [('length',11),('length',13),('name','OTHER'),('class_name','CODE'),('attributes',0x28),('unsupported_data',True),('name_index',3),('overlay_index',0)]:
   o=copy.deepcopy(self.obj);setattr(o.segments[1],k,v)
   with self.subTest(k=k,v=v):self.reject(o)
 def test_no_undefined_or_alias_publics(self):
  for change in ['remove','extra','offset','group','segment','type']:
   o=copy.deepcopy(self.obj);name='_saved_timer_vector_2eaf';q=o.publics[name]
   if change=='remove':del o.publics[name]
   elif change=='extra':o.publics['_extra']=Public('_extra',1,0,1,0)
   else:o.publics[name]=dataclasses.replace(q,**{dict(offset='offset',group='group',segment='segment',type='type_index')[change]:0 if change in ['offset','group']else 2})
   with self.subTest(change=change):self.reject(o)
 def test_no_holes_overlap_or_extra_tail(self):
  for chunks in [[(1,b'\0'*11)],[(0,b'\0'*11)],[(0,b'\0'*13)],[(0,b'\0'*6),(5,b'\0'*7)],[(0,b'')]]:
   o=copy.deepcopy(self.obj);o.segments[1].chunks=chunks
   with self.subTest(chunks=chunks):self.reject(o)
 def test_no_extra_records_LIDATA_COMMON_debug_or_fixups(self):
  for kind in [0xa2,0xb0,0xb8,0x9c,0x88]:
   o=copy.deepcopy(self.obj);o.records.append((kind,0,b''))
   with self.subTest(kind=kind):self.reject(o)
  o=copy.deepcopy(self.obj);o.externals[1]='_extra';self.reject(o)
  o=copy.deepcopy(self.obj);o.procedures['_fake']={};self.reject(o)
 def test_group_and_header_mutation(self):
  for kind in [0x80,0x9a,0x88,0x8a]:
   o=copy.deepcopy(self.obj);o.records=[(k,a,b'\xff')if k==kind else(k,a,b)for k,a,b in o.records]
   with self.subTest(kind=kind):self.reject(o)
 def test_initial_group0_control_is_rejected(self):
  with self.assertRaises(p.HardwareDataError):p.validate_object(read_omf((D/'platform_state.obj').read_bytes()))
 def test_exact_unit_keys_and_source_tool_placement_pins(self):
  u=json.loads((D/'proposed-unit.json').read_text());p.validate_unit(u)
  for key,value in [('size',11),('image_offset','0x5facf'),('source_sha256','0'*64),('assembler_sha256','0'*64),('reference_region','unchanged-prefix'),('symbols',list(reversed(u['symbols']))),('source','unreviewed.asm'),('extra',1)]:
   v=dict(u);v[key]=value
   with self.subTest(key=key),self.assertRaises(p.HardwareDataError):p.validate_unit(v)
 def test_existing_generic_ASM_DATA_policy_remains_strict(self):
  import asm_data16
  with self.assertRaises(ValueError):asm_data16.extract_data(self.obj,list(p.PUBLICS))
if __name__=='__main__':unittest.main()
