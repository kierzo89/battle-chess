"""Provenance and complete-byte validation of expanded-image references."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
import reference


@unittest.skipUnless((PROJECT.parent / 'CHESS.EXE').exists(), 'Pinned original required')
class ExpandedReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = (PROJECT.parent / 'CHESS.EXE').read_bytes()
        cls.context = reference.build_reference(cls.original)
        cls.profiles = json.loads((PROJECT / 'evidence/runtime-data-members.json').read_text())['members']

    def example(self):
        profile = next(p for p in self.profiles if p['name'] == 'days.c')
        unit = {'image_offset': hex(profile['origin']), 'size': profile['size'], 'reference_region': 'exepack-expanded'}
        evidence = json.loads((PROJECT / profile['rea_evidence']).read_text())
        linked = self.context['image'][profile['origin']:profile['origin'] + profile['size']]
        return evidence, unit, linked

    def test_factory_checks_original_and_deterministic_carrier(self):
        self.assertEqual(len(self.context['image']), 401131)
        self.assertEqual(self.context['prefix_size'], 0x110dc)
        self.assertEqual(len(self.context['relocations']), 173)
        self.assertEqual(self.context['carrier_sha256'], reference.CARRIER_SHA256)
        with self.assertRaisesRegex(ValueError, 'original SHA'):
            reference.build_reference(self.original[:-1])
        fake = Mock()
        fake.analysis_mz.return_value = b'changed analysis carrier'
        with patch.object(reference, 'unpack_exepack', return_value=fake):
            with self.assertRaisesRegex(ValueError, 'carrier SHA'):
                reference.build_reference(self.original)

    def test_every_independently_initialized_data_read_is_complete_and_exact(self):
        for profile in self.profiles:
            with self.subTest(member=profile['name']):
                unit = {'image_offset': hex(profile['origin']), 'size': profile['size'], 'reference_region': 'exepack-expanded'}
                evidence = json.loads((PROJECT / profile['rea_evidence']).read_text())
                linked = self.context['image'][profile['origin']:profile['origin'] + profile['size']]
                self.assertEqual(reference.validate_expanded_read(evidence, unit, linked, self.context), evidence['evidence_id'])

    def test_wrong_subject_profile_region_or_context_fails(self):
        evidence, unit, linked = self.example()
        for path, value in [('subject', reference.ORIGINAL_SHA256), ('load', '0x2000'), ('language', 'x86:LE:32:default')]:
            wrong = deepcopy(evidence)
            if path == 'subject':
                wrong['subject']['digest']['sha256'] = value
            elif path == 'load':
                wrong['analysis_profile']['parameters']['load_segment'] = value
            else:
                wrong['analysis_profile']['parameters']['language_id'] = value
            with self.assertRaisesRegex(ValueError, 'target/profile'):
                reference.validate_expanded_read(wrong, unit, linked, self.context)
        with self.assertRaisesRegex(ValueError, 'explicit expanded'):
            reference.validate_expanded_read(evidence, unit | {'reference_region': 'disk'}, linked, self.context)
        with self.assertRaisesRegex(ValueError, 'context provenance'):
            reference.validate_expanded_read(evidence, unit, linked, self.context | {'carrier_sha256': '0' * 64})

    def test_wrong_bytes_lengths_addresses_and_partial_reads_fail(self):
        evidence, unit, linked = self.example()
        for change in ({'complete': False}, {'returned_bytes': unit['size'] - 1},
                       {'requested_bytes': unit['size'] + 1}, {'address': '0x71743'},
                       {'bytes_hex': '00' * unit['size']}, {'bytes_hex': 'not hex'}):
            wrong = deepcopy(evidence)
            wrong['normalized_result'].update(change)
            with self.assertRaises(ValueError):
                reference.validate_expanded_read(wrong, unit, linked, self.context)
        with self.assertRaisesRegex(ValueError, 'complete unit extent'):
            reference.validate_expanded_read(evidence, unit, linked[:-1], self.context)
        with self.assertRaisesRegex(ValueError, 'raw-byte comparison'):
            reference.validate_expanded_read(evidence, unit, bytes([linked[0] ^ 1]) + linked[1:], self.context)

    def test_relocated_words_and_crossing_word_extents_are_rejected_without_masking(self):
        evidence, _, _ = self.example()
        self.assertIn(0x61580, self.context['relocations'])
        for origin, size in [(0x61580, 2), (0x61581, 1)]:
            unit = {'image_offset': hex(origin), 'size': size, 'reference_region': 'exepack-expanded'}
            linked = self.context['image'][origin:origin + size]
            with self.assertRaisesRegex(ValueError, 'overlaps MZ relocation'):
                reference.validate_expanded_read(evidence, unit, linked, self.context)

    def crt0_data(self):
        bundle = json.loads((PROJECT / 'evidence/rea-crt0-full-data.json').read_text())
        evidence = next(r for r in bundle['records'] if r['operation'] == 'read_bytes')
        unit = {'image_offset': '0x61578', 'size': 88, 'reference_region': 'exepack-expanded'}
        # Comparison fixture only: this test does not assert generation credit.
        linked = self.context['image'][0x61578:0x615d0]
        return evidence, unit, linked

    def test_crt0_full_data_forward_loader_addition_and_independent_emission_proof(self):
        evidence, unit, linked = self.crt0_data()
        proof = json.loads((PROJECT / 'evidence/crt0-data-experiment.json').read_text())
        self.assertEqual(proof['data_segment']['initialized_ranges'], [[0, 10], [86, 88]])
        self.assertEqual(proof['data_segment']['reserved_no_data_ranges'], [[10, 86]])
        controls = [r for r in proof['link_runs'] if r['status'] == 'linked']
        self.assertEqual(len(controls), 3)
        for control in controls:
            self.assertFalse(control['reference_read_or_mounted'])
            self.assertEqual(bytes.fromhex(control['crt0_data_hex'])[10:86], bytes(76))
            self.assertIn(control['crt0_data_image_offset'] + 8, control['relocation_sites'])
        self.assertEqual(linked[8:10], bytes.fromhex('c25c'))
        self.assertEqual(bytes.fromhex(evidence['normalized_result']['bytes_hex'])[8:10], bytes.fromhex('c26c'))
        before = deepcopy((evidence, unit, self.context))
        self.assertEqual(reference.validate_expanded_read(
            evidence, unit, linked, self.context, emitted_mz_sites=[0x61580]), evidence['evidence_id'])
        self.assertEqual((evidence, unit, self.context), before)
        with self.assertRaisesRegex(ValueError, 'overlaps MZ relocation'):
            reference.validate_expanded_read(evidence, unit, linked, self.context)

    def test_missing_extra_and_outside_emitted_sites_are_rejected(self):
        evidence, unit, linked = self.crt0_data()
        for sites in ([], [0x61580, 0x61582], [0x61582]):
            with self.subTest(sites=sites), self.assertRaisesRegex(ValueError, 'sites differ'):
                reference.validate_expanded_read(evidence, unit, linked, self.context, emitted_mz_sites=sites)
        for sites in ([0x61577, 0x61580], [0x61580, 0x615cf], [0x61580, -1]):
            with self.subTest(sites=sites), self.assertRaisesRegex(ValueError, 'out-of-extent'):
                reference.validate_expanded_read(evidence, unit, linked, self.context, emitted_mz_sites=sites)
        evidence, unit, linked = self.example()
        self.assertEqual(reference.validate_expanded_read(
            evidence, unit, linked, self.context, emitted_mz_sites=[]), evidence['evidence_id'])
        with self.assertRaisesRegex(ValueError, 'sites differ'):
            reference.validate_expanded_read(evidence, unit, linked, self.context,
                                            emitted_mz_sites=[int(unit['image_offset'], 0)])

    def test_crossing_original_words_fail_even_with_explicit_sites(self):
        evidence, _, _ = self.crt0_data()
        for origin, size in ((0x6157f, 2), (0x61581, 1)):
            unit = {'image_offset': origin, 'size': size, 'reference_region': 'exepack-expanded'}
            linked = self.context['image'][origin:origin + size]
            for sites in ([], [0x61580]):
                with self.subTest(origin=origin, sites=sites), self.assertRaisesRegex(ValueError, 'crossing'):
                    reference.validate_expanded_read(evidence, unit, linked, self.context, emitted_mz_sites=sites)

    def test_relocated_path_requires_unrelocated_source_bytes_and_all_raw_bytes(self):
        evidence, unit, linked = self.crt0_data()
        loaded = bytes.fromhex(evidence['normalized_result']['bytes_hex'])
        for wrong_source in (loaded, bytes([linked[0] ^ 1]) + linked[1:]):
            with self.assertRaisesRegex(ValueError, 'unrelocated source'):
                reference.validate_expanded_read(evidence, unit, wrong_source, self.context,
                                                emitted_mz_sites=[0x61580])
        for wrong_bytes in (linked, loaded[:8] + bytes.fromhex('c27c') + loaded[10:],
                            bytes([loaded[0] ^ 1]) + loaded[1:]):
            wrong = deepcopy(evidence)
            wrong['normalized_result']['bytes_hex'] = wrong_bytes.hex()
            with self.assertRaisesRegex(ValueError, 'complete raw-byte comparison'):
                reference.validate_expanded_read(wrong, unit, linked, self.context, emitted_mz_sites=[0x61580])

    def test_relocated_path_retains_exact_carrier_and_load_profile(self):
        evidence, unit, linked = self.crt0_data()
        for key, value in (('load_segment', '0x2000'), ('language_id', 'x86:LE:32:default'),
                           ('target_format', 'dos-com')):
            wrong = deepcopy(evidence)
            wrong['analysis_profile']['parameters'][key] = value
            with self.assertRaisesRegex(ValueError, 'target/profile'):
                reference.validate_expanded_read(wrong, unit, linked, self.context, emitted_mz_sites=[0x61580])
        wrong = deepcopy(evidence)
        wrong['subject']['digest']['sha256'] = reference.ORIGINAL_SHA256
        with self.assertRaisesRegex(ValueError, 'target/profile'):
            reference.validate_expanded_read(wrong, unit, linked, self.context, emitted_mz_sites=[0x61580])

    def test_emitted_sites_are_explicit_unique_integer_offsets(self):
        evidence, unit, linked = self.crt0_data()
        for sites in ([0x61580, 0x61580], ['0x61580'], [True], 0x61580, iter([0x61580])):
            with self.subTest(sites=sites), self.assertRaisesRegex(ValueError, 'emitted MZ sites'):
                reference.validate_expanded_read(evidence, unit, linked, self.context, emitted_mz_sites=sites)


if __name__ == '__main__':
    unittest.main()
