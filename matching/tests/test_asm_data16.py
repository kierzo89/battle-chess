"""Separate ASM DATA credit, complete storage and pinned tool/source boundaries."""
from copy import deepcopy
from dataclasses import replace
import hashlib
import importlib.util
import io
from contextlib import redirect_stdout
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
import asm_data16 as backend
from omf import read_omf
from reference import build_reference, ORIGINAL_SHA256
spec = importlib.util.spec_from_file_location('asm_data_check', PROJECT / 'check.py')
check = importlib.util.module_from_spec(spec); spec.loader.exec_module(check)
SOURCE = PROJECT / 'src/probes/asset-index-group/archive_index_tables_nasm.asm'
sha = lambda b: hashlib.sha256(b).hexdigest()


def unit_for(source=SOURCE):
    return {'id': 'archive_index_tables_data', 'language': 'asm-data',
        'backend': 'nasm-data-omf', 'source': str(source.relative_to(PROJECT)),
        'source_sha256': sha(source.read_bytes()),
        'assembler_sha256': sha(Path(shutil.which('nasm')).resolve().read_bytes()),
        'symbols': backend.parse_source(source.read_bytes())['symbols'],
        'image_offset': '0x5f74e', 'size': 896, 'reference_region': 'exepack-expanded',
        'rea_evidence': 'evidence/rea_archive_index_tables_896_expanded.json',
        'boundary_evidence': 'Complete independent numeric DD WORD PUBLIC DATA.'}


@unittest.skipUnless(shutil.which('nasm'), 'NASM required')
class ASMDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit = unit_for(); cls.built = backend.assemble(SOURCE, cls.unit)
        cls.obj = read_omf(cls.built.object_bytes)
        cls.reference = build_reference((PROJECT.parent / 'CHESS.EXE').read_bytes())

    def test_fresh_complete896_allocation_eight_publics_and_numeric_model(self):
        original = deepcopy(self.obj)
        data, meta = backend.extract_data(self.obj, self.unit['symbols'])
        self.assertEqual(len(data), 896)
        self.assertEqual([p['offset'] for p in meta['publics']], [0,32,156,208,448,480,604,656])
        self.assertEqual([p['group'] for p in meta['publics']], [1]*8)
        self.assertEqual(meta['segment']['attributes'], 0x48)
        self.assertEqual(meta['boundary'], 'complete_asm_data_SEGDEF')
        self.assertEqual(meta['authored_c_credit'], 0); self.assertEqual(meta['function_credit'], 0)
        self.assertEqual(meta['emitted_mz_sites'], [])
        self.assertEqual(self.obj, original)
        self.assertTrue(self.built.provenance['fresh_directory'])
        self.assertEqual(self.built.provenance['numeric_DD_values'], 224)
        again = backend.assemble(SOURCE, self.unit)
        self.assertEqual(again.data, data)

    def test_source_forbids_binary_inclusion_code_reservations_and_preprocessing(self):
        prefix = b'bits 16\nsegment _DATA public align=2 class=DATA use16\ngroup DGROUP _DATA\nglobal _a\n_a:\n'
        for tail in [b'incbin "target.bin"', b'%include "x"', b'times 2 dd 0', b'resd 1',
                     b'db 1,2,3,4', b'mov ax,1', b'dd _external', b'dd $', b'dd 1+2',
                     b'dd 4294967296', b'dd -2147483649', b'%define X 1', b'align 16']:
            with self.subTest(tail=tail), self.assertRaises(backend.ASMDataError):
                backend.parse_source(prefix + tail + b'\n')
        for source in [prefix+b'_b:\ndd 1\n', prefix+b'global _a\ndd 1\n', prefix,
                       prefix.replace(b'align=2', b'align=16')+b'dd 1\n',
                       prefix.replace(b'global _a\n', b'')+b'dd 1\n',
                       prefix+b'dd 1\nlocal:\ndd 2\n']:
            with self.subTest(source=source), self.assertRaises(backend.ASMDataError):
                backend.parse_source(source)
        self.assertEqual(backend.parse_source(prefix+b'dd -1,0xffffffff,0\n')['numeric_values'], [0xffffffff,0xffffffff,0])

    def test_source_and_assembler_pins_and_whole_unit_schema_are_mandatory(self):
        for change in [{'source_sha256': '0'*64}, {'assembler_sha256': '0'*64},
                       {'symbols': self.unit['symbols'][1:]}, {'symbols': ['_one']}]:
            with self.subTest(change=change), self.assertRaises(backend.ASMDataError):
                backend.assemble(SOURCE, self.unit | change)
        for change in [{'language':'c-data'}, {'backend':'nasm-bin'}, {'reference_region':'unchanged-prefix'},
                       {'source_sha256':None}, {'symbols':[{}]}, {'symbols':[]}, {'symbols':['_a','_a']},
                       {'symbol':'_setup_lengths_data'}, {'flags':[]}, {'externals':{}},
                       {'extended_extent':{}}, {'owned_data':{}}, {'data_address':{'segment':1,'offset':0}}]:
            with self.subTest(change=change), self.assertRaises(ValueError):
                check.validate_units([self.unit | change], 82903, 401131)

    def test_no_partial_public_slice_missing_global_or_group0_frame(self):
        for symbols in [self.unit['symbols'][1:], self.unit['symbols'][:1], list(reversed(self.unit['symbols']))]:
            with self.assertRaises(backend.ASMDataError): backend.extract_data(self.obj, symbols)
        for change in ['group','offset','class','alignment','entry','extra_group','bad_member']:
            obj=deepcopy(self.obj);seg=next(iter(obj.segments.values()))
            if change=='group':
                p=obj.publics[self.unit['symbols'][0]];obj.publics[p.name]=replace(p,group=0)
            elif change=='offset':
                p=obj.publics[self.unit['symbols'][0]];obj.publics[p.name]=replace(p,offset=4)
            elif change=='class':seg.class_name='FAR_DATA'
            elif change=='alignment':seg.attributes=0x68
            elif change=='entry':obj.records=[(k,a,b'\x40' if k==0x8a else v) for k,a,v in obj.records]
            elif change=='extra_group':obj.records.append(next(x for x in obj.records if x[0]==0x9a))
            else:obj.records=[(k,a,v+b'\xff\x01' if k==0x9a else v)for k,a,v in obj.records]
            with self.subTest(change=change), self.assertRaises(backend.ASMDataError):
                backend.extract_data(obj,self.unit['symbols'])

    def test_other_allocations_fixups_externals_comm_lidata_holes_and_tails_fail(self):
        for change in ['other_segment','fixup','external','COMM','LIDATA','hole','overlap','tail','alias','linker_comment']:
            obj=deepcopy(self.obj);seg=next(iter(obj.segments.values()))
            if change=='other_segment':obj.segments[2]=deepcopy(seg);obj.segments[2].index=2
            elif change=='fixup':obj.fixups.append(object())
            elif change=='external':obj.externals[1]='_other'
            elif change=='COMM':obj.records.append((0xb0,0,b''))
            elif change=='alias':obj.records.append((0xc6,0,b''))
            elif change=='linker_comment':obj.records.append((0x88,0,b'\x00\xa0\x01'))
            elif change=='LIDATA':seg.unsupported_data=True
            elif change=='hole':seg.chunks=[(1,seg.chunks[0][1])]
            elif change=='overlap':seg.chunks.append(seg.chunks[0])
            elif change=='tail':seg.length+=4
            with self.subTest(change=change), self.assertRaises(backend.ASMDataError):
                backend.extract_data(obj,self.unit['symbols'])
        with self.assertRaises(backend.ASMDataError): backend.extract_data(self.built.object_bytes,self.unit['symbols'])

    def test_independent_source_model_rejects_even_wellformed_extra_storage(self):
        obj=deepcopy(self.obj);seg=next(iter(obj.segments.values()));end=seg.length
        seg.chunks.append((end,b'\0'*4));seg.length+=4
        # Complete OMF alone cannot label a legal trailing element padding;
        # independent numeric source model authenticates every emitted byte.
        self.assertEqual(len(backend.extract_data(obj,self.unit['symbols'])[0]),900)
        with patch.object(backend,'read_omf',return_value=obj), self.assertRaisesRegex(backend.ASMDataError,'numeric source model'):
            backend.assemble(SOURCE,self.unit)

    def test_checker_whole_primary_reference_and_separate_status(self):
        self.assertTrue(check.validate_rea_extent(self.unit,PROJECT,ORIGINAL_SHA256,self.reference).startswith('ev_'))
        result=check.build_unit(self.unit,self.reference['image'],PROJECT,'nasm',reference=self.reference)
        self.assertEqual(result['status'],'asm_data_matched');self.assertEqual(result['actual_size'],896)
        self.assertEqual(result['authored_c_function_credit'],0);self.assertEqual(result['authored_c_data_credit'],0)
        self.assertEqual(result['relocations'],[])
        check.validate_emitted_mz_sites(result,self.reference['relocations'])
        with self.assertRaises(ValueError):check.validate_emitted_mz_sites(result,[0x5f750])
        with self.assertRaises(ValueError):check.validate_rea_extent(self.unit|{'size':895},PROJECT,ORIGINAL_SHA256,self.reference)
        bad=check.build_unit(self.unit|{'size':895},self.reference['image'],PROJECT,'nasm',reference=self.reference)
        self.assertEqual(bad['status'],'build_error')
        wrongref=self.reference|{'image':bytes(401131)}
        self.assertEqual(check.build_unit(self.unit,wrongref['image'],PROJECT,'nasm',reference=wrongref)['status'],'build_error')

    def test_report_separate_counts_coverage_failure_and_incomplete_goal(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'matching';(p/'config').mkdir(parents=True);(p/'evidence').mkdir()
            shutil.copyfile(PROJECT/'config/target.json',p/'config/target.json')
            for name in ['rea_procedures.json','rea_archive_index_tables_896_expanded.json']:
                shutil.copyfile(PROJECT/'evidence'/name,p/'evidence'/name)
            source=p/self.unit['source'];source.parent.mkdir(parents=True);shutil.copyfile(SOURCE,source)
            (p/'config/units.json').write_text(json.dumps([self.unit]));output=Path(temp)/'output'
            report=check.run(PROJECT.parent,p,PROJECT.parent/'CHESS.EXE',output,'nasm');s=report['summary']
            self.assertEqual((s['asm_data_matched_units'],s['asm_data_matched_bytes']),(1,896))
            self.assertEqual((s['c_matched_functions'],s['source_data_bytes'],s['asm_matched_functions']),(0,0,0))
            self.assertEqual(s['verified_file_span_bytes'],0);self.assertEqual(s['verified_image_span_bytes'],896)
            self.assertEqual(s['failed_units'],0);self.assertFalse(s['full_executable_match'])
            coverage=json.loads((output/'image_coverage.json').read_text())['ranges']
            self.assertEqual([r['status']for r in coverage],['unreconstructed','asm_data_matched','unreconstructed'])
            self.assertTrue((output/'asm-data/archive_index_tables_data.obj').exists())
            # Separate initialized ASM success never satisfies the full-byte goal.
            with patch.object(check,'run',return_value=report), patch.object(sys,'argv',['check.py','--require-complete','--output',str(output)]), redirect_stdout(io.StringIO()):
                self.assertEqual(check.main(),1)
            with patch.object(check,'run',return_value=report), patch.object(sys,'argv',['check.py','--output',str(output)]), redirect_stdout(io.StringIO()):
                self.assertEqual(check.main(),0)
            source.write_text(source.read_text().replace(' DD 192,10097',' DD 193,10097'))
            failed=check.run(PROJECT.parent,p,PROJECT.parent/'CHESS.EXE',output,'nasm')
            self.assertEqual(failed['summary']['failed_units'],1)
            self.assertEqual(failed['summary']['verified_image_span_bytes'],0)
            self.assertEqual(failed['units'][0]['status'],'build_error')


if __name__=='__main__':unittest.main()
