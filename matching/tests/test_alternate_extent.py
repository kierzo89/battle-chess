"""Fixed alternate-view extent proof attacks using the actual whole756 OMF."""
import copy,json,sys,tempfile,unittest
from pathlib import Path
from dataclasses import replace
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P))
from extent import validate_extended_extent
from omf import read_omf
from alternate_extent import ORIGINAL

class AlternateExtentTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.project=Path(self.temp.name)
  self.paths=dict(body='evidence/rea-alternate-view-17e6b.json',raw='evidence/rea-alternate-view-17e6b-raw.json',next='evidence/rea-alternate-view-next.json',xrefs='evidence/rea-alternate-view-table-xrefs.json')
  self.e={k:json.loads((P/p).read_text())for k,p in self.paths.items()}
  self.unit=dict(id='alternate_view_7e6b',symbol='_alternate_view',language='c',backend='msc500-omf',flags=['/AS','/Gs','/Os','/Zi'],image_offset='0x7e6b',size=431,rea_evidence=self.paths['body'],extended_extent=dict(kind='alternate_view_switch_7e6b_v1',raw_span_evidence=self.paths['raw'],next_entry_evidence=self.paths['next'],table_xref_evidence=self.paths['xrefs']))
  self.obj=read_omf((P/'build/alternate-view-review/typed_cell_caller.obj').read_bytes());self.emitted=self.obj.function_info('_alternate_view');self.linked=bytes.fromhex(self.e['raw']['normalized_result']['bytes_hex'])[:431]
 def validate(self):
  for k,p in self.paths.items():
   q=self.project/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(self.e[k]))
  return validate_extended_extent(self.unit,self.project,ORIGINAL,self.emitted,self.linked)
 def mutate_bytes(self,offset,value):
  n=self.e['raw']['normalized_result'];b=bytearray.fromhex(n['bytes_hex']);b[offset]=value;n['bytes_hex']=b.hex();self.linked=bytes(b[:431])
 def test_actual756_object_proves_complete431_and_eighteen_words(self):
  p=self.validate();self.assertEqual((self.emitted['offset'],p['span_bytes'],p['reachable_body_bytes'],p['table_bytes'],p['compiler_code_fixups'],p['closed_CFG_blocks']),(325,431,395,36,19,29))
 def test_all_nineteen_real_CODE_fixups_required(self):
  original=copy.deepcopy(self.emitted)
  for off in [33,*range(386,422,2)]:
   self.emitted=copy.deepcopy(original);self.emitted['fixups']=[f for f in self.emitted['fixups']if f.offset!=325+off]
   with self.subTest(off=off),self.assertRaisesRegex(ValueError,'all19'):self.validate()
 def test_target_frame_width_segment_mode_and_duplicate_attacks(self):
  original=copy.deepcopy(self.emitted);i=next(i for i,f in enumerate(original['fixups'])if f.offset==711)
  for change in [dict(target=(0,2)),dict(frame=(0,2)),dict(width=4),dict(location_type=2),dict(segment_relative=False),dict(segment=2)]:
   self.emitted=copy.deepcopy(original);self.emitted['fixups'][i]=replace(self.emitted['fixups'][i],**change)
   with self.subTest(change=change),self.assertRaises(ValueError):self.validate()
  self.emitted=copy.deepcopy(original);self.emitted['fixups'].append(self.emitted['fixups'][i])
  with self.assertRaisesRegex(ValueError,'duplicate'):self.validate()
 def test_overlapping_unlisted_table_fixup_rejected(self):
  f=next(f for f in self.emitted['fixups']if f.offset==711);self.emitted['fixups'].append(replace(f,offset=710))
  with self.assertRaisesRegex(ValueError,'overlapping'):self.validate()
 def test_unlisted_own_CODE_field_and_dispatch_overlap_are_rejected(self):
  original=copy.deepcopy(self.emitted);f=next(f for f in self.emitted['fixups']if f.target==(0,1)and f.segment_relative)
  for offset in [326,357]:
   self.emitted=copy.deepcopy(original);self.emitted['fixups'].append(replace(f,offset=offset))
   with self.subTest(offset=offset),self.assertRaises(ValueError):self.validate()
 def test_agreeing_bytes_cannot_change_bound_default_dispatch_table_or_tail(self):
  original=copy.deepcopy(self.e);linked=self.linked
  for off,value in [(0,0x90),(20,2),(23,16),(25,0x76),(26,0),(27,0x90),(33,0),(384,0x90),(386,0),(422,0x90),(430,0x90)]:
   self.e=copy.deepcopy(original);self.linked=linked;self.mutate_bytes(off,value)
   with self.subTest(off=off),self.assertRaises(ValueError):self.validate()
 def test_all_closed_CFG_blocks_and_case_targets_required(self):
  original=copy.deepcopy(self.e)
  for mode in ['missing','duplicate','table','entry_in_table','case','block_end']:
   self.e=copy.deepcopy(original);b=self.e['body']['normalized_result']['basic_blocks']
   if mode=='missing':b.pop()
   if mode=='duplicate':b.append(copy.deepcopy(b[0]))
   if mode=='table':b.append(dict(start='0x17fed',end='0x18011',successors=[]))
   if mode=='entry_in_table':b[0]['successors'].append('0x17fed')
   if mode=='case':b[2]['successors'].pop()
   if mode=='block_end':b[0]['end']='0x17e85'
   with self.subTest(mode=mode),self.assertRaisesRegex(ValueError,'CFG'):self.validate()
 def test_exact_native_body_ranges_and_reachable_byte_counts(self):
  original=copy.deepcopy(self.e)
  for key,value in [('total_bytes',431),('span_bytes',395),('non_contiguous',False),('contains_entry',False),('available',False),('ranges',[dict(start='0x17e6b',end='0x18019')])]:
   self.e=copy.deepcopy(original);self.e['body']['normalized_result']['procedure']['body'][key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):self.validate()
 def test_xref_bundle_identity_completeness_and_unique_addresses(self):
  original=copy.deepcopy(self.e)
  for mode in ['missing','duplicate','nonempty','address','target','operation','profile','load_profile']:
   self.e=copy.deepcopy(original);xs=self.e['xrefs'];x=xs[0]
   if mode=='missing':xs.pop()
   if mode=='duplicate':xs[0]=copy.deepcopy(xs[1])
   if mode=='nonempty':x['normalized_result']=['0x17e6b']
   if mode=='address':x['parameters']['address']='0x17fec'
   if mode=='target':x['subject']['digest']['sha256']='0'*64
   if mode=='operation':x['operation']='read_bytes'
   if mode=='profile':x['analysis_profile']['digest']='0'*64
   if mode=='load_profile':x['analysis_profile']['parameters']['load_segment']='0x1001'
   with self.subTest(mode=mode),self.assertRaises(ValueError):self.validate()
 def test_xref_bundle_cannot_escape_project(self):
  self.unit['extended_extent']['table_xref_evidence']='../outside.json'
  with self.assertRaisesRegex(ValueError,'outside'):self.validate()
 def test_raw_metadata_completeness_identity_and_byte_equality(self):
  original=copy.deepcopy(self.e)
  for mode in ['complete','parameters','returned','requested','address','truncated','mismatch','target','profile']:
   self.e=copy.deepcopy(original);e=self.e['raw'];n=e['normalized_result']
   if mode=='complete':n['complete']=False
   if mode=='parameters':e['parameters']['length']-=1
   if mode=='returned':n['returned_bytes']-=1
   if mode=='requested':n['requested_bytes']-=1
   if mode=='address':n['address']='0x17e6c'
   if mode=='truncated':n['bytes_hex']=n['bytes_hex'][:-2]
   if mode=='mismatch':n['bytes_hex']='90'+n['bytes_hex'][2:]
   if mode=='target':e['subject']['digest']['sha256']='0'*64
   if mode=='profile':e['analysis_profile']['digest']='0'*64
   with self.subTest(mode=mode),self.assertRaises(ValueError):self.validate()
 def test_no_partial_or_inferred_CodeView_boundary(self):
  original=copy.deepcopy(self.emitted)
  for key,value in [('size',395),('end',720),('symbol','_other'),('boundary','next_public_or_segment_end')]:
   self.emitted=copy.deepcopy(original);self.emitted[key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):self.validate()
 def test_next_native_entry_is_exactly801A(self):
  original=copy.deepcopy(self.e)
  for mode in ['entry','body','range','raw']:
   self.e=copy.deepcopy(original);p=self.e['next']['normalized_result']['procedure']
   if mode=='entry':p['address']='0x1801b'
   if mode=='body':p['body']['total_bytes']=72
   if mode=='range':p['body']['ranges'][0]['end']='0x18061'
   if mode=='raw':self.mutate_bytes(431,0x90)
   with self.subTest(mode=mode),self.assertRaises(ValueError):self.validate()
 def test_no_generic_kind_size_symbol_or_compiler_grant(self):
  original=copy.deepcopy(self.unit)
  for key,value in [('size',395),('image_offset','0x7e6c'),('language','asm'),('symbol','_other'),('backend','msc510-omf'),('flags',['/AS','/Zi'])]:
   self.unit=copy.deepcopy(original);self.unit[key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):self.validate()
  self.unit=copy.deepcopy(original);self.unit['extended_extent']['extra']=True
  with self.assertRaises(ValueError):self.validate()

if __name__=='__main__':unittest.main()
