"""A nonzero real-mode CS must not become a 16-bit image-offset shortcut."""
import copy
import json
from pathlib import Path
import sys
import unittest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from test_link16 import object_with, fixup
from link16 import link_function, LinkError
from omf import Fixup
import check


class CodeFrameTests(unittest.TestCase):
    def test_near_arithmetic_uses_cs_offsets_and_logs_linear_positions(self):
        obj = object_with(b'\xe8\0\0\xc3', [fixup(1, True, (2, 2))])
        code, logs = link_function(obj, '_test', 0xd25, {'_callee': 0xc09}, image_origin=0x10b15)
        self.assertEqual(code, b'\xe8'+((0xc09-0xd28)&65535).to_bytes(2, 'little')+b'\xc3')
        self.assertEqual(logs[0]['arithmetic_result'], 0xc09-0xd28)
        self.assertEqual(logs[0]['image_offset'], 0x10b16)
        self.assertEqual(logs[0]['code_offset'], 0xd26)
        self.assertEqual(logs[0]['code_frame_image_base'], 0xfdf0)

    def test_nonzero_public_own_code_fixups_keep_cs_frame(self):
        obj = object_with(b'\x04\0\xc3', [fixup(0x11, target=(0, 1))], start=0x11)
        before = copy.deepcopy(obj)
        code, logs = link_function(obj, '_test', 0xd25, {}, image_origin=0x10b15)
        self.assertEqual(code, (0xd25-0x11+4).to_bytes(2, 'little')+b'\xc3')
        self.assertEqual(logs[0]['image_offset'], 0x10b15)
        self.assertEqual(obj, before)

    def test_far_segment_loader_site_remains_a_linear_image_position(self):
        f = Fixup(1, 1, 4, 3, True, (5, None), (2, 1), None, 123, b'proof')
        obj = object_with(b'\x9a\0\0\0\0\xcb', [f])
        code, logs = link_function(obj, '_test', 0xd25,
                       {'_global': {'offset': 0xf, 'segment': 0x95d}}, image_origin=0x10b15)
        self.assertEqual(code, bytes.fromhex('9a0f005d09cb'))
        self.assertEqual(logs[0]['mz_segment_relocation_image_offset'], 0x10b18)
        self.assertEqual([x['image_offset'] for x in logs[0]['fields']], [0x10b16, 0x10b18])

    def test_implicit_large_origins_and_ambiguous_mappings_fail(self):
        obj = object_with(b'\xc3', [])
        with self.assertRaises(LinkError): link_function(obj, '_test', 0x10b15, {})
        for image in (True, -1, 0xd24, 0x10b16, 0x110d25):
            with self.subTest(image=image), self.assertRaises(LinkError):
                link_function(obj, '_test', 0xd25, {}, image_origin=image)
        with self.assertRaises(LinkError):
            link_function(object_with(b'\xc3\xc3', []), '_test', 0xffff, {}, image_origin=0x10b0f)

    def test_registry_requires_explicit_consistent_complete_code_address(self):
        unit = json.loads((PROJECT/'config/units.json').read_text())[0]
        unit = unit | {'image_offset': '0x10b15', 'code_address': {'segment': 0xfdf, 'offset': 0xd25}}
        check.validate_units([unit], 82903, 401131)
        for changed in ({'segment': 0xfde, 'offset': 0xd25}, {'segment': True, 'offset': 0xd25},
                        {'segment': 0xfdf, 'offset': 0x10d25}, {'offset': 0xd25}):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                check.validate_units([unit | {'code_address': changed}], 82903, 401131)


if __name__ == '__main__': unittest.main()
