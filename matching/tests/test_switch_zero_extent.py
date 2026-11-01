"""The zero-return switch proof must account for all omitted and final bytes."""
import copy
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from extent import validate_extended_extent

TARGET = 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
PATHS = ['evidence/rea_search_next_b5ea.json', 'evidence/rea_search_b5ea_full_span.json',
         'evidence/rea_search_next_b860.json']


class ZeroReturnSwitchTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.project = Path(self.scratch.name)
        self.records = [json.loads((PROJECT / path).read_text()) for path in PATHS]
        self.unit = {'language': 'c', 'symbol': '_quiet_moves_b5ea', 'image_offset': '0xb5ea',
                     'size': 630, 'rea_evidence': PATHS[0], 'extended_extent': {
                         'kind': 'inline_switch_zero_return_v1', 'raw_span_evidence': PATHS[1],
                         'next_entry_evidence': PATHS[2]}}
        self.emitted = {'symbol': self.unit['symbol'], 'segment': 1, 'offset': 0,
                        'end': 630, 'size': 630, 'boundary': 'codeview3_procedure',
                        'fixups': [SimpleNamespace(offset=a-0xb5ea, segment=1, width=2,
                          location_type=1, segment_relative=True, target=(0, 1), frame=(5, None))
                          for a in (0xb843, 0xb845, 0xb847, 0xb849, 0xb84b, 0xb84d, 0xb84f)]}
        self.linked = bytes.fromhex(self.records[1]['normalized_result']['bytes_hex'])[:630]

    def validate(self):
        for path, record in zip(PATHS, self.records):
            file = self.project / path
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(json.dumps(record))
        return validate_extended_extent(self.unit, self.project, TARGET, self.emitted, self.linked)

    def test_full_630_byte_span_has_616_body_bytes_and_seven_real_fixups(self):
        p = self.validate()
        self.assertEqual((p['span_bytes'], p['reachable_body_bytes']), (630, 616))
        self.assertEqual(p['compiler_code_fixups'], 7)
        self.assertEqual((p['return_tail_address'], p['return_tail_bytes']), ('0x1b851', 15))
        self.assertEqual(p['case_targets'], ['0x1b62c', '0x1b6ce', '0x1b6ce',
                                           '0x1b6ce', '0x1b67d', '0x1b77b'])

    def test_agreeing_generated_and_raw_mutants_do_not_bypass_tail_or_dispatch(self):
        old, linked = copy.deepcopy(self.records), self.linked
        for address in [0x1b831, 0x1b833, 0x1b835, 0x1b839, 0x1b843, 0x1b845,
                        *range(0x1b851, 0x1b860)]:
            self.records = copy.deepcopy(old)
            raw = bytearray.fromhex(self.records[1]['normalized_result']['bytes_hex'])
            raw[address-0x1b5ea] ^= 1
            self.records[1]['normalized_result']['bytes_hex'] = raw.hex()
            self.linked = bytes(raw[:630])
            with self.subTest(address=hex(address)), self.assertRaises(ValueError): self.validate()
        self.records, self.linked = old, linked

    def test_missing_or_wrong_code_fixups_fail(self):
        old = copy.deepcopy(self.emitted)
        for i in range(7):
            self.emitted = copy.deepcopy(old)
            del self.emitted['fixups'][i]
            with self.subTest(missing=i), self.assertRaises(ValueError): self.validate()
        self.emitted = copy.deepcopy(old)
        self.emitted['fixups'][0].target = (0, 2)
        with self.assertRaises(ValueError): self.validate()

    def test_tail_cfg_and_excluded_regions_must_agree(self):
        old = copy.deepcopy(self.records)
        for address, field, value in [('0x1b851', 'successors', []),
                                      ('0x1b85a', 'end', '0x1b85f'),
                                      ('0x1b840', 'successors', []),
                                      ('0x1b835', 'successors', ['0x1b833'])]:
            self.records = copy.deepcopy(old)
            blocks = self.records[0]['normalized_result']['basic_blocks']
            next(b for b in blocks if b['start'] == address)[field] = value
            with self.subTest(address=address), self.assertRaises(ValueError): self.validate()
        self.records = copy.deepcopy(old)
        self.records[0]['normalized_result']['basic_blocks'][0]['successors'].append('0x1b845')
        with self.assertRaises(ValueError): self.validate()

    def test_boundaries_provenance_and_old_kind_are_not_interchangeable(self):
        self.unit['extended_extent']['kind'] = 'inline_switch_table_v1'
        with self.assertRaises(ValueError): self.validate()
        self.unit['extended_extent']['kind'] = 'inline_switch_zero_return_v1'
        self.emitted['size'] = 616
        with self.assertRaises(ValueError): self.validate()
        self.emitted['size'] = 630
        self.records[1]['subject']['digest']['sha256'] = '0' * 64
        with self.assertRaises(ValueError): self.validate()


if __name__ == '__main__': unittest.main()
