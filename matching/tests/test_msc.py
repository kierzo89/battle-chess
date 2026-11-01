"""Validation and optional execution of the actual pinned historic compiler."""
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import struct
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('matching_msc', Path(__file__).resolve().parents[1] / 'msc.py')
msc = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = msc
spec.loader.exec_module(msc)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import setup_toolchain


def synthetic_archive(loop=False):
    """Four-sector FAT12 disk with one file and a compressed repeated tail."""
    disk = bytearray(2048)
    struct.pack_into('<H', disk, 11, 512)
    disk[13] = 1
    struct.pack_into('<H', disk, 14, 1)
    disk[16] = 1
    struct.pack_into('<H', disk, 17, 16)
    struct.pack_into('<H', disk, 22, 1)
    disk[512:515] = b'\xfd\xff\xff'
    disk[515:517] = b'\x02\0' if loop else b'\xff\x0f'
    disk[1024:1035] = b'UNIT    C  '
    disk[1035] = 0x20
    struct.pack_into('<H', disk, 1024 + 26, 2)
    struct.pack_into('<I', disk, 1024 + 28, 512)
    disk[1536:] = b'abcd' * 128
    sectors = []
    for i in range(4):
        words = list(struct.unpack('<128I', disk[i * 512:(i + 1) * 512]))
        while len(words) > 1 and words[-1] == words[-2]:
            words.pop()
        sectors.append({'c': 0, 'h': 0, 's': i + 1, 'l': 512, 'd': words})
    return json.dumps({'imageInfo': {'cylinders': 1, 'heads': 1, 'trackDefault': 4,
                                     'sectorDefault': 512}, 'diskData': [[sectors]]}).encode()


class CompilerTests(unittest.TestCase):
    def test_unknown_compiler_rejected(self):
        with self.assertRaises(ValueError):
            msc.compiler_config('../../other')

    def test_archived_profile_has_separate_provenance(self):
        config = msc.compiler_config('msc500')
        self.assertNotIn('license', config)
        self.assertIn('proprietary', config['provenance']['classification'])
        self.assertEqual(len(config['files']), 7)
        self.assertEqual(msc.default_toolchain('msc500').name, 'msc500')

    def test_archived_400_profile_has_separate_provenance(self):
        config = msc.compiler_config('msc400')
        self.assertNotIn('license', config)
        self.assertIn('proprietary', config['provenance']['classification'])
        self.assertEqual([f['name'] for f in config['files']],
                         ['MSC.EXE', 'C1.EXE', 'C2.EXE', 'C3.EXE'])

    @unittest.skipUnless(msc.default_toolchain('msc400').exists() and shutil.which('dosbox'),
                         'archived C4 compiler and DOSBox required')
    def test_archived_400_legacy_driver_and_codeview_extent(self):
        from omf import read_omf
        from link16 import link_function
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'source.c'
            source.write_text('unsigned lowbit(value) unsigned value; {return value & 1;}\n')
            result = msc.compile_c(source, ['/AS', '/Zi'], compiler='msc400')
            self.assertEqual(result.compiler, 'msc400')
            self.assertEqual(len(result.tool_hashes), 4)
            self.assertIn('C:\\UNIT.C,C:\\UNIT.OBJ;', result.command)
            obj = read_omf(result.object_bytes)
            self.assertEqual(obj.function_info('_lowbit')['boundary'], 'codeview3_procedure')
            code, _ = link_function(obj, '_lowbit', 0xa514, {'__chkstk': 0xecaa})
            self.assertEqual(code.hex(), '558bec33c0e88e478b4604250100eb008be55dc3')
            destination = Path(tmp) / '400'
            shutil.copytree(msc.default_toolchain('msc400'), destination)
            (destination / 'C3.EXE').write_bytes(b'corrupt')
            with self.assertRaisesRegex(ValueError, 'C3.EXE'):
                msc.validate_toolchain(destination, compiler='msc400')

    def test_archive_fat12_and_repeated_dword_tail(self):
        files = setup_toolchain.archive_files(synthetic_archive(), ['UNIT.C'])
        self.assertEqual(files, {'UNIT.C': b'abcd' * 128})
        with self.assertRaisesRegex(ValueError, 'looping'):
            setup_toolchain.archive_files(synthetic_archive(loop=True), ['UNIT.C'])
        with self.assertRaisesRegex(ValueError, 'Missing requested'):
            setup_toolchain.archive_files(synthetic_archive(), ['OTHER.C'])

    def test_source_rejects_assembly_and_preprocessing(self):
        for source in (b'void f(){_asm { nop }}', b'void f(){__asm nop;}',
                       b'#pragma aux f = 0x90', b'#include "x.h"',
                       b'void f(){_a\\\nsm nop;}', b'void f(){}\x1a', b'void f(){_emit(1);}',
                       b'void f(){char *x="//"; _asm nop;}'):
            with self.subTest(source=source), self.assertRaises(ValueError):
                msc.validate_source(source)

    def test_source_allows_plain_c_and_comments(self):
        msc.validate_source(b'/* _asm */ int f(int x) { return x + 3; }')

    def test_flags_rejected_before_compiler_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'unit.c'
            source.write_text('int f(void){return 3;}')
            for flag in ('/Fa', '/FoOTHER.OBJ', '/O & del *.*', '/D_asm=', '/I.'):
                with self.subTest(flag=flag), self.assertRaises(ValueError):
                    msc.compile_c(source, [flag], toolchain=Path(tmp) / 'absent')

    def test_dos_source_names_cannot_change_paths_or_batch_commands(self):
        for name in ('../EVAL.C', 'C:\\EVAL.C', 'EVAL.C & DIR', 'EVAL.C\nDIR',
                     'TOOLONGNAME.C', 'EVAL.OBJ', 'eval.c', 'CON.C', 'NUL.C',
                     'COM1.C', 'LPT9.C', '', None, 3):
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'DOS source name'):
                msc.compile_c(Path('missing.c'), ['/AM'], compiler='msc500', source_name=name)

    @unittest.skipUnless(msc.default_toolchain('msc500').exists() and shutil.which('dosbox'),
                         'archived compiler and DOSBox required')
    def test_named_medium_segment_preserves_explicit_far_procedure(self):
        from omf import read_omf
        from link16 import link_function
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'source.c'
            source.write_text('unsigned far lowbit(unsigned value) { return value & 1; }\n')
            code = []
            for model, segment in (('/AS', '_TEXT'), ('/AM', 'EVALA_TEXT')):
                result = msc.compile_c(source, [model, '/Gs', '/Zi'], compiler='msc500',
                                       source_name='EVALA.C')
                self.assertEqual(result.source_name, 'EVALA.C')
                self.assertEqual(result.command[-1], 'C:\\EVALA.C')
                obj = read_omf(result.object_bytes)
                public = obj.publics['_lowbit']
                self.assertEqual(obj.segments[public.segment].name, segment)
                info = obj.function_info('_lowbit')
                self.assertEqual(info['boundary'], 'codeview3_procedure')
                linked, relocations = link_function(obj, '_lowbit', 0x5a, {}, image_origin=0xfe4a)
                self.assertFalse(relocations)
                self.assertEqual(info['size'], len(linked))
                code.append(linked)
            self.assertEqual(code[0], code[1])
            self.assertEqual(code[0].hex(), '558bec8b4606250100eb008be55dcb')

    @unittest.skipUnless(msc.DEFAULT_TOOLCHAIN.exists(), 'pinned compiler not installed')
    def test_corrupt_tool_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / 'toolchain'
            shutil.copytree(msc.DEFAULT_TOOLCHAIN, destination)
            (destination / 'C2.EXE').write_bytes(b'corrupt')
            with self.assertRaisesRegex(ValueError, 'C2.EXE'):
                msc.validate_toolchain(destination)

    @unittest.skipUnless(msc.DEFAULT_TOOLCHAIN.exists() and shutil.which('dosbox'),
                         'pinned compiler and DOSBox required')
    def test_actual_c_object_and_failed_compile(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'source.c'
            source.write_text('int add(int a, int b) { return a+b; }\n')
            result = msc.compile_c(source, ['/AS', '/Gs', '/O'])
            self.assertEqual(result.object_bytes[0], 0x80)
            self.assertEqual(len(result.tool_hashes), 10)
            self.assertIn('UNIT.C', result.compiler_log)
            source.write_text('int f( { invalid syntax }')
            with self.assertRaisesRegex(RuntimeError, 'compilation failed'):
                msc.compile_c(source, ['/AS'])

    @unittest.skipUnless(msc.default_toolchain('msc500').exists() and shutil.which('dosbox'),
                         'archived compiler and DOSBox required')
    def test_archived_500_compiler_runs_and_is_independently_pinned(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'source.c'
            source.write_text('int add(int a, int b) { return a+b; }\n')
            result = msc.compile_c(source, ['/AS', '/Gs', '/Os', '/Zi'], compiler='msc500')
            self.assertEqual(result.compiler, 'msc500')
            self.assertEqual(result.object_bytes[0], 0x80)
            self.assertEqual(len(result.tool_hashes), 7)
            destination = Path(tmp) / '500'
            shutil.copytree(msc.default_toolchain('msc500'), destination)
            manifest = json.loads((destination / 'manifest.json').read_text())
            manifest['files'][0]['sha256'] = '0' * 64
            (destination / 'manifest.json').write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, 'manifest differs'):
                msc.validate_toolchain(destination, compiler='msc500')


if __name__ == '__main__':
    unittest.main()
