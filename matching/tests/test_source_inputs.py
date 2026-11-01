"""Strict source-only COMMON inputs; no matching-byte credit."""
import copy
import dataclasses
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = next(p for p in Path(__file__).resolve().parents if (p / 'config/msc500.json').is_file()) / 'tests'
sys.path.insert(0, str(HERE.parent))
import source_inputs as backend
from msc import CompileResult


def record(kind, payload):
    raw = bytes([kind])+struct.pack('<H', len(payload)+1)+payload
    return raw+bytes([-sum(raw) & 255])


def change_record(data, kind, transform):
    obj = backend.read_omf(data)
    changed = False
    output = []
    for k, _, payload in obj.records:
        if k == kind and not changed:
            payload = transform(payload)
            changed = True
        output.append(record(k, payload))
    assert changed
    return b''.join(output)


class SourceInputsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project = backend.PROJECT
        cls.target = cls.project.parent/'CHESS.EXE'
        cls.config = json.loads((cls.project/'config/source-inputs.json').read_text())
        cls.config['source_allocations'] = [row for row in cls.config['source_allocations']
                                            if row['id'] == 'asset-selector-common']
        # One new authentic compile shared by the pure mutation tests.
        cls.compiled = backend.compile_c(cls.project/backend.SOURCE, backend.FLAGS, compiler='msc500')
        cls.obj = cls.compiled.object_bytes

    def run_config(self, config):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'config.json'
            path.write_text(json.dumps(config))
            with patch.object(backend, 'compile_c', return_value=self.compiled):
                return backend.build_source_inputs(self.project, self.target, Path(tmp)/'objects', path)

    def test_fresh_actual_compiler_complete_module(self):
        self.assertEqual(backend.sha(self.obj), backend.OBJECT_SHA)
        self.assertEqual(len(backend.validate_object(self.obj)), 8)
        self.assertEqual(self.compiled.toolchain_manifest_sha256, backend.MANIFEST_SHA)

    def test_absent_registry_backward_compatible(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(backend, 'compile_c', side_effect=AssertionError('must not compile')):
                report = backend.build_source_inputs(self.project, Path('absent-target'), Path(tmp)/'out', Path(tmp)/'absent.json')
            self.assertEqual(report['objects'], [])
            self.assertFalse((Path(tmp)/'out').exists())

    def test_empty_registry(self):
        self.assertEqual(self.run_config({'schema_version': 1, 'source_allocations': []})['objects'], [])

    def test_real_evidence_full_backend_zero_credit(self):
        result = self.run_config(self.config)
        self.assertEqual(result['matching_credit'], 0)
        self.assertFalse(result['placement_proven'])
        self.assertEqual(len(result['objects']), 1)
        obj = result['objects'][0]
        self.assertEqual(obj['allocation_bytes'], 32)
        self.assertEqual(obj['initialized_bytes'], 0)
        self.assertEqual([x['symbol'] for x in obj['definitions']], backend.NAMES)
        self.assertTrue(all(not x['resolved'] for x in obj['original_map_constraints']))
        # No matching report row, function count or image/file-byte score is produced.
        self.assertFalse({'units', 'summary', 'c_matched_bytes', 'source_data_bytes',
                          'verified_image_span_bytes', 'verified_file_span_bytes'} & set(result))

    def bad_config(self, edit, message):
        config = copy.deepcopy(self.config)
        edit(config)
        with self.assertRaisesRegex(ValueError, message):
            self.run_config(config)

    def test_no_credit_override(self):
        self.bad_config(lambda c: c['source_allocations'][0].update(size=32), 'unknown allocation fields')

    def test_wrong_schema(self):
        self.bad_config(lambda c: c.update(schema_version=2), 'schema')

    def test_duplicate_input(self):
        self.bad_config(lambda c: c['source_allocations'].append(copy.deepcopy(c['source_allocations'][0])), 'duplicate')

    def test_partial_object_selection(self):
        self.bad_config(lambda c: c['source_allocations'][0]['objects'].pop(), 'incomplete COMMON')

    def test_source_pin(self):
        self.bad_config(lambda c: c['source_allocations'][0].update(source_sha256='0'*64), 'source/profile')

    def test_compiler_profile(self):
        self.bad_config(lambda c: c['source_allocations'][0].update(flags=['/AS', '/Zi']), 'source/profile')

    def test_toolchain_pin(self):
        self.bad_config(lambda c: c['source_allocations'][0].update(toolchain_manifest_sha256='0'*64), 'source/profile')

    def test_primary_pin(self):
        self.bad_config(lambda c: c['source_allocations'][0]['evidence']['native'].update(sha256='0'*64), 'evidence pin')

    def test_evidence_cannot_escape_project(self):
        self.bad_config(lambda c: c['source_allocations'][0]['evidence']['native'].update(path='../CHESS.EXE'), 'escapes project')

    def test_runtime_library_pin(self):
        self.bad_config(lambda c: c['source_allocations'][0]['evidence']['runtime'].update(sha256='0'*64), 'evidence pin')

    def test_actual_link_artifact_pin(self):
        self.bad_config(lambda c: c['source_allocations'][0]['evidence']['linked_exe'].update(sha256='0'*64), 'evidence pin')

    def test_wrong_fresh_tool_hashes(self):
        compiled = dataclasses.replace(self.compiled, tool_hashes={})
        with patch.object(self, 'compiled', compiled):
            self.bad_config(lambda c: None, 'fresh tool pin')

    def bad_object(self, obj, message):
        with self.assertRaisesRegex(ValueError, message):
            backend.validate_object(obj)

    def test_far_common_rejected(self):
        self.bad_object(change_record(self.obj, 0xb0, lambda p: p.replace(b'\x62\x04', b'\x61\x01\x04', 1)), 'not near COMMON')

    def test_wrong_size(self):
        self.bad_object(change_record(self.obj, 0xb0, lambda p: p.replace(b'\x62\x04', b'\x62\x06', 1)), 'not near COMMON')

    def test_missing_common(self):
        self.bad_object(change_record(self.obj, 0xb0, lambda p: b''), 'missing/duplicate')

    def test_extra_definition(self):
        self.bad_object(change_record(self.obj, 0xb0, lambda p: p+p[:19]), 'missing/duplicate')

    def test_wrong_common_type(self):
        self.bad_object(change_record(self.obj, 0xb0, lambda p: p.replace(b'\x82\x0c', b'\x82\x0b', 1)), 'COMMON type')

    def test_nonzero_code_segment(self):
        self.bad_object(change_record(self.obj, 0x98, lambda p: p[:1]+b'\x01\x00'+p[3:]), 'nondebug allocation')

    def test_unreviewed_debug_thread(self):
        self.bad_object(change_record(self.obj, 0x9c, lambda p: p[:1]+bytes([p[1]-1])+p[2:]), 'object changed')

    def test_debug_fixup_field(self):
        rows = backend.read_omf(self.obj).records
        changed = b''.join(record(k, p.replace(bytes.fromhex('cca9'), bytes.fromhex('cca8'), 1)
                          if k == 0x9c else p) for k, _, p in rows)
        self.bad_object(changed, 'CodeView fixup')

    def test_already_matched_definition_conflict(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp)/'config.json'; config.write_text(json.dumps(self.config))
            with self.assertRaisesRegex(ValueError, 'already matched definition'):
                backend.build_source_inputs(self.project, self.target, Path(tmp)/'objects', config,
                                            defined_symbols={'_setup_offsets'})

    def test_minimal_report_does_not_export_scores(self):
        report = backend.report_inputs(self.run_config(self.config))
        self.assertEqual(set(report[0]), {'id', 'source', 'object', 'object_sha256', 'definitions'})
        self.assertEqual(set(report[0]['definitions'][0]), {'symbol', 'size'})

    def test_debug_type_corruption(self):
        self.bad_object(change_record(self.obj, 0xa0, lambda p: p[:-1]+bytes([p[-1]^1])), 'object changed')

    def test_entrypoint_not_allowed(self):
        self.bad_object(change_record(self.obj, 0x8a, lambda p: b'\x40'), 'entry point')

    def test_bad_checksum(self):
        self.bad_object(self.obj[:-1]+bytes([self.obj[-1]^1]), 'checksum')

    def test_truncated_record(self):
        self.bad_object(self.obj[:-1], 'truncated')

    def test_second_module_rejected(self):
        self.bad_object(self.obj+self.obj, 'after MODEND')

    def test_unreviewed_linker_directive(self):
        self.bad_object(change_record(self.obj, 0x88, lambda p: p+b'X'), 'linker directive')


if __name__ == '__main__':
    unittest.main(verbosity=2)
