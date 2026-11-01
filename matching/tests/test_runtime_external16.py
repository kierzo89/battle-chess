"""Strict external-runtime ownership, authentic LINK and one-field comparison."""
import copy
import dataclasses
import hashlib
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import unittest
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
import runtime_external16 as backend
from library16 import LibraryError, extract_member
import omf


def record(kind, payload):
    data = bytes([kind]) + (len(payload) + 1).to_bytes(2, 'little') + payload
    return data + bytes([-sum(data) & 255])


def records(data):
    result, pos = [], 0
    while pos < len(data):
        length = int.from_bytes(data[pos + 1:pos + 3], 'little')
        result.append((data[pos], data[pos + 3:pos + length + 2]))
        pos += length + 3
    return result


def mutate(data, kind, edit, occurrence=0):
    rows = records(data)
    indexes = [i for i, (k, _) in enumerate(rows) if k == kind]
    i = indexes[occurrence]
    rows[i] = kind, edit(rows[i][1])
    return b''.join(record(k, p) for k, p in rows)


def unit():
    return {'member': 'near_aldiv', 'language': 'runtime', 'backend': 'msc500-authentic-external16',
            'symbol': '__aNNaldiv', 'size': 34, 'image_offset': '0xF37A',
            'externals': {'__aNldiv': {'segment': 0, 'offset': 0xF87C}}}


@unittest.skipUnless((PROJECT / 'toolchains/runtime-libh/LIBH.LIB').exists(), 'Pinned LIBH required')
class MemberAdmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = backend.load_profile('near_aldiv')
        cls.raw = cls.profile['object_bytes']

    def test_complete_pinned_members_allocations_and_overlaps_remain_unflattened(self):
        p = self.profile
        self.assertEqual(p['object_size'], 203)
        self.assertEqual(p['library_offset'], 8160)
        self.assertEqual(p['segment']['length'], 34)
        self.assertEqual(set(p['publics']), {'__aNFbldiv', '__aNNaldiv'})
        self.assertEqual(p['externals'], {1: '__aNldiv'})
        self.assertEqual([(m['segment']['length'], m['segments'][1]['length']) for m in p['members'].values()], [(34, 0), (163, 0), (52, 0)])
        self.assertEqual(p['data_writes'][1]['overlaps'], [{'start': 31, 'end': 32}])
        self.assertNotIn('image', p)
        with self.assertRaisesRegex(omf.OMFError, 'overlapping LEDATA'):
            omf.read_omf(self.raw)
        lib = (PROJECT / 'toolchains/runtime-libh/LIBH.LIB').read_bytes()
        with self.assertRaisesRegex(omf.OMFError, 'overlapping LEDATA'):
            extract_member(lib, 'ALDIV', backend.LIBRARY_SHA256, backend.SPECS['ALDIV']['sha256'])

    def test_holes_extra_allocations_groups_and_public_offsets_are_rejected(self):
        examples = [
            (mutate(self.raw, 0xa0, lambda p: p[:1] + b'\x01\0' + p[3:]), 'ownership|outside|zero source'),
            (mutate(self.raw, 0x98, lambda p: p[:1] + b'\x02\0' + p[3:], 1), 'allocation'),
            (mutate(self.raw, 0x9a, lambda p: p[:-1] + b'\x01'), 'group'),
            (mutate(self.raw, 0x90, lambda p: p[:-3] + b'\x01\0\0'), 'public'),
            (mutate(self.raw, 0xa0, lambda p: p[:1] + b'\x1e\0' + p[3:], 1), 'ownership'),
        ]
        for raw, message in examples:
            with self.subTest(message=message), self.assertRaisesRegex(LibraryError, message):
                backend._layout(raw, 'ALDIV')

    def test_external_fixup_mode_frame_width_target_and_source_field_are_exact(self):
        examples = [
            (0x8c, lambda p: p.replace(b'__aNldiv', b'__xNldiv'), 'dependency'),
            (0x9c, lambda p: bytes([p[0] | 0x40]) + p[1:], 'fixup shape'),
            (0x9c, lambda p: b'\x88' + p[1:], 'fixup shape'),
            (0x9c, lambda p: p[:2] + b'\x16' + p[3:], 'fixup shape'),
            (0x9c, lambda p: p[:-1] + b'\x02', 'fixup shape'),
            (0xa0, lambda p: p[:21] + b'\x01' + p[22:], 'zero source'),
        ]
        for kind, edit, message in examples:
            with self.subTest(kind=kind, message=message), self.assertRaisesRegex(LibraryError, message):
                backend._layout(mutate(self.raw, kind, edit), 'ALDIV')

    def test_missing_or_extra_records_and_corrupt_checksum_fail(self):
        rows = records(self.raw)
        missing = b''.join(record(k, p) for k, p in rows if k != 0x9c)
        extra_ext = rows[:-1] + [(0x8c, b'\x04_xxx\0')] + rows[-1:]
        extra_allocation = rows[:-1] + [(0x98, b'\x48\x01\0\x05\x03\x01')] + rows[-1:]
        for data, message in [(missing, 'fixup count'),
                              (b''.join(record(k, p) for k, p in extra_ext), 'dependency'),
                              (b''.join(record(k, p) for k, p in extra_allocation), 'allocation'),
                              (self.raw + b'\0', 'boundary')]:
            with self.subTest(message=message), self.assertRaisesRegex(LibraryError, message):
                backend._layout(data, 'ALDIV')
        bad = bytearray(self.raw); bad[10] ^= 1
        with self.assertRaisesRegex(LibraryError, 'checksum'):
            backend._layout(bytes(bad), 'ALDIV')

    def test_profile_pins_fail_before_link_and_unknown_id_fails(self):
        with patch.object(backend.subprocess, 'run') as run:
            with self.assertRaisesRegex(LibraryError, 'unknown'):
                backend.build('arbitrary')
            for changes in [{'library_sha256': '0' * 64}, {'archive_sha256': '0' * 64},
                            {'destination': '../elsewhere'}, {'linker_sha256': '0' * 64}]:
                with patch.object(backend, 'helper_config', return_value=dict(self.profile['config'], **changes)):
                    with self.assertRaisesRegex(LibraryError, 'pinned'):
                        backend.build('near_aldiv')
            run.assert_not_called()


@unittest.skipUnless(shutil.which('dosbox') and (PROJECT / 'toolchains/msc510/LINK.EXE').exists()
                     and (PROJECT / 'toolchains/runtime-libh/LIBH.LIB').exists(), 'Pinned LINK/LIBH and DOSBox required')
class AuthenticExternalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mounts = []
        actual_run = subprocess.run
        def observe(args, **kwargs):
            conf = Path(args[args.index('-conf') + 1])
            lines = [l for l in conf.read_text().splitlines() if l.startswith('mount ')]
            if len(lines) != 2:
                raise AssertionError(lines)
            drive, tools = [Path(l.split('"')[1]) for l in lines]
            if {p.name for p in drive.iterdir()} != {'ALDIV.OBJ', 'LDIV.OBJ', 'LMUL.OBJ', 'BUILD.BAT'}:
                raise AssertionError(list(drive.iterdir()))
            if {p.name for p in tools.iterdir()} != {'LINK.EXE'} or '-ro' not in lines[1]:
                raise AssertionError(lines)
            if drive == PROJECT.parent:
                raise AssertionError('target mounted')
            cls.mounts.append(str(drive))
            return actual_run(args, **kwargs)
        with patch.object(backend.subprocess, 'run', side_effect=observe):
            cls.authentic = backend.build('near_aldiv')
            cls.second = backend.build('near_aldiv')

    def test_fresh_isolated_complete_image_has_all_collateral_allocations(self):
        a = self.authentic
        self.assertEqual(a.image, self.second.image)
        self.assertEqual(len(set(self.mounts)), 2)
        p = a.provenance
        self.assertEqual(p['full_image_size'], 250)
        self.assertEqual([(x.get('name'), x['origin'], x['size']) for x in p['complete_allocations']],
                         [('ALDIV', 0, 34), ('LDIV', 34, 163), (None, 197, 1), ('LMUL', 198, 52)])
        self.assertEqual(len(bytes.fromhex(p['full_image_hex'])), 250)
        self.assertEqual(p['MZ_relocations'], [])
        self.assertEqual(len(p['actual_fixups']), 2)
        self.assertEqual(a.image[18:20], b'\x0e\0')
        self.assertEqual(a.image[31:], b'\xc2\x06\0')
        self.assertEqual(p['actual_publics']['__aNldiv'], {'segment': 0, 'offset': 34})
        self.assertFalse(p['reference_executable_read_or_mounted'])
        self.assertEqual(p['authored_c_credit'], 0)

    def test_only_one_forward_field_changes_full_primary_and_decoded_match(self):
        a = self.authentic
        compared = backend.relocate_for_comparison(unit(), a)
        raw = json.loads((PROJECT / 'evidence/rea-aldiv-authentic-raw.json').read_text())
        self.assertEqual(raw['subject']['digest']['sha256'], 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd')
        self.assertTrue(raw['normalized_result']['complete'])
        self.assertEqual(raw['normalized_result']['returned_bytes'], 34)
        self.assertEqual(compared.image, bytes.fromhex(raw['normalized_result']['bytes_hex']))
        self.assertEqual(compared.image[:18], a.image[:18])
        self.assertEqual(compared.image[20:], a.image[20:])
        self.assertEqual(compared.image[18:20], b'\xee\x04')
        self.assertEqual(compared.provenance['comparison_relocation']['mz_segment_relocations'], [])
        from reference import build_reference
        context = build_reference((PROJECT.parent / 'CHESS.EXE').read_bytes())
        self.assertEqual(compared.image, context['image'][0xf37a:0xf39c])
        self.assertEqual([s for s in context['relocations'] if s < 0xf39c and s + 2 > 0xf37a], [])

    def test_missing_extra_wrong_shaped_or_wrong_frame_bindings_rejected(self):
        changes = [{'externals': {}}, {'externals': None},
                   {'externals': {'__aNldiv': {'segment': 0, 'offset': 1}, '_extra': 2}},
                   {'externals': {'__aNldiv': 0xf87c}},
                   {'externals': {'__aNldiv': {'segment': 1, 'offset': 0xf87c}}},
                   {'externals': {'__aNldiv': {'segment': False, 'offset': 0xf87c}}},
                   {'externals': {'__aNldiv': {'segment': 0, 'offset': 65536}}},
                   {'symbol': '__aNFbldiv'}, {'size': 33}, {'image_offset': 65520},
                   {'language': 'c'}, {'backend': 'generic'}, {'member': 'near_lmul'}]
        for c in changes:
            with self.subTest(change=c), self.assertRaises(LibraryError):
                backend.relocate_for_comparison(dict(unit(), **c), self.authentic)

    def test_comparison_revalidates_authentic_field_full_exe_and_map(self):
        a = self.authentic
        for change in ['image', 'member', 'field', 'map', 'exe', 'size', 'mz', 'fixups', 'dependency']:
            p = copy.deepcopy(a.provenance)
            image, obj = a.image, a.object_bytes
            if change == 'image': image = image[:10] + bytes([image[10] ^ 1]) + image[11:]
            elif change == 'member': obj += b'\0'
            elif change == 'field':
                exe = bytearray.fromhex(p['linked_executable_hex'])
                header = int.from_bytes(exe[8:10], 'little') * 16
                exe[header + 18] ^= 1
                p['linked_executable_hex'] = exe.hex()
            elif change == 'map': p['linker_map'] = p['linker_map'].replace('0000:0022', '0000:0024')
            elif change == 'exe': p['linked_executable_hex'] += '00'
            elif change == 'size': p['members']['LDIV']['segment']['length'] += 1
            elif change == 'mz': p['member_MZ_relocations'] = [18]
            elif change == 'fixups': p['members']['ALDIV']['fixups'][0]['offset'] = 19
            elif change == 'dependency': del p['members']['LDIV']
            with self.subTest(change=change), self.assertRaises(LibraryError):
                backend.relocate_for_comparison(unit(), dataclasses.replace(a, image=image, object_bytes=obj, provenance=p))

    def test_production_gate_and_full_runtime_build(self):
        import check
        configured = next(u for u in json.loads((PROJECT / 'config/units.json').read_text())
                          if u['id'] == 'near_aldiv')
        loaded = check.external16_inputs(configured, PROJECT)
        self.assertEqual(loaded['segment']['length'], 34)
        for changes in [{'source': 'arbitrary'}, {'backend': 'msc500-authentic-link'},
                        {'runtime_kind': 'data'}, {'reference_region': 'exepack-expanded'},
                        {'member': 'near_lmul'}, {'symbol': '__aNFbldiv'}, {'size': 33},
                        {'image_offset': '0xf37b'}, {'externals': {}},
                        {'externals': {'__aNldiv': {'segment': 1, 'offset': 0xf87c}}}]:
            with self.subTest(changes=changes), patch.object(backend, 'load_profile') as load:
                with self.assertRaises(ValueError):
                    check.external16_inputs(dict(configured, **changes), PROJECT)
                load.assert_not_called()
        from reference import build_reference
        context = build_reference((PROJECT.parent / 'CHESS.EXE').read_bytes())
        import tempfile
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            # The real production branch launches authentic LINK freshly.
            result = check.build_unit(configured, context['image'], PROJECT, 'nasm', output=output)
            self.assertEqual(result['status'], 'runtime_matched', result)
            self.assertEqual(result['authored_c_credit'], 0)
            self.assertEqual(result['emitted_segment']['length'], 34)
            self.assertEqual(result['authentic_link']['MZ_relocations'], [])
            self.assertEqual(result['authentic_link']['member_MZ_relocations'], [])
            emitted = (output / 'runtime/near_aldiv.bin').read_bytes()
            self.assertEqual(emitted, context['image'][0xf37a:0xf39c])
            raw = json.loads((PROJECT / configured['rea_evidence']).read_text())
            self.assertEqual(check.raw_runtime_extent(raw, configured, emitted), emitted)
            with self.assertRaisesRegex(ValueError, 'raw-byte extent'):
                check.raw_runtime_extent(raw, configured, emitted[:-1] + bytes([emitted[-1] ^ 1]))

    def test_output_rejects_extra_allocation_or_missing_alias_even_with_valid_exe(self):
        a = self.authentic; p = backend.load_profile('near_aldiv')
        exe = bytes.fromhex(a.provenance['linked_executable_hex']); text = a.provenance['linker_map']
        for tampered in [text.replace('_DATA                  DATA', '_BSS                   BSS'),
                         text.replace('0000:0000       __aNFbldiv', '0000:0001       __aNFbldiv'),
                         text.replace('000F:0   DGROUP', '000E:0   DGROUP')]:
            with self.assertRaises(LibraryError):
                backend._output(exe, tampered, p, ['ALDIV', 'LDIV', 'LMUL'])
        extra = bytearray(exe); extra += b'\0'
        struct.pack_into('<H', extra, 2, len(extra) % 512)
        with self.assertRaisesRegex(LibraryError, 'size mismatch'):
            backend._output(bytes(extra), text, p, ['ALDIV', 'LDIV', 'LMUL'])


if __name__ == '__main__':
    unittest.main()
