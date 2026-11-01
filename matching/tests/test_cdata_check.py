"""C data uses independent allocation boundaries and receives no function credit."""
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
import check
from msc import compile_c


class CDataCheckerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit = next(u for u in json.loads((PROJECT / 'config/units.json').read_text())
                        if u['id'] == 'move_lookup_tables')
        original = (PROJECT.parent / 'CHESS.EXE').read_bytes()
        cls.reference = check.build_reference(original)
        cls.compiled = compile_c(PROJECT / cls.unit['source'], cls.unit['flags'], compiler='msc500')

    def build(self, unit=None, reference=None):
        context = self.reference if reference is None else reference
        with patch.object(check, 'compile_c', return_value=self.compiled):
            return check.build_unit(unit or self.unit, context['image'], PROJECT, 'nasm', reference=context)

    def test_fresh_compiler_data_matches_all_bytes_without_a_procedure(self):
        result = self.build()
        self.assertEqual(result['status'], 'c_data_matched')
        self.assertEqual(result['authored_c_function_credit'], 0)
        self.assertNotIn('emitted_procedure', result)
        self.assertEqual(result['emitted_data_segment']['segment']['length'], 80)
        self.assertEqual(result['relocations'], [])
        check.validate_emitted_mz_sites(result, self.reference['relocations'])
        self.assertTrue(check.validate_rea_extent(self.unit, PROJECT,
                        self.reference['original_sha256'], self.reference).startswith('ev_'))

    def test_data_cannot_use_code_or_direct_file_reference_rules(self):
        check.validate_units([self.unit], 82903, 401131)
        for changed in ({'reference_region': 'unchanged-prefix'},
                        {'language': 'c', 'backend': 'msc500-omf'},
                        {'externals': {'_placeholder': 123}},
                        {'extended_extent': {'kind': 'unreachable_return_gap_v1'}}):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                check.validate_units([self.unit | changed], 82903, 401131)
        with patch.object(check, 'compile_c', return_value=self.compiled):
            result = check.build_unit(self.unit, self.reference['image'], PROJECT, 'nasm')
        self.assertEqual(result['status'], 'build_error')
        self.assertIn('pinned expanded', result['error'])

    def test_wrong_extents_reference_or_object_bytes_cannot_earn_credit(self):
        for changed in ({'size': 79}, {'image_offset': '0x5d10b'}):
            with self.subTest(changed=changed):
                self.assertEqual(self.build(self.unit | changed)['status'], 'build_error')
        bad = self.reference | {'carrier_sha256': '0' * 64}
        self.assertEqual(self.build(reference=bad)['status'], 'build_error')
        obj = check.read_omf(self.compiled.object_bytes)
        public = obj.publics[self.unit['symbol']]
        segment = obj.segments[public.segment]
        offset, chunk = segment.chunks[0]
        segment.chunks[0] = (offset, bytes([chunk[0] ^ 1]) + chunk[1:])
        with patch.object(check, 'read_omf', return_value=obj):
            self.assertEqual(self.build()['status'], 'build_error')


if __name__ == '__main__':
    unittest.main()
