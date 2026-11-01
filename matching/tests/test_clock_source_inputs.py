"""Focused clock profile gates and mixed dispatcher; no LINK/global checker."""
import copy
import dataclasses
import importlib.util
import json
from pathlib import Path
import shutil
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch

PROJECT=next(p for p in Path(__file__).resolve().parents if(p/'config/msc500.json').exists())
STAGE=Path(__file__).resolve().parent
sys.path[:0]=[str(STAGE),str(PROJECT)]
import clock_source_inputs as clock
from msc import compile_c
from omf import read_omf
spec=importlib.util.spec_from_file_location('staged_source_inputs_clock',(STAGE/'source_inputs.py'if(STAGE/'source_inputs.py').exists()else PROJECT/'source_inputs.py'))
dispatch=importlib.util.module_from_spec(spec);spec.loader.exec_module(dispatch)


def record(kind,payload):
    b=bytes([kind])+struct.pack('<H',len(payload)+1)+payload
    return b+bytes([-sum(b)&255])


def mutate(data,kind,change):
    rows=read_omf(data).records;changed=False;out=[]
    for k,_,p in rows:
        if k==kind and not changed:p=change(p);changed=True
        out.append(record(k,p))
    assert changed
    return b''.join(out)


class ClockSourceInputsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config=json.loads((PROJECT/'build/clock-common-profile/source-inputs.proposed.json').read_text())
        cls.item=cls.config['source_allocations'][1]
        cls.compiled=compile_c(PROJECT/'src/probes/clock-common-storage/scalars.c',clock.FLAGS,compiler='msc500')
        cls.selectors=compile_c(PROJECT/dispatch.SOURCE,dispatch.FLAGS,compiler='msc500')
        cls.obj=cls.compiled.object_bytes

    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='bc-clock-profile-tests-');self.addCleanup(self.tmp.cleanup)
        self.project=Path(self.tmp.name)/'matching';self.project.mkdir()
        for item in self.config['source_allocations']:
            source=PROJECT/('src/probes/clock-common-storage/scalars.c'if item['source']==clock.SOURCE else item['source'])
            p=self.project/item['source'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,p)
            for row in item['evidence'].values():
                dest=self.project/row['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(PROJECT/row['path'],dest)
        self.path=self.project/'registry.json';self.out=self.project/'objects'
        self.path.write_text(json.dumps(self.config))

    def compile_for_source(self,path,flags,compiler):
        return self.compiled if Path(path).name=='clock_state.c'else self.selectors

    def run_config(self,config=None,defined=()):
        self.path.write_text(json.dumps(self.config if config is None else config))
        with patch.object(dispatch,'compile_c',side_effect=self.compile_for_source):
            return dispatch.build_source_inputs(self.project,PROJECT.parent/'CHESS.EXE',self.out,self.path,defined_symbols=defined)

    def bad_obj(self,obj):
        with self.assertRaises(ValueError):clock.validate_object(obj)

    def test_fresh_real_compiler_whole_definition(self):
        self.assertEqual(clock.sha(self.obj),clock.OBJECT_SHA)
        rows=clock.validate_object(self.obj)
        self.assertEqual([r['symbol']for r in rows],clock.NAMES)
        self.assertTrue(all(r['size']==4 and r['type_index']==0x82 and r['datatype']==0x62 for r in rows))
        self.assertFalse(read_omf(self.obj).publics)

    def test_full_clock_build_fresh_real_compile_and_zero_credit(self):
        built=clock.build_input(self.item,self.project,PROJECT.parent/'CHESS.EXE',self.out)
        self.assertEqual(built['allocation_bytes'],12);self.assertEqual(built['initialized_bytes'],0)
        self.assertEqual(built['matching_credit'],0);self.assertFalse(built['placement_proven'])
        self.assertEqual((self.out/'clock-common.obj').read_bytes(),self.obj)
        self.assertTrue(all(not x['resolved']for x in built['original_map_constraints']))
        self.assertFalse({'units','summary','source_data_bytes','verified_image_span_bytes'}&set(built))

    def test_mixed_profiles_eleven_actual_definitions(self):
        result=self.run_config()
        self.assertEqual(len(result['objects']),2)
        self.assertEqual([r['allocation_bytes']for r in result['objects']],[32,12])
        self.assertEqual(sum(len(r['definitions'])for r in result['objects']),11)
        self.assertEqual(result['matching_credit'],0);self.assertFalse(result['placement_proven'])
        rows=dispatch.report_inputs(result);self.assertEqual(len(rows),2)
        self.assertEqual(rows[1]['definitions'],[{'symbol':n,'size':4}for n in clock.NAMES])

    def test_selector_profile_results_unchanged(self):
        config=copy.deepcopy(self.config);config['source_allocations']=config['source_allocations'][:1]
        result=self.run_config(config)
        self.assertEqual(result['objects'][0]['object_sha256'],dispatch.OBJECT_SHA)
        self.assertEqual(len(dispatch.validate_object(self.selectors.object_bytes)),8)
        self.assertEqual(result['objects'][0]['definitions'],dispatch.validate_object(self.selectors.object_bytes))

    def test_no_config_or_empty_still_no_inputs(self):
        result=dispatch.build_source_inputs(self.project,Path('missing'),self.out,self.project/'absent')
        self.assertEqual(result['objects'],[])
        self.assertEqual(self.run_config({'schema_version':1,'source_allocations':[]})['objects'],[])

    def test_duplicate_profile_and_already_matched_symbols(self):
        c=copy.deepcopy(self.config);c['source_allocations'].append(copy.deepcopy(self.item))
        with self.assertRaisesRegex(ValueError,'duplicate'):self.run_config(c)
        for name in clock.NAMES:
            with self.subTest(name=name),self.assertRaisesRegex(ValueError,'already matched'):
                self.run_config(defined=[name])

    def test_reordered_profiles_both_paths_work(self):
        c=copy.deepcopy(self.config);c['source_allocations'].reverse()
        self.assertEqual([x['allocation_bytes']for x in self.run_config(c)['objects']],[12,32])

    def test_closed_item_schema_and_no_credit_override(self):
        for key,value in [('id','other'),('backend','msc500-near-common-source-v1'),('source','../clock.c'),
            ('source_sha256','0'*64),('compiler','msc510'),('flags',['/AS','/Zi']),
            ('toolchain_manifest_sha256','0'*64),('matching_credit',12)]:
            row=copy.deepcopy(self.item);row[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):clock.validate_item(row)

    def test_partial_or_wrong_object_selection(self):
        for edit in (lambda r:r['objects'].pop(),lambda r:r['objects'][0].update(size=2),
                     lambda r:r['objects'][0].update(storage='far-common'),
                     lambda r:r['objects'][0].update(symbol='_other')):
            row=copy.deepcopy(self.item);edit(row)
            with self.assertRaises(ValueError):clock.validate_item(row)

    def test_unknown_backend_does_not_fall_back_to_clock(self):
        c=copy.deepcopy(self.config);c['source_allocations'][1]['backend']='unknown'
        with self.assertRaises(ValueError):self.run_config(c)

    def test_changed_source_rejected_before_compile(self):
        (self.project/clock.SOURCE).write_text('long clock_epoch=0,clock_sample=0,clock_value=0;')
        with patch.object(clock,'compile_c',side_effect=AssertionError('must not compile')):
            with self.assertRaisesRegex(ValueError,'source pin'):clock.build_input(self.item,self.project,PROJECT.parent/'CHESS.EXE',self.out)

    def test_tool_manifest_flags_and_command_provenance(self):
        for obj in (dataclasses.replace(self.compiled,source_sha256='0'*64),
                    dataclasses.replace(self.compiled,toolchain_manifest_sha256='0'*64),
                    dataclasses.replace(self.compiled,tool_hashes={}),
                    dataclasses.replace(self.compiled,flags=('/AS',)),
                    dataclasses.replace(self.compiled,source_name='OTHER.C'),
                    dataclasses.replace(self.compiled,command=()),
                    dataclasses.replace(self.compiled,compiler='msc510')):
            with self.subTest(obj=obj.compiler),self.assertRaises(ValueError):
                clock.build_input(self.item,self.project,PROJECT.parent/'CHESS.EXE',self.out,compiler_fn=lambda *a,**k:obj)

    def test_changed_during_generation_rejected(self):
        def compile_and_change(*a,**k):
            (self.project/clock.SOURCE).write_bytes(b'long changed;');return self.compiled
        with self.assertRaisesRegex(ValueError,'provenance'):
            clock.build_input(self.item,self.project,PROJECT.parent/'CHESS.EXE',self.out,compiler_fn=compile_and_change)

    def test_evidence_identity_and_path_escape(self):
        for key in self.item['evidence']:
            row=copy.deepcopy(self.item);row['evidence'][key]['sha256']='0'*64
            with self.subTest(key=key),self.assertRaises(ValueError):clock.validate_item(row)
        with self.assertRaises(ValueError):clock.local(self.project,'../CHESS.EXE')

    def test_corrupt_primary_and_retained_link_artifact(self):
        for key in ('native_raw','prepare','refresh','crt','SCALARS-MAIN_exe','MAIN-SCALARS_map','runtime','helper_library','linker'):
            p=self.project/self.item['evidence'][key]['path'];before=p.read_bytes();p.write_bytes(before+b'x')
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'evidence pin'):
                clock.validate_evidence(self.project,self.item['evidence'],PROJECT.parent/'CHESS.EXE')
            p.write_bytes(before)

    def test_wrong_original_target(self):
        path=self.project/'wrong.exe';path.write_bytes(b'MZwrong')
        with self.assertRaisesRegex(ValueError,'target pin'):
            clock.validate_evidence(self.project,self.item['evidence'],path)

    def test_raw_checksums_truncation_and_tail(self):
        bad=bytearray(self.obj);bad[250]^=1
        for raw in (bytes(bad),self.obj[:-1],self.obj+b'\0'):self.bad_obj(raw)

    def test_near_common_signed_long_size_required(self):
        for before,after in [(b'\x62\x04',b'\x62\x02'),(b'\x62\x04',b'\x61\x01\x04'),
                             (b'\x80\x82',b'\x80\x85')]:
            self.bad_obj(mutate(self.obj,0xb0,lambda p:p.replace(before,after,1)))

    def test_missing_extra_and_wrong_names(self):
        for f in (lambda p:b'',lambda p:p+p[:18],lambda p:p.replace(b'clock_epoch',b'clock_other',1)):
            self.bad_obj(mutate(self.obj,0xb0,f))

    def test_nonzero_code_data_const_bss_and_debug_allocations(self):
        rows=read_omf(self.obj).records
        for index in range(4,10):
            changed=b''.join(record(k,p[:1]+b'\x02\0'+p[3:]if i==index else p)for i,(k,_,p)in enumerate(rows))
            self.bad_obj(changed)

    def test_extra_common_public_and_lidata_records(self):
        for kind,payload in [(0xb0,b'\x04_more\x80\x82\x62\x04'),
                             (0x90,b'\x01\x02\x04_more\0\0\0'),(0xa2,bytes.fromhex('020000040000000100')),
                             (0xa0,bytes.fromhex('02000000'))]:
            self.bad_obj(self.obj[:-5]+record(kind,payload)+self.obj[-5:])

    def test_debug_fields_names_group_and_entry_point(self):
        for kind,change in [(0x9c,lambda p:p+b'\0'),(0x9a,lambda p:b'\x02\xff\x02'),
                           (0x8a,lambda p:b'\x80'),(0xa0,lambda p:p.replace(b'clock_epoch',b'clock_other',1)),
                           (0x88,lambda p:b'\0\x9e')]:
            self.bad_obj(mutate(self.obj,kind,change))
        # Actual CV relocation width/frame/target cannot be replaced by a code
        # or absolute field hidden inside a named debug segment.
        rows=read_omf(self.obj).records
        for before,after in [(bytes.fromhex('cc2b'),bytes.fromhex('c42b')),
                             (bytes.fromhex('5604'),bytes.fromhex('5603'))]:
            self.bad_obj(b''.join(record(k,p.replace(before,after,1)if k==0x9c else p)for k,_,p in rows))

    def test_failure_writes_no_success_object(self):
        row=copy.deepcopy(self.item);row['objects'].pop()
        with self.assertRaises(ValueError):clock.build_input(row,self.project,PROJECT.parent/'CHESS.EXE',self.out)
        self.assertFalse(self.out.exists())


if __name__=='__main__':unittest.main()
