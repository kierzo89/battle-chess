import unittest,json,copy,importlib.util
from pathlib import Path
P=Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location('bss_test_cohort',P/'build_pipeline/engine_v1/cohort.py');cohort=importlib.util.module_from_spec(spec);spec.loader.exec_module(cohort)
F=Path(__file__).resolve().parent/'fixtures/near_bss_layout190'
class NearBSSSourceKindTests(unittest.TestCase):
 def d(self):return json.loads((F/'descriptor-optional-BSS.json').read_text())
 def reject(self,d):
  with self.assertRaises(Exception):cohort.validate_descriptor(d)
 def test_explicit_new_optional_kind(self):self.assertEqual(cohort.validate_descriptor(self.d())['counts']['BSS'],1)
 def test_no_BSS_default_unchanged(self):
  d=self.d();d['rows'].pop();d['counts']['SOURCE']-=1;d['counts'].pop('BSS');self.assertNotIn('BSS',cohort.validate_descriptor(d)['counts'])
 def test_undeclared_BSS_count(self):
  d=self.d();d['counts'].pop('BSS');self.reject(d)
 def test_BSS_not_COMMON(self):
  d=self.d();d['rows'][-1]['kind']='common-whole-omf';self.reject(d)
 def test_wrong_source(self):
  d=self.d();d['rows'][-1]['source']='asm/link/fake.asm';self.reject(d)
 def test_extra_owner(self):
  d=self.d();d['rows'][-1]['selected_owners'].append('unproved_alias');self.reject(d)
 def test_wrong_NASM_command(self):
  d=self.d();d['rows'][-1]['generator_argv_tail'].insert(0,'-DBLOB');self.reject(d)
 def test_counts_cannot_smuggle_MIXED_or_BSS(self):
  d=self.d();d['counts']['COMMON']+=1;self.reject(d)
