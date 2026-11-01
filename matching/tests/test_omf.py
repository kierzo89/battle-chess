"""Synthetic OMF86 validation tests; no original game bytes are fixtures."""
import importlib.util
from pathlib import Path
import struct
import sys
import unittest

spec = importlib.util.spec_from_file_location('matching_omf', Path(__file__).resolve().parents[1] / 'omf.py')
omf = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = omf
spec.loader.exec_module(omf)


def record(kind, payload=b''):
    prefix = bytes([kind]) + struct.pack('<H', len(payload) + 1) + payload
    return prefix + bytes([-sum(prefix) & 255])


def name(value):
    value = value.encode('ascii')
    return bytes([len(value)]) + value


def public(symbol, offset):
    return name(symbol) + struct.pack('<H', offset) + b'\x00'


def module(chunks=((0, b'\x55\x5d\xc3\x90'),), size=4, symbols=(('_first', 0),), extra=()):
    records = [record(0x80, name('synthetic.c')),
               record(0x96, name('') + name('_TEXT') + name('CODE')),
               record(0x98, b'\x48' + struct.pack('<H', size) + b'\x02\x03\x01'),
               record(0x90, b'\x00\x01' + b''.join(public(*p) for p in symbols))]
    records += [record(0xa0, b'\x01' + struct.pack('<H', offset) + data)
                for offset, data in chunks]
    records += list(extra)
    return b''.join(records) + record(0x8a, b'\x00')


class OMFTests(unittest.TestCase):
    def test_extract_all_bytes_including_padding(self):
        obj = omf.read_omf(module())
        self.assertEqual(obj.extract_function('_first'), b'\x55\x5d\xc3\x90')
        self.assertEqual(obj.function_info('_first')['size'], 4)
        self.assertEqual(obj.segments[1].class_name, 'CODE')

    def test_public_boundaries_and_explicit_end(self):
        data = module(symbols=(('_first', 0), ('_end', 3)))
        self.assertEqual(omf.extract_function(data, '_first'), b'\x55\x5d\xc3')
        self.assertEqual(omf.extract_function(data, '_first', '_end'), b'\x55\x5d\xc3')
        obj = omf.read_omf(data)
        self.assertEqual(obj.function_info('_first', '_end')['boundary'], 'explicit_public')
        with self.assertRaises(omf.OMFError):
            obj.extract_function('_first', '_missing')
        with self.assertRaises(omf.OMFError):
            obj.extract_function('_end', '_first')

    def test_out_of_order_contiguous_ledata_is_valid(self):
        self.assertEqual(omf.extract_function(module(chunks=((2, b'\xc3\x90'),
                                                            (0, b'\x55\x5d'))), '_first'),
                         b'\x55\x5d\xc3\x90')

    def test_holes_overlap_and_bounds_rejected(self):
        for chunks, message in [(((0, b'\x55'), (2, b'\xc3\x90')), 'hole'),
                                (((0, b'123'), (2, b'45')), 'exceeds|overlapping'),
                                (((4, b'x'),), 'exceeds')]:
            with self.subTest(chunks=chunks), self.assertRaisesRegex(omf.OMFError, message):
                omf.extract_function(module(chunks=chunks), '_first')

    def test_invalid_record_framing_and_checksum(self):
        good = module()
        for bad in (good[:-1], good[:2], good + b'\x00', b'\x80\x00\x00',
                    good[:4] + bytes([good[4] ^ 1]) + good[5:]):
            with self.subTest(bad=bad[:10]), self.assertRaises(omf.OMFError):
                omf.read_omf(bad)

    def test_symbols_must_be_unambiguous_and_in_bounds(self):
        for symbols in ((('_first', 0), ('_first', 1)), (('_first', 5),)):
            with self.assertRaises(omf.OMFError):
                omf.read_omf(module(symbols=symbols))
        with self.assertRaisesRegex(omf.OMFError, 'not found'):
            omf.extract_function(module(), 'missing')

    def test_fixup_is_recorded_and_blocks_extraction(self):
        # OFFSET16 at LEDATA+1; frame is current segment, target segment 1;
        # P=1 means no target displacement. Every object byte is preserved.
        fixup = b'\xc4\x01\x54\x01'
        obj = omf.read_omf(module(extra=(record(0x9c, fixup),)))
        f = obj.fixups[0]
        self.assertEqual((f.segment, f.offset, f.width, f.location_type), (1, 1, 2, 1))
        self.assertEqual(f.frame, (5, None))
        self.assertEqual(f.target, (0, 1))
        self.assertEqual(f.raw, fixup)
        with self.assertRaisesRegex(omf.OMFError, 'unresolved FIXUPP'):
            obj.extract_function('_first')

    def test_fixup_outside_function_does_not_block_other_function(self):
        obj = omf.read_omf(module(symbols=(('_first', 0), ('_second', 1)),
                                 extra=(record(0x9c, b'\xc4\x01\x54\x01'),)))
        self.assertEqual(obj.extract_function('_first'), b'\x55')
        with self.assertRaises(omf.OMFError):
            obj.extract_function('_second')

    def test_fixup_crossing_boundary_blocks_both_functions(self):
        obj = omf.read_omf(module(symbols=(('_first', 0), ('_second', 2)),
                                 extra=(record(0x9c, b'\xc4\x01\x54\x01'),)))
        for symbol in ('_first', '_second'):
            with self.assertRaisesRegex(omf.OMFError, 'FIXUPP'):
                obj.extract_function(symbol)

    def test_thread_definitions_before_ledata_and_thread_reference(self):
        data = module()
        # Frame thread 0 uses segment 1; target thread 0 uses segment 1.
        marker = record(0xa0, b'\x01\x00\x00\x55\x5d\xc3\x90')
        data = data.replace(marker, record(0x9c, b'\x40\x01\x00\x01') + marker
                            + record(0x9c, b'\xc4\x01\x8c'))
        obj = omf.read_omf(data)
        self.assertEqual(obj.fixups[0].frame, (0, 1))
        self.assertEqual(obj.fixups[0].target, (0, 1))

    def test_codeview3_compiler_extent_excludes_padding_and_backpatches(self):
        def proc(length):
            payload = (b'\x01' + struct.pack('<6H', 0, 0x206, length, 1, 2, 0)
                       + b'\x00' + name('first'))
            return bytes([len(payload)]) + payload

        debug = proc(3)
        extra = [record(0x96, name('$$SYMBOLS') + name('DEBSYM')),
                 record(0x98, b'\x20' + struct.pack('<H', len(debug)) + b'\x04\x05\x01'),
                 record(0x8c, name('_first') + b'\x00'),
                 record(0xa0, b'\x02\x00\x00' + proc(0)),
                 record(0x9c, b'\xc4\x02\x56\x01'),
                 record(0xa0, b'\x02\x00\x00' + debug),
                 record(0x9c, b'\xc4\x02\x56\x01')]
        obj = omf.read_omf(module(extra=extra))
        self.assertEqual(obj.extract_function('_first'), b'\x55\x5d\xc3')
        self.assertEqual(obj.function_info('_first')['boundary'], 'codeview3_procedure')
        self.assertEqual(obj.procedures['_first']['length'], 3)
        # Even superseded debug relocations remain recorded as evidence.
        self.assertEqual(len(obj.fixups), 2)
        # Missing / malformed procedure relocation cannot silently bound code.
        with self.assertRaisesRegex(omf.OMFError, 'unique external'):
            omf.read_omf(module(extra=extra[:-1]))
        bad_extra = list(extra)
        bad_extra[-1] = record(0x9c, b'\xc4\x02\x54\x01')
        with self.assertRaisesRegex(omf.OMFError, 'unique external'):
            omf.read_omf(module(extra=bad_extra))

    def test_target_thread_high_method_bit_does_not_override_fixup_p(self):
        # TIS OMF1.1: target THREAD uses low two method bits; actual
        # referring FIXUP P controls displacement, even for encoded T4.
        obj = omf.read_omf(module(extra=(record(0x9c, b'\x10\x01\xc4\x00\x58\x34\x12'),)))
        self.assertEqual(obj.fixups[0].target, (0, 1))
        self.assertEqual(obj.fixups[0].displacement, 0x1234)
        obj = omf.read_omf(module(extra=(record(0x9c, b'\x18\x01\xc4\x00\x5c'),)))
        self.assertEqual(obj.fixups[0].target, (2, 1))
        self.assertIsNone(obj.fixups[0].displacement)
        with self.assertRaisesRegex(omf.OMFError, 'reserved target'):
            omf.read_omf(module(extra=(record(0x9c, b'\x1c\x01'),)))

    def test_bad_fixups_and_32bit_or_iterated_data_are_rejected(self):
        for payload in (b'\xc4', b'\xc4\x03\x54\x01', b'\xc4\x01\x8c'):
            with self.assertRaises(omf.OMFError):
                omf.read_omf(module(extra=(record(0x9c, payload),)))
        for kind in (0x99, 0xa1, 0x9d, 0xc2):
            with self.assertRaises(omf.OMFError):
                omf.read_omf(module(extra=(record(kind),)))
        with self.assertRaisesRegex(omf.OMFError, 'iterated'):
            omf.extract_function(module(extra=(record(0xa2, b'\x01\x00\x00'),)), '_first')


if __name__ == '__main__':
    unittest.main()
