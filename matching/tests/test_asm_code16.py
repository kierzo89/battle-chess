"""Isolated strict CODE50 backend and proposed checker integration controls."""
import copy
import io
from contextlib import redirect_stdout
from dataclasses import replace
import importlib.util
from importlib.machinery import SourceFileLoader
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
PROJECT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT));sys.path.insert(0,str(HERE))
import asm_code16 as backend
from omf import read_omf, Public
loader=SourceFileLoader('proposed_bios_check',str(PROJECT/'check.py'))
spec=importlib.util.spec_from_loader(loader.name,loader)
check=importlib.util.module_from_spec(spec);loader.exec_module(check)

PROPOSAL=PROJECT/'build/bios-input-omf-203/units-proposed.json'

class BIOSCodeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.units=json.loads(PROPOSAL.read_text())['units']
        cls.built=backend.assemble(PROJECT/cls.units[0]['source'],cls.units[0])
        cls.obj=read_omf(cls.built.object_bytes)
        cls.image=bytearray(backend.BASE+50)
        cls.image[backend.BASE:]=cls.built.code
        cls.reference={'original_sha256':backend.ORIGINAL_SHA256,'relocations':()}

    def reject_obj(self,mutate):
        obj=copy.deepcopy(self.obj);mutate(obj)
        with self.assertRaises(ValueError):backend.extract_code(obj)

    def test_fresh_complete_segment_public_extents(self):
        code,meta=backend.extract_code(self.obj)
        self.assertEqual(len(code),50)
        self.assertEqual(backend.public_extent(meta,'_poll_event'),(0,41))
        self.assertEqual(backend.public_extent(meta,'_ticks_ea5b'),(41,9))
        self.assertEqual(meta['emitted_mz_sites'],[])
        self.assertTrue(self.built.provenance['fresh_directory'])

    def test_native_raw_whole_both_scopes(self):
        for unit in self.units:
            selected,proof=backend.validate_comparison(unit,self.built,self.image,PROJECT,())
            self.assertEqual(len(selected),unit['size'])
            self.assertEqual(proof['whole_allocation_size'],50)
            self.assertEqual(proof['whole_original_mz_sites'],[])
            self.assertEqual(proof['unit_original_mz_sites'],[])

    def test_every_original_byte_corruption_rejected_for_each_public(self):
        # Corruptions in the OTHER body must also reject a locally exact slice.
        for unit in self.units:
            for i in range(50):
                with self.subTest(symbol=unit['symbol'],byte=i):
                    image=bytearray(self.image);image[backend.BASE+i]^=1
                    with self.assertRaises(ValueError):
                        backend.validate_comparison(unit,self.built,image,PROJECT,())

    def test_every_emitted_byte_corruption_rejected(self):
        for i in range(50):
            raw=bytearray(self.built.object_bytes);cursor=0
            while cursor<len(raw):
                kind=raw[cursor];length=int.from_bytes(raw[cursor+1:cursor+3],'little')
                if kind==0xa0:
                    # Genuine strict OMF: segment index1 + offset16 + complete50.
                    self.assertEqual(raw[cursor+3:cursor+6],b'\x01\0\0')
                    raw[cursor+6+i]^=1
                    raw[cursor+2+length]=(-sum(raw[cursor:cursor+2+length]))&255
                    break
                cursor+=3+length
            code,meta=backend.extract_code(read_omf(bytes(raw)))
            self.assertNotEqual(code,self.built.code)
            built=replace(self.built,object_bytes=bytes(raw),code=code,metadata=meta)
            with self.assertRaises(ValueError):
                backend.validate_comparison(self.units[0],built,self.image,PROJECT,())

    def test_hole_overlap_empty_tail_and_excess(self):
        data=self.built.code
        for chunks in [[(1,data[1:])],[(0,data[:20]),(21,data[21:])],
                       [(0,data),(49,data[-1:])],[(0,b'')],[(0,data[:-1])],[(0,data+b'\x90')]]:
            with self.subTest(chunks=chunks):
                self.reject_obj(lambda o:setattr(o.segments[1],'chunks',chunks))

    def test_wrong_segment_attributes_names_size_other_allocation(self):
        for attr,value in [('length',49),('length',51),('attributes',0x28),
                           ('name','FRAME_TEXT'),('class_name','DATA'),('unsupported_data',True)]:
            with self.subTest(attr=attr,value=value):
                self.reject_obj(lambda o:setattr(o.segments[1],attr,value))
        self.reject_obj(lambda o:o.segments.update({2:copy.deepcopy(o.segments[1])}))

    def test_groups_comm_lidata_fixupp_and_extra_pseudo_code_records(self):
        for kind in (0x9a,0xb0,0xb8,0xa2,0x9c,0x8c,0x94,0xc6):
            with self.subTest(kind=kind):
                self.reject_obj(lambda o:o.records.append((kind,0,b'\0')))
        self.reject_obj(lambda o:o.externals.update({1:'_fake'}))
        self.reject_obj(lambda o:o.fixups.append(object()))
        self.reject_obj(lambda o:o.records.append((0x88,0,b'\x80\x9e')))
        self.reject_obj(lambda o:o.records.append((0x8a,0,b'\x80')))

    def test_public_extra_alias_missing_wrong_offset_group_type(self):
        self.reject_obj(lambda o:o.publics.update({'_extra':Public('_extra',1,49,0,0)}))
        self.reject_obj(lambda o:o.publics.pop('_ticks_ea5b'))
        for field,value in [('offset',40),('group',1),('segment',2),('type_index',1)]:
            def mutate(o):o.publics['_ticks_ea5b']=replace(o.publics['_ticks_ea5b'],**{field:value})
            with self.subTest(field=field):self.reject_obj(mutate)

    def test_unit_cannot_select_boundary_slice_or_foreign_ownership(self):
        for key,value in [('size',40),('image_offset','0xea33'),('symbol','_fake'),
                          ('object_profile','other'),('externals',{}),('end_symbol','_ticks_ea5b'),
                          ('owned_data',{}),('flags',[]),('source_sha256','0'*64),
                          ('assembler_sha256','0'*64),('rea_evidence','evidence/other.json')]:
            unit=dict(self.units[0],**{key:value})
            with self.subTest(key=key):
                with self.assertRaises(ValueError):backend.validate_unit(unit)
        meta=copy.deepcopy(self.built.metadata);meta['public_extents'][0]['size']=40
        with self.assertRaises(ValueError):backend.public_extent(meta,'_poll_event')

    def test_source_insertion_or_tool_pin_rejected_before_generation(self):
        with tempfile.TemporaryDirectory()as tmp:
            source=Path(tmp)/'bad.asm'
            for trailer in (b'\nincbin "TARGET"\n',b'\norg 0xea32\n',b'\ntimes 1 db 0\n',b'\nsegment OTHER class=CODE\n'):
                source.write_bytes((PROJECT/self.units[0]['source']).read_bytes()+trailer)
                with self.assertRaises(ValueError):backend.assemble(source,self.units[0])
        with patch.object(backend.shutil,'which',return_value=None):
            with self.assertRaises(ValueError):backend.assemble(PROJECT/self.units[0]['source'],self.units[0])
        with patch.object(backend,'NASM_SHA256','0'*64):
            with self.assertRaises(ValueError):backend.assemble(PROJECT/self.units[0]['source'],self.units[0])

    def test_original_mz_in_other_body_and_crossing_words_rejected(self):
        for unit in self.units:
            for site in (backend.BASE-1,backend.BASE,backend.BASE+40,backend.BASE+41,backend.BASE+49):
                with self.subTest(symbol=unit['symbol'],site=site):
                    with self.assertRaises(ValueError):
                        backend.validate_comparison(unit,self.built,self.image,PROJECT,(site,))
        backend.validate_comparison(self.units[0],self.built,self.image,PROJECT,(backend.BASE-2,backend.BASE+50))

    def fixture_project(self,tmp):
        project=Path(tmp)
        for rel in [backend.RAW_EVIDENCE]+[u['rea_evidence']for u in self.units]:
            path=project/rel;path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes((PROJECT/rel).read_bytes())
        return project

    def test_primary_wrong_subject_profile_read_length_raw_and_native_boundary(self):
        changes=[('raw','subject',None),('raw','profile',None),('raw','complete',None),
                 ('raw','address',None),('raw','length',None),('raw','byte',None),
                 ('native','boundary',None),('native','entry',None),('native','slice',None)] + [(scope,key,None)for scope in('raw','native')for key in('digest','format','target_format','provider')]
        for scope,change,_ in changes:
            with self.subTest(scope=scope,change=change),tempfile.TemporaryDirectory()as tmp:
                project=self.fixture_project(tmp);unit=self.units[0]
                path=project/(backend.RAW_EVIDENCE if scope=='raw'else unit['rea_evidence'])
                e=json.loads(path.read_text())
                if change=='subject':e['subject']['digest']['sha256']='0'*64
                elif change=='profile':e['analysis_profile']['parameters']['load_segment']='0x1001'
                elif change=='digest':e['analysis_profile']['digest']='other'
                elif change=='format':e['subject']['format']='dos-com'
                elif change=='target_format':e['analysis_profile']['parameters']['target_format']='dos-com'
                elif change=='provider':e['provider']['id']='other'
                elif change=='complete':e['raw_result']['complete']=False
                elif change=='address':e['raw_result']['address']='0x1ea33'
                elif change=='length':e['parameters']['length']=50
                elif change=='byte':
                    b=bytearray.fromhex(e['raw_result']['bytes_hex']);b[49]^=1;e['raw_result']['bytes_hex']=b.hex()
                elif change=='boundary':e['normalized_result']['procedure']['body']['total_bytes']=40
                elif change=='entry':e['normalized_result']['procedure']['body']['contains_entry']=False
                elif change=='slice':e['normalized_result']['procedure']['body']['ranges'][0]['end']='0x1ea59'
                path.write_text(json.dumps(e))
                with self.assertRaises(ValueError):backend.validate_comparison(unit,self.built,self.image,project,())

    def test_generation_has_no_original_or_evidence_reads(self):
        real_read=Path.read_bytes
        allowed={(PROJECT/self.units[0]['source']).resolve(),Path(shutil.which('nasm')).resolve()}
        def guarded(path):
            resolved=path.resolve()
            if resolved not in allowed and path.name!='UNIT.OBJ':
                raise AssertionError('Generation attempted undeclared read: '+str(path))
            return real_read(path)
        with patch.object(Path,'read_bytes',guarded):
            built=backend.assemble(PROJECT/self.units[0]['source'],self.units[0])
        self.assertEqual(built.code,self.built.code)
        with patch.object(Path,'read_bytes',side_effect=AssertionError('Extraction read file')):
            backend.extract_code(self.obj)

    def test_minimal_real_report_and_require_complete_exit(self):
        # Real target only enters post-generation comparison through check.run.
        # This minimal project owns only the two already-credited ASM bodies.
        with tempfile.TemporaryDirectory()as tmp:
            project=self.fixture_project(tmp)
            for rel in ('config/target.json','evidence/rea_procedures.json',self.units[0]['source']):
                dest=project/rel;dest.parent.mkdir(parents=True,exist_ok=True)
                dest.write_bytes((PROJECT/rel).read_bytes())
            (project/'config/units.json').write_text(json.dumps(self.units))
            output=project/'result'
            report=check.run(PROJECT.parent,project,PROJECT.parent/'CHESS.EXE',output,'nasm')
            summary=report['summary']
            self.assertEqual(summary['asm_matched_functions'],2)
            self.assertEqual(summary['asm_matched_bytes'],50)
            for key in ('c_matched_functions','c_matched_bytes','source_data_units','source_data_bytes',
                        'asm_data_matched_units','asm_data_matched_bytes','runtime_matched_units','failed_units'):
                self.assertEqual(summary[key],0)
            self.assertEqual(summary['verified_file_span_bytes'],50)
            self.assertEqual(summary['verified_image_span_bytes'],50)
            self.assertFalse(summary['full_executable_match'])
            self.assertEqual([u['status']for u in report['units']],['asm_matched']*2)
            for unit in report['units']:
                meta=unit['emitted_code_segment']
                self.assertEqual([(p['name'],p['offset'])for p in meta['publics']],
                                 [('_poll_event',0),('_ticks_ea5b',41)])
                self.assertEqual(meta['segment']['length'],50)
                self.assertEqual(unit['complete_allocation_proof']['whole_original_mz_sites'],[])
                self.assertEqual(unit['complete_allocation_proof']['unit_original_mz_sites'],[])
            self.assertEqual(len({u['object_artifact']for u in report['units']}),1)
            self.assertTrue((output/'report.json').is_file())
            with patch.object(check,'HERE',project),patch.object(check,'ROOT',PROJECT.parent), \
                    patch.object(sys,'argv',['check.py','--target',str(PROJECT.parent/'CHESS.EXE'),
                                            '--output',str(project/'cli-result'),'--require-complete']), \
                    redirect_stdout(io.StringIO()):
                self.assertEqual(check.main(),1)
            cli=json.loads((project/'cli-result/report.json').read_text())
            self.assertEqual(cli['summary']['asm_matched_bytes'],50)
            self.assertEqual(cli['summary']['failed_units'],0)

    def test_proposed_checker_two_units_same_actual_object_unchanged_credit(self):
        check.validate_units(self.units,len(self.image))
        with tempfile.TemporaryDirectory()as tmp:
            out=Path(tmp)
            results=[check.build_unit(u,bytes(self.image),PROJECT,'nasm',output=out,reference=self.reference)for u in self.units]
            self.assertEqual([r['status']for r in results],['asm_matched']*2)
            self.assertEqual(sum(r['size']for r in results),50)
            self.assertEqual(len({r['object_sha256']for r in results}),1)
            self.assertEqual(len({r['object_artifact']for r in results}),1)
            self.assertTrue(all(r['authored_c_credit']==0 and not r['relocations']for r in results))
            self.assertEqual(Path(results[0]['object_artifact']).read_bytes(),self.built.object_bytes)
        for reference in (None,dict(self.reference,original_sha256='0'*64),dict(self.reference,relocations=(backend.BASE+49,))):
            result=check.build_unit(self.units[0],bytes(self.image),PROJECT,'nasm',reference=reference)
            self.assertEqual(result['status'],'build_error')

if __name__=='__main__':unittest.main()
