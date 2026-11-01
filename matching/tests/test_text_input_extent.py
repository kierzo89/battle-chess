"""Full original-prefix / pinned expanded native boundary and mutation controls."""
import copy
import dataclasses
import json
from pathlib import Path
import sys
import tempfile
import unittest
PROJECT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT))
from text_input_extent import ORIGINAL_SHA256,START,SIZE,FIXUPS
from extent import validate_extended_extent
from msc import compile_c
from omf import read_omf
from link16 import link_function

class TextInputExtentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Exercise the current reviewed source and its actual call-name bindings.
        # The retained historical policy proposal may predate source-interface cleanup.
        units=json.loads((PROJECT/'config/units.json').read_text())
        cls.unit=next(u for u in units if u['id']=='text_input_1064')
        r=compile_c(PROJECT/cls.unit['source'],cls.unit['flags'],compiler='msc500')
        obj=read_omf(r.object_bytes);cls.info=obj.function_info(cls.unit['symbol'])
        cls.linked,_=link_function(obj,cls.unit['symbol'],0x1064,cls.unit['externals'])
        validate_extended_extent(cls.unit,PROJECT,ORIGINAL_SHA256,cls.info,cls.linked)

    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.project=Path(self.tmp.name)/'matching';self.project.mkdir()
        (self.project.parent/'CHESS.EXE').write_bytes((PROJECT.parent/'CHESS.EXE').read_bytes())
        self.unit=copy.deepcopy(type(self).unit);self.info=copy.deepcopy(type(self).info);self.linked=type(self).linked
        self.paths=[self.unit['rea_evidence']]+[v for k,v in self.unit['extended_extent'].items()if k!='kind']
        self.es={p:json.loads((PROJECT/p).read_text())for p in self.paths};self.written={}
        for e in self.es.values():
            e.pop('raw_result',None)
            if e['operation']=='analyze_function':
                n=e['normalized_result'];e['normalized_result']={k:n[k]for k in ['procedure','basic_blocks','incoming_references']}
    def e(self,key):return self.es[self.unit['extended_extent'][key]]
    def validate(self):
        for p,e in self.es.items():
            text=json.dumps(e)
            if self.written.get(p)!=text:
                path=self.project/p;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text);self.written[p]=text
        return validate_extended_extent(self.unit,self.project,ORIGINAL_SHA256,self.info,self.linked)
    def test_fresh_C256_and_corrected18block_native_boundary(self):
        r=self.validate();self.assertEqual(r['span_bytes'],256);self.assertEqual(r['closed_cfg_blocks'],18)
        self.assertEqual(r['next_complete_body_bytes'],306);self.assertEqual(r['false_far_aliases'],8)
    def test_every_original_context_byte_rejected_even_if_expanded_and_linked_agree(self):
        raw=self.e('original_raw_evidence');other=self.e('expanded_raw_evidence');original=bytes.fromhex(raw['normalized_result']['bytes_hex'])
        for at in range(562):
            b=bytearray(original);b[at]^=1
            raw['normalized_result']['bytes_hex']=b.hex();other['normalized_result']['bytes_hex']=b.hex();self.linked=bytes(b[:256])
            with self.subTest(at=at),self.assertRaises(ValueError):self.validate()
    def test_each_linked_byte_rejected(self):
        for at in range(256):
            b=bytearray(type(self).linked);b[at]^=1;self.linked=bytes(b)
            with self.subTest(at=at),self.assertRaises(ValueError):self.validate()
    def test_expanded_context_cannot_differ_from_original(self):
        r=self.e('expanded_raw_evidence')['normalized_result'];r['bytes_hex']='00'+r['bytes_hex'][2:]
        with self.assertRaises(ValueError):self.validate()
    def test_complete_original_binary_pin(self):
        p=self.project.parent/'CHESS.EXE';b=bytearray(p.read_bytes());b[10]^=1;p.write_bytes(b)
        with self.assertRaises(ValueError):self.validate()
    def test_fixed_unit_and_metadata_fields(self):
        saved=copy.deepcopy(self.unit)
        for delta in [{'id':'other'},{'symbol':'_other'},{'flags':['/AS','/Gs','/Zi']},{'size':255},{'image_offset':'0x1065'},{'backend':'msc400-omf'},{'language':'asm'},{'code_address':{'segment':0,'offset':0x1064}}]:
            self.unit=copy.deepcopy(saved);self.unit.update(delta)
            with self.subTest(delta=delta),self.assertRaises(ValueError):self.validate()
        self.unit=copy.deepcopy(saved);self.unit['extended_extent']['extra']='x'
        with self.assertRaises(ValueError):self.validate()
    def test_all_evidence_subject_operation_profile_and_uniqueness(self):
        original=copy.deepcopy(self.es)
        for path in self.paths:
            for field in ['subject','operation','digest','load_segment','language_id','target_format','identity']:
                self.es=copy.deepcopy(original);e=self.es[path]
                if field=='subject':e['subject']['digest']['sha256']='0'*64
                elif field=='operation':e['operation']='other'
                elif field=='digest':e['analysis_profile']['digest']='other'
                elif field=='identity':e['evidence_id']=original[self.paths[(self.paths.index(path)+1)%len(self.paths)]]['evidence_id']
                else:e['analysis_profile']['parameters'][field]='other'
                with self.subTest(path=path,field=field),self.assertRaises(ValueError):self.validate()
    def test_full_native_body_and_both_next_extents(self):
        old=copy.deepcopy(self.es)
        for key in ['expanded_body_evidence','original_next_evidence','expanded_next_evidence']:
            for field,value in [('available',False),('contains_entry',False),('non_contiguous',True),('total_bytes',1),('span_bytes',1),('ranges',[])]:
                self.es=copy.deepcopy(old);self.e(key)['normalized_result']['procedure']['body'][field]=value
                with self.subTest(key=key,field=field),self.assertRaises(ValueError):self.validate()
    def test_all_native_function_query_addresses_are_exact(self):
        old=copy.deepcopy(self.es)
        paths=[p for p,e in self.es.items()if e['operation']=='analyze_function']
        for path in paths:
            self.es=copy.deepcopy(old);self.es[path]['parameters']['procedure']='0x10000'
            with self.subTest(path=path),self.assertRaises(ValueError):self.validate()
    def test_original_split_and_false_entry_observation_are_mandatory(self):
        old=copy.deepcopy(self.es)
        for path in [self.unit['rea_evidence'],self.unit['extended_extent']['original_overlap_evidence']]:
            self.es=copy.deepcopy(old);self.es[path]['normalized_result']['procedure']['body']['ranges']=[]
            with self.subTest(path=path),self.assertRaises(ValueError):self.validate()
    def test_all_false_original_xrefs_and_no_expanded_xrefs(self):
        old=copy.deepcopy(self.es)
        for key in ['original_false_xrefs_evidence','expanded_false_xrefs_evidence']:
            self.es=copy.deepcopy(old);self.e(key)['normalized_result']=['0x10000']
            with self.subTest(key=key),self.assertRaises(ValueError):self.validate()
        self.es=copy.deepcopy(old);self.e('expanded_false_xrefs_evidence')['parameters']['address']='0x110d2'
        with self.assertRaises(ValueError):self.validate()
    def test_each_CFG_range_and_successor_mutation(self):
        old=copy.deepcopy(self.e('expanded_body_evidence')['normalized_result']['basic_blocks'])
        for at,block in enumerate(old):
            for field in ['start','end','successors']:
                blocks=copy.deepcopy(old)
                blocks[at][field]=['0x110d3']if field=='successors'else hex(int(block[field],0)+1)
                self.e('expanded_body_evidence')['normalized_result']['basic_blocks']=blocks
                with self.subTest(at=at,field=field),self.assertRaises(ValueError):self.validate()
    def test_incoming_external_interior_entry_rejected(self):
        self.e('expanded_body_evidence')['normalized_result']['incoming_references'].append({'source_address':'0x12000','target_address':'0x110dc'})
        with self.assertRaises(ValueError):self.validate()
    def test_independent_AND_and_interior_instruction_status(self):
        old=copy.deepcopy(self.es)
        for key,field,value in [('expanded_instruction_evidence','bytes','2500e0'),('expanded_instruction_evidence','length',2),('expanded_instruction_evidence','status','data'),('expanded_interior_evidence','status','decoded'),('expanded_interior_evidence','length',2)]:
            self.es=copy.deepcopy(old);self.e(key)['normalized_result'][field]=value
            with self.subTest(key=key,field=field),self.assertRaises(ValueError):self.validate()
    def test_complete_raw_parameters_counts_and_status(self):
        old=copy.deepcopy(self.es)
        for key in ['original_raw_evidence','expanded_raw_evidence']:
            for field,value in [('complete',False),('address','0x11065'),('requested_bytes',561),('returned_bytes',561)]:
                self.es=copy.deepcopy(old);self.e(key)['normalized_result'][field]=value
                with self.subTest(key=key,field=field),self.assertRaises(ValueError):self.validate()
    def test_CV_identity_size_and_offset(self):
        old=copy.deepcopy(self.info)
        for field,value in [('symbol','_other'),('size',255),('end',255),('offset',-1),('segment',0),('boundary','other')]:
            self.info=copy.deepcopy(old);self.info[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.validate()
    def test_fixup_missing_duplicate_outside_and_wrong_semantics(self):
        old=copy.deepcopy(self.info)
        variants=[old['fixups'][:-1],old['fixups'][:-1]+old['fixups'][:1]]
        for changes in [{'offset':256},{'frame':(0,1)},{'target':(0,1)},{'width':4},{'location_type':2},{'segment_relative':True},{'displacement':1},{'segment':2}]:
            fs=copy.deepcopy(old['fixups']);fs[0]=dataclasses.replace(fs[0],**changes);variants.append(fs)
        for fs in variants:
            self.info=copy.deepcopy(old);self.info['fixups']=fs
            with self.subTest(fs=fs),self.assertRaises(ValueError):self.validate()
if __name__=='__main__':unittest.main()
