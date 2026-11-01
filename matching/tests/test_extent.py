"""Fail-closed tests for the explicitly proved unreachable-return gap only."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from extent import validate_extended_extent

TARGET = 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
PATHS = {'body': 'evidence/rea_repetition_9c34.json',
         'raw': 'evidence/rea_repetition_9c34_fullspan.json',
         'next': 'evidence/rea_repetition_next_9db3.json'}


class ExtendedExtentTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.project = Path(self.scratch.name)
        self.evidence = {k: json.loads((PROJECT / v).read_text()) for k, v in PATHS.items()}
        self.unit = {'language': 'c', 'symbol': '_repetition_9c34',
                     'image_offset': '0x9c34', 'size': 383,
                     'rea_evidence': PATHS['body'], 'extended_extent': {
                         'kind': 'unreachable_return_gap_v1',
                         'raw_span_evidence': PATHS['raw'],
                         'next_entry_evidence': PATHS['next']}}
        self.emitted = {'symbol': '_repetition_9c34', 'size': 383,
                        'offset': 0, 'end': 383, 'boundary': 'codeview3_procedure'}
        self.linked = bytes.fromhex(self.evidence['raw']['normalized_result']['bytes_hex'])[:383]

    def validate(self):
        for key, relative in PATHS.items():
            path = self.project / relative
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_text(json.dumps(self.evidence[key]))
        return validate_extended_extent(self.unit, self.project, TARGET, self.emitted, self.linked)

    def test_retained_proof_covers_full_compiler_span(self):
        result = self.validate()
        self.assertEqual(result['span_bytes'], 383)
        self.assertEqual(result['gap_address'], '0x19da9')
        self.assertEqual(result['gap_hex'], '8b46feeb00')
        self.assertEqual(result['predecessor_target'], '0x19ca4')
        self.assertEqual(result['next_entry'], '0x19db3')

    def test_missing_or_unknown_proof_is_not_a_general_relaxation(self):
        for proof in [None, {}, {'kind': 'generic_gap'}]:
            with self.subTest(proof=proof):
                self.unit['extended_extent'] = proof
                with self.assertRaises(ValueError):
                    self.validate()

    def test_missing_evidence_and_path_escape_rejected(self):
        for value in ['evidence/missing.json', '../outside.json']:
            self.unit['extended_extent']['raw_span_evidence'] = value
            with self.subTest(value=value), self.assertRaises((ValueError, FileNotFoundError)):
                self.validate()

    def test_target_profile_and_operation_must_match(self):
        original = copy.deepcopy(self.evidence)
        for key in PATHS:
            for kind in ['target', 'profile', 'operation']:
                self.evidence = copy.deepcopy(original)
                if kind == 'target': self.evidence[key]['subject']['digest']['sha256'] = '0'*64
                if kind == 'profile': self.evidence[key]['analysis_profile']['parameters']['load_segment'] = '0'
                if kind == 'operation': self.evidence[key]['operation'] = 'other'
                with self.subTest(key=key, kind=kind), self.assertRaises(ValueError):
                    self.validate()

    def test_raw_truncation_and_any_byte_mismatch_rejected(self):
        original = copy.deepcopy(self.evidence)
        for kind in ['incomplete', 'truncated', 'gap', 'ordinary_byte']:
            self.evidence = copy.deepcopy(original)
            n = self.evidence['raw']['normalized_result']
            if kind == 'incomplete': n['complete'] = False
            if kind == 'truncated': n['bytes_hex'] = n['bytes_hex'][:-2]
            if kind == 'gap': n['bytes_hex'] = n['bytes_hex'][:373*2]+'90'+n['bytes_hex'][374*2:]
            if kind == 'ordinary_byte': n['bytes_hex'] = '90'+n['bytes_hex'][2:]
            with self.subTest(kind=kind), self.assertRaises(ValueError): self.validate()

    def test_cfg_entry_into_gap_rejected(self):
        self.evidence['body']['normalized_result']['basic_blocks'][0]['successors'].append('0x19da9')
        with self.assertRaisesRegex(ValueError, 'branches into'): self.validate()

    def test_wrong_gap_or_branch_bytes_rejected_even_if_linked_agrees(self):
        original = copy.deepcopy(self.evidence)
        linked = self.linked
        for offset in [370, 373]:
            self.evidence = copy.deepcopy(original)
            self.linked = linked
            raw = self.evidence['raw']['normalized_result']
            blob = bytearray.fromhex(raw['bytes_hex']); blob[offset] = 0x90
            raw['bytes_hex'] = blob.hex(); self.linked = bytes(blob[:383])
            with self.subTest(offset=offset), self.assertRaises(ValueError): self.validate()

    def test_next_entry_must_be_adjacent(self):
        self.evidence['next']['normalized_result']['procedure']['address'] = '0x19db4'
        with self.assertRaisesRegex(ValueError, 'next retained function'): self.validate()

    def test_independent_codeview_extent_is_mandatory(self):
        for changes in [{'size': 378}, {'end': 378}, {'boundary': 'next_public_or_segment_end'},
                        {'symbol': '_other'}]:
            current = dict(self.emitted); self.emitted.update(changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError): self.validate()
            self.emitted = current


if __name__ == '__main__': unittest.main()
