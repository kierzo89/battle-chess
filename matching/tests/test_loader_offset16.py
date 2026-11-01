"""Real C500 LOC5 field checked against independent authentic Microsoft LINK."""
import copy
import dataclasses
import hashlib
import json
from pathlib import Path
import sys
import unittest

M = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(M))
from omf import read_omf
from link16 import link_function, LinkError


class LoaderOffset16Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads((M/'tests/fixtures/loader_offset16.json').read_text())
        raw = bytes.fromhex(cls.fixture['object_hex'])
        assert hashlib.sha256(raw).hexdigest() == cls.fixture['object_sha256']
        cls.original = read_omf(raw)
        cls.field = next(f for f in cls.original.function_info('_main')['fixups']
                         if f.location_type == 5)

    def setUp(self):
        self.obj = copy.deepcopy(self.original)
        pub = self.fixture['runs'][0]['publics']
        self.bindings = {name: ({'segment':pub[name][0], 'offset':pub[name][1]}
                               if name == '_loc5_target' else pub[name][1])
                         for name in self.obj.externals.values() if name != '__acrtused'}

    def link(self, obj=None, bindings=None):
        run = self.fixture['runs'][0]
        check = run['check']
        return link_function(obj or self.obj, '_main', check['code_address']['offset'],
                             self.bindings if bindings is None else bindings,
                             image_origin=check['image_origin'])

    def replace(self, **changes):
        self.obj.fixups = [dataclasses.replace(f, **changes) if f == self.field else f
                           for f in self.obj.fixups]

    def test_real_compiler_full_body_matches_both_authentic_link_orders(self):
        for run in self.fixture['runs']:
            with self.subTest(order=run['object_order']):
                self.assertTrue(run['harness_exit_zero'])
                check = run['check']; pub = run['publics']; seg,off = pub['_loc5_target']
                self.assertGreater(seg, 0)
                bindings = dict(self.bindings, _loc5_target={'segment':seg,'offset':off})
                body,log = link_function(self.obj, '_main', check['code_address']['offset'],
                                         bindings, image_origin=check['image_origin'])
                self.assertEqual(body.hex(), check['linked_hex'])
                entry = next(e for e in log if e.get('location_type') == 5)
                self.assertTrue(entry['loader_resolved_offset16'])
                self.assertEqual(entry['encoded_value'], off)
                self.assertNotIn('mz_segment_relocation_image_offset', entry)
                self.assertEqual(sorted(e['mz_segment_relocation_image_offset'] for e in log
                                        if 'mz_segment_relocation_image_offset' in e),
                                 sorted(check['authentic_mz_sites']))
        # Loader relocation occurs on the adjacent BASE16 field, not LOC5.
        self.assertEqual(self.field.width, 2)
        self.assertEqual(self.field.frame, (5, None))

    def test_rejects_unsupported_width(self):
        self.replace(width=4)
        with self.assertRaises(LinkError): self.link()

    def test_rejects_self_relative_loader_field(self):
        self.replace(segment_relative=False)
        with self.assertRaisesRegex(LinkError, 'segment-relative external'): self.link()

    def test_rejects_non_external_target(self):
        self.replace(target=(0,1))
        with self.assertRaisesRegex(LinkError, 'segment-relative external'): self.link()

    def test_rejects_other_frame(self):
        self.replace(frame=(0,1))
        with self.assertRaisesRegex(LinkError, 'frame'): self.link()

    def test_requires_explicit_far_placement_and_binding(self):
        for bad in [0x100, {'absolute':0x100}]:
            with self.subTest(value=bad), self.assertRaisesRegex(LinkError, 'explicit offset and segment'):
                self.link(bindings=dict(self.bindings, _loc5_target=bad))
        del self.bindings['_loc5_target']
        with self.assertRaisesRegex(LinkError, 'missing explicit external'): self.link()

    def test_rejects_overlap_and_crossing_extent(self):
        self.obj.fixups.append(self.field)
        with self.assertRaisesRegex(LinkError, 'overlapping'): self.link()
        self.obj = copy.deepcopy(self.original)
        self.replace(offset=self.obj.function_info('_main')['end']-1)
        with self.assertRaises(LinkError): self.link()


if __name__ == '__main__': unittest.main()
