from pathlib import Path
import sys,copy,json,unittest,hashlib,ast
from unittest.mock import patch
M=next(p for p in Path(__file__).resolve().parents if(p/'config/msc500.json').is_file())
D=M/'build/owned-context-mz-accounting-stage'
sys.path.insert(0,str(M))
import owned_context_mz as accounting
assert Path(accounting.__file__).resolve()==(M/'owned_context_mz.py').resolve(), 'Canonical helper module path required'
from reference import build_reference

class OwnedContextAccounting(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.report=json.loads((M/'build/future-coherent443-proposal/staged-report.json').read_text())
  cls.rows=[r for r in cls.report['units']if r.get('owned_selector_const')]
  # Historical443 owners retain their exact pre-rename source bytes.
  for row in cls.rows:row['source']='build/move8d12-rename-controls/baseline-sources/src/book_context_match.c'
  cls.reference=build_reference((M.parent/'CHESS.EXE').read_bytes())
  cls.native=cls.reference['relocations'];assert len(cls.rows)==5
 def call(self,rows=None,native=None,reference=None):
  return accounting.collect_owned_context_mz(self.rows if rows is None else rows,M,self.reference if reference is None else reference,self.native if native is None else native)
 def mutate(self,f):
  rows=copy.deepcopy(self.rows);f(rows[0]);return rows
 def test_actual_five_owners_one_site(self):
  p=self.call();self.assertEqual(p['sites'],[0x619c6]);self.assertEqual(len(p['contexts']),1);self.assertEqual(len(p['matched_owner_units']),5);self.assertEqual(p['byte_credit'],0);self.assertEqual(p['function_credit'],0)
 def test_native_in_memory_tuple_proof(self):
  from omf import read_omf
  rows=copy.deepcopy(self.rows)
  for r in rows:
   _,_,p=accounting.selector.validate(r,read_omf(Path(r['object_artifact']).read_bytes()),M,self.reference)
   r['owned_selector_const_proof']=p
  self.assertEqual(self.call(rows)['sites'],[0x619c6])
 def test_individual_owner(self):
  for r in self.rows:self.assertEqual(self.call([r])['sites'],[0x619c6])
 def test_empty_backward_compatible(self):self.assertEqual(self.call([])['sites'],[])
 def test_nonowners_unchanged(self):self.assertEqual(self.call([r for r in self.report['units']if not r.get('owned_selector_const')])['sites'],[])
 def test_failed_owners_excluded(self):
  for status in ['mismatch','build_error','c_data_matched','runtime_matched','asm_matched','asm_code_matched',None]:
   rows=self.mutate(lambda r:r.update(status=status));self.assertEqual(len(self.call(rows)['matched_owner_units']),4)
 def test_all_failed_no_sites(self):
  rows=copy.deepcopy(self.rows)
  for r in rows:r['status']='mismatch'
  self.assertEqual(self.call(rows)['sites'],[])
 def test_duplicate_owner_rejected(self):
  with self.assertRaisesRegex(ValueError,'Duplicate'):self.call(self.rows+[self.rows[0]])
 def test_missing_proof(self):
  with self.assertRaises(ValueError):self.call(self.mutate(lambda r:r.pop('owned_selector_const_proof')))
 def test_proof_without_descriptor(self):
  with self.assertRaises(ValueError):self.call(self.mutate(lambda r:r.pop('owned_selector_const')))
 def test_foreign_profile(self):
  with self.assertRaises(ValueError):self.call(self.mutate(lambda r:r['owned_selector_const'].update(kind='generic_proof')))
 def test_wrong_native_site(self):
  with self.assertRaises(ValueError):self.call(self.mutate(lambda r:r['owned_selector_const_proof'].update(complete_MZ_sites=[0x619c4])))
 def test_duplicate_claimed_sites(self):
  with self.assertRaises(ValueError):self.call(self.mutate(lambda r:r['owned_selector_const_proof'].update(complete_MZ_sites=[0x619c6]*2)))
 def test_bool_claimed_site(self):
  with self.assertRaises(ValueError):self.call(self.mutate(lambda r:r['owned_selector_const_proof'].update(complete_MZ_sites=[True])))
 def test_malformed_proof(self):
  with self.assertRaises(ValueError):self.call(self.mutate(lambda r:r.update(owned_selector_const_proof=[])))
 def test_native_membership_required(self):
  native=[p for p in self.native if p!=0x619c6]
  with self.assertRaises(ValueError):self.call(native=native)
 def test_native_membership_missing_from_both_inputs(self):
  ref=dict(self.reference);ref['relocations']=[p for p in self.native if p!=0x619c6]
  with self.assertRaises(ValueError):self.call(native=ref['relocations'],reference=ref)
 def test_duplicate_native_sites_rejected(self):
  with self.assertRaises(ValueError):self.call(native=list(self.native)+[0x619c6])
 def test_changed_source_fingerprint(self):
  with self.assertRaisesRegex(ValueError,'source fingerprint'):self.call(self.mutate(lambda r:r.update(source_sha256='0'*64)))
 def test_changed_object_fingerprint(self):
  with self.assertRaisesRegex(ValueError,'object fingerprint'):self.call(self.mutate(lambda r:r.update(object_sha256='0'*64)))
 def test_missing_object_artifact(self):
  with self.assertRaises(ValueError):self.call(self.mutate(lambda r:r.pop('object_artifact')))
 def test_relative_object_artifact(self):
  with self.assertRaises(ValueError):self.call(self.mutate(lambda r:r.update(object_artifact='not-a-real-output.obj')))
 def test_source_escape(self):
  with self.assertRaises(ValueError):self.call(self.mutate(lambda r:r.update(source='../CHESS.EXE')))
 def test_tampered_code_proof(self):
  with self.assertRaises(ValueError):self.call(self.mutate(lambda r:r['owned_selector_const_proof'].update(complete_CODE_bytes=799)))
 def test_tampered_selector_fixup(self):
  with self.assertRaises(ValueError):self.call(self.mutate(lambda r:r['owned_selector_const_proof']['raw_CONST_fixup'].update(width=4)))
 def test_tampered_selector_bytes(self):
  with self.assertRaises(ValueError):self.call(self.mutate(lambda r:r['owned_selector_const_proof'].update(selector_bytes_hex='0000')))
 def test_tampered_primary_digest(self):
  with self.assertRaises(ValueError):self.call(self.mutate(lambda r:r['owned_selector_const_proof'].update(selector_primary_sha256='0'*64)))
 def test_wrong_descriptor_placement(self):
  with self.assertRaises(ValueError):self.call(self.mutate(lambda r:r['owned_selector_const'].update(image_offset='0x619c4')))
 def test_generic_proof_cannot_supply_sites(self):
  row={'status':'c_matched','owned_selector_const_proof':{'complete_MZ_sites':[0x619c6]}}
  with self.assertRaises(ValueError):self.call([row])
 def test_reference_required(self):
  with self.assertRaises(ValueError):self.call(reference={})
 def test_actual_accounting_delta_only(self):
  rs=self.report['units'];oldc={f['mz_segment_relocation_image_offset']for r in rs if r['status']=='c_matched'for f in r.get('relocations',[])if 'mz_segment_relocation_image_offset'in f}
  oldall={f['mz_segment_relocation_image_offset']for r in rs if r['status']in ['c_matched','runtime_matched','asm_code_matched']for f in r.get('relocations',[])if 'mz_segment_relocation_image_offset'in f}
  new=oldall|set(self.call()['sites']);self.assertEqual(len(oldc),116);self.assertEqual(len(oldall),139);self.assertEqual(len(new),140);self.assertEqual(new-oldall,{0x619c6});self.assertEqual(len(set(self.native)-new),33)
 def test_patch_preserves_old_procedure_collection(self):
  before=(D/'implementation/check.base.py').read_text();after=(D/'implementation/check.py').read_text()
  anchor="    emitted_mz_relocations = sorted({r['mz_segment_relocation_image_offset']"
  self.assertEqual(before[before.index(anchor):before.index('    verified_mz_relocations')],after[after.index(anchor):after.index('    owned_context_mz_proof')])
  for name in ['validate_emitted_mz_sites','build_unit']:
   a=next(n for n in ast.parse(before).body if isinstance(n,ast.FunctionDef)and n.name==name);b=next(n for n in ast.parse(after).body if isinstance(n,ast.FunctionDef)and n.name==name);self.assertEqual(ast.dump(a),ast.dump(b))

if __name__=='__main__':unittest.main(verbosity=2)
