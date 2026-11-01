"""Packet tests use synthetic bytes; optional original-file test is analysis only."""
import importlib.util
from pathlib import Path
import struct
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('matching_exepack', ROOT / 'exepack.py')
exepack = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = exepack
spec.loader.exec_module(exepack)


class EXEPACKTests(unittest.TestCase):
    def test_fill_final_packet_keeps_prefix(self):
        packed = b'abc' + b'X' + struct.pack('<H', 20) + b'\xb1' + b'\xff' * 7
        image, prefix, packets = exepack.decode_stream(packed, len(packed), 23)
        self.assertEqual(image, b'abc' + b'X' * 20)
        self.assertEqual(prefix, 3)
        self.assertEqual(packets[0].command, 0xb1)

    def test_literal_and_fill_reverse_order(self):
        packed = b'abc' + b'X' + struct.pack('<H', 20) + b'\xb1'
        packed += b'xyz' + struct.pack('<H', 3) + b'\xb2'
        image, prefix, packets = exepack.decode_stream(packed, len(packed), 26)
        self.assertEqual(image, b'abc' + b'X' * 20 + b'xyz')
        self.assertEqual([p.command for p in packets], [0xb2, 0xb1])

    def test_malformed_streams(self):
        for data, size in [(b'\xb0', 20), (b'X\x14\0\xb1', 19),
                           (b'X\x14\0\xb1', 21), (b'X\x14\0\xb8', 20),
                           (b'X\x14\0\xb0', 20), (b'\x14\0\xb3', 20),
                           (b'X\0\0\xb1', 20)]:
            with self.subTest(data=data, size=size), self.assertRaises(exepack.EXEPACKError):
                exepack.decode_stream(data, len(data), size)

    def test_rejects_non_mz(self):
        with self.assertRaises(exepack.EXEPACKError):
            exepack.unpack_exepack(b'not an executable')

    @unittest.skipUnless((ROOT.parent / 'CHESS.EXE').exists(), 'local original unavailable')
    def test_local_original_analysis(self):
        data = (ROOT.parent / 'CHESS.EXE').read_bytes()
        result = exepack.unpack_exepack(data)
        self.assertEqual(len(result.image), 0x61ef0)
        self.assertEqual(result.prefix_size, 0x110dc)
        self.assertEqual(len(result.relocations), 173)
        self.assertEqual(len(result.packets), 249)
        self.assertEqual(result.image[:result.prefix_size], data[512:512 + result.prefix_size])
        analysis_mz = result.analysis_mz(5)
        self.assertEqual(len(analysis_mz), 1024 + 0x61eeb)
        self.assertEqual(analysis_mz[1024:], result.image[:-5])
        self.assertEqual(struct.unpack_from('<H', analysis_mz, 24)[0], 30)
        with self.assertRaises(exepack.EXEPACKError):
            result.analysis_mz(16)
        damaged = bytearray(data)
        damaged[512 + 0x14142] ^= 1
        with self.assertRaisesRegex(exepack.EXEPACKError, 'decompressor'):
            exepack.unpack_exepack(damaged)


if __name__ == '__main__':
    unittest.main()
