"""Corrected-CS evidence is accepted only for the fixed complete FE59 span."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from extent import validate_extended_extent
from segmented_extent import TARGET

PATHS = {'weak': 'evidence/rea_full_evaluation_fe59.json',
         'carrier': 'evidence/evaluation-context-carriers.json',
         'body': 'evidence/rea_full_evaluation_rebased_callee.json',
         'raw': 'evidence/rea_full_evaluation_rebased_raw.json',
         'next': 'evidence/rea_evaluate_pawn_bit_count.json',
         'xref0': 'evidence/rea_full_evaluation_gap_6c2.json',
         'xref1': 'evidence/rea_full_evaluation_gap_6c3.json'}
META = {'kind': 'segmented_evaluation_v1', 'carrier_evidence': PATHS['carrier'],
        'derived_body_evidence': PATHS['body'], 'raw_span_evidence': PATHS['raw'],
        'next_entry_evidence': PATHS['next'],
        'gap_xref_evidence': [PATHS['xref0'], PATHS['xref1']]}


class SegmentedExtentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / 'matching'
        self.project.mkdir()
        shutil.copyfile(PROJECT.parent/'CHESS.EXE', self.project.parent/'CHESS.EXE')
        self.evidence = {k: json.loads((PROJECT/v).read_text()) for k, v in PATHS.items()}
        self.unit = {'language': 'c', 'image_offset': '0xfe59', 'size': 2803,
                     'code_address': {'segment': 0xfdf, 'offset': 0x69},
                     'symbol': '_full_evaluation', 'rea_evidence': PATHS['weak'],
                     'extended_extent': copy.deepcopy(META)}
        # Synthetic CV metadata exercises the contract; this fixture is not
        # compilation evidence and never registers/credits original bytes.
        self.emitted = {'symbol': '_full_evaluation', 'size': 2803, 'offset': 26,
                        'end': 2829, 'boundary': 'codeview3_procedure'}
        self.linked = bytes.fromhex(self.evidence['raw']['normalized_result']['bytes_hex'])[:2803]

    def validate(self, target=TARGET):
        for key, relative in PATHS.items():
            path = self.project / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(self.evidence[key]))
        return validate_extended_extent(self.unit, self.project, target, self.emitted, self.linked)

    def test_fixed_proof_validates_complete_span(self):
        result = self.validate()
        self.assertEqual(result['span_bytes'], 2803)
        self.assertEqual(result['reachable_bytes'], 2801)
        self.assertEqual(result['cfg_blocks'], 265)
        self.assertEqual(result['gap_address'], '0x104b2')
        self.assertEqual(result['next_entry'], '0x1094c')

    def test_unit_cannot_generalize_rebasing_or_gap_policy(self):
        base = copy.deepcopy(self.unit)
        for field, value in [('language', 'asm'), ('image_offset', '0xfe58'), ('size', 2801),
                             ('code_address', {'segment': 0x1000, 'offset': 0xfe59})]:
            self.unit = copy.deepcopy(base)
            self.unit[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError): self.validate()

    def test_wrong_original_hash_and_target_rejected(self):
        with self.assertRaises(ValueError): self.validate('0'*64)
        original = self.project.parent/'CHESS.EXE'
        data = bytearray(original.read_bytes()); data[512+0xfe59] ^= 1
        original.write_bytes(data)
        with self.assertRaises(ValueError): self.validate()

    def test_missing_proof_paths_and_extra_fields_rejected(self):
        self.unit['extended_extent']['arbitrary'] = True
        with self.assertRaises(ValueError): self.validate()
        del self.unit['extended_extent']['arbitrary']
        self.unit['extended_extent']['carrier_evidence'] = '../outside.json'
        with self.assertRaises(ValueError): self.validate()

    def test_carrier_hash_mapping_header_stub_rejected(self):
        base = copy.deepcopy(self.evidence)
        mutations = [('mapping', 'arbitrary'), ('original_code_sha256', '0'*64),
                     ('original_image_start', '0xfe00')]
        for field, value in mutations:
            self.evidence = copy.deepcopy(base); self.evidence['carrier'][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError): self.validate()
        for field, value in [('sha256', '0'*64), ('header_hex', '00'*32),
                             ('analysis_stub_hex', '90'*10), ('mz_sites', [3906])]:
            self.evidence = copy.deepcopy(base)
            self.evidence['carrier']['carriers'][1][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError): self.validate()

    def test_every_evidence_subject_profile_operation_bound(self):
        base = copy.deepcopy(self.evidence)
        for key in set(PATHS)-{'carrier'}:
            for mutation in ['digest', 'profile', 'operation']:
                self.evidence = copy.deepcopy(base); e = self.evidence[key]
                if mutation == 'digest': e['subject']['digest']['sha256'] = '0'*64
                if mutation == 'profile': e['analysis_profile']['parameters']['load_segment'] = '0'
                if mutation == 'operation': e['operation'] = 'other'
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError): self.validate()

    def test_raw_span_next48_and_any_linked_byte_must_match_original(self):
        base = copy.deepcopy(self.evidence)
        for index in [0, 0x106c2-0x10069, 2802, 2803, 2850]:
            self.evidence = copy.deepcopy(base)
            data = bytearray.fromhex(self.evidence['raw']['normalized_result']['bytes_hex'])
            data[index] ^= 1
            self.evidence['raw']['normalized_result']['bytes_hex'] = data.hex()
            with self.subTest(index=index), self.assertRaises(ValueError): self.validate()
        self.evidence = copy.deepcopy(base)
        self.linked = self.linked[:-1]
        with self.assertRaises(ValueError): self.validate()

    def test_incomplete_or_mapped_raw_read_rejected(self):
        base = copy.deepcopy(self.evidence)
        for field, value in [('complete', False), ('address', '0x1fe59'),
                             ('returned_bytes', 2803), ('requested_bytes', 2852)]:
            self.evidence = copy.deepcopy(base)
            self.evidence['raw']['normalized_result'][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError): self.validate()

    def test_exact_body_ranges_and_next_extent_required(self):
        base = copy.deepcopy(self.evidence)
        for key, field, value in [('body', 'total_bytes', 2803), ('body', 'span_bytes', 2801),
                                  ('next', 'total_bytes', 47), ('next', 'non_contiguous', True)]:
            self.evidence = copy.deepcopy(base)
            self.evidence[key]['normalized_result']['procedure']['body'][field] = value
            with self.subTest(key=key, field=field), self.assertRaises(ValueError): self.validate()

    def test_cfg_coverage_closure_and_gap_entries_rejected(self):
        base = copy.deepcopy(self.evidence)
        for kind in ['missing', 'hole', 'overlap', 'gap', 'external', 'unreachable', 'predecessor']:
            self.evidence = copy.deepcopy(base)
            blocks = self.evidence['body']['normalized_result']['basic_blocks']
            if kind == 'missing': blocks.pop()
            if kind == 'hole': blocks[0]['end'] = hex(int(blocks[0]['end'], 0)-1)
            if kind == 'overlap': blocks[1]['start'] = hex(int(blocks[1]['start'], 0)-1)
            if kind == 'gap': blocks[0]['successors'] = ['0x106c2']
            if kind == 'external': blocks[0]['successors'] = ['0x20000']
            if kind == 'unreachable': blocks[0]['successors'] = [blocks[0]['start']]
            if kind == 'predecessor':
                next(b for b in blocks if b['start']=='0x106c0')['successors'] = ['0x106c4']
            with self.subTest(kind=kind), self.assertRaises(ValueError): self.validate()

    def test_gap_needs_two_empty_distinct_global_xrefs(self):
        self.evidence['xref0']['normalized_result'] = ['incoming']
        with self.assertRaises(ValueError): self.validate()
        self.evidence['xref0']['normalized_result'] = []
        self.unit['extended_extent']['gap_xref_evidence'][1] = PATHS['xref0']
        with self.assertRaises(ValueError): self.validate()

    def test_incoming_gap_reference_rejected(self):
        self.evidence['body']['normalized_result']['incoming_references'].append({'target_address':'0x106c3'})
        with self.assertRaises(ValueError): self.validate()

    def test_fresh_cv_symbol_boundary_and_full_extent_required(self):
        base = copy.deepcopy(self.emitted)
        for field, value in [('symbol', '_other'), ('boundary', 'next_public'), ('size', 2801), ('end', 2828)]:
            self.emitted = copy.deepcopy(base); self.emitted[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError): self.validate()


if __name__ == '__main__':
    unittest.main()
