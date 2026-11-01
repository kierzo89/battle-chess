"""Successful complete C DATA MZ class, isolated from procedure/ASM credit."""
from pathlib import Path
import ast,copy,hashlib,json,sys,tempfile,unittest
from unittest.mock import patch
PROJECT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(PROJECT))
import check
import source_data_mz as accounting
from reference import build_reference
D=PROJECT/'build/source-data-mz-accounting-stage'

class SourceDataAccountingTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  assert Path(accounting.__file__).resolve()==PROJECT/'source_data_mz.py'
  cls.reference=build_reference((PROJECT.parent/'CHESS.EXE').read_bytes());cls.native=cls.reference['relocations']
  cls.normal=json.loads((D/'actual-minimal-output-v2/report.json').read_text());cls.row=cls.normal['units'][0]
  cls.baseline=json.loads((D/'baseline-report.json').read_text())
 def call(self,rows=None,native=None,reference=None,project=None):
  return accounting.collect_source_data_mz([self.row]if rows is None else rows,PROJECT if project is None else project,self.reference if reference is None else reference,self.native if native is None else native)
 def change(self,f):
  row=copy.deepcopy(self.row);f(row);return row
 def test_actual_fresh_normal_DATA_scope_one_native_MZ(self):
  result=self.call();self.assertEqual(result['sites'],[0x5d1f0]);self.assertEqual(result['byte_credit'],0);self.assertEqual(result['function_credit'],0)
  self.assertEqual(result['matched_DATA_units'][0]['actual_artifact_proof']['raw_field_count'],2)
  self.assertEqual(self.normal['summary']['sourcedata_emitted_mz_relocations'],1);self.assertEqual(self.normal['summary']['source_emitted_mz_relocations'],0)
 def test_actual_minimal_report_JSON_and_display(self):
  r=self.normal;s=r['summary'];c=json.loads((D/'actual-minimal-output-v2/relocation_coverage.json').read_text())
  self.assertEqual(c['sourcedata_emitted_sites'],[0x5d1f0]);self.assertEqual(c['verified_emitted_sites'],[0x5d1f0]);self.assertEqual(len(c['remaining_sites']),172)
  self.assertEqual(s['owned_context_emitted_mz_relocations'],0);self.assertEqual(s['verified_emitted_mz_relocations'],1)
  text=(D/'actual-minimal-output-v2/PROGRESS.md').read_text();self.assertIn('C DATA-emitted MZ segment relocations verified | 1',text);self.assertIn('Verified union MZ segment relocations | 1 / 173',text)
 def test_current_near_and_relocation_free_DATA_stay_zero(self):
  p=self.call(self.baseline['units']);self.assertEqual(p['sites'],[])
  self.assertEqual(len(p['matched_DATA_units']),self.baseline['summary']['source_data_units'])
 def test_failed_or_nonDATA_results_never_contribute_or_read_artifacts(self):
  for status in ['mismatch','build_error','c_matched','runtime_matched','asm_code_matched',None]:
   row=self.change(lambda r:r.update(status=status,object_artifact='/does/not/exist'))
   with patch.object(Path,'read_bytes',side_effect=AssertionError('failed row read')),patch.object(Path,'read_text',side_effect=AssertionError('failed row read')):
    self.assertEqual(self.call([row])['sites'],[])
 def test_wrong_status_language_pair_rejected(self):
  with self.assertRaises(ValueError):self.call([self.change(lambda r:r.update(language='c'))])
 def test_missing_MZ_record_fails_complete_native_extent(self):
  with self.assertRaisesRegex(ValueError,'complete original extent'):self.call([self.change(lambda r:r.update(relocations=[]))])
 def test_extra_or_outside_native_field_fails(self):
  for site in [0x5d1ee,0x5d1ef,0x5d1f2,0x619c6,-1,True]:
   row=self.change(lambda r:r['relocations'][0].update(mz_segment_relocation_image_offset=site))
   with self.subTest(site=site),self.assertRaises(ValueError):self.call([row])
 def test_duplicate_field_not_silently_set_deduplicated(self):
  row=self.change(lambda r:r['relocations'].append(copy.deepcopy(r['relocations'][0])))
  with self.assertRaisesRegex(ValueError,'duplicate emitted'):self.call([row])
 def test_duplicate_unit_and_cross_unit_site_ownership_rejected(self):
  with self.assertRaisesRegex(ValueError,'Duplicate'):self.call([self.row,self.row])
  row=self.change(lambda r:r.update(id='different_owner'))
  with self.assertRaisesRegex(ValueError,'across matched units'):self.call([self.row,row])
 def test_malformed_record_collection_rejected(self):
  for value in [{},None,[None],[{'mz_segment_relocation_image_offset':None}]]:
   with self.subTest(value=value),self.assertRaises(ValueError):self.call([self.change(lambda r:r.update(relocations=value))])
 def test_crossing_native_word_at_both_edges_rejected(self):
  for origin,size in [('0x5d1ef',2),('0x5d1f1',1)]:
   with self.subTest(origin=origin),self.assertRaisesRegex(ValueError,'crosses'):self.call([self.change(lambda r:r.update(image_offset=origin,size=size))])
 def test_invalid_native_identity_duplicates_or_wrong_reference_reject(self):
  for n in [list(self.native)+[self.native[0]],list(self.native)+[True],list(self.native)[:-1]]:
   with self.assertRaises(ValueError):self.call(native=n)
  with self.assertRaises(ValueError):self.call(reference={})
 def test_nonreviewed_nonempty_DATA_MZ_backend_rejects(self):
  with self.assertRaisesRegex(ValueError,'reviewed'):self.call([self.change(lambda r:r.update(backend='msc500-pointer-data-omf'))])
 def test_closed_source_profile_and_unit_flags_rechecked(self):
  for change in [{'object_profile':'other'},{'flags':['/AM']},{'compiler':'Microsoft C 5.10'}]:
   with self.subTest(change=change),self.assertRaises(ValueError):self.call([self.change(lambda r:r.update(**change))])
 def test_changed_source_hash_object_hash_and_tool_hash_fail(self):
  for change in [{'source_sha256':'0'*64},{'object_sha256':'0'*64},{'compiler_tool_hashes':{}},{'toolchain_manifest_sha256':'0'*64},{'compiler_flags':['/AS']}]:
   with self.subTest(change=change),self.assertRaises(ValueError):self.call([self.change(lambda r:r.update(**change))])
 def test_actual_object_and_source_payload_tampering_fails(self):
  with tempfile.TemporaryDirectory()as tmp:
   path=Path(tmp)/'wrong.obj';path.write_bytes(Path(self.row['object_artifact']).read_bytes()+b'\0')
   with self.assertRaisesRegex(ValueError,'fingerprint'):self.call([self.change(lambda r:r.update(object_artifact=str(path)))])
   p=Path(tmp);source=p/self.row['source'];source.parent.mkdir(parents=True);source.write_bytes((PROJECT/self.row['source']).read_bytes()+b' ')
   with self.assertRaisesRegex(ValueError,'source identity'):self.call(project=p)
 def test_missing_relative_output_or_source_escape_fails(self):
  for change in [{'object_artifact':None},{'object_artifact':'relative.obj'},{'source':'../CHESS.EXE'}]:
   with self.subTest(change=change),self.assertRaises(ValueError):self.call([self.change(lambda r:r.update(**change))])
 def test_actual_field_and_complete_metadata_cannot_be_forged(self):
  for mutate in [lambda r:r['relocations'][0].update(encoded_segment=0),lambda r:r['emitted_data_segment'].update(emitted_mz_sites=[]),lambda r:r['emitted_data_segment']['segment'].update(length=2)]:
   with self.assertRaises(ValueError):self.call([self.change(mutate)])
 def test_wrong_binding_or_DS_placement_fails(self):
  for mutate in [lambda r:r['externals']['_screen_pixels'].update(segment=1),lambda r:r['externals']['_screen_pixels'].update(offset=1),lambda r:r['data_address'].update(offset=0x5cc),lambda r:r['data_address'].update(segment=1)]:
   with self.assertRaises(ValueError):self.call([self.change(mutate)])
 def test_source_and_decoded_bytes_full_native_MZ_rechecked(self):
  bad=dict(self.reference);bad['image']=self.reference['image'][:0x5d1ee]+b'\0'+self.reference['image'][0x5d1ef:]
  with self.assertRaises(ValueError):self.call(reference=bad)
 def test_actual_baseline_and_single_unit_replay_union_only(self):
  # This is explicitly a bounded replay, not a synthetic whole check.run.
  b=self.baseline;old=json.loads((D/'baseline-relocation-coverage.json').read_text())
  c={f['mz_segment_relocation_image_offset']for r in b['units']if r['status']=='c_matched'for f in r.get('relocations',[])if 'mz_segment_relocation_image_offset'in f}
  data=set(self.call(b['units']+[self.row])['sites']);before=set(old['verified_emitted_sites']);after=before|data
  self.assertEqual(len(c),116);self.assertEqual(len(old['owned_context_emitted_sites']),1)
  self.assertEqual(data,{0x5d1f0});self.assertFalse(before&data);self.assertEqual(len(after)-len(before),1)
  self.assertEqual(len(after),141);self.assertEqual(len(self.native),173)
 def test_patch_keeps_all_existing_build_and_native_validation_AST(self):
  a=ast.parse((D/'implementation/check.base.py').read_text());b=ast.parse((D/'implementation/check.py').read_text())
  defs=lambda tree:{n.name:ast.dump(n,include_attributes=False)for n in tree.body if isinstance(n,ast.FunctionDef)}
  old,new=defs(a),defs(b);self.assertEqual(set(old),set(new));self.assertEqual({k for k in old if old[k]!=new[k]},{'run','report_markdown'})
  before=(D/'implementation/check.base.py').read_text();after=(D/'implementation/check.py').read_text()
  start="    emitted_mz_relocations = sorted({r['mz_segment_relocation_image_offset']"
  self.assertEqual(before[before.index(start):before.index('    owned_context_mz_proof')],after[after.index(start):after.index('    sourcedata_mz_proof')])

if __name__=='__main__':unittest.main(verbosity=2)
