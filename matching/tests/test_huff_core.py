"""Execute freshly assembled decoder code on independent synthetic Huffman data.

The refill hook models a 512-byte source, not DOS I/O or the original refill.
No original executable bytes enter the emulated code or input stream.
"""
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import unittest

try:
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE
    from unicorn.x86_const import (UC_X86_REG_AX, UC_X86_REG_BP, UC_X86_REG_CS,
        UC_X86_REG_DS, UC_X86_REG_ES, UC_X86_REG_SS, UC_X86_REG_SP,
        UC_X86_REG_IP, UC_X86_REG_SI, UC_X86_REG_DX)
except ImportError:
    Uc = None

M = Path(__file__).resolve().parents[1]
CORE = [('huff_frame_decode_entry',0xe03a),('huff_tree_build_recursive',0xe077),
        ('huff_read_byte',0xe0a8),('huff_get_bit',0xe0b6),
        ('huff_build_lookup',0xe0d8),('huff_decode_bytes',0xe197),
        ('huff_decode_stream',0xe282),('huff_window_save',0xe394),
        ('huff_window_init',0xe3ba)]

def encode(tree, payload):
    codes = {}
    def visit(node, prefix):
        if isinstance(node,int):
            codes[node]=prefix
            return '1'+format(node,'08b')
        return '0'+visit(node[0],prefix+'0')+'0'+visit(node[1],prefix+'1')
    bits=visit(tree,'')+''.join(codes[b] for b in payload)
    bits += '0' * (-len(bits)%8)
    return struct.pack('<IHH',len(payload),0,0)+bytes(int(bits[i:i+8],2) for i in range(0,len(bits),8))

@unittest.skipUnless(Uc and shutil.which('nasm'),'Unicorn and NASM required')
class HuffmanCoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.code=[]
        with tempfile.TemporaryDirectory() as tmp:
            for stem,offset in CORE:
                p=Path(tmp)/(stem+'.bin')
                subprocess.run(['nasm','-f','bin','-o',str(p),str(M/'asm'/(stem+'.asm'))],check=True)
                cls.code.append((offset,p.read_bytes()))

    def machine(self, tree, payload):
        data=encode(tree,payload); cursor=0; refills=[]
        u=Uc(UC_ARCH_X86,UC_MODE_16);u.mem_map(0,0x100000)
        for at,code in self.code:u.mem_write(at,code)
        # High-bit masks for one through eight extra Huffman code bits.
        u.mem_write(0x244cc,bytes([0]+[256-(1<<(8-i)) for i in range(1,9)]))
        for reg,value in [(UC_X86_REG_CS,0),(UC_X86_REG_DS,0x2000),
                          (UC_X86_REG_ES,0x6000),(UC_X86_REG_SS,0x4000)]:u.reg_write(reg,value)
        def refill(cpu,address,size,user):
            nonlocal cursor
            if address==0xe410:raise AssertionError('Unsupported high count/tree depth trapped')
            if address!=0xe3ea:return
            block=data[cursor:cursor+512];refills.append(cursor);cursor+=512
            cpu.mem_write(0x22ec2,block.ljust(512,b'\0'))
            cpu.reg_write(UC_X86_REG_SI,0x2ec2)
            sp=cpu.reg_read(UC_X86_REG_SP)
            ret=struct.unpack('<H',cpu.mem_read(0x40000+sp,2))[0]
            cpu.reg_write(UC_X86_REG_SP,sp+2);cpu.reg_write(UC_X86_REG_IP,ret)
        u.hook_add(UC_HOOK_CODE,refill)
        def call(at,*args):
            u.mem_write(0x48000,struct.pack('<'+'H'*(len(args)+1),0x200,*args))
            u.reg_write(UC_X86_REG_SP,0x8000);u.reg_write(UC_X86_REG_BP,0x7654)
            u.emu_start(at,0x200,count=1000000)
            self.assertEqual(u.reg_read(UC_X86_REG_IP),0x200)
            self.assertEqual(u.reg_read(UC_X86_REG_SP),0x8002)
            self.assertEqual(u.reg_read(UC_X86_REG_BP),0x7654)
        call(0xe03a)
        return u,call,refills

    def test_fast_codes_and_incremental_decode(self):
        payload=bytes([0x41,0x42,0x42,0x41]*125)
        u,call,refills=self.machine((0x41,0x42),payload)
        call(0xe197,0x2000,0x6000,197,0)
        self.assertEqual(u.reg_read(UC_X86_REG_AX),197)
        call(0xe197,0x2000+197,0x6000,len(payload)-197,0)
        self.assertEqual(bytes(u.mem_read(0x62000,len(payload))),payload)
        self.assertEqual(u.mem_read(0x244df,1),bytes([sum(payload)&255]))

    def test_long_codes_and_multiple_input_refills(self):
        tree=16
        for symbol in reversed(range(16)):tree=(symbol,tree)
        payload=bytes(list(range(17))*53)
        u,call,refills=self.machine(tree,payload)
        call(0xe197,0x2000,0x6000,len(payload),0)
        self.assertEqual(bytes(u.mem_read(0x62000,len(payload))),payload)
        self.assertGreater(len(refills),1)
        self.assertEqual(u.mem_read(0x244df,1),bytes([sum(payload)&255]))

    def test_huge_output_crosses_64k_boundary(self):
        payload=bytes([7,9]*20)
        u,call,_=self.machine((7,9),payload)
        call(0xe197,0xfffe,0x6000,len(payload),0)
        self.assertEqual(bytes(u.mem_read(0x6fffe,len(payload))),payload)

    def test_requested_count_is_clamped_to_header_remaining(self):
        payload=bytes([3,5]*13)
        u,call,_=self.machine((3,5),payload)
        u.mem_write(0x62000,b'\xcc'*64)
        call(0xe197,0x2000,0x6000,60,0)
        self.assertEqual(u.reg_read(UC_X86_REG_AX),len(payload))
        self.assertEqual(bytes(u.mem_read(0x62000,64)),payload+b'\xcc'*(64-len(payload)))

    def test_rows_keep_odd_width_padding_and_return_pointer(self):
        for width in (3,4):
            with self.subTest(width=width):
                payload=bytes([11,22]*6)
                u,call,_=self.machine((11,22),payload)
                u.mem_write(0x62000,b'\xcc'*32)
                call(0xe282,0x2000,0x6000,len(payload),0,width)
                expected=bytearray()
                for i in range(0,len(payload),width):
                    expected.extend(payload[i:i+width])
                    if width&1:expected.append(0)
                if not width&1:expected.append(0)
                self.assertEqual(bytes(u.mem_read(0x62000,len(expected))),bytes(expected))
                end=0x2000+len(payload)+(len(payload)//width if width&1 else 0)
                self.assertEqual(u.reg_read(UC_X86_REG_AX),end)
                self.assertEqual(u.reg_read(UC_X86_REG_DX),0x6000)
