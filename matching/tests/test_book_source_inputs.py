"""Fourth profile fixtures are isolated; no canonical registry or global tests."""
import copy,dataclasses,importlib.util,json,shutil,struct,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
PROJECT=next(p for p in Path(__file__).resolve().parents if(p/'config/msc500.json').exists())
STAGE=PROJECT/'build/book-common-profile-stage'
sys.path.insert(0,str(PROJECT))
import book_source_inputs as book
from msc import compile_c
from omf import read_omf
spec=importlib.util.spec_from_file_location('staged_book_dispatch',PROJECT/'source_inputs.py');dispatch=importlib.util.module_from_spec(spec);spec.loader.exec_module(dispatch)

def record(kind,payload):
 b=bytes([kind])+struct.pack('<H',len(payload)+1)+payload
 return b+bytes([-sum(b)&255])
def mutate(data,kind,change):
 out=[];changed=False
 for k,_,p in read_omf(data).records:
  if k==kind and not changed:p=change(p);changed=True
  out.append(record(k,p))
 assert changed
 return b''.join(out)

class BookInputsTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.cfg=json.loads((STAGE/'source-inputs.proposed.json').read_text());cls.item=cls.cfg['source_allocations'][3]
  cls.compiled={}
  for name,source in [('asset_selectors.c','src/link/asset_selectors.c'),('clock_state.c','src/link/clock_state.c'),('side_history_state.c','src/link/side_history_state.c'),('book_state.c','build/book-storage-followup/scalars.c')]:
   cls.compiled[name]=compile_c(PROJECT/source,book.FLAGS,compiler='msc500')
  cls.raw=cls.compiled['book_state.c'].object_bytes
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.p=Path(self.tmp.name)/'matching';self.p.mkdir();self.output=self.p/'objects'
  for item in self.cfg['source_allocations']:
   source=PROJECT/('build/book-storage-followup/scalars.c'if item['source']==book.SOURCE else item['source'])
   dest=self.p/item['source'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
   for v in item['evidence'].values():
    dest=self.p/v['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(PROJECT/v['path'],dest)
  self.target=self.p.parent/'CHESS.EXE';shutil.copyfile(PROJECT.parent/'CHESS.EXE',self.target)
 def build(self,item=None):
  return book.build_input(self.item if item is None else item,self.p,self.target,self.output,compiler_fn=lambda *a,**k:self.compiled['book_state.c'])
 def run_config(self,cfg=None,defined=()):
  path=self.p/'config.json';path.write_text(json.dumps(self.cfg if cfg is None else cfg))
  def compile_fixture(source,*args,**kwargs):return self.compiled[Path(source).name]
  with patch.object(dispatch,'compile_c',side_effect=compile_fixture):return dispatch.build_source_inputs(self.p,self.target,self.output,config_path=path,defined_symbols=defined)
 def evidence_mutation(self,rel,fn):
  path=self.p/rel;data=json.loads(path.read_text());fn(data);path.write_text(json.dumps(data));pins=copy.deepcopy(book.PINS);pins[rel]['sha256']=book.sha(path.read_bytes())
  with patch.object(book,'PINS',pins),self.assertRaises(ValueError):book.validate_evidence(self.p,pins,self.target)
 def test_actual_fresh_complete_object(self):
  self.assertEqual(book.sha(self.raw),book.OBJECT_SHA);defs=book.validate_object(self.raw);self.assertEqual([r['size']for r in defs],[2]*7+[8]);self.assertEqual([r['type_index']for r in defs],[129]*7+[522])
 def test_build_evidence_allocation_only(self):
  r=self.build();self.assertEqual((r['allocation_bytes'],r['initialized_bytes'],r['matching_credit'],r['authored_C_function_credit']),(22,0,0,0));self.assertFalse(r['placement_proven']);self.assertTrue(all(not c['resolved']for c in r['original_map_constraints']))
 def test_four_profiles_actual_fresh_objects(self):
  r=self.run_config();self.assertEqual(len(r['objects']),4);self.assertEqual(sum(len(x['definitions'])for x in r['objects']),25);self.assertEqual(sum(x['allocation_bytes']for x in r['objects']),84);self.assertEqual(r['matching_credit'],0);self.assertEqual(sum(x['initialized_bytes']for x in r['objects']),0)
 def test_existing_three_rows_identical(self):
  old=json.loads((STAGE/'source-inputs.base.json').read_text());self.assertEqual(self.cfg['source_allocations'][:3],old['source_allocations'])
 def test_source_drift(self):
  (self.p/book.SOURCE).write_text('int replacement;')
  with self.assertRaises(ValueError):self.build()
 def test_unknown_item_field(self):
  i=copy.deepcopy(self.item);i['credit']=22
  with self.assertRaises(ValueError):book.validate_item(i)
 def test_wrong_source_flags_tool(self):
  for key,value in [('source','src/link/other.c'),('flags',['/AS','/Zi']),('compiler','msc510'),('source_sha256','0'*64),('toolchain_manifest_sha256','0'*64)]:
   with self.subTest(key=key),self.assertRaises(ValueError):i=copy.deepcopy(self.item);i[key]=value;book.validate_item(i)
 def test_omitted_or_duplicate_selection(self):
  for names in (self.item['objects'][:-1],self.item['objects']+[self.item['objects'][0]]):
   i=copy.deepcopy(self.item);i['objects']=names
   with self.assertRaises(ValueError):book.validate_item(i)
 def test_config_duplicate_id_source(self):
  c=copy.deepcopy(self.cfg);c['source_allocations'].append(c['source_allocations'][-1])
  with self.assertRaises(ValueError):self.run_config(c)
 def test_existing_matched_definition(self):
  for n in book.NAMES:
   with self.subTest(n=n),self.assertRaises(ValueError):self.run_config(defined=[n])
 def test_wrong_debug_type(self):
  # checksum-correct change of first int type129 to unsigned129+1
  raw=mutate(self.raw,0xb0,lambda p:p.replace(b'\x80\x81\x62\x02',b'\x80\x82\x62\x02',1))
  with self.assertRaises(ValueError):book.validate_object(raw)
 def test_far_common(self):
  raw=mutate(self.raw,0xb0,lambda p:p.replace(b'\x62\x02',b'\x61\x02',1))
  with self.assertRaises(ValueError):book.validate_object(raw)
 def test_wrong_size(self):
  with self.assertRaises(ValueError):book.validate_object(mutate(self.raw,0xb0,lambda p:p.replace(b'\x62\x08',b'\x62\x06',1)))
 def test_reordered_name(self):
  with self.assertRaises(ValueError):book.validate_object(mutate(self.raw,0xb0,lambda p:p.replace(b'_book_matches',b'_fake_matches',1)))
 def test_loaded_allocation(self):
  with self.assertRaises(ValueError):book.validate_object(mutate(self.raw,0x98,lambda p:p[:1]+b'\x02\x00'+p[3:]))
 def test_lidata_record(self):
  raw=self.raw[:-4]+record(0xa2,b'\x02\0\0\x01\0\0\0\x01\0')+self.raw[-4:]
  with self.assertRaises(ValueError):book.validate_object(raw)
 def test_group_change(self):
  with self.assertRaises(ValueError):book.validate_object(mutate(self.raw,0x9a,lambda p:p[:-1]+b'\x03'))
 def test_fixup_change(self):
  with self.assertRaises(ValueError):book.validate_object(mutate(self.raw,0x9c,lambda p:bytes([p[0]^4])+p[1:]))
 def test_cv_byte_change(self):
  with self.assertRaises(ValueError):book.validate_object(mutate(self.raw,0xa0,lambda p:p[:-1]+bytes([p[-1]^1])))
 def test_checksum(self):
  b=bytearray(self.raw);b[-1]^=1
  with self.assertRaises(ValueError):book.validate_object(bytes(b))
 def test_extra_tail(self):
  with self.assertRaises(ValueError):book.validate_object(self.raw+b'\0')
 def test_provenance_mismatch(self):
  for kw in ({'source_name':'SCALARS.C'},{'compiler':'msc510'},{'toolchain_manifest_sha256':'0'*64},{'tool_hashes':{}}):
   with self.subTest(kw=kw),self.assertRaises(ValueError):book.build_input(self.item,self.p,self.target,self.output,compiler_fn=lambda *a,**k:dataclasses.replace(self.compiled['book_state.c'],**kw))
 def test_generation_precedes_target_validation(self):
  self.target.unlink();called=[]
  with self.assertRaises(FileNotFoundError):book.build_input(self.item,self.p,self.target,self.output,compiler_fn=lambda *a,**k:(called.append(True)or self.compiled['book_state.c']))
  self.assertEqual(called,[True])
 def test_evidence_pin_mismatch(self):
  path=self.p/'build/book-storage-followup/main.c';path.write_bytes(path.read_bytes()+b' ')
  with self.assertRaises(ValueError):self.build()
 def test_native_CRT_pin_bounds(self):
  self.evidence_mutation('build/book-storage-followup/storage-audit.json',lambda e:e['CRT_clear'].update(start_inclusive='0x52cb'))
 def test_no_initialized_zero_borrow(self):
  self.evidence_mutation('build/book-storage-followup/rea-book-offset.json',lambda e:e['normalized_result'].update(returned_bytes=2,bytes_hex='0000',complete=True))
 def test_carrier_import_checks(self):
  self.evidence_mutation('build/book-storage-followup/rea-carrier-load-image.json',lambda e:e['normalized_result']['checks'][0].update(matched=False))
 def test_native_width(self):
  self.evidence_mutation('build/book-storage-followup/storage-audit.json',lambda e:e['constraints'][0]['native_width_proof'][0].update(observed_instructions=['0x18324: MOV BL, byte ptr [0xb0d2]']))
 def test_capacity_hold(self):
  self.evidence_mutation('build/book-storage-followup/storage-audit.json',lambda e:e['splash_buffer'].update(definition_proposed=True))
 def test_diagnostic_execution(self):
  self.evidence_mutation('build/book-storage-followup/common-diagnostic-proof.json',lambda e:e['authentic_LINK_trials'][0].update(execution_exit_zero=False))
 def test_diagnostic_whole_code(self):
  self.evidence_mutation('build/book-storage-followup/common-diagnostic-proof.json',lambda e:e['authentic_LINK_trials'][0]['complete_CODE'].update(hex=e['authentic_LINK_trials'][0]['complete_CODE']['hex'][:-2]+'00'))
 def test_diagnostic_MZ(self):
  self.evidence_mutation('build/book-storage-followup/common-diagnostic-proof.json',lambda e:e['authentic_LINK_trials'][0]['MZ_sites'].append(0))
 def test_diagnostic_MAP_not_native(self):
  self.evidence_mutation('build/book-storage-followup/common-diagnostic-proof.json',lambda e:e['original_constraints'][0].update(original_MAP_placement_not_reproduced=False))

if __name__=='__main__':unittest.main()
