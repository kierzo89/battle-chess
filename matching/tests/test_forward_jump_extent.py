"""Fail-closed proof of the two-byte dead short jump in far min/max output."""
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


class ForwardJumpExtentTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.project = Path(self.scratch.name)
        self.configure('max')

    def configure(self, name):
        image, gap, next_name = ((0xfe0c, 0x1fe1f, 'min') if name == 'max'
                                  else (0xfe2b, 0x1fe3e, 'parity'))
        self.paths = {'body': 'evidence/rea_evaluation_'+name+'_far.json',
                      'raw': 'evidence/rea_evaluation_'+name+'_fullspan.json',
                      'next': 'evidence/rea_evaluation_'+next_name+'_far.json',
                      'xref0': 'evidence/rea_evaluation_gap_xrefs_'+format(gap, 'x')+'.json',
                      'xref1': 'evidence/rea_evaluation_gap_xrefs_'+format(gap+1, 'x')+'.json'}
        self.evidence = {k: json.loads((PROJECT / p).read_text()) for k, p in self.paths.items()}
        self.unit = {'language': 'c', 'symbol': '_evaluation_'+name,
                     'image_offset': hex(image), 'size': 31,
                     'rea_evidence': self.paths['body'], 'extended_extent': {
                         'kind': 'unreachable_forward_jump_gap_v1',
                         'raw_span_evidence': self.paths['raw'],
                         'next_entry_evidence': self.paths['next'],
                         'gap_xref_evidence': [self.paths['xref0'], self.paths['xref1']]}}
        self.emitted = {'symbol': self.unit['symbol'], 'size': 31, 'offset': 0,
                        'end': 31, 'boundary': 'codeview3_procedure', 'fixups': []}
        self.linked = bytes.fromhex(self.evidence['raw']['normalized_result']['bytes_hex'])[:31]

    def validate(self):
        for k, p in self.paths.items():
            path = self.project / p
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(self.evidence[k]))
        return validate_extended_extent(self.unit, self.project, TARGET, self.emitted, self.linked)

    def test_both_complete_far_comparisons_and_actual_next_body_forms(self):
        for name, gap, next_entry in [('max', '0x1fe1f', '0x1fe2b'), ('min', '0x1fe3e', '0x1fe4a')]:
            self.configure(name)
            result = self.validate()
            self.assertEqual(result['span_bytes'], 31)
            self.assertEqual(result['gap_address'], gap)
            self.assertEqual(result['gap_hex'], 'eb04')
            self.assertEqual(result['gap_size'], 2)
            self.assertEqual(result['predecessor_target'], result['dead_jump_target'])
            self.assertEqual(result['next_entry'], next_entry)
            self.assertEqual(len(result['gap_xref_evidence_ids']), 2)

    def test_only_exact_ordinary_c_proof_fields_and_span_are_admitted(self):
        for change in ({'language': 'asm'}, {'size': 29}, {'size': 32}):
            self.configure('max'); self.unit.update(change)
            with self.subTest(change=change), self.assertRaises(ValueError): self.validate()
        self.configure('max'); self.unit['extended_extent']['unexpected'] = True
        with self.assertRaises(ValueError): self.validate()
        self.configure('max'); self.unit['extended_extent']['raw_span_evidence'] = '../outside.json'
        with self.assertRaisesRegex(ValueError, 'outside'): self.validate()

    def test_targets_profiles_operations_and_digest_must_match_for_all_evidence(self):
        for key in self.paths:
            for mutation in ('target', 'profile', 'operation', 'digest'):
                self.configure('max'); e = self.evidence[key]
                if mutation == 'target': e['subject']['digest']['sha256'] = '0'*64
                if mutation == 'profile': e['analysis_profile']['parameters']['load_segment'] = '0x2000'
                if mutation == 'operation': e['operation'] = 'not_the_operation'
                if mutation == 'digest': e['analysis_profile']['digest'] = '0'*64
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError): self.validate()

    def test_raw_must_be_exact_complete_and_cover_full_adjacent_function(self):
        for mutation in ('incomplete', 'length', 'address', 'short_next', 'different_linked'):
            self.configure('max'); r = self.evidence['raw']['normalized_result']
            if mutation == 'incomplete': r['complete'] = False
            if mutation == 'length': r['requested_bytes'] -= 1
            if mutation == 'address': self.evidence['raw']['parameters']['address'] = '0x1fe0d'
            if mutation == 'short_next':
                r['bytes_hex'] = r['bytes_hex'][:34*2]
                r['requested_bytes'] = r['returned_bytes'] = self.evidence['raw']['parameters']['length'] = 34
            if mutation == 'different_linked': self.linked = b'\x90' + self.linked[1:]
            with self.subTest(mutation=mutation), self.assertRaises(ValueError): self.validate()

    def test_every_branch_gap_and_abi_byte_remains_narrow_even_if_raw_and_linked_agree(self):
        for offset in (0, 13, 14, 17, 18, 19, 20, 21, 23, 24, 25, 30):
            self.configure('max'); r = self.evidence['raw']['normalized_result']
            blob = bytearray.fromhex(r['bytes_hex']); blob[offset] = 0x90
            r['bytes_hex'] = blob.hex(); self.linked = bytes(blob[:31])
            with self.subTest(offset=offset), self.assertRaisesRegex(ValueError, 'return shape'): self.validate()

    def test_cfg_must_be_four_closed_blocks_with_no_gap_overlap_or_successor(self):
        for mutation in ('incoming_gap', 'overlap_gap', 'wrong_predecessor', 'missing', 'duplicate', 'open_exit'):
            self.configure('max'); blocks = self.evidence['body']['normalized_result']['basic_blocks']
            if mutation == 'incoming_gap': blocks[0]['successors'].append('0x1fe20')
            if mutation == 'overlap_gap': blocks[1]['end'] = '0x1fe20'
            if mutation == 'wrong_predecessor': blocks[1]['successors'] = ['0x1fe21']
            if mutation == 'missing': blocks.pop()
            if mutation == 'duplicate': blocks.append(copy.deepcopy(blocks[0]))
            if mutation == 'open_exit': blocks[-1]['successors'] = ['0x1fe2b']
            with self.subTest(mutation=mutation), self.assertRaises(ValueError): self.validate()

    def test_gap_global_xrefs_are_required_for_each_byte_and_must_be_empty(self):
        for mutation in ('missing', 'duplicate', 'wrong_address', 'reference', 'dossier_incoming'):
            self.configure('max')
            if mutation == 'missing': self.unit['extended_extent']['gap_xref_evidence'].pop()
            if mutation == 'duplicate': self.unit['extended_extent']['gap_xref_evidence'][1] = self.paths['xref0']
            if mutation == 'wrong_address': self.evidence['xref1']['parameters']['address'] = '0x1fe21'
            if mutation == 'reference': self.evidence['xref0']['normalized_result'] = ['incoming jump']
            if mutation == 'dossier_incoming':
                self.evidence['body']['normalized_result']['incoming_references'].append({'target_address': '0x1fe1f'})
            with self.subTest(mutation=mutation), self.assertRaises(ValueError): self.validate()

    def test_body_ranges_and_adjacent_next_must_be_complete_consistent_and_contain_entry(self):
        for mutation in ('body_gap', 'body_total', 'next_address', 'next_entry', 'next_flag', 'next_total', 'next_span'):
            self.configure('max'); current = self.evidence['body']['normalized_result']['procedure']['body']
            proc = self.evidence['next']['normalized_result']['procedure']; body = proc['body']
            if mutation == 'body_gap': current['ranges'][0]['end'] = '0x1fe1f'
            if mutation == 'body_total': current['total_bytes'] = 31
            if mutation == 'next_address': proc['address'] = '0x1fe2c'
            if mutation == 'next_entry': body['contains_entry'] = False
            if mutation == 'next_flag': body['non_contiguous'] = False  # actual min is disjoint; do not fabricate contiguous.
            if mutation == 'next_total': body['total_bytes'] = 31
            if mutation == 'next_span': body['span_bytes'] = 29
            with self.subTest(mutation=mutation), self.assertRaises(ValueError): self.validate()

    def test_full_independent_codeview_length_and_no_fixups_are_mandatory(self):
        for changes in ({'size': 29}, {'end': 29}, {'symbol': '_other'}, {'fixups': [object()]},
                        {'boundary': 'next_public_or_segment_end'}):
            self.configure('min'); self.emitted.update(changes)
            with self.subTest(changes=changes), self.assertRaisesRegex(ValueError, 'CodeView'): self.validate()


if __name__ == '__main__': unittest.main()
