"""Attack the boundaries of the retained inline-switch proof."""
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
PATHS = {'body': 'evidence/rea_moves_engine_a181.json',
         'raw': 'evidence/rea_moves_a181_raw.json',
         'next': 'evidence/rea_moves_a181_next.json'}


class SwitchExtentTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.project = Path(self.scratch.name)
        self.evidence = {k: json.loads((PROJECT / p).read_text()) for k, p in PATHS.items()}
        self.unit = {'language': 'c', 'symbol': '_generate_quiet', 'image_offset': '0xa181',
                     'size': 455, 'rea_evidence': PATHS['body'], 'extended_extent': {
                         'kind': 'inline_switch_table_v1', 'raw_span_evidence': PATHS['raw'],
                         'next_entry_evidence': PATHS['next']}}
        # Metadata-only tests supply the seven required compiler fixup shapes.
        # Actual fresh OMF and linked byte production is also checked by check.py.
        self.emitted = {'symbol': '_generate_quiet', 'segment': 1, 'offset': 0,
                        'end': 455, 'size': 455, 'boundary': 'codeview3_procedure',
                        'fixups': [SimpleNamespace(offset=address-0xa181, segment=1,
                            width=2, location_type=1, segment_relative=True,
                            target=(0, 1), frame=(0, 1)) for address in
                            [0xa335, 0xa337, 0xa339, 0xa33b, 0xa33d, 0xa33f, 0xa341]]}
        self.linked = bytes.fromhex(self.evidence['raw']['normalized_result']['bytes_hex'])[:455]

    def validate(self):
        for key, relative in PATHS.items():
            path = self.project / relative
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_text(json.dumps(self.evidence[key]))
        return validate_extended_extent(self.unit, self.project, TARGET, self.emitted, self.linked)

    def mutate_raw_and_linked(self, address, value):
        raw = self.evidence['raw']['normalized_result']
        blob = bytearray.fromhex(raw['bytes_hex'])
        blob[address-0x1a181] = value
        raw['bytes_hex'] = blob.hex()
        self.linked = bytes(blob[:455])

    def test_complete_switch_table_and_dead_branch_are_accounted_for(self):
        proof = self.validate()
        self.assertEqual(proof['span_bytes'], 455)
        self.assertEqual(proof['reachable_body_bytes'], 441)
        self.assertEqual(proof['table_address'], '0x1a337')
        self.assertEqual(proof['compiler_code_fixups'], 7)
        self.assertEqual(proof['case_targets'],
                         ['0x1a1aa', '0x1a226', '0x1a226', '0x1a226', '0x1a1e8', '0x1a29e'])

    def test_all_seven_real_code_relocations_are_mandatory(self):
        for changes in [{'target': (0, 2)}, {'frame': (0, 2)}, {'width': 4},
                        {'segment_relative': False}, {'location_type': 2}, {'segment': 2}]:
            with self.subTest(changes=changes):
                old = copy.deepcopy(self.emitted)
                for key, value in changes.items(): setattr(self.emitted['fixups'][1], key, value)
                with self.assertRaises(ValueError): self.validate()
                self.emitted = old
        for index in range(7):
            old = copy.deepcopy(self.emitted)
            del self.emitted['fixups'][index]
            with self.subTest(missing=index), self.assertRaises(ValueError): self.validate()
            self.emitted = old
        self.emitted['fixups'].append(copy.copy(self.emitted['fixups'][0]))
        with self.assertRaisesRegex(ValueError, 'duplicate'): self.validate()

    def test_agreeing_raw_and_generated_bytes_do_not_bypass_structure(self):
        for address, byte in [(0x1a325, 0x90), (0x1a326, 0), (0x1a323, 0x90),
                              (0x1a32b, 4), (0x1a335, 0), (0x1a343, 0x90),
                              (0x1a337, 0xab)]:
            old, linked = copy.deepcopy(self.evidence), self.linked
            self.mutate_raw_and_linked(address, byte)
            with self.subTest(address=hex(address)), self.assertRaises(ValueError): self.validate()
            self.evidence, self.linked = old, linked

    def test_cfg_cases_and_exclusion_of_gaps_are_required(self):
        original = copy.deepcopy(self.evidence)
        for kind in ['missing_case', 'entry_in_gap', 'table_as_code', 'wrong_bound']:
            self.evidence = copy.deepcopy(original)
            blocks = self.evidence['body']['normalized_result']['basic_blocks']
            if kind == 'missing_case':
                next(b for b in blocks if b['start'] == '0x1a332')['successors'].pop()
            if kind == 'entry_in_gap': blocks[0]['successors'].append('0x1a325')
            if kind == 'table_as_code':
                blocks.append({'start': '0x1a337', 'end': '0x1a343', 'successors': []})
            if kind == 'wrong_bound':
                next(b for b in blocks if b['start'] == '0x1a327')['successors'] = []
            with self.subTest(kind=kind), self.assertRaises(ValueError): self.validate()

    def test_raw_identity_completeness_and_profiles_are_required(self):
        original = copy.deepcopy(self.evidence)
        for kind in ['target', 'digest', 'address', 'length', 'complete', 'truncated', 'mismatch']:
            self.evidence = copy.deepcopy(original)
            raw = self.evidence['raw']; n = raw['normalized_result']
            if kind == 'target': raw['subject']['digest']['sha256'] = '0'*64
            if kind == 'digest': raw['analysis_profile']['digest'] = '0'*64
            if kind == 'address': raw['parameters']['address'] = '0x1a182'
            if kind == 'length': raw['parameters']['length'] -= 1
            if kind == 'complete': n['complete'] = False
            if kind == 'truncated': n['bytes_hex'] = n['bytes_hex'][:-2]
            if kind == 'mismatch': n['bytes_hex'] = '90'+n['bytes_hex'][2:]
            with self.subTest(kind=kind), self.assertRaises(ValueError): self.validate()

    def test_exact_body_ranges_and_next_entry_are_required(self):
        original = copy.deepcopy(self.evidence)
        for kind in ['body_bytes', 'range', 'contiguous', 'next']:
            self.evidence = copy.deepcopy(original)
            body = self.evidence['body']['normalized_result']['procedure']['body']
            if kind == 'body_bytes': body['total_bytes'] += 1
            if kind == 'range': body['ranges'][1]['start'] = '0x1a326'
            if kind == 'contiguous': body['non_contiguous'] = False
            if kind == 'next': self.evidence['next']['normalized_result']['procedure']['address'] = '0x1a349'
            with self.subTest(kind=kind), self.assertRaises(ValueError): self.validate()

    def test_codeview_is_independent_and_complete(self):
        for change in [{'symbol': '_other'}, {'size': 441}, {'end': 441},
                       {'boundary': 'next_public_or_segment_end'}]:
            old = copy.deepcopy(self.emitted); self.emitted.update(change)
            with self.subTest(change=change), self.assertRaises(ValueError): self.validate()
            self.emitted = old

    def test_extra_proof_metadata_and_other_languages_are_rejected(self):
        self.unit['extended_extent']['expected_length'] = 455
        with self.assertRaises(ValueError): self.validate()
        del self.unit['extended_extent']['expected_length']
        self.unit['language'] = 'asm'
        with self.assertRaises(ValueError): self.validate()


if __name__ == '__main__': unittest.main()
