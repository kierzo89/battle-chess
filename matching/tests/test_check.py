import importlib.util
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

PROJECT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('matching_check', PROJECT / 'check.py')
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


class CheckerTests(unittest.TestCase):
    def test_exact_length_and_each_byte_are_required(self):
        self.assertEqual(check.compare(b'\xc3', b'\xc3')['status'], 'asm_matched')
        for actual in (b'', b'\xc3\x90', b'\xcb'):
            self.assertEqual(check.compare(b'\xc3', actual)['status'], 'mismatch')
        self.assertEqual(check.compare(b'\x55\xc3', b'\x55\xcb')['first_difference'], 1)

    def test_duplicate_and_overlapping_extents_rejected(self):
        units = json.loads((PROJECT / 'config/units.json').read_text())
        for extra in (units[0], units[0] | {'id': 'another'}):
            with self.assertRaises(ValueError):
                check.validate_units(units + [extra], 82903)

    def test_invalid_extents_and_c_claim_rejected(self):
        unit = json.loads((PROJECT / 'config/units.json').read_text())[0]
        for change in ({'size': 0}, {'image_offset': '-1'}, {'size': 999999}, {'backend': 'nasm-bin'}):
            with self.assertRaises(ValueError):
                check.validate_units([unit | change], 82903)

    def test_target_hash_is_mandatory(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'CHESS.EXE'
            p.write_bytes(b'MZ wrong revision')
            with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
                check.pinned(p, '0' * 64)

    def test_cli_wrong_target_invalidates_previous_success_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            target = tmp / 'wrong.exe'
            target.write_bytes(b'wrong revision')
            (tmp / 'report.json').write_text('{"status": "asm_matched"}')
            (tmp / 'functions.csv').write_text('stale successful results')
            result = subprocess.run([sys.executable, str(PROJECT / 'check.py'),
                                     '--target', str(target), '--output', str(tmp)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads((tmp / 'report.json').read_text())['status'], 'error')
            self.assertFalse((tmp / 'functions.csv').exists())

    def test_mz_header_and_module_bounds(self):
        data = bytearray(64)
        data[:2] = b'MZ'
        struct.pack_into('<4H', data, 2, 64, 1, 0, 2)
        self.assertEqual(check.mz_image(data), (32, data[32:]))
        for bad in (b'', b'MZ', bytes(64)):
            with self.assertRaises(ValueError):
                check.mz_image(bad)
        struct.pack_into('<H', data, 6, 1)
        with self.assertRaisesRegex(ValueError, 'relocations'):
            check.mz_image(data)

    @unittest.skipUnless(shutil.which('nasm'), 'NASM required')
    def test_real_assembly_build_and_mutation_regression(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            project = tmp / 'matching'
            shutil.copytree(PROJECT / 'asm', project / 'asm')
            unit = json.loads((PROJECT / 'config/units.json').read_text())[0]
            unit.update(language='asm', backend='nasm-bin', source='asm/min_i16.asm')
            config = json.loads((PROJECT / 'config/target.json').read_text())
            exe = check.pinned(PROJECT.parent / 'CHESS.EXE', config['sha256'])
            _, image = check.mz_image(exe)
            self.assertEqual(check.build_unit(unit, image, project, 'nasm')['status'], 'asm_matched')
            src = project / unit['source']
            src.write_text(src.read_text().replace('jle short', 'jge short'))
            self.assertEqual(check.build_unit(unit, image, project, 'nasm')['status'], 'mismatch')
            src.write_text('this is not assembly\n')
            self.assertEqual(check.build_unit(unit, image, project, 'nasm')['status'], 'build_error')

    @unittest.skipUnless(shutil.which('nasm') and shutil.which('dosbox') and (PROJECT / 'toolchains/msc500').exists(), 'Pinned toolchains required')
    def test_generated_status_counts_real_c_separately_and_full_file_is_incomplete(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = check.run(PROJECT.parent, PROJECT, PROJECT.parent / 'CHESS.EXE', Path(tmp), 'nasm')
            self.assertGreaterEqual(r['summary']['c_matched_functions'], 6)
            self.assertGreaterEqual(r['summary']['c_matched_bytes'], 122)
            self.assertEqual(r['summary']['asm_matched_bytes'], 994)
            self.assertEqual(r['summary']['runtime_matched_units'], 54)
            self.assertEqual(r['summary']['runtime_matched_bytes'], 4696)
            self.assertEqual(r['summary']['runtime_matched_data_bytes'], 250)
            self.assertEqual(r['summary']['verified_image_span_bytes'] - r['summary']['verified_file_span_bytes'],
                             r['summary']['runtime_matched_data_bytes'] + r['summary']['source_data_bytes'] + r['summary']['asm_data_matched_bytes']
                             + sum(u['size'] for u in r['units'] if u['status'] == 'asm_code_matched'
                                   and u.get('reference_region') == 'exepack-expanded'))
            self.assertEqual(r['summary']['runtime_emitted_mz_relocations'], 3)
            runtime_cov = json.loads((Path(tmp) / 'relocation_coverage.json').read_text())
            self.assertEqual(runtime_cov['runtime_emitted_sites'], [0xea91, 0xeb1c, 0x61614])
            crt0dat = next(u for u in r['units'] if u['id'] == 'runtime_data_crt0dat_s3')
            self.assertEqual([f['mz_segment_relocation_image_offset']
                              for f in crt0dat['relocations']
                              if 'mz_segment_relocation_image_offset' in f], [0x61614])
            self.assertGreaterEqual(r['summary']['rea_confirmed_extents'], 11)
            self.assertEqual(r['summary']['failed_units'], 0)
            self.assertIsNone(r['summary']['whole_program_completion_percent'])
            self.assertEqual(r['summary']['legacy_candidates'], 371)
            self.assertFalse(r['summary']['full_executable_match'])
            cov = json.loads((Path(tmp) / 'file_coverage.json').read_text())
            self.assertEqual(cov['ranges'][0]['start'], 0)
            self.assertEqual(cov['ranges'][-1]['end'], 83415)
            self.assertTrue(all(a['end'] == b['start'] for a,b in zip(cov['ranges'], cov['ranges'][1:])))

    def test_rea_evidence_rejects_wrong_target_or_extent(self):
        unit = json.loads((PROJECT / 'config/units.json').read_text())[0]
        sha = json.loads((PROJECT / 'config/target.json').read_text())['sha256']
        self.assertTrue(check.validate_rea_extent(unit, PROJECT, sha).startswith('ev_'))
        with self.assertRaisesRegex(ValueError, 'target/profile mismatch'):
            check.validate_rea_extent(unit, PROJECT, '0' * 64)
        with self.assertRaisesRegex(ValueError, 'extent mismatch'):
            check.validate_rea_extent(unit | {'size': unit['size'] - 1}, PROJECT, sha)

    def test_c_source_race_does_not_earn_matching_credit(self):
        unit = next(u for u in json.loads((PROJECT / 'config/units.json').read_text()) if u['language'] == 'c')
        with patch.object(check, 'compile_c', return_value=SimpleNamespace(source_sha256='0' * 64)):
            result = check.build_unit(unit, bytes(82903), PROJECT, 'nasm')
        self.assertEqual(result['status'], 'build_error')
        self.assertIn('source changed', result['error'])

    @unittest.skipUnless(shutil.which('nasm'), 'NASM required')
    def test_require_complete_cli_does_not_pass_with_only_assembly(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(PROJECT / 'check.py'),
                                     '--require-complete', '--output', tmp],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)

    @unittest.skipUnless(shutil.which('dosbox') and (PROJECT / 'toolchains/msc500').exists(), 'Pinned compiler required')
    def test_c_requires_compiler_extent_and_wrong_link_address_fails(self):
        # This checks the ordinary external-field backend independently of
        # the current compiler-owned literal migration. Keep the original
        # source/metadata fixture and all original byte/CodeView assertions.
        unit = json.loads((PROJECT / 'tests/fixtures/pop_value_external_231.json').read_text())
        cfg = json.loads((PROJECT / 'config/target.json').read_text())
        _, image = check.mz_image(check.pinned(PROJECT.parent / 'CHESS.EXE', cfg['sha256']))
        bad = unit | {'externals': unit['externals'] | {'_exhausted_message': 0x4d6c}}
        result = check.build_unit(bad, image, PROJECT, 'nasm')
        self.assertEqual(result['status'], 'mismatch')
        self.assertEqual(result['first_difference'], 23)
        no_debug = unit | {'flags': ['/AS', '/Ox']}
        result = check.build_unit(no_debug, image, PROJECT, 'nasm')
        self.assertEqual(result['status'], 'build_error')
        self.assertIn('CodeView', result['error'])

    @unittest.skipUnless(shutil.which('dosbox') and (PROJECT / 'toolchains/msc500').exists(), 'Pinned compiler required')
    def test_far_alias_is_compared_byte_for_byte(self):
        unit = next(u for u in json.loads((PROJECT / 'config/units.json').read_text()) if u['id'] == 'turn_7ddb')
        cfg = json.loads((PROJECT / 'config/target.json').read_text())
        data = check.pinned(PROJECT.parent / 'CHESS.EXE', cfg['sha256'])
        _, image = check.mz_image(data)
        cache = {}
        good = check.build_unit(unit, image, PROJECT, 'nasm', cache)
        self.assertEqual(good['status'], 'c_matched')
        far_fields = [r for r in good['relocations'] if r['mode'] == 'far16_pointer']
        self.assertEqual(far_fields[0]['mz_segment_relocation_image_offset'], 0x7e22)
        self.assertIn(0x7e22, check.unpack_exepack(data).relocations)
        # Same real-mode linear target, different pointer bytes: must fail.
        wrong = unit | {'externals': unit['externals'] | {'_draw_fce8': {'segment': 0, 'offset': 0xfce8}}}
        bad = check.build_unit(wrong, image, PROJECT, 'nasm', cache)
        self.assertEqual(bad['status'], 'mismatch')
        self.assertEqual(bad['first_difference'], 69)


if __name__ == '__main__':
    unittest.main()
