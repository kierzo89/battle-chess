"""Execute freshly authored wrappers with synthetic BIOS interrupt responses.

This checks 8086 wrapper behavior, not actual keyboard/timer devices. No
original executable bytes enter the emulated code or synthetic responses.
"""
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import unittest

try:
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_INTR
    from unicorn.x86_const import (UC_X86_REG_AX, UC_X86_REG_BP,
        UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_SS, UC_X86_REG_SP,
        UC_X86_REG_IP, UC_X86_REG_CX, UC_X86_REG_DX, UC_X86_REG_EFLAGS)
except ImportError:
    Uc = None

M = Path(__file__).resolve().parents[1]


@unittest.skipUnless(Uc and shutil.which('nasm'), 'Unicorn and NASM required')
class BiosWrapperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.code = {}
        with tempfile.TemporaryDirectory() as tmp:
            for name, at in [('poll_event_ea32', 0xea32), ('bios_ticks_ea5b', 0xea5b)]:
                output = Path(tmp) / (name + '.bin')
                subprocess.run(['nasm', '-f', 'bin', str(M/'asm'/(name+'.asm')),
                                '-o', str(output)], check=True)
                cls.code[at] = output.read_bytes()

    def machine(self, interrupt):
        cpu = Uc(UC_ARCH_X86, UC_MODE_16)
        cpu.mem_map(0, 0x100000)
        for at, code in self.code.items():
            cpu.mem_write(at, code)
        for reg, value in [(UC_X86_REG_CS, 0), (UC_X86_REG_DS, 0x2000),
                           (UC_X86_REG_SS, 0x4000)]:
            cpu.reg_write(reg, value)
        cpu.hook_add(UC_HOOK_INTR, interrupt)
        return cpu

    def call(self, cpu, at, *args):
        cpu.mem_write(0x48000, struct.pack('<'+'H'*(len(args)+1), 0x200, *args))
        cpu.reg_write(UC_X86_REG_SP, 0x8000)
        cpu.reg_write(UC_X86_REG_BP, 0x7654)
        cpu.emu_start(at, 0x200, count=200)
        self.assertEqual(cpu.reg_read(UC_X86_REG_IP), 0x200)
        self.assertEqual(cpu.reg_read(UC_X86_REG_SP), 0x8002)
        self.assertEqual(cpu.reg_read(UC_X86_REG_BP), 0x7654)
        self.assertEqual(cpu.reg_read(UC_X86_REG_DS), 0x2000)

    def test_no_key_returns_zero_and_does_not_write_outputs(self):
        calls = []
        def bios(cpu, number, _):
            calls.append((number, cpu.reg_read(UC_X86_REG_AX) >> 8))
            self.assertEqual(calls[-1], (0x16, 1))
            cpu.reg_write(UC_X86_REG_EFLAGS, cpu.reg_read(UC_X86_REG_EFLAGS) | 0x40)
        cpu = self.machine(bios)
        before = bytes(range(32))
        cpu.mem_write(0x21000, before)
        self.call(cpu, 0xea32, 0x1001, 0x1009, 0x1011)
        self.assertEqual(cpu.reg_read(UC_X86_REG_AX), 0)
        self.assertEqual(bytes(cpu.mem_read(0x21000, 32)), before)
        self.assertEqual(calls, [(0x16, 1)])

    def test_key_writes_only_three_low_bytes_including_extended_key(self):
        for ascii_byte, scan, shift in [(ord('A'), 0x1e, 3), (0, 0x48, 0x82)]:
            with self.subTest(ascii=ascii_byte, scan=scan, shift=shift):
                calls = []
                def bios(cpu, number, _):
                    ah = cpu.reg_read(UC_X86_REG_AX) >> 8
                    self.assertEqual(number, 0x16)
                    calls.append(ah)
                    if ah == 1:
                        cpu.reg_write(UC_X86_REG_EFLAGS,
                                      cpu.reg_read(UC_X86_REG_EFLAGS) & ~0x40)
                    elif ah == 0:
                        cpu.reg_write(UC_X86_REG_AX, scan << 8 | ascii_byte)
                    elif ah == 2:
                        cpu.reg_write(UC_X86_REG_AX, 0xab00 | shift)
                    else:
                        self.fail('Unexpected synthetic BIOS function')
                cpu = self.machine(bios)
                before = bytes(range(32))
                cpu.mem_write(0x21000, before)
                self.call(cpu, 0xea32, 0x1001, 0x1009, 0x1011)
                expected = bytearray(before)
                expected[1], expected[9], expected[17] = shift, ascii_byte, scan
                self.assertEqual(bytes(cpu.mem_read(0x21000, 32)), bytes(expected))
                self.assertEqual(cpu.reg_read(UC_X86_REG_AX), 1)
                self.assertEqual(calls, [1, 0, 2])

    def test_ticks_convert_cx_dx_to_dx_ax_and_preserve_bios_carry(self):
        for high, low, rollover, carry in [(0x12, 0x3456, 0, 0), (0xabcd, 0xffff, 1, 1)]:
            with self.subTest(high=high, low=low, carry=carry):
                calls = []
                def bios(cpu, number, _):
                    self.assertEqual(number, 0x1a)
                    self.assertEqual(cpu.reg_read(UC_X86_REG_AX) >> 8, 0)
                    calls.append(number)
                    cpu.reg_write(UC_X86_REG_CX, high)
                    cpu.reg_write(UC_X86_REG_DX, low)
                    cpu.reg_write(UC_X86_REG_AX, rollover)
                    flags = cpu.reg_read(UC_X86_REG_EFLAGS)
                    cpu.reg_write(UC_X86_REG_EFLAGS, (flags & ~1) | carry)
                cpu = self.machine(bios)
                self.call(cpu, 0xea5b)
                self.assertEqual(cpu.reg_read(UC_X86_REG_DX), high)
                self.assertEqual(cpu.reg_read(UC_X86_REG_AX), low)
                self.assertEqual(cpu.reg_read(UC_X86_REG_EFLAGS) & 1, carry)
                self.assertEqual(calls, [0x1a])


if __name__ == '__main__':
    unittest.main()
