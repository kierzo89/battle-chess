"""Complete loader-site coverage matters even when unrelocated bytes match."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check import validate_emitted_mz_sites


class MZSiteTests(unittest.TestCase):
    def unit(self, sites, language='c'):
        return {'language': language, 'image_offset': '0x100', 'size': 10,
                'relocations': [{'mz_segment_relocation_image_offset': p} for p in sites]}

    def test_complete_set_is_required_for_both_c_and_runtime(self):
        for language in ('c', 'runtime'):
            validate_emitted_mz_sites(self.unit([0x102, 0x107], language), {0x80, 0x102, 0x107, 0x110})
            validate_emitted_mz_sites(self.unit([], language), {0x80, 0x110})
            for emitted in ([], [0x102], [0x102, 0x107, 0x108]):
                with self.subTest(language=language, emitted=emitted), self.assertRaisesRegex(ValueError, 'set differs'):
                    validate_emitted_mz_sites(self.unit(emitted, language), {0x102, 0x107})

    def test_loader_word_cannot_cross_the_extent_end(self):
        with self.assertRaisesRegex(ValueError, 'crosses'):
            validate_emitted_mz_sites(self.unit([0x109]), {0x109})

    def test_ordinary_offsets_do_not_count_as_loader_sites(self):
        u = self.unit([])
        u['relocations'] = [{'mode': 'far_offset16', 'image_offset': 0x102},
                            {'mode': 'absolute16', 'image_offset': 0x107}]
        with self.assertRaisesRegex(ValueError, 'set differs'):
            validate_emitted_mz_sites(u, {0x102})


if __name__ == '__main__': unittest.main()
