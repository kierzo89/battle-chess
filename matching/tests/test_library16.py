"""Runtime library linking is separate from authored C reconstruction."""
import hashlib
import contextlib
import io
import tempfile
from unittest.mock import patch
import json
from pathlib import Path
import sys
import unittest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
import library16
import omf


def sample(fixups, data=b'\0\0\0\0'):
    obj = omf.OMFObject()
    obj.segments[1] = omf.Segment(1, len(data), 0, 0, 0, 0x48, [(0, data)], name='_TEXT', class_name='CODE')
    obj.externals = {1: '_data', 2: '_callee'}
    obj.fixups = fixups
    return obj


def fixup(at=0, location=1, relative=False, frame=(1, 1), target=(2, 1), displacement=None):
    return omf.Fixup(1, at, 2, location, not relative, frame, target, displacement, 123, b'')


class Library16ArithmeticTests(unittest.TestCase):
    def test_data_frame_and_offset_addends(self):
        obj = sample([fixup(displacement=6)], b'\x04\x00\xc3')
        data, log = library16.link_segment(obj, 1, {1: (0, 0x800)}, {1: 0x5000}, {'_data': (0x5000, 0x4958)})
        self.assertEqual(data, b'\x62\x49\xc3')
        self.assertEqual(log[0]['mode'], 'offset16')
        self.assertEqual(obj.segments[1].chunks[0][1], b'\x04\x00\xc3')

    def test_negative_displacement_wrap_and_segment_base_relocation(self):
        obj = sample([fixup(relative=True, frame=(2, 2), target=(2, 2)),
                      fixup(at=2, location=2, target=(1, 1))])
        data, log = library16.link_segment(obj, 1, {1: (0, 0xff00)}, {1: 0x5cc2}, {'_callee': (0, 0x10)})
        self.assertEqual(data, b'\x0e\x01\xc2\x5c')
        self.assertEqual(log[1]['mz_relocation_image_offset'], 0xff02)

    def test_segment_target_and_code_frame_offset(self):
        obj = sample([fixup(target=(0, 3), displacement=4),
                      fixup(at=2, frame=(0, 1), target=(2, 2))])
        data, _ = library16.link_segment(obj, 1, {1: (0, 0xea86), 3: (0x5cc2, 0x4958)},
                                         {1: 0x5cc2}, {'_callee': (0, 0xebfe)})
        self.assertEqual(data, b'\x5c\x49\xfe\xeb')

    def test_missing_placements_and_unsupported_forms_fail(self):
        failures = [fixup(), fixup(frame=(4, None)), fixup(target=(3, 0)),
                    fixup(location=3), fixup(location=2, relative=True),
                    fixup(location=2, displacement=1)]
        for f in failures:
            with self.subTest(f=f), self.assertRaises(library16.LibraryError):
                library16.link_segment(sample([f]), 1, {1: (0, 100)}, {1: 0x5000}, {})
        with self.assertRaisesRegex(library16.LibraryError, 'share code frame'):
            library16.link_segment(sample([fixup(relative=True)]), 1, {1: (0, 0)}, {1: 2}, {'_data': (2, 0)})

    def test_extent_overlap_hole_and_invalid_placement_fail(self):
        obj = sample([fixup(), fixup()])
        with self.assertRaisesRegex(library16.LibraryError, 'overlapping'):
            library16.link_segment(obj, 1, {1: (0, 0)}, {1: 2}, {'_data': (2, 0)})
        obj = sample([])
        obj.segments[1].chunks = [(1, b'\0\0\0')]
        with self.assertRaisesRegex(library16.LibraryError, 'hole'):
            library16.link_segment(obj, 1, {1: (0, 0)}, {}, {})
        for value in [(True, 0), (0, 65536), (0, -1), 0]:
            with self.assertRaises(library16.LibraryError):
                library16.link_segment(sample([]), 1, {1: value}, {}, {})


class PinnedRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library_path = PROJECT / 'build/probes/SLIBC.LIB'
        if not cls.library_path.exists():
            raise unittest.SkipTest('archived MSC5.00 runtime library not installed')
        cls.library = cls.library_path.read_bytes()
        cls.profile = json.loads((PROJECT / 'evidence/runtime500-placements.json').read_text())

    def test_exact_complete_runtime_segments_and_mz_sites(self):
        target = PROJECT.parent / 'CHESS.EXE'
        if not target.exists():
            self.skipTest('original CHESS.EXE not available for independent comparison')
        from exepack import unpack_exepack
        original = target.read_bytes()
        self.assertEqual(hashlib.sha256(original).hexdigest(), 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd')
        decoded = unpack_exepack(original)
        for module in self.profile['members']:
            member = library16.extract_member(self.library, module['name'], self.profile['library_sha256'], module['member_sha256'])
            self.assertEqual(member.offset, module['library_offset'])
            obj = omf.read_omf(member.data)
            data, log = library16.link_segment(obj, module['segment'],
                       {int(k): v for k, v in module['segments'].items()},
                       {int(k): v for k, v in module['groups'].items()}, module['externals'])
            origin = module['segments']['1'][1]
            self.assertEqual(len(data), obj.segments[1].length)
            self.assertEqual(data, decoded.image[origin:origin + len(data)])
            self.assertEqual([f['mz_relocation_image_offset'] for f in log if f['mode'] == 'base16'],
                             [r for r in decoded.relocations if origin <= r < origin + len(data)])

    def test_pins_checksums_names_and_truncation_fail_closed(self):
        module = self.profile['members'][0]
        args = (module['name'], self.profile['library_sha256'], module['member_sha256'])
        with self.assertRaisesRegex(library16.LibraryError, 'library SHA'):
            library16.extract_member(self.library[:-1], *args)
        with self.assertRaisesRegex(library16.LibraryError, 'member SHA'):
            library16.extract_member(self.library, args[0], args[1], '0' * 64)
        with self.assertRaisesRegex(library16.LibraryError, 'exactly one'):
            library16.extract_member(self.library, 'NO_SUCH_MEMBER', args[1], args[2])
        corrupt = bytearray(self.library)
        corrupt[24] ^= 1
        with self.assertRaisesRegex(library16.LibraryError, 'checksum'):
            library16.extract_member(corrupt, args[0], hashlib.sha256(corrupt).hexdigest(), args[2])


    def test_duplicate_module_names_are_selected_by_independent_member_digest(self):
        profile = json.loads((PROJECT / 'config/runtime500.json').read_text())
        module = next(m for m in profile['members'] if m['name'] == 'MEMCPY')
        member = library16.extract_member(self.library, 'MEMCPY', profile['library_sha256'], module['member_sha256'])
        self.assertEqual(member.offset, module['library_offset'])
        self.assertEqual(omf.read_omf(member.data).segments[module['segment']].length, 44)
        # Even matching digest pins must not pick an arbitrary identical copy.
        raw = bytearray(16)
        raw[0] = 0xf0
        raw[1:3] = (13).to_bytes(2, 'little')
        for _ in range(2):
            raw.extend(member.data)
            raw.extend(b'\0' * ((-len(raw)) % 16))
        dictionary = ((len(raw) + 3 + 511) // 512) * 512
        length = dictionary - len(raw) - 3
        raw.extend(b'\xf1' + length.to_bytes(2, 'little') + b'\0' * length)
        raw.extend(b'\0' * 512)
        raw[3:7] = dictionary.to_bytes(4, 'little')
        raw[7:9] = (1).to_bytes(2, 'little')
        with self.assertRaisesRegex(library16.LibraryError, 'exactly one'):
            library16.extract_member(raw, 'MEMCPY', hashlib.sha256(raw).hexdigest(), member.sha256)

    def test_all_registered_runtime_and_initialized_data_segments_match_in_full(self):
        from exepack import unpack_exepack
        original = (PROJECT.parent / 'CHESS.EXE').read_bytes()
        self.assertEqual(hashlib.sha256(original).hexdigest(), 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd')
        decoded = unpack_exepack(original)
        profiles = [json.loads((PROJECT / 'config/runtime500.json').read_text()),
                    json.loads((PROJECT / 'evidence/runtime-data-members.json').read_text())]
        for profile in profiles:
            for module in profile['members']:
                with self.subTest(member=module['name'], segment=module['segment']):
                    member = library16.extract_member(self.library, module['name'], profile['library_sha256'], module['member_sha256'])
                    self.assertEqual(member.offset, module['library_offset'])
                    obj = omf.read_omf(member.data)
                    segments = {int(k): v for k, v in module['segments'].items()}
                    if module.get('initialized_record_policy') is not None:
                        import runtime_lidata16
                        data, fixups = runtime_lidata16.link_segment(obj, module)
                    else:
                        data, fixups = library16.link_segment(obj, module['segment'], segments,
                                      {int(k): v for k, v in module['groups'].items()}, module['externals'])
                    paragraph, offset = segments[module['segment']]
                    origin = paragraph * 16 + offset
                    self.assertEqual(len(data), obj.segments[module['segment']].length)
                    self.assertEqual(data, decoded.image[origin:origin + len(data)])
                    self.assertEqual([f['mz_relocation_image_offset'] for f in fixups if f['mode'] == 'base16'],
                                     [r for r in decoded.relocations if origin <= r < origin + len(data)])
                    if module.get('reference_region') == 'exepack-expanded':
                        evidence = json.loads((PROJECT / module['rea_evidence']).read_text())
                        self.assertEqual(evidence['subject']['digest']['sha256'], 'faf3516d0e72e30005ad90cb2da165081af5fe6871f5e8c3663980a5d725ef02')
                        self.assertTrue(evidence['normalized_result']['complete'])
                        self.assertEqual(bytes.fromhex(evidence['normalized_result']['bytes_hex']), data)


    def test_cli_uses_distinct_profile_ids_for_code_and_data_artifacts(self):
        config = json.loads((PROJECT / 'config/runtime500.json').read_text())
        code = next(m for m in config['members'] if m['name'] == 'CHKSTK' and m['segment'] == 1)
        data = next(m for m in json.loads((PROJECT / 'evidence/runtime-data-members.json').read_text())['members'] if m['name'] == 'CHKSTK')
        profile = {'library_sha256': config['library_sha256'],
                   'members': [code | {'id': 'chk_code'}, data | {'id': 'chk_data'}]}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / 'profile.json'
            path.write_text(json.dumps(profile))
            args = ['library16', '--library', str(self.library_path), '--profile', str(path), '--output', str(root / 'good')]
            with patch.object(sys, 'argv', args), contextlib.redirect_stdout(io.StringIO()):
                library16.main()
            self.assertEqual(len((root / 'good/chk_code.bin').read_bytes()), 22)
            self.assertEqual(len((root / 'good/chk_data.bin').read_bytes()), 2)
            report = json.loads((root / 'good/GENERATED.json').read_text())
            self.assertEqual([m['id'] for m in report['members']], ['chk_code', 'chk_data'])
            self.assertFalse(report['reference_executable_read'])
            profile['members'][1]['id'] = 'chk_code'
            path.write_text(json.dumps(profile))
            args[-1] = str(root / 'bad')
            with patch.object(sys, 'argv', args), self.assertRaisesRegex(library16.LibraryError, 'unique'):
                library16.main()
            self.assertFalse((root / 'bad').exists())


if __name__ == '__main__':
    unittest.main()
