"""Attack the fixed fifteen-entry step872A extent using a real C5 OMF."""
import copy,json,sys,tempfile,unittest
from pathlib import Path
from dataclasses import replace
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P))
from extent import validate_extended_extent
from omf import read_omf
from step_extent import ORIGINAL,CFG

class StepExtentTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.project=Path(self.temp.name)
  self.paths={'body':'evidence/rea_frame_next_1872a.json','raw':'build/command-step-872a/rea-raw.json','next':'evidence/rea-next-source-18834.json'}
  self.paths.update({'xref'+str(i):'build/command-step-872a/rea-xrefs-'+format(0x18812+i,'x')+'.json'for i in range(30)})
  self.e={k:json.loads((P/p).read_text())for k,p in self.paths.items()}
  self.unit={'id':'step_872a','symbol':'_step_872a','language':'c','backend':'msc500-omf','flags':['/AS','/Gs','/Os','/Zi'],'image_offset':'0x872a','size':266,'rea_evidence':self.paths['body'],'extended_extent':{'kind':'step_switch_872a_v1','raw_span_evidence':self.paths['raw'],'next_entry_evidence':self.paths['next'],'table_xref_evidence':[self.paths['xref'+str(i)]for i in range(30)]}}
  self.obj=read_omf((P/'build/command-step-872a/full-context.obj').read_bytes())
  self.emitted=self.obj.function_info('_step_872a');self.linked=bytes.fromhex(self.e['raw']['normalized_result']['bytes_hex'])[:266]
 def validate(self):
  for k,p in self.paths.items():
   path=self.project/p;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(self.e[k]))
  return validate_extended_extent(self.unit,self.project,ORIGINAL,self.emitted,self.linked)
 def mutate_bytes(self,off,val):
  n=self.e['raw']['normalized_result'];b=bytearray.fromhex(n['bytes_hex']);b[off]=val;n['bytes_hex']=b.hex();self.linked=bytes(b[:266])
 def test_real_whole_context_OMF_proves_all_fifteen_words(self):
  p=self.validate();self.assertEqual((p['span_bytes'],p['reachable_body_bytes'],p['table_bytes'],p['compiler_code_fixups'],p['closed_CFG_blocks']),(266,236,30,16,36));self.assertEqual(self.emitted['offset'],358)
 def test_missing_every_table_and_dispatch_fixup_is_rejected(self):
  original=copy.deepcopy(self.emitted)
  for off in [37,*range(232,262,2)]:
   self.emitted=copy.deepcopy(original);self.emitted['fixups']=[f for f in self.emitted['fixups']if f.offset!=358+off]
   with self.subTest(off=off),self.assertRaisesRegex(ValueError,'sixteen'):self.validate()
 def test_wrong_fixup_target_frame_width_mode_segment_and_duplicate(self):
  original=copy.deepcopy(self.emitted);index=next(i for i,f in enumerate(original['fixups'])if f.offset==590)
  for change in [dict(target=(0,2)),dict(frame=(0,2)),dict(width=4),dict(location_type=2),dict(segment_relative=False),dict(segment=2)]:
   self.emitted=copy.deepcopy(original);self.emitted['fixups'][index]=replace(self.emitted['fixups'][index],**change)
   with self.subTest(change=change),self.assertRaises(ValueError):self.validate()
  self.emitted=copy.deepcopy(original);self.emitted['fixups'].append(self.emitted['fixups'][index])
  with self.assertRaisesRegex(ValueError,'duplicate'):self.validate()
 def test_unexpected_overlapping_table_fixup_is_rejected(self):
  f=next(f for f in self.emitted['fixups']if f.offset==590);self.emitted['fixups'].append(replace(f,offset=589))
  with self.assertRaisesRegex(ValueError,'overlapping'):self.validate()
 def test_unlisted_own_CODE_field_and_dispatch_overlap_are_rejected(self):
  original=copy.deepcopy(self.emitted);f=next(f for f in self.emitted['fixups']if f.target==(0,1)and f.segment_relative)
  for offset in [359,394]:
   self.emitted=copy.deepcopy(original);self.emitted['fixups'].append(replace(f,offset=offset))
   with self.subTest(offset=offset),self.assertRaises(ValueError):self.validate()
 def test_agreeing_raw_and_linked_corruptions_cannot_change_fixed_shape(self):
  original=copy.deepcopy(self.e);linked=self.linked
  for off,val in [(21,1),(24,13),(26,0x77),(29,0),(31,0x90),(37,0),(230,0x90),(232,0),(262,0x90),(265,0x90)]:
   self.e=copy.deepcopy(original);self.linked=linked;self.mutate_bytes(off,val)
   with self.subTest(off=off),self.assertRaises(ValueError):self.validate()
 def test_all_exact_closed_CFG_blocks_required(self):
  original=copy.deepcopy(self.e)
  for mode in ['missing','duplicate','wrong_successor','table_code','body_end','wrong_case']:
   self.e=copy.deepcopy(original);b=self.e['body']['normalized_result']['basic_blocks']
   if mode=='missing':b.pop()
   if mode=='duplicate':b.append(copy.deepcopy(b[0]))
   if mode=='wrong_successor':b[0]['successors'].append('0x18812')
   if mode=='table_code':b.append(dict(start='0x18812',end='0x18830',successors=[]))
   if mode=='body_end':b[0]['end']='0x18731'
   if mode=='wrong_case':b[5]['successors'].pop()
   with self.subTest(mode=mode),self.assertRaisesRegex(ValueError,'CFG'):self.validate()
 def test_exact_native_body_ranges_and_counts_required(self):
  original=copy.deepcopy(self.e)
  for key,value in [('total_bytes',266),('span_bytes',236),('non_contiguous',False),('contains_entry',False),('available',False),('ranges',[dict(start='0x1872a',end='0x18833')])]:
   self.e=copy.deepcopy(original);self.e['body']['normalized_result']['procedure']['body'][key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):self.validate()
 def test_one_empty_global_query_per_table_byte_required(self):
  original=copy.deepcopy(self.e)
  for mode in ['reference','duplicate_address','wrong_address','wrong_operation','target','profile']:
   self.e=copy.deepcopy(original);x=self.e['xref0']
   if mode=='reference':x['normalized_result']=['0x1872a']
   if mode=='duplicate_address':x['parameters']['address']='0x18813'
   if mode=='wrong_address':x['parameters']['address']='0x18811'
   if mode=='wrong_operation':x['operation']='read_bytes'
   if mode=='target':x['subject']['digest']['sha256']='0'*64
   if mode=='profile':x['analysis_profile']['digest']='0'*64
   with self.subTest(mode=mode),self.assertRaises(ValueError):self.validate()
 def test_raw_completeness_parameters_identity_and_equality(self):
  original=copy.deepcopy(self.e)
  for mode in ['incomplete','length','address','returned','requested','truncated','mismatch','target','profile']:
   self.e=copy.deepcopy(original);e=self.e['raw'];n=e['normalized_result']
   if mode=='incomplete':n['complete']=False
   if mode=='length':e['parameters']['length']-=1
   if mode=='address':n['address']='0x1872b'
   if mode=='returned':n['returned_bytes']-=1
   if mode=='requested':n['requested_bytes']-=1
   if mode=='truncated':n['bytes_hex']=n['bytes_hex'][:-2]
   if mode=='mismatch':n['bytes_hex']='90'+n['bytes_hex'][2:]
   if mode=='target':e['subject']['digest']['sha256']='0'*64
   if mode=='profile':e['analysis_profile']['digest']='0'*64
   with self.subTest(mode=mode),self.assertRaises(ValueError):self.validate()
 def test_no_sliced_or_inferred_compiler_extent(self):
  original=copy.deepcopy(self.emitted)
  for key,value in [('size',236),('end',624-30),('boundary','next_public_or_segment_end'),('symbol','_other')]:
   self.emitted=copy.deepcopy(original);self.emitted[key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):self.validate()
 def test_exact_native_RET1_and_adjacent_prompt_required(self):
  original=copy.deepcopy(self.e)
  for mode in ['body','address','CFG','raw']:
   self.e=copy.deepcopy(original);n=self.e['next']['normalized_result']
   if mode=='body':n['procedure']['body']['total_bytes']=2
   if mode=='address':n['procedure']['address']='0x18835'
   if mode=='CFG':n['basic_blocks'][0]['successors']=['0x18835']
   if mode=='raw':self.mutate_bytes(266,0x90)
   with self.subTest(mode=mode),self.assertRaises(ValueError):self.validate()
 def test_no_generic_extent_or_compiler_profile_grant(self):
  original=copy.deepcopy(self.unit)
  for key,value in [('size',264),('image_offset','0x872b'),('language','asm'),('symbol','_other'),('backend','msc510-omf'),('flags',['/AS','/Zi'])]:
   self.unit=copy.deepcopy(original);self.unit[key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):self.validate()
  self.unit=copy.deepcopy(original);self.unit['extended_extent']['extra']=True
  with self.assertRaises(ValueError):self.validate()

if __name__=='__main__':unittest.main()
