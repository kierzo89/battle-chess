"""Focused staged closed-buffer gates; no canonical code/tests are modified."""
import copy
from dataclasses import replace
import importlib.util
import json
from pathlib import Path
import struct
import sys
import unittest
from unittest.mock import patch

PROJECT=next(p for p in Path(__file__).resolve().parents if (p/'config/msc500.json').is_file())
sys.path.insert(0,str(PROJECT))
sys.path.insert(0,str(Path(__file__).resolve().parent))
import buffer_data16 as backend
from cdata import extract_data as ordinary_extract
from omf import read_omf, OMFError
from msc import CompileResult
from reference import build_reference,validate_expanded_read

FIXTURE=PROJECT/'build/huff-data-state/input512.obj'
SOURCE=PROJECT/'src/probes/huff-data-state/input512.c'


def rec(kind,payload):
    b=bytes([kind])+struct.pack('<H',len(payload)+1)+payload
    return b+bytes([-sum(b)&255])


def mutation(index,payload=None,kind=None):
    rows=list(read_omf(FIXTURE.read_bytes()).records)
    oldkind,_,oldpayload=rows[index]
    rows[index]=(oldkind if kind is None else kind,0,oldpayload if payload is None else payload)
    return b''.join(rec(k,p)for k,_,p in rows)


class BufferDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=FIXTURE.read_bytes()
        cls.rows=read_omf(cls.raw).records
        cls.proof=json.loads((PROJECT/'evidence/huff-data-state-proposal.json').read_text())
        cls.row=cls.proof['contributions'][1]
        m=cls.row['compiler']
        cls.compiled=CompileResult(object_bytes=cls.raw,**{**m,'command':tuple(m['command']),'flags':tuple(m['flags'])})
        cls.reference=build_reference((PROJECT.parent/'CHESS.EXE').read_bytes())
        cls.unit=json.loads((PROJECT/'build/huff-data-state/initialized-lidata-proposal.json').read_text())['candidate']
        cls.unit['backend']=backend.BACKEND
        cls.evidence=json.loads((PROJECT/'evidence/rea-huff-data-input512.json').read_text())

    def reject(self,data):
        with self.assertRaises((OMFError,ValueError)):
            backend.extract_data(data)

    def test_whole_initialized_contribution_and_preserved_raw_records(self):
        before=bytes(self.raw);data,m=backend.extract_data(self.raw)
        self.assertEqual(self.raw,before)
        self.assertEqual(data,bytes(512));self.assertEqual(m['segment']['length'],512)
        self.assertEqual(m['cv']['array_bit_size'],4096)
        self.assertEqual(m['cv']['records'][-1]['type_index'],515)
        self.assertEqual(m['public']['type_index'],515)
        self.assertEqual(m['data_writes'][1]['raw_payload'],'020100ff0100000100')
        self.assertTrue(m['all_segments'][1]['unsupported_data_retained'])
        self.assertEqual(m['emitted_mz_sites'],[])
        self.assertFalse(m['historical_array_capacity_proven'])
        self.assertEqual(backend.extract_data(self.raw)[0],data)

    def test_ordinary_backend_still_rejects_unmodified_lidata(self):
        with self.assertRaisesRegex(OMFError,'LIDATA'):
            ordinary_extract(read_omf(self.raw),backend.SYMBOL)
        with self.assertRaises(OMFError):backend.extract_data(read_omf(self.raw))

    def test_checksums_lengths_and_modend_eof(self):
        bad=bytearray(self.raw);bad[270]^=1
        for raw in (bytes(bad),self.raw[:-1],self.raw+b'\0',self.raw[:260]+b'\xa2\xff\xff'+self.raw[263:]):
            with self.subTest(length=len(raw)):self.reject(raw)

    def test_repeat_count_zero_short_long(self):
        for n in (0,1,510,512,65535):
            p=bytearray(self.rows[16][2]);p[3:5]=struct.pack('<H',n)
            with self.subTest(n=n):self.reject(mutation(16,bytes(p)))

    def test_nested_leaf_and_wrong_literal_length(self):
        for field,value in ((5,1),(6,1),(7,0),(7,2),(8,1)):
            p=bytearray(self.rows[16][2]);p[field]=value
            with self.subTest(field=field,value=value):self.reject(mutation(16,bytes(p)))

    def test_truncated_and_trailing_lidata(self):
        p=self.rows[16][2]
        for q in (p[:-1],p+b'\0',p[:3]):self.reject(mutation(16,q))

    def test_foreign_overlap_and_hole_lidata(self):
        for p in (b'\x03'+self.rows[16][2][1:],b'\x02\0\0'+self.rows[16][2][3:],b'\x02\x02\0'+self.rows[16][2][3:]):
            self.reject(mutation(16,p))

    def test_first_explicit_ledata_not_synthetic_fill(self):
        for p in (b'\x02\x01\0\0',b'\x02\0\0',b'\x02\0\0\0\0',b'\x02\0\0\x01'):
            self.reject(mutation(15,p))

    def test_other_loaded_allocations_and_attributes(self):
        for index in (4,6,7,8):
            p=bytearray(self.rows[index][2]);p[1:3]=b'\x02\0'
            self.reject(mutation(index,bytes(p)))
        for value in (0x28,0x49,0x08):
            p=bytes([value])+self.rows[5][2][1:];self.reject(mutation(5,p))

    def test_group_names_and_segment_overlay_indices(self):
        p=bytearray(self.rows[3][2]);p[2]^=1;self.reject(mutation(3,bytes(p)))
        p=bytearray(self.rows[5][2]);p[-1]=2;self.reject(mutation(5,bytes(p)))

    def test_tool_change_rejected_before_generation(self):
        with patch.object(backend,'validate_toolchain',return_value=('0'*64,backend.TOOL_HASHES)), \
             patch.object(backend,'compile_c',side_effect=AssertionError('must reject before compile')):
            with self.assertRaisesRegex(ValueError,'tool pins'):backend.build(SOURCE)

    def test_segdef_capacity_not_unit_size(self):
        for size in (511,513,0):
            p=bytearray(self.rows[5][2]);p[1:3]=struct.pack('<H',size)
            self.reject(mutation(5,bytes(p)))
        for size in (511,513):
            unit=copy.deepcopy(self.unit);unit['size']=size
            with self.assertRaisesRegex(ValueError,'extent'):backend.validate_unit(unit)

    def test_array_cv_wrong_capacity_element_and_public_type(self):
        # Array bit-count and element-type mutations are independently checked.
        for at in (17,18,20):
            p=bytearray(self.rows[17][2]);p[3+at]^=1
            self.reject(mutation(17,bytes(p)))
        p=bytearray(self.rows[13][2]);p[-1]^=1;self.reject(mutation(13,bytes(p)))

    def test_public_offset_symbol_and_group(self):
        p=bytearray(self.rows[13][2]);p[-4]=1;self.reject(mutation(13,bytes(p)))
        p=bytearray(self.rows[13][2]);p[3]^=1;self.reject(mutation(13,bytes(p)))
        p=bytearray(self.rows[13][2]);p[0]=0;self.reject(mutation(13,bytes(p)))
        self.reject(mutation(10,b'\x02\xff\x02'))
        with self.assertRaises(ValueError):backend.extract_data(self.raw,'_other')

    def test_extra_record_allocation_common_fixup_group(self):
        for kind,p in ((0x9a,b'\x02\xff\x02'),(0xb0,b'\x04_junk\0\x62\x04'),
                       (0x98,b'\x48\x02\0\x05\x06\x01'),(0xa0,b'\x02\0\0\0')):
            self.reject(self.raw[:-5]+rec(kind,p)+self.raw[-5:])
        # A thread-only record is legitimate; an actual relocation is not.
        self.reject(mutation(11,bytes.fromhex('c4005601')))

    def test_startup_marker_directives_and_entry_point(self):
        for i,p in ((12,b'\x04_junk\x01'),(1,b'\0\x9e'),(18,b'\x80'),(11,b'')):
            self.reject(mutation(i,p))

    def test_reviewed_source_flags_tool_manifest_command_pins(self):
        self.assertEqual(backend.validate_compiled(self.compiled,SOURCE.read_bytes())[0],bytes(512))
        for changed in (replace(self.compiled,compiler='msc510'),
                        replace(self.compiled,flags=('/AS','/Zi')),
                        replace(self.compiled,source_sha256='0'*64),
                        replace(self.compiled,toolchain_manifest_sha256='0'*64),
                        replace(self.compiled,tool_hashes={}),
                        replace(self.compiled,command=()),replace(self.compiled,source_name='OTHER.C')):
            with self.assertRaises(ValueError):backend.validate_compiled(changed,SOURCE.read_bytes())
        with self.assertRaises(ValueError):backend.validate_compiled(self.compiled,SOURCE.read_bytes()+b' ')
        with patch.object(backend,'compile_c',side_effect=AssertionError('must reject before compile')):
            import tempfile
            with tempfile.TemporaryDirectory()as d:
                p=Path(d)/'wrong.c';p.write_bytes(SOURCE.read_bytes()+b' ')
                with self.assertRaises(ValueError):backend.build(p)

    def test_closed_unit_rejects_external_ownership_and_wrong_profile(self):
        backend.validate_unit(self.unit)
        for key,value in [('backend','msc500-data-omf'),('language','c'),('symbol','_other'),
                          ('flags',['/AS']),('externals',{'_x':1}),('reference_region','unchanged-prefix'),
                          ('owned_data',{}),('owned_const',{}),('owned_bss',{}),('extended_extent',{}),('code_address',{}),('data_address',{})]:
            u=copy.deepcopy(self.unit);u[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):backend.validate_unit(u)

    def test_primary_complete_all_bytes_and_all_four_bases(self):
        data,_=backend.extract_data(self.raw)
        validate_expanded_read(self.evidence,self.unit,data,self.reference,emitted_mz_sites=[])
        start=int(self.unit['image_offset'],0)
        self.assertEqual(data,self.reference['image'][start:start+len(data)])
        self.assertFalse(any(p<start+512 and p+2>start for p in self.reference['relocations']))
        for base in (0,1,0x1000,0xffff):self.assertEqual(data,self.reference['image'][start:start+512])
        for i in range(512):
            bad=bytearray(data);bad[i]^=1
            with self.assertRaises(ValueError):validate_expanded_read(self.evidence,self.unit,bytes(bad),self.reference,emitted_mz_sites=[])

    def test_wrong_raw_profile_and_extra_mz_rejected(self):
        data,_=backend.extract_data(self.raw)
        e=copy.deepcopy(self.evidence);e['analysis_profile']['parameters']['load_segment']='0x1001'
        with self.assertRaises(ValueError):validate_expanded_read(e,self.unit,data,self.reference,emitted_mz_sites=[])
        with self.assertRaises(ValueError):validate_expanded_read(self.evidence,self.unit,data,self.reference,emitted_mz_sites=[int(self.unit['image_offset'],0)])

    def test_uninitialized_actual_source_object_not_credited(self):
        self.reject((PROJECT/'build/huff-data-state/input512_uninitialized.obj').read_bytes())

    def test_fresh_real_source_only_generation(self):
        built=backend.build(SOURCE)
        self.assertEqual(built.data,bytes(512))
        self.assertEqual(built.object_bytes,self.raw)
        self.assertEqual(built.provenance['source_sha256'],backend.SOURCE_SHA256)
        self.assertEqual(built.metadata['object_sha256'],backend.sha(built.object_bytes))


if __name__=='__main__':unittest.main()
