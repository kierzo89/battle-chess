"""Whole C DATA ownership tests, independent of function-extent extraction."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import struct
import sys
import unittest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from cdata import extract_data, CDataError
from omf import read_omf, OMFError


def record(kind, payload=b''):
    prefix = bytes([kind]) + struct.pack('<H', len(payload) + 1) + payload
    return prefix + bytes([-sum(prefix) & 255])


def name(value):
    b = value.encode('ascii')
    return bytes([len(b)]) + b


def module(data=b'\x01\0\x02\0\x03\0', size=None, chunks=None, public_offset=0,
           code_size=0, bss_size=0, external='__acrtused', group=True,
           group_name='DGROUP', extra_group=False, extra_data=False, fixup=False):
    size = len(data) if size is None else size
    chunks = [(0, data)] if chunks is None else chunks
    names = ['', group_name, '_DATA', 'DATA', '_BSS', 'BSS', '_TEXT', 'CODE', '$$TYPES', 'DEBTYP']
    records = [record(0x80, name('data.c')), record(0x96, b''.join(name(x) for x in names)),
               record(0x98, b'\x48' + struct.pack('<H', size) + b'\x03\x04\x01'),
               record(0x98, b'\x48' + struct.pack('<H', bss_size) + b'\x05\x06\x01'),
               record(0x98, b'\x48' + struct.pack('<H', code_size) + b'\x07\x08\x01'),
               record(0x98, b'\x20\x02\0\x09\x0a\x01')]
    if extra_data:
        records.append(record(0x98, b'\x48\x02\0\x03\x04\x01'))
    if group:
        records.append(record(0x9a, b'\x02\xff\x01\xff\x02'))
    if extra_group:
        records.append(record(0x9a, b'\x02\xff\x01'))
    if external is not None:
        records.append(record(0x8c, name(external) + b'\0'))
    records.append(record(0x90, b'\x01\x01' + name('_values') + struct.pack('<H', public_offset) + b'\0'))
    records += [record(0xa0, b'\x01' + struct.pack('<H', offset) + body) for offset, body in chunks]
    if fixup:
        records.append(record(0x9c, b'\xc4\0\x56\x01'))
    records.append(record(0xa0, b'\x04\0\0CV'))
    return b''.join(records) + record(0x8a, b'\0')


class CDataTests(unittest.TestCase):
    def test_size_is_complete_segment_not_expected_size_or_next_public(self):
        obj = read_omf(module())
        before = deepcopy(obj)
        data, metadata = extract_data(obj, '_values')
        self.assertEqual(data, b'\x01\0\x02\0\x03\0')
        self.assertEqual(metadata['segment']['length'], 6)
        self.assertEqual(metadata['boundary'], 'complete_omf_data_segment')
        self.assertTrue(metadata['startup_marker_unused'])
        self.assertEqual(metadata['authored_c_function_count'], 0)
        self.assertEqual(metadata['group']['name'], 'DGROUP')
        self.assertEqual(metadata['sha256'], hashlib.sha256(data).hexdigest())
        self.assertEqual(obj, before)
        obj.publics['_inside'] = obj.publics['_values'].__class__('_inside', 1, 2, 1, 0)
        self.assertEqual(extract_data(obj, '_values')[0], data)
        self.assertFalse(extract_data(read_omf(module(external=None)), '_values')[1]['startup_marker_unused'])

    def test_code_bss_and_ambiguous_allocations_are_rejected(self):
        for options in ({'code_size': 1}, {'bss_size': 2}, {'extra_data': True}):
            with self.subTest(options=options), self.assertRaisesRegex(CDataError, 'other nondebug allocations'):
                extract_data(read_omf(module(**options)), '_values')
        obj = read_omf(module())
        obj.segments[4].class_name = 'DATA'
        with self.assertRaisesRegex(CDataError, 'other nondebug allocations'):
            extract_data(obj, '_values')

    def test_full_ledata_holes_overlaps_and_reserved_tail_are_rejected(self):
        for chunks, size in (([(1, b'ab')], 3), ([(0, b'ab'), (1, b'bc')], 3),
                             ([(0, b'ab')], 3), ([(0, b'abc')], 2)):
            with self.subTest(chunks=chunks), self.assertRaises(OMFError):
                extract_data(read_omf(module(chunks=chunks, size=size)), '_values')
        obj = read_omf(module(chunks=[(4, b'\x03\0'), (0, b'\x01\0\x02\0')]))
        self.assertEqual(extract_data(obj, '_values')[0], b'\x01\0\x02\0\x03\0')

    def test_public_offset_missing_public_group_and_segment_identity_are_rejected(self):
        for options in ({'public_offset': 1}, {'group': False}, {'group_name': 'OTHER'}, {'extra_group': True}):
            with self.subTest(options=options), self.assertRaises(CDataError):
                extract_data(read_omf(module(**options)), '_values')
        obj = read_omf(module())
        with self.assertRaisesRegex(CDataError, 'public at segment offset zero'):
            extract_data(obj, '_missing')
        obj.segments[1].name = 'not_DATA'
        with self.assertRaisesRegex(CDataError, '_DATA class DATA'):
            extract_data(obj, '_values')
        obj = read_omf(module())
        obj.segments[1].attributes = 0x28  # byte alignment is legal; absolute alignment below is not.
        self.assertEqual(len(extract_data(obj, '_values')[0]), 6)
        obj.segments[1].attributes = 0x08
        with self.assertRaisesRegex(CDataError, 'relocatable'):
            extract_data(obj, '_values')

    def test_fixups_and_every_other_external_fail_including_marker_reference(self):
        for external in ('_game_table', '__acrtused_extra'):
            with self.subTest(external=external), self.assertRaisesRegex(CDataError, 'unused __acrtused'):
                extract_data(read_omf(module(external=external)), '_values')
        with self.assertRaisesRegex(CDataError, 'no FIXUPP'):
            extract_data(read_omf(module(fixup=True)), '_values')
        obj = read_omf(module())
        obj.externals[2] = '__acrtused'
        with self.assertRaisesRegex(CDataError, 'one unused'):
            extract_data(obj, '_values')

    def test_lidata_communal_and_invalid_group_components_fail(self):
        obj = read_omf(module())
        obj.segments[1].unsupported_data = True
        with self.assertRaisesRegex(CDataError, 'LIDATA'):
            extract_data(obj, '_values')
        obj = read_omf(module())
        obj.records.append((0xb0, 1000, b''))
        with self.assertRaisesRegex(CDataError, 'communal'):
            extract_data(obj, '_values')
        for payload in (b'\x02\xff\x01\xff\x01', b'\x02\xff\x7f', b'\x02\x00'):
            obj = read_omf(module())
            obj.records = [(k, at, payload if k == 0x9a else v) for k, at, v in obj.records]
            with self.subTest(payload=payload), self.assertRaises(CDataError):
                extract_data(obj, '_values')

    def test_strict_reader_rejects_bad_checksum_before_extraction(self):
        b = bytearray(module())
        b[6] ^= 1
        with self.assertRaisesRegex(OMFError, 'checksum'):
            extract_data(read_omf(bytes(b)), '_values')
        with self.assertRaisesRegex(CDataError, 'strict-reader'):
            extract_data(bytes(b), '_values')

    @unittest.skipUnless((PROJECT / 'toolchains/msc500/CL.EXE').exists()
                         and (PROJECT.parent / 'CHESS.EXE').exists(), 'Pinned compiler/original required')
    def test_fresh_typed80byte_aggregate_and_full_expanded_rea_read(self):
        from msc import compile_c
        from reference import build_reference, validate_expanded_read
        source = PROJECT / 'src/data/move_lookup_tables.c'
        compiled = compile_c(source, ['/AS', '/Zl', '/Zi'], compiler='msc500')
        data, metadata = extract_data(read_omf(compiled.object_bytes), '_move_lookup_tables')
        self.assertEqual(len(data), 80)
        self.assertEqual(metadata['public']['offset'], 0)
        self.assertTrue(metadata['startup_marker_unused'])
        self.assertEqual(metadata['emitted_mz_sites'], [])
        evidence = json.loads((PROJECT / 'evidence/rea-move-lookup-data.json').read_text())['records'][0]
        context = build_reference((PROJECT.parent / 'CHESS.EXE').read_bytes())
        unit = {'image_offset': 0x5d10a, 'size': len(data), 'reference_region': 'exepack-expanded'}
        self.assertEqual(validate_expanded_read(evidence, unit, data, context, emitted_mz_sites=[]), evidence['evidence_id'])


if __name__ == '__main__':
    unittest.main()
