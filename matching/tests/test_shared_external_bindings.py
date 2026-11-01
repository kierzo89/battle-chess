"""Reject global-name/address drift before expensive compiler comparisons."""
import copy
import json
from pathlib import Path
import sys
import unittest
M = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(M))
from check import validate_shared_external_bindings

def unit(name, address, **kwargs):
    return dict(id=name, symbol='_'+name, language='c', image_offset=hex(address), **kwargs)

class SharedBindingsTests(unittest.TestCase):
    def test_real_registry_has_one_binding_per_name(self):
        units = json.loads((M/'config/units.json').read_text())
        result = validate_shared_external_bindings(units)
        self.assertTrue(result)

    def test_distinct_globals_cannot_share_one_name(self):
        rows = [unit('engine', 0x100, externals={'_state_index': 0xa852}),
                unit('book', 0x200, externals={'_state_index': 0x8cfe})]
        with self.assertRaisesRegex(ValueError, '_state_index'):
            validate_shared_external_bindings(rows)
        rows[1]['externals'] = {'_book_state_index': 0x8cfe}
        validate_shared_external_bindings(rows)

    def test_near_and_far_known_code_views_are_equivalent(self):
        rows = [unit('target', 0x1234), unit('near', 0x100, externals={'_target': 0x1234}),
                unit('far', 0x200, externals={'_target': {'segment': 0x100, 'offset': 0x234}})]
        self.assertEqual(set(validate_shared_external_bindings(rows)['_target']), {'4660'})
        rows[-1]['externals']['_target']['offset'] += 1
        with self.assertRaisesRegex(ValueError, '_target'):
            validate_shared_external_bindings(rows)

    def test_nonzero_caller_cs_is_used_for_known_near_code(self):
        rows = [unit('target', 0x10234), unit('caller', 0x10100,
            code_address={'segment': 0x1000, 'offset': 0x100}, externals={'_target': 0x234})]
        validate_shared_external_bindings(rows)
        del rows[-1]['code_address']
        with self.assertRaisesRegex(ValueError, '_target'):
            validate_shared_external_bindings(rows)

    def test_absolute_and_data_contracts_are_not_conflated(self):
        rows = [unit('a', 0x100, externals={'_value': 12}),
                unit('b', 0x200, externals={'_value': {'absolute': 12}})]
        with self.assertRaisesRegex(ValueError, '_value'):
            validate_shared_external_bindings(rows)
        rows[-1]['externals'] = {'_value': {'segment': 0, 'offset': 12}}
        with self.assertRaisesRegex(ValueError, '_value'):
            validate_shared_external_bindings(rows)

    def test_c_data_consumers_share_the_same_global_contract(self):
        rows = [unit('code', 0x100, externals={'_value': 0x1234}),
                dict(id='pointers', language='c-data', image_offset='0x60000', externals={'_value': 0x1234})]
        validate_shared_external_bindings(rows)
        rows[-1]['externals']['_value'] += 2
        with self.assertRaisesRegex(ValueError, '_value'):
            validate_shared_external_bindings(rows)

    def test_input_maps_stay_unchanged_and_runtime_has_separate_scope(self):
        rows = [unit('target', 0x1234), unit('a', 0x100, externals={'_target': {'segment': 0, 'offset': 0x1234}}),
                dict(id='runtime', language='runtime', externals={'_target': {'segment': 0, 'offset': 0x4321}})]
        before = copy.deepcopy(rows)
        validate_shared_external_bindings(rows)
        self.assertEqual(rows, before)

if __name__ == '__main__':
    unittest.main()
