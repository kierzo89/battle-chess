"""Relocation arithmetic tests using synthetic compiler-object structures."""
import importlib.util
import json
from pathlib import Path
import sys
import unittest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
import omf
import link16


def object_with(data, fixups, start=0, length=None):
    obj = omf.OMFObject()
    obj.segments[1] = omf.Segment(1, start + len(data), 0, 0, 0, 0x48,
                                 [(start, data)], name='_TEXT', class_name='CODE')
    obj.publics['_test'] = omf.Public('_test', 1, start, 0, 0)
    obj.externals = {1: '_global', 2: '_callee'}
    obj.fixups = fixups
    if length is not None:
        obj.procedures['_test'] = {'length': length}
    return obj


def fixup(offset, relative=False, target=(2, 1), frame=(5, None), displacement=None):
    return omf.Fixup(1, offset, 2, 1, not relative, frame, target,
                     displacement, 123, b'\xc4\x00\x56\x01')


class Link16Tests(unittest.TestCase):
    def test_dgroup_addend_and_displacement_are_applied_without_masking(self):
        obj = object_with(b'\xa1\x04\x00\xc3', [fixup(1, displacement=2)])
        linked, log = link16.link_function(obj, '_test', 0x2000, {'_global': 0x9880})
        self.assertEqual(linked, b'\xa1\x86\x98\xc3')
        self.assertEqual(log[0]['original_addend'], 4)
        self.assertEqual(log[0]['target_displacement'], 2)
        self.assertEqual(log[0]['mode'], 'segment_relative_dgroup')
        json.dumps(log)
        self.assertEqual(obj.segments[1].chunks[0][1], b'\xa1\x04\x00\xc3')

    def test_positive_and_negative_near_call_displacements(self):
        for target in (0x2500, 0x0d8d):
            obj = object_with(b'\xe8\x00\x00\xc3', [fixup(1, True, (2, 2))])
            linked, log = link16.link_function(obj, '_test', 0x2000, {'_callee': target})
            self.assertEqual(int.from_bytes(linked[1:3], 'little'), (target - 0x2003) & 0xffff)
            self.assertEqual(log[0]['arithmetic_result'], target - 0x2003)

    def test_origin_is_function_origin_not_object_segment_origin(self):
        obj = object_with(b'\xe8\x02\x00\xc3', [fixup(0x11, True, (2, 2), displacement=3)],
                          start=0x10)
        linked, log = link16.link_function(obj, '_test', 0x2000, {'_callee': 0x2100})
        self.assertEqual(linked, b'\xe8\x02\x01\xc3')
        self.assertEqual(log[0]['code_segment_origin'], 0x1ff0)
        self.assertEqual(log[0]['image_offset'], 0x2001)

    def test_same_code_segment_target_uses_segment_placement(self):
        obj = object_with(b'\xe8\x20\x00\xc3', [fixup(0x11, True, (0, 1))], start=0x10)
        linked, _ = link16.link_function(obj, '_test', 0x2000, {})
        self.assertEqual(linked, b'\xe8\x0d\x00\xc3')

    def test_own_public_code_offsets_use_combined_cs_frame_for_both_frame_forms(self):
        # Dispatcher operand (F5) plus a switch word (F0), at a nonzero public
        # offset. Their targets retain the object's CODE contribution placement.
        original = b'\xff\x04\x00\x08\x00\xc3'
        fixes = [fixup(0x31, target=(0, 1), displacement=3),
                 fixup(0x33, target=(0, 1), frame=(0, 1), displacement=5)]
        obj = object_with(original, fixes, start=0x30)
        for origin in (0x2000, 0x9000):
            with self.subTest(origin=origin):
                linked, log = link16.link_function(obj, '_test', origin, {})
                base = origin - 0x30
                self.assertEqual(linked, b'\xff' + (base+4+3).to_bytes(2, 'little') +
                                 (base+8+5).to_bytes(2, 'little') + b'\xc3')
                for entry, addend, displacement in zip(log, [4, 8], [3, 5]):
                    self.assertEqual(entry['mode'], 'segment_relative_code')
                    self.assertEqual(entry['target_offset'], base)
                    self.assertEqual(entry['original_addend'], addend)
                    self.assertEqual(entry['target_displacement'], displacement)
                    self.assertEqual(entry['arithmetic_result'], base+addend+displacement)
                    self.assertEqual(entry['code_frame_offset'], 0)
                    self.assertEqual(entry['code_frame_segment'], 1)
                self.assertEqual([e['frame_method'] for e in log], [5, 0])
                json.dumps(log)
        self.assertEqual(obj.segments[1].chunks[0][1], original)

    def test_own_code_accepts_only_public_combine_variants(self):
        # TIS SEGDEF C=2,4,7 are PUBLIC; stack/common/private are different.
        for combine in (2, 4, 7):
            obj = object_with(b'\x03\x00\xc3', [fixup(0, target=(0, 1))])
            obj.segments[1].attributes = 0x40 | (combine << 2)
            self.assertEqual(link16.link_function(obj, '_test', 0x100, {})[0],
                             b'\x03\x01\xc3')
        for attributes in (0x40, 0x44, 0x4c, 0x54, 0x58, 0x08, 0x49):
            with self.subTest(attributes=attributes):
                obj = object_with(b'\x00\x00\xc3', [fixup(0, target=(0, 1))])
                obj.segments[1].attributes = attributes
                with self.assertRaisesRegex(link16.LinkError, 'public CODE SEGDEF'):
                    link16.link_function(obj, '_test', 0x100, {})

    def test_own_code_rejects_other_segment_frame_class_and_group(self):
        for target, frame in [((0, 2), (5, None)), ((0, 1), (0, 2)),
                              ((0, 1), (1, 1)), ((0, 1), (4, None)),
                              ((0, 1), (5, 1))]:
            with self.subTest(target=target, frame=frame):
                obj = object_with(b'\x00\x00\xc3', [fixup(0, target=target, frame=frame)])
                with self.assertRaises(link16.LinkError):
                    link16.link_function(obj, '_test', 0x100, {})
        obj = object_with(b'\x00\x00\xc3', [fixup(0, target=(0, 1))])
        obj.segments[1].class_name = 'DATA'  # _TEXT name alone is insufficient.
        with self.assertRaisesRegex(link16.LinkError, 'public CODE SEGDEF'):
            link16.link_function(obj, '_test', 0x100, {})
        obj.segments[1].class_name = 'CODE'
        obj.publics['_test'] = omf.Public('_test', 1, 0, 1, 0)
        with self.assertRaisesRegex(link16.LinkError, 'public CODE SEGDEF'):
            link16.link_function(obj, '_test', 0x100, {})

    def test_explicit_code_frame_does_not_relax_external_or_far_pointer_policy(self):
        obj = object_with(b'\x00\x00\xc3', [fixup(0, frame=(0, 1))])
        with self.assertRaisesRegex(link16.LinkError, 'frame'):
            link16.link_function(obj, '_test', 0x100, {'_global': 0x200})
        far = omf.Fixup(1, 0, 4, 3, True, (0, 1), (2, 2), None, 1, b'')
        with self.assertRaisesRegex(link16.LinkError, 'frame'):
            link16.link_function(object_with(b'\x00'*5, [far]), '_test', 0x100,
                                 {'_callee': {'offset': 0x200, 'segment': 0}})

    def test_codeview_extent_is_respected_and_fallback_keeps_padding(self):
        obj = object_with(b'\xc3\x90', [], length=1)
        self.assertEqual(link16.link_function(obj, '_test', 0x100, {})[0], b'\xc3')
        obj.procedures.clear()
        self.assertEqual(link16.link_function(obj, '_test', 0x100, {})[0], b'\xc3\x90')

    def test_relocations_may_not_cross_procedure_boundary_or_overlap(self):
        obj = object_with(b'\x00\x00\xc3', [fixup(0)], length=1)
        with self.assertRaisesRegex(link16.LinkError, 'crosses'):
            link16.link_function(obj, '_test', 0x100, {'_global': 0})
        obj = object_with(b'\x00\x00\xc3', [fixup(0), fixup(0)])
        with self.assertRaisesRegex(link16.LinkError, 'overlapping'):
            link16.link_function(obj, '_test', 0x100, {'_global': 0})

    def test_unknown_placements_frames_targets_and_locations_fail(self):
        for f in (fixup(0, frame=(1, 1)), fixup(0, target=(1, 1)),
                  fixup(0, target=(0, 2)), fixup(0)):
            obj = object_with(b'\x00\x00\xc3', [f])
            with self.assertRaises(link16.LinkError):
                link16.link_function(obj, '_test', 0x100, {})
        f = omf.Fixup(1, 0, 1, 0, True, (5, None), (2, 1), None, 1, b'')
        with self.assertRaisesRegex(link16.LinkError, 'OFFSET16'):
            link16.link_function(object_with(b'\x00\xc3', [f]), '_test', 0x100, {'_global': 0})

    def test_segment_wrap_encoding_and_input_validation(self):
        obj = object_with(b'\xe8\x00\x00\xc3', [fixup(1, True, (2, 2))])
        linked, _ = link16.link_function(obj, '_test', 0xff00, {'_callee': 0x100})
        self.assertEqual(linked[1:3], ((0x100 - 0xff03) & 0xffff).to_bytes(2, 'little'))
        for origin, placements in ((-1, {}), (True, {}), (0x10000, {}),
                                   (0xffff, {}), (0, {'_callee': '0x100'}),
                                   (0, {'_callee': 0x10000})):
            with self.assertRaises(link16.LinkError):
                link16.link_function(obj, '_test', origin, placements)

    def test_far16_pointer_external_and_segment_relocation_log(self):
        f = omf.Fixup(1, 1, 4, 3, True, (5, None), (2, 2), None, 12, b'far')
        obj = object_with(b'\x9a\x00\x00\x00\x00\xc3', [f])
        linked, log = link16.link_function(obj, '_test', 0x7ddb,
                                          {'_callee': {'offset': 0xfce8, 'segment': 0}})
        self.assertEqual(linked, b'\x9a\xe8\xfc\x00\x00\xc3')
        self.assertEqual(log[0]['width'], 4)
        self.assertEqual(log[0]['encoded_hex'], 'e8fc0000')
        self.assertEqual(log[0]['mz_segment_relocation_image_offset'], 0x7dde)
        self.assertEqual(log[0]['fields'][1]['encoded_value'], 0)
        json.dumps(log)

    def test_far16_addends_and_displacement_and_unsupported_forms(self):
        f = omf.Fixup(1, 0, 4, 3, True, (5, None), (2, 2), 3, 12, b'far')
        obj = object_with(b'\x02\x00\x01\x00\xc3', [f])
        linked, log = link16.link_function(obj, '_test', 0x100,
                                          {'_callee': {'offset': 0x1234, 'segment': 0x2345}})
        self.assertEqual(linked, b'\x39\x12\x46\x23\xc3')
        self.assertEqual(log[0]['original_segment_addend'], 1)
        for target in (0x1234, {'offset': 1}, {'offset': 1, 'segment': 2, 'unknown': 0},
                       {'offset': 1, 'segment': 0x10000}):
            with self.assertRaises(link16.LinkError):
                link16.link_function(obj, '_test', 0x100, {'_callee': target})
        for location, width, relative, target in ((2, 2, True, (0, 1)),
                                                  (3, 4, False, (2, 2)),
                                                  (3, 4, True, (0, 1))):
            bad = omf.Fixup(1, 0, width, location, relative, (5, None), target, None, 1, b'')
            with self.assertRaises(link16.LinkError):
                link16.link_function(object_with(b'\x00' * 5, [bad]), '_test', 0x100,
                                     {'_callee': {'offset': 1, 'segment': 2}})
        # A separate OFFSET16 deliberately selects the explicit far offset.
        linked, log = link16.link_function(object_with(b'\x00\x00\xc3', [fixup(0)]),
                                          '_test', 0x100,
                                          {'_global': {'offset': 1, 'segment': 2}})
        self.assertEqual(linked, b'\x01\x00\xc3')
        self.assertEqual(log[0]['mode'], 'far_offset16')
        self.assertNotIn('mz_segment_relocation_image_offset', log[0])

    def test_split_far_offset_and_base_have_independent_addends_and_mz_site(self):
        base = omf.Fixup(1, 0x24, 2, 2, True, (5, None), (2, 1), None, 12, b'base')
        offset = fixup(0x21, displacement=2)
        obj = object_with(b'\xb8\x04\x00\xba\x01\x00\xc3', [offset, base], start=0x20)
        for origin in (0x2000, 0x7000):
            linked, log = link16.link_function(obj, '_test', origin,
                                               {'_global': {'offset': 0x3f90, 'segment': 0x120d}})
            self.assertEqual(linked, bytes.fromhex('b8963fba0e12c3'))
            self.assertEqual([x['mode'] for x in log], ['far_offset16', 'segment_base16'])
            self.assertNotIn('mz_segment_relocation_image_offset', log[0])
            self.assertEqual(log[1]['mz_segment_relocation_image_offset'], origin+4)
            self.assertEqual(log[1]['encoded_segment_value'], 0x120e)
            self.assertEqual(log[1]['fields'][0]['original_addend'], 1)
        self.assertEqual(obj.segments[1].chunks[0][1], bytes.fromhex('b80400ba0100c3'))

    def test_base_requires_explicit_far_target_and_proven_frame_forms(self):
        for relative, target, frame, displacement in [
                (False, (2, 1), (5, None), None), (True, (0, 1), (5, None), None),
                (True, (2, 1), (0, 1), None), (True, (2, 1), (5, None), 1)]:
            f = omf.Fixup(1, 0, 2, 2, relative, frame, target, displacement, 1, b'')
            with self.subTest(f=f), self.assertRaises(link16.LinkError):
                link16.link_function(object_with(b'\x00\x00\xc3', [f]), '_test', 0x100,
                                     {'_global': {'offset': 0x3f90, 'segment': 0x120d}})
        base = omf.Fixup(1, 0, 2, 2, True, (5, None), (2, 1), None, 1, b'')
        for target in [0x120d, {'absolute': 12}]:
            with self.subTest(target=target), self.assertRaises(link16.LinkError):
                link16.link_function(object_with(b'\x00\x00\xc3', [base]), '_test',
                                     0x100, {'_global': target})

    def test_absolute_word_is_explicit_and_never_emits_loader_relocation(self):
        obj = object_with(b'\x03\x00\xc3', [fixup(0, displacement=2)])
        linked, log = link16.link_function(obj, '_test', 0x100, {'_global': {'absolute': 12}})
        self.assertEqual(linked, bytes.fromhex('1100c3'))
        self.assertEqual(log[0]['mode'], 'absolute16')
        self.assertNotIn('mz_segment_relocation_image_offset', log[0])
        for value in [True, -1, 0x10000, '12']:
            with self.subTest(value=value), self.assertRaises(link16.LinkError):
                link16.link_function(obj, '_test', 0x100, {'_global': {'absolute': value}})
        near = object_with(b'\xe8\x00\x00\xc3', [fixup(1, relative=True)])
        with self.assertRaises(link16.LinkError):
            link16.link_function(near, '_test', 0x100, {'_global': {'absolute': 12}})

    def test_hole_in_function_data_is_not_zero_filled(self):
        obj = object_with(b'\x55\x5d\xc3', [])
        obj.segments[1].chunks = [(0, b'\x55'), (2, b'\xc3')]
        with self.assertRaisesRegex(link16.LinkError, 'hole'):
            link16.link_function(obj, '_test', 0x100, {})


if __name__ == '__main__':
    unittest.main()
