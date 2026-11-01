"""Real compiler/REA/reference/production checks for near-pointer DATA."""
import copy
import json
from pathlib import Path
import shutil
import sys
import unittest
M=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(M))
import check
from msc import compile_c
from reference import build_reference,validate_data_address,ORIGINAL_SHA256


class PointerDataAddressTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ref=build_reference((M.parent/'CHESS.EXE').read_bytes())
        proof=json.loads((M/'evidence/main-menu-pointer-data-experiment.json').read_text())
        cls.unit=dict(id='main_menus_114a',language='c-data',backend='msc500-pointer-data-omf',
            source='src/probes/main_menu_pointer_data.c',symbol='_main_menus_114a',
            flags=['/AS','/Zl','/Zi'],image_offset='0x5dd6a',size=20,
            data_address=dict(segment=0x5cc2,offset=0x114a),
            reference_region='exepack-expanded',externals=proof['externals'],
            rea_evidence='evidence/rea-main-menu-array20.json',
            boundary_evidence='Whole independent20-byte typed DATA segment and all8externalfields.')

    def test_actual_DGROUP_operands_and_explicit_address(self):
        self.assertEqual(validate_data_address(self.unit,self.ref),(0x5cc2,0x114a))
        check.validate_units([self.unit],self.ref['prefix_size'],len(self.ref['image']))
        check.validate_rea_extent(self.unit,M,ORIGINAL_SHA256,self.ref)

    def test_frame_alias_and_coordinate_mutations_rejected(self):
        for address in [None,{},dict(segment=0x5cc1,offset=0x115a),
                dict(segment=0x5cc2,offset=True),dict(segment=-1,offset=0),
                dict(segment=0x5cc2,offset=0x10000),
                dict(segment=0x5cc2,offset=0x114a,extra=0)]:
            u=copy.deepcopy(self.unit);u['data_address']=address
            with self.subTest(address=address),self.assertRaises(ValueError):
                validate_data_address(u,self.ref)
        for delta in [dict(image_offset='0x5dd6b'),dict(size=0),dict(size=True),
                dict(size=0x10000),dict(image_offset=True)]:
            u=self.unit|delta
            with self.subTest(delta=delta),self.assertRaises(ValueError):
                validate_data_address(u,self.ref)

    def test_original_CRT0_words_and_MZ_ownership_cannot_be_forged(self):
        for at in [0xea90,0xea91,0xea92,0xeb1b,0xeb1c,0xeb1d,0xeb1e,0xeb1f]:
            ref=dict(self.ref);b=bytearray(ref['image']);b[at]^=1;ref['image']=bytes(b)
            with self.subTest(at=at),self.assertRaises(ValueError):
                validate_data_address(self.unit,ref)
        for at in [0xea91,0xeb1c]:
            ref=self.ref|dict(relocations=tuple(x for x in self.ref['relocations']if x!=at))
            with self.subTest(site=at),self.assertRaises(ValueError):
                validate_data_address(self.unit,ref)

    def test_data_backend_gate_preserves_old_no_external_policy(self):
        for delta in [dict(backend='msc500-data-omf'),dict(language='c'),
                dict(reference_region='unchanged-prefix'),dict(externals={}),
                dict(externals={'_x':dict(segment=0x5cc2,offset=1)}),
                dict(extended_extent={'kind':'main_unreachable_epilogue_0010_v1'})]:
            with self.subTest(delta=delta),self.assertRaises(ValueError):
                check.validate_units([self.unit|delta],self.ref['prefix_size'],len(self.ref['image']))


@unittest.skipUnless(shutil.which('dosbox')and(M/'toolchains/msc500').exists(),'Pinned C500 required')
class PointerDataBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        PointerDataAddressTests.setUpClass.__func__(cls)
        c=compile_c(M/cls.unit['source'],cls.unit['flags'],compiler='msc500')
        cls.cache={('msc500',c.source_sha256,tuple(cls.unit['flags'])):c}

    def build(self,unit):
        return check.build_unit(unit,self.ref['image'],M,'nasm',c_cache=self.cache,reference=self.ref)

    def test_fresh_actual20byte_DATA_production_build(self):
        r=self.build(self.unit)
        self.assertEqual(r['status'],'c_data_matched',r.get('error'))
        self.assertEqual(r['actual_size'],20)
        self.assertEqual(len(r['relocations']),8)
        self.assertEqual(r['classification'],'authored_c_initialized_pointer_data')
        self.assertEqual(r['authored_c_function_credit'],0)
        check.validate_emitted_mz_sites(r,self.ref['relocations'])

    def test_fresh_build_rejects_missing_extra_or_wrong_external(self):
        for mutate in ['missing','extra','wrong','far']:
            u=copy.deepcopy(self.unit);name=next(iter(u['externals']))
            if mutate=='missing':del u['externals'][name]
            if mutate=='extra':u['externals']['_invented']=1
            if mutate=='wrong':u['externals'][name]^=1
            if mutate=='far':u['externals'][name]=dict(segment=0x5cc2,offset=1)
            with self.subTest(mutate=mutate):
                self.assertNotEqual(self.build(u)['status'],'c_data_matched')

    def test_declared_size_cannot_slice_independent_SEGDEF(self):
        for n in [18,19,21,22]:
            with self.subTest(size=n):
                self.assertNotEqual(self.build(self.unit|dict(size=n))['status'],'c_data_matched')
