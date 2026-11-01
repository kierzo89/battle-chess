"""Canonical runtime backend freshness, classification and boundary policy."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
import check
from reference import build_reference
from setup_runtime import install, runtime_config, validate_runtime


@unittest.skipUnless((PROJECT / 'toolchains/runtime500/SLIBC.LIB').exists(), 'Pinned runtime installation required')
class RuntimeCheckerTests(unittest.TestCase):
    def setUp(self):
        self.units = [u for u in json.loads((PROJECT / 'config/units.json').read_text()) if u['language'] == 'runtime']
        self.sha = json.loads((PROJECT / 'config/target.json').read_text())['sha256']
        original = check.pinned(PROJECT.parent / 'CHESS.EXE', self.sha)
        self.image = check.mz_image(original)[1]
        self.reference = build_reference(original)

    def image_for(self, unit):
        return self.reference['image'] if unit.get('reference_region') == 'exepack-expanded' else self.image

    def test_full_runtime_builds_are_classified_separately_and_fresh(self):
        # The direct renderer covers54; CRT88 requires the separate fresh lifecycle.
        deferred = [u for u in self.units if u['id'] == 'runtime_data_crt0_s3']
        self.assertEqual(len(self.units), 55)
        self.assertEqual(len(deferred), 1)
        self.assertEqual((deferred[0]['member'], deferred[0]['runtime_kind'], deferred[0]['size']),
                         ('CRT0_DATA_3', 'initialized_data', 88))
        ordinary = [u for u in self.units if u['id'] != deferred[0]['id']]
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            results = [check.build_unit(u, self.image_for(u), PROJECT, 'unused', output=output) for u in ordinary]
            self.assertEqual(len(results), 54)
            self.assertEqual(sum(r['size'] for r in results), 4696)
            self.assertTrue(all(r['status'] == 'runtime_matched' and r['authored_c_credit'] == 0 for r in results))
            self.assertTrue(all(r['source'] in ('config/runtime500.json', 'config/runtime_libh.json', 'config/runtime_external3.json')
                                and 'compiler_flags' not in r for r in results))
            rejected = check.build_unit(deferred[0], self.image_for(deferred[0]), PROJECT, 'unused', output=output)
            self.assertEqual(rejected['status'], 'build_error')
            self.assertIn('hole or overlap in segment LEDATA', rejected['error'])
            self.assertFalse((output / 'runtime' / (deferred[0]['id'] + '.bin')).exists())
            unit = self.units[0]
            artifact = output / 'runtime' / (unit['id'] + '.bin')
            artifact.write_bytes(b'stale output must not earn credit')
            result = check.build_unit(unit, self.image, PROJECT, 'unused', output=output)
            self.assertEqual(result['status'], 'runtime_matched')
            self.assertEqual(hashlib.sha256(artifact.read_bytes()).hexdigest(), result['actual_sha256'])

    def test_runtime_full_segment_boundary_does_not_weaken_c_policy(self):
        from library16 import LibraryError
        deferred = [u for u in self.units if u['id'] == 'runtime_data_crt0_s3']
        self.assertEqual(len(deferred), 1)
        with self.assertRaisesRegex(LibraryError, 'hole or overlap in segment LEDATA'):
            check.validate_rea_extent(deferred[0], PROJECT, self.sha, self.reference)
        ordinary = [u for u in self.units if u['id'] != deferred[0]['id']]
        self.assertEqual(len(ordinary), 54)
        for unit in ordinary:
            self.assertTrue(check.validate_rea_extent(unit, PROJECT, self.sha, self.reference).startswith('ev_'))
            extent_error = 'runtime3 closed whole-unit identity' if unit['backend'] == 'msc500-authentic-external-runtime3-v1' else 'extent mismatch'
            with self.assertRaisesRegex(ValueError, extent_error):
                check.validate_rea_extent(unit | {'size': unit['size'] - 1}, PROJECT, self.sha, self.reference)
            with self.assertRaisesRegex(ValueError, 'target/profile mismatch'):
                check.validate_rea_extent(unit | {'language': 'c'}, PROJECT, self.sha, self.reference)
            result = check.build_unit(unit | {'symbol': '_invented'}, self.image_for(unit), PROJECT, 'unused')
            self.assertEqual(result['status'], 'build_error')
            symbol_error = 'runtime3 closed whole-unit identity' if unit['backend'] == 'msc500-authentic-external-runtime3-v1' else 'segment/public extent'
            self.assertIn(symbol_error, result['error'])

    def test_runtime_raw_evidence_and_library_tampering_are_rejected(self):
        unit = next(u for u in self.units if u['member'] == 'CRT0')
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / 'config').mkdir()
            (project / 'evidence').mkdir()
            shutil.copy(PROJECT / 'config/runtime500.json', project / 'config/runtime500.json')
            shutil.copytree(PROJECT / 'toolchains/runtime500', project / 'toolchains/runtime500')
            evidence = json.loads((PROJECT / unit['rea_evidence']).read_text())
            raw = evidence['normalized_result']['bytes_hex']
            evidence['normalized_result']['bytes_hex'] = ('00' if raw[:2] != '00' else 'ff') + raw[2:]
            (project / unit['rea_evidence']).write_text(json.dumps(evidence))
            with self.assertRaisesRegex(ValueError, 'raw-byte extent'):
                check.validate_rea_extent(unit, project, self.sha)
            lib = project / 'toolchains/runtime500/SLIBC.LIB'
            lib.write_bytes(lib.read_bytes()[:-1])
            result = check.build_unit(unit, self.image, project, 'unused')
            self.assertEqual(result['status'], 'build_error')
            self.assertIn('pinned configuration', result['error'])

    def test_installer_checks_archive_and_existing_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wrong = root / 'wrong.json'
            wrong.write_bytes(b'wrong archive')
            with self.assertRaisesRegex(ValueError, 'archive SHA'):
                install(root / 'runtime', wrong)
            self.assertFalse((root / 'runtime').exists())
            shutil.copytree(PROJECT / 'toolchains/runtime500', root / 'runtime')
            (root / 'runtime/manifest.json').write_text('{}')
            with self.assertRaisesRegex(ValueError, 'manifest'):
                validate_runtime(root / 'runtime', runtime_config())


if __name__ == '__main__':
    unittest.main()
