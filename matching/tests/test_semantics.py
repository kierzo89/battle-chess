"""Portable C versus execution of original 8086 bytes, not just a restated formula.

Requires host cc and the optional Unicorn dependency. This establishes bounded
semantic evidence, not C byte matching or whole-game runtime correctness.
"""
import ctypes
import hashlib
from pathlib import Path
import random
import shutil
import struct
import subprocess
import tempfile
import unittest

try:
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16
    from unicorn.x86_const import (UC_X86_REG_AX, UC_X86_REG_BP, UC_X86_REG_SP,
                                  UC_X86_REG_ES, UC_X86_REG_CX, UC_X86_REG_IP)
except ImportError:
    Uc = None

PROJECT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(Uc and shutil.which('cc'), 'Unicorn and host cc required')
class OriginalCodeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmp.cleanup)
        lib = Path(cls.tmp.name) / 'math16.so'
        subprocess.run(['cc', '-std=c99', '-Wall', '-Wextra', '-Werror', '-pedantic',
                        '-shared', '-fPIC', str(PROJECT / 'src/math16.c'),
                        str(PROJECT / 'src/sign_5c8b_probe.c'), '-o', str(lib)], check=True)
        cls.lib = ctypes.CDLL(str(lib))
        cls.image = (PROJECT.parent / 'CHESS.EXE').read_bytes()
        if hashlib.sha256(cls.image).hexdigest() != 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd':
            raise ValueError('Wrong executable')
        cls.image = cls.image[512:]
        cls.cpu = Uc(UC_ARCH_X86, UC_MODE_16)
        cls.cpu.mem_map(0, 0x10000)
        cls.cpu.mem_write(0, cls.image[:0x10000])
        for name, count in [('min_i16', 2), ('max_i16', 2), ('abs_i16', 1)]:
            f = getattr(cls.lib, name)
            f.argtypes = [ctypes.c_int16] * count
            f.restype = ctypes.c_int16

    def original(self, offset, *args):
        # Near cdecl: return IP, arguments. RET stops at sentinel IP 0200.
        self.cpu.mem_write(0x7000, struct.pack('<' + 'H' * (len(args) + 1), 0x0200, *(x & 0xffff for x in args)))
        self.cpu.reg_write(UC_X86_REG_SP, 0x7000)
        self.cpu.reg_write(UC_X86_REG_BP, 0x6abc)
        self.cpu.emu_start(offset, 0x0200, count=32)
        self.assertEqual(self.cpu.reg_read(UC_X86_REG_SP), 0x7002)
        self.assertEqual(self.cpu.reg_read(UC_X86_REG_BP), 0x6abc)
        return ctypes.c_int16(self.cpu.reg_read(UC_X86_REG_AX)).value

    def test_abs_all_65536_inputs(self):
        for a in range(-32768, 32768):
            self.assertEqual(self.lib.abs_i16(a), self.original(0x8fb5, a), a)

    def test_signum_all_65536_inputs_with_original_stack_probe(self):
        sign = self.lib.sign_5c8b
        sign.argtypes = [ctypes.c_int]
        sign.restype = ctypes.c_int
        self.cpu.mem_write(0x4a00, struct.pack('<H', 0x6000))
        for value in range(-32768, 32768):
            self.assertEqual(sign(value), self.original(0x5c8b, value), value)

    def test_min_max_signed_edges_and_deterministic_pairs(self):
        edges = [-32768, -32767, -256, -1, 0, 1, 255, 32766, 32767]
        rng = random.Random(1988)
        pairs = [(a, b) for a in edges for b in edges]
        pairs += [(rng.randrange(-32768, 32768), rng.randrange(-32768, 32768)) for _ in range(4096)]
        for name, off in [('min_i16', 0x8f95), ('max_i16', 0x8fa5)]:
            for a, b in pairs:
                self.assertEqual(getattr(self.lib, name)(a, b), self.original(off, a, b), (name, a, b))

    def test_original_segment_load_resolves_rea_disassembly_discrepancy(self):
        self.cpu.reg_write(UC_X86_REG_AX, 0x3456)
        self.cpu.reg_write(UC_X86_REG_ES, 0x1234)
        self.cpu.emu_start(0xe04d, 0xe04f, count=1)
        self.assertEqual(self.cpu.reg_read(UC_X86_REG_ES), 0x3456)
        self.assertEqual(self.cpu.reg_read(UC_X86_REG_AX), 0x3456)

    def test_original_stack_allocation_success_boundary_and_overflow(self):
        self.cpu.mem_write(0x4a00, struct.pack('<H', 0x6000))
        for request, overflow in [(0x20, False), (0x1002, False), (0x1003, True), (0x8000, True)]:
            self.cpu.mem_write(0x7000, struct.pack('<H', 0x0200))
            self.cpu.reg_write(UC_X86_REG_SP, 0x7000)
            self.cpu.reg_write(UC_X86_REG_AX, request)
            stop = 0xeb2a if overflow else 0x0200
            self.cpu.emu_start(0xecaa, stop, count=32)
            self.assertEqual(self.cpu.reg_read(UC_X86_REG_IP), stop)
            self.assertEqual(self.cpu.reg_read(UC_X86_REG_CX), 0x0200)
            self.assertEqual(self.cpu.reg_read(UC_X86_REG_SP), 0x7002 if overflow else 0x7002 - request)
            self.assertEqual(self.cpu.reg_read(UC_X86_REG_AX), 0 if overflow else request)


if __name__ == '__main__':
    unittest.main()
