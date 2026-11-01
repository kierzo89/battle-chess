"""Mutation controls for fixed 0DAF original/expanded boundary, not a span heuristic."""
import copy
import dataclasses
import json
from pathlib import Path
import sys
import tempfile
import unittest
PROJECT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT))
from board_pointer_extent import validate_board_pointer_extent,ORIGINAL_SHA256
from msc import compile_c
from omf import read_omf
from link16 import link_function

class BoardPointerExtentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        units=json.loads((PROJECT/'config/units.json').read_text())
        cls.unit=next((u for u in units if u['id']=='board_pointer_0daf'),None)
        if cls.unit is None: cls.unit=json.loads((PROJECT/'evidence/board-pointer-extent-unit.json').read_text())
        r=compile_c(PROJECT/cls.unit['source'],cls.unit['flags'],compiler='msc500')
        o=read_omf(r.object_bytes);cls.info=o.function_info(cls.unit['symbol'])
        cls.linked,_=link_function(o,cls.unit['symbol'],0xdaf,cls.unit['externals'],owned_bss=cls.unit.get('owned_bss'))
        validate_board_pointer_extent(cls.unit,PROJECT,ORIGINAL_SHA256,cls.info,cls.linked)
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.project=Path(self.tmp.name)/'matching';self.project.mkdir()
        (self.project.parent/'CHESS.EXE').write_bytes((PROJECT.parent/'CHESS.EXE').read_bytes())
        self.unit=copy.deepcopy(type(self).unit);self.info=copy.deepcopy(type(self).info);self.linked=type(self).linked
        self.paths=[self.unit['rea_evidence']]
        for key,value in self.unit['extended_extent'].items():
            if key!='kind':self.paths.extend(value if isinstance(value,list)else[value])
        self.es={p:json.loads((PROJECT/p).read_text())for p in self.paths};self.written={}
        for e in self.es.values():
            e.pop('raw_result',None)
            if e['operation']=='analyze_function':
                n=e['normalized_result'];e['normalized_result']={k:n[k]for k in['procedure','basic_blocks','incoming_references']}
    def e(self,key):return self.es[self.unit['extended_extent'][key]]
    def validate(self):
        for p,e in self.es.items():
            text=json.dumps(e)
            if self.written.get(p)!=text:
                path=self.project/p;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text);self.written[p]=text
        return validate_board_pointer_extent(self.unit,self.project,ORIGINAL_SHA256,self.info,self.linked)
    def test_fresh_full513_and_next125_with_exact_MZ_loader_accounting(self):
        r=self.validate();self.assertEqual(r['span_bytes'],513);self.assertEqual(r['closed_cfg_blocks'],44)
        self.assertEqual(r['next_complete_body_bytes'],125);self.assertEqual(r['mz_relocations'],[0xf35,0xf64]);self.assertEqual(r['false_far_aliases'],4)
    def test_every_original_context_byte_rejected_even_with_matching_expanded_and_compiler(self):
        old=bytes.fromhex(self.e('original_raw_evidence')['normalized_result']['bytes_hex'])
        exp=bytes.fromhex(self.e('expanded_raw_evidence')['normalized_result']['bytes_hex'])
        for at in range(638):
            a=bytearray(old);a[at]^=1;b=bytearray(exp);b[at]^=1
            self.e('original_raw_evidence')['normalized_result']['bytes_hex']=a.hex();self.e('expanded_raw_evidence')['normalized_result']['bytes_hex']=b.hex();self.linked=bytes(a[:513])
            with self.subTest(at=at),self.assertRaises(ValueError):self.validate()
    def test_each_compiler_byte_rejected(self):
        for at in range(513):
            b=bytearray(type(self).linked);b[at]^=1;self.linked=bytes(b)
            with self.subTest(at=at),self.assertRaises(ValueError):self.validate()
    def test_expanded_must_include_exact_loader_adjustment_of_both_segment_words(self):
        old=self.e('expanded_raw_evidence')['normalized_result']['bytes_hex']
        original=bytes.fromhex(self.e('original_raw_evidence')['normalized_result']['bytes_hex'])
        for site in[0xf35,0xf64]:
            b=bytearray.fromhex(old);at=site-0xdaf;b[at:at+2]=original[at:at+2]
            self.e('expanded_raw_evidence')['normalized_result']['bytes_hex']=b.hex()
            with self.subTest(site=site),self.assertRaises(ValueError):self.validate()
    def test_complete_original_pin(self):
        p=self.project.parent/'CHESS.EXE';b=bytearray(p.read_bytes());b[10]^=1;p.write_bytes(b)
        with self.assertRaises(ValueError):self.validate()
    def test_fixed_identity_metadata_and_flags(self):
        old=copy.deepcopy(self.unit)
        for delta in[{'id':'other'},{'symbol':'_other'},{'size':512},{'image_offset':'0xdb0'},{'flags':['/AS','/Os','/Zi']},{'language':'asm'},{'backend':'msc400-omf'},{'code_address':{'segment':0,'offset':0xdaf}}]:
            self.unit=copy.deepcopy(old);self.unit.update(delta)
            with self.subTest(delta=delta),self.assertRaises(ValueError):self.validate()
        self.unit=copy.deepcopy(old);self.unit['extended_extent']['extra']='x'
        with self.assertRaises(ValueError):self.validate()
    def test_each_evidence_subject_operation_profile_and_unique_identity(self):
        old=copy.deepcopy(self.es)
        for p in self.paths:
            for key in['subject','operation','digest','load_segment','language_id','target_format','identity']:
                self.es=copy.deepcopy(old);e=self.es[p]
                if key=='subject':e['subject']['digest']['sha256']='0'*64
                elif key=='operation':e['operation']='other'
                elif key=='digest':e['analysis_profile']['digest']='other'
                elif key=='identity':e['evidence_id']=old[self.paths[(self.paths.index(p)+1)%len(self.paths)]]['evidence_id']
                else:e['analysis_profile']['parameters'][key]='other'
                with self.subTest(path=p,key=key),self.assertRaises(ValueError):self.validate()
    def test_original_partial_observations_cannot_be_replaced_by_assumed_complete_bodies(self):
        old=copy.deepcopy(self.es)
        for path in[self.unit['rea_evidence'],self.unit['extended_extent']['original_overlap_evidence'],self.unit['extended_extent']['original_next_evidence']]:
            self.es=copy.deepcopy(old);self.es[path]['normalized_result']['procedure']['body']['ranges']=[]
            with self.subTest(path=path),self.assertRaises(ValueError):self.validate()
    def test_complete_body_next_and_function_query_bounds(self):
        old=copy.deepcopy(self.es)
        for p in[p for p,e in old.items()if e['operation']=='analyze_function']:
            for key in['query','ranges','total_bytes','span_bytes','contains_entry','available','non_contiguous']:
                self.es=copy.deepcopy(old)
                if key=='query':self.es[p]['parameters']['procedure']='0x10000'
                else:
                    b=self.es[p]['normalized_result']['procedure']['body'];b[key]=[]if key=='ranges'else not b[key]if isinstance(b[key],bool)else 1
                with self.subTest(path=p,key=key),self.assertRaises(ValueError):self.validate()
    def test_each_CFG_block_and_successor_of_both_complete_procedures(self):
        old=copy.deepcopy(self.es)
        for key in['expanded_body_evidence','expanded_next_evidence']:
            for at,block in enumerate(self.e(key)['normalized_result']['basic_blocks']):
                for field in['start','end','successors']:
                    self.es=copy.deepcopy(old);b=self.e(key)['normalized_result']['basic_blocks'][at];b[field]=['0x10de6']if field=='successors'else hex(int(block[field],0)+1)
                    with self.subTest(key=key,at=at,field=field),self.assertRaises(ValueError):self.validate()
    def test_external_interior_incoming_reference_rejected_for_body_and_next(self):
        old=copy.deepcopy(self.es)
        for key,target in[('expanded_body_evidence','0x10e0d'),('expanded_next_evidence','0x11013')]:
            self.es=copy.deepcopy(old);self.e(key)['normalized_result']['incoming_references'].append({'source_address':'0x12000','target_address':target})
            with self.subTest(key=key),self.assertRaises(ValueError):self.validate()
    def test_all_false_alias_lists_and_empty_expanded_lists_are_mandatory(self):
        old=copy.deepcopy(self.es)
        for key in['original_false_xrefs_evidence','expanded_false_xrefs_evidence']:
            for path in self.unit['extended_extent'][key]:
                self.es=copy.deepcopy(old);self.es[path]['normalized_result']=['0x10000']
                with self.subTest(path=path),self.assertRaises(ValueError):self.validate()
    def test_decoded_MOV_immediate_interior_byte_and_internal_JG_are_independent(self):
        old=copy.deepcopy(self.es)
        for key in['expanded_instruction_evidence','expanded_interior_evidence','expanded_branch_evidence']:
            for field,value in[('status','other'),('bytes','90'),('length',1),('mnemonic','NOP'),('procedure','0x10e0d')]:
                self.es=copy.deepcopy(old);self.e(key)['normalized_result'][field]=value
                with self.subTest(key=key,field=field),self.assertRaises(ValueError):self.validate()
    def test_full_raw_query_counts_and_complete_status(self):
        old=copy.deepcopy(self.es)
        for key in['original_raw_evidence','expanded_raw_evidence']:
            for field,value in[('complete',False),('address','0x10db0'),('requested_bytes',637),('returned_bytes',637)]:
                self.es=copy.deepcopy(old);self.e(key)['normalized_result'][field]=value
                with self.subTest(key=key,field=field),self.assertRaises(ValueError):self.validate()
    def test_CV_only_reviewed_offsets_zero_and65_permitted(self):
        old=copy.deepcopy(self.info)
        for pos in([65] if self.unit.get('owned_bss') else [0,65]):
            self.info=copy.deepcopy(old);d=pos-old['offset'];self.info.update(offset=pos,end=pos+513);self.info['fixups']=[dataclasses.replace(f,offset=f.offset+d)for f in old['fixups']];self.validate()
        if self.unit.get('owned_bss'):
            self.info=copy.deepcopy(old);self.info.update(offset=0,end=513);self.info['fixups']=[dataclasses.replace(f,offset=f.offset-old['offset'])for f in old['fixups']]
            with self.assertRaises(ValueError):self.validate()
        for field,value in[('symbol','_other'),('size',512),('end',513),('offset',1),('segment',0),('boundary','other')]:
            self.info=copy.deepcopy(old);self.info[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.validate()
    def test_all_actual_compiler_fields_and_both_far_MZ_sites_required(self):
        old=copy.deepcopy(self.info)
        for at in range(60):
            for changes in[{'frame':(0,1)},{'target':(0,1)},{'width':1},{'location_type':2},{'segment_relative':not old['fixups'][at].segment_relative},{'displacement':1},{'segment':2},{'offset':999}]:
                self.info=copy.deepcopy(old);self.info['fixups'][at]=dataclasses.replace(self.info['fixups'][at],**changes)
                with self.subTest(at=at,changes=changes),self.assertRaises(ValueError):self.validate()
        for fs in[old['fixups'][:-1],old['fixups'][:-1]+old['fixups'][:1]]:
            self.info=copy.deepcopy(old);self.info['fixups']=fs
            with self.assertRaises(ValueError):self.validate()

if __name__=='__main__':unittest.main()
