"""Authentic helper LINK isolation, library provenance and complete extents."""
import hashlib
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
import library16
import omf
import runtime_libh
import setup_libh


def record(kind, payload):
    result = bytes([kind]) + (len(payload) + 1).to_bytes(2, 'little') + payload
    return result + bytes([-sum(result) & 255])


def object_records(size=5, writes=((0, b'\x90\x90\xc3'), (2, b'\xc2\x08\x00')), data_size=0, extra=b''):
    names = b'\x05_TEXT\x04CODE\x05_DATA\x04DATA\x00'
    return (record(0x80, b'\x04TEST') + record(0x96, names)
            + record(0x98, b'\x48' + size.to_bytes(2, 'little') + b'\x01\x02\x05')
            + record(0x98, b'\x48' + data_size.to_bytes(2, 'little') + b'\x03\x04\x05')
            + record(0x90, b'\x00\x01\x06_entry\x00\x00\x00')
            + b''.join(record(0xa0, b'\x01' + off.to_bytes(2, 'little') + data) for off, data in writes)
            + extra + record(0x8a, b'\0'))


def mz(image=b'\x90\x90\xc2\x08\0', relocation=None):
    header = bytearray(32)
    header[:2] = b'MZ'
    size = 32 + len(image)
    struct.pack_into('<4H', header, 2, size % 512, (size + 511) // 512, int(relocation is not None), 2)
    struct.pack_into('<H', header, 24, 28)
    if relocation is not None:
        struct.pack_into('<HH', header, 28, relocation, 0)
    return bytes(header) + image


def fat_media(loop=False, duplicate=False):
    disk = bytearray(8 * 512)
    struct.pack_into('<H', disk, 11, 512)
    disk[13], disk[16] = 1, 1
    struct.pack_into('<H', disk, 14, 1)
    struct.pack_into('<H', disk, 17, 16)
    struct.pack_into('<H', disk, 22, 1)
    def fat(cluster, value):
        off = 512 + cluster + cluster // 2
        word = int.from_bytes(disk[off:off + 2], 'little')
        word = ((word & 15) | (value << 4)) if cluster & 1 else ((word & 0xf000) | value)
        disk[off:off + 2] = word.to_bytes(2, 'little')
    fat(2, 2 if loop else 0xfff)
    fat(3, 0xfff)
    def entry(name, ext, attrs, cluster, size):
        raw = bytearray(32)
        raw[:11] = name.ljust(8).encode() + ext.ljust(3).encode()
        raw[11] = attrs
        struct.pack_into('<HI', raw, 26, cluster, size)
        return raw
    disk[1024:1056] = entry('LIB', '', 0x10, 2, 0)
    file = entry('LIBH', 'LIB', 0x20, 3, 4)
    disk[1536:1568] = file
    if duplicate:
        disk[1568:1600] = file
    disk[2048:2052] = b'LIB!'
    sectors = [{'c': 0, 'h': 0, 's': i + 1, 'd': list(struct.unpack('<128I', disk[i * 512:(i + 1) * 512]))} for i in range(8)]
    return json.dumps({'imageInfo': {'cylinders': 1, 'heads': 1, 'trackDefault': 8, 'sectorDefault': 512}, 'diskData': [[sectors]]}).encode()


class HelperMetadataTests(unittest.TestCase):
    def test_overlap_is_recorded_but_strict_c_reader_still_rejects_it(self):
        data = object_records()
        layout = runtime_libh.member_layout(data)
        self.assertEqual(layout['segment']['length'], 5)
        self.assertEqual(layout['publics']['_entry']['offset'], 0)
        self.assertEqual(layout['data_writes'][1]['overlaps'], [{'start': 2, 'end': 3}])
        self.assertNotIn('image', layout)
        with self.assertRaisesRegex(omf.OMFError, 'overlapping LEDATA'):
            omf.read_omf(data)

    def test_holes_extents_externals_and_extra_allocations_are_rejected(self):
        examples = [(object_records(writes=((0, b'\0\0'),)), 'holes'),
                    (object_records(writes=((0, b'\0' * 6),)), 'outside'),
                    (object_records(data_size=2), 'exactly one'),
                    (object_records(extra=record(0x8c, b'\x04_ext\0')), 'no externals')]
        for data, message in examples:
            with self.subTest(message=message), self.assertRaisesRegex(library16.LibraryError, message):
                runtime_libh.member_layout(data)
        corrupt = bytearray(object_records())
        corrupt[10] ^= 1
        with self.assertRaisesRegex(library16.LibraryError, 'checksum'):
            runtime_libh.member_layout(corrupt)

    def test_entire_mz_image_is_required_without_trimming_or_relocation_masks(self):
        image, relocations, metadata = runtime_libh.mz_output(mz(), 5)
        self.assertEqual(image, b'\x90\x90\xc2\x08\0')
        self.assertEqual(relocations, ())
        self.assertEqual(metadata['file_bytes'], 37)
        with self.assertRaisesRegex(library16.LibraryError, 'overlay mismatch'):
            runtime_libh.mz_output(mz() + b'\0', 5)
        with self.assertRaisesRegex(library16.LibraryError, 'declared CODE size'):
            runtime_libh.mz_output(mz(image=image + b'\0'), 5)
        with self.assertRaisesRegex(library16.LibraryError, 'not supported yet'):
            runtime_libh.mz_output(mz(relocation=2), 5)
        with self.assertRaisesRegex(library16.LibraryError, 'relocation site'):
            runtime_libh.mz_output(mz(relocation=4), 5)

    def test_nested_fat12_file_and_unsafe_chains_are_checked(self):
        self.assertEqual(setup_libh.archive_member(fat_media(), '/LIB/LIBH.LIB'), b'LIB!')
        for raw, path, message in [(fat_media(loop=True), '/LIB/LIBH.LIB', 'looping'),
                                   (fat_media(duplicate=True), '/LIB/LIBH.LIB', 'ambiguous'),
                                   (fat_media(), '/LIB/../LIBH.LIB', 'Invalid'),
                                   (fat_media(), '/LIBH.LIB', 'absent')]:
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                setup_libh.archive_member(raw, path)


@unittest.skipUnless(shutil.which('dosbox') and (PROJECT / 'toolchains/runtime-libh/LIBH.LIB').exists()
                     and (PROJECT / 'toolchains/msc510/LINK.EXE').exists(), 'Pinned helper library, LINK and DOSBox required')
class AuthenticHelperTests(unittest.TestCase):
    def test_default_member_extraction_stays_strict_and_optout_preserves_raw_member(self):
        config = setup_libh.helper_config()
        profile = config['members'][0]
        library = setup_libh.validate_helpers(PROJECT / config['destination'], config)
        with self.assertRaisesRegex(omf.OMFError, 'overlapping LEDATA'):
            library16.extract_member(library, profile['name'], config['library_sha256'], profile['member_sha256'])
        member = library16.extract_member(library, profile['name'], config['library_sha256'], profile['member_sha256'], validate_object=False)
        self.assertEqual(member.offset, profile['library_offset'])
        self.assertEqual(member.sha256, profile['member_sha256'])
        self.assertEqual(len(member.data), 200)

    def test_all_registered_helpers_match_full_original_extents_and_relocations(self):
        from exepack import unpack_exepack
        original = (PROJECT.parent / 'CHESS.EXE').read_bytes()
        self.assertEqual(hashlib.sha256(original).hexdigest(), 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd')
        decoded = unpack_exepack(original)
        total = 0
        for profile in setup_libh.helper_config()['members']:
            with self.subTest(member=profile['id']):
                result = runtime_libh.link_member(profile['id'])
                origin = int(profile['image_offset'], 0)
                self.assertEqual(len(result.image), profile['code_size'])
                self.assertEqual(result.image, decoded.image[origin:origin + profile['code_size']])
                self.assertEqual(result.provenance['mz_relocations'],
                                 [r - origin for r in decoded.relocations if origin <= r < origin + profile['code_size']])
                evidence = json.loads((PROJECT / profile['rea_evidence']).read_text())
                self.assertEqual(bytes.fromhex(evidence['normalized_result']['bytes_hex']), result.image)
                self.assertFalse(result.provenance['reference_executable_read_or_mounted'])
                self.assertEqual(result.provenance['authored_c_credit'], 0)
                total += len(result.image)
        self.assertEqual(total, 119)

    def test_hdiff_keeps_strict_reader_and_independent_library_pins(self):
        config, profile, member, layout = runtime_libh.load_member('near_hdiff')
        self.assertEqual(config['library_name'], 'SLIBC.LIB')
        self.assertEqual(layout['library_profile'], 'runtime500')
        self.assertEqual(layout['segment']['length'], 45)
        self.assertTrue(layout['runtime_config_sha256'])
        self.assertEqual(len(layout['data_writes']), 2)
        self.assertEqual(layout['data_writes'][1]['overlaps'], [{'start': 42, 'end': 43}])
        with self.assertRaisesRegex(omf.OMFError, 'overlapping LEDATA'):
            omf.read_omf(member.data)
        with patch.object(runtime_libh, 'runtime_config', return_value=dict(config, library_sha256='0'*64)):
            with patch.object(runtime_libh.subprocess, 'run') as run:
                with self.assertRaisesRegex(ValueError, 'manifest'):
                    runtime_libh.link_member('near_hdiff')
                run.assert_not_called()

    def test_unknown_library_profile_is_rejected_before_launch(self):
        config = setup_libh.helper_config()
        config['members'][0]['library_profile'] = '../arbitrary'
        with patch.object(runtime_libh, 'helper_config', return_value=config):
            with patch.object(runtime_libh.subprocess, 'run') as run:
                with self.assertRaisesRegex(library16.LibraryError, 'unknown.*profile'):
                    runtime_libh.link_member(config['members'][0]['id'])
                run.assert_not_called()

    def test_runner_is_fresh_and_mounts_no_reference_executable(self):
        actual_run = subprocess.run
        observed = []
        def observe(args, **kwargs):
            conf = Path(args[args.index('-conf') + 1])
            mounts = [line for line in conf.read_text().splitlines() if line.startswith('mount ')]
            self.assertEqual(len(mounts), 2)
            drive = Path(mounts[0].split('"')[1])
            tools = Path(mounts[1].split('"')[1])
            self.assertEqual({p.name for p in drive.iterdir()}, {'UNIT.OBJ', 'BUILD.BAT'})
            self.assertEqual({p.name for p in tools.iterdir()}, {'LINK.EXE'})
            self.assertNotEqual(drive, PROJECT.parent)
            self.assertIn('-ro', mounts[1])
            observed.append(str(drive))
            return actual_run(args, **kwargs)
        with patch.object(runtime_libh.subprocess, 'run', side_effect=observe):
            first = runtime_libh.link_member('near_lshl')
            second = runtime_libh.link_member('near_lshl')
        self.assertEqual(first.image, second.image)
        self.assertEqual(len(observed), 2)
        self.assertNotEqual(observed[0], observed[1])

    def test_installed_manifest_and_library_forgery_fail_before_linking(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            (project / 'config').mkdir()
            shutil.copy(PROJECT / 'config/runtime_libh.json', project / 'config/runtime_libh.json')
            shutil.copytree(PROJECT / 'toolchains/runtime-libh', project / 'toolchains/runtime-libh')
            library = project / 'toolchains/runtime-libh/LIBH.LIB'
            library.write_bytes(library.read_bytes()[:-1])
            with patch.object(runtime_libh.subprocess, 'run') as run:
                with self.assertRaisesRegex(ValueError, 'pinned configuration'):
                    runtime_libh.link_member('near_lmul', project)
                run.assert_not_called()

    def test_explicit_installer_extracts_the_independent_nested_archive_member(self):
        archive = PROJECT / 'toolchains/runtime-libh/MSC500-DISK4-INCLIBS.json'
        if not archive.exists():
            self.skipTest('retained helper archive unavailable')
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / 'fresh'
            self.assertEqual(setup_libh.install(destination, archive), destination)
            self.assertEqual(hashlib.sha256((destination / 'LIBH.LIB').read_bytes()).hexdigest(), setup_libh.helper_config()['library_sha256'])
            (destination / 'manifest.json').write_text('{}')
            with self.assertRaisesRegex(ValueError, 'manifest'):
                setup_libh.install(destination, archive)
            wrong = Path(temp) / 'wrong.json'
            wrong.write_bytes(b'wrong archive')
            with self.assertRaisesRegex(ValueError, 'archive SHA'):
                setup_libh.install(Path(temp) / 'bad', wrong)
            self.assertFalse((Path(temp) / 'bad').exists())


if __name__ == '__main__':
    unittest.main()
