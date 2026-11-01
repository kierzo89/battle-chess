"""Fixed complete67FB proof: actual eight-word compiler table, not cropped C."""
import copy
import dataclasses
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT))
from task_dispatch_extent import TARGET_SHA256, BODY_SHA256, NEXT_SHA256, START, SIZE, NEXT_SIZE, OMITTED, SWITCHES
from extent import validate_extended_extent
from msc import compile_c
from omf import read_omf
from link16 import link_function
from exepack import unpack_exepack

class TaskDispatchExtentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        canonical=json.loads((PROJECT/'config/units.json').read_text())
        cls.unit=next((u for u in canonical if u['id']=='dispatch_tasks_67fb'),None)
        if cls.unit is None:
            # Retained primary proof supports testing before parent registration.
            cls.unit=json.loads((PROJECT/'evidence/task-dispatch-67fb-policy-unit.json').read_text())['unit']
        r=compile_c(PROJECT/cls.unit['source'],cls.unit['flags'],compiler='msc500')
        o=read_omf(r.object_bytes)
        cls.info=o.function_info(cls.unit['symbol'])
        cls.linked,_=link_function(o,cls.unit['symbol'],0x67fb,cls.unit['externals'])
        # Validate the unmodified complete retained dossiers before making compact
        # mutation fixtures; unrelated native value-flow can exceed two megabytes.
        validate_extended_extent(cls.unit,PROJECT,TARGET_SHA256,cls.info,cls.linked)
        original=(PROJECT.parent/'CHESS.EXE').read_bytes()
        assert hashlib.sha256(original).hexdigest()==TARGET_SHA256
        image=unpack_exepack(original).image
        assert hashlib.sha256(image[0x67fb:0x68ea]).hexdigest()==BODY_SHA256
        assert hashlib.sha256(image[0x68ea:0x6ab1]).hexdigest()==NEXT_SHA256
        assert image[0x67fb:0x6ab1]==original[512+0x67fb:512+0x6ab1]

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.project=Path(self.temp.name);self.unit=copy.deepcopy(type(self).unit)
        self.emitted=copy.deepcopy(type(self).info);self.linked=type(self).linked
        meta=self.unit['extended_extent'];self.paths=[self.unit['rea_evidence'],meta['raw_span_evidence'],meta['next_entry_evidence']]+meta['omitted_byte_xref_evidence']
        self._written={}
        self.evidence={p:json.loads((PROJECT/p).read_text())for p in self.paths}
        for e in self.evidence.values():
            e.pop('raw_result',None)
            if e['operation']=='analyze_function':
                n=e['normalized_result']
                e['normalized_result']={k:n[k]for k in ['procedure','basic_blocks','incoming_references']}

    def validate(self):
        for p,e in self.evidence.items():
            encoded=json.dumps(e)
            if self._written.get(p)!=encoded:
                path=self.project/p;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(encoded)
                self._written[p]=encoded
        return validate_extended_extent(self.unit,self.project,TARGET_SHA256,self.emitted,self.linked)

    @property
    def body(self):return self.evidence[self.unit['rea_evidence']]['normalized_result']
    @property
    def raw(self):return self.evidence[self.unit['extended_extent']['raw_span_evidence']]
    @property
    def following(self):return self.evidence[self.unit['extended_extent']['next_entry_evidence']]['normalized_result']

    def test_fresh_complete239_CV_and_all9_actual_own_CODE_fixups(self):
        r=self.validate();self.assertEqual(r['span_bytes'],239);self.assertEqual(r['reachable_body_bytes'],221)
        self.assertEqual(r['closed_cfg_blocks'],22);self.assertEqual(r['compiler_own_CODE_fixups'],9)
        self.assertEqual(len(r['omitted_byte_xref_evidence_ids']),18)
        self.assertEqual(r['next_complete_body_bytes'],455)

    def test_entire_next_body_authentication_rejects_each_of455_mutations(self):
        original=bytes.fromhex(self.raw['normalized_result']['bytes_hex'])
        for at in range(SIZE,SIZE+NEXT_SIZE):
            b=bytearray(original);b[at]^=1;self.raw['normalized_result']['bytes_hex']=b.hex()
            with self.subTest(at=at),self.assertRaises(ValueError):self.validate()

    def test_every_linked_and_retained_body_byte_mutant_is_rejected(self):
        original=self.linked;context=bytes.fromhex(self.raw['normalized_result']['bytes_hex'])[SIZE:]
        for at in range(SIZE):
            self.linked=original[:at]+bytes([original[at]^1])+original[at+1:]
            self.raw['normalized_result']['bytes_hex']=(self.linked+context).hex()
            with self.subTest(at=at),self.assertRaises(ValueError):self.validate()

    def test_fixed_unit_scope_and_profile_are_mandatory(self):
        original=copy.deepcopy(self.unit)
        for change in [{'id':'other'},{'language':'asm'},{'backend':'msc400-omf'},{'symbol':'_other'},{'flags':['/AS','/Os','/Zi']},{'size':221},{'image_offset':'0x67fc'},{'code_address':{'segment':0,'offset':0x67fb}}]:
            self.unit=copy.deepcopy(original);self.unit.update(change)
            with self.subTest(change=change),self.assertRaises(ValueError):self.validate()
        self.unit=copy.deepcopy(original)
        with self.assertRaises(ValueError):validate_extended_extent(self.unit,self.project,'0'*64,self.emitted,self.linked)

    def test_exact_proof_fields_and_all18_xrefs_are_mandatory(self):
        original=copy.deepcopy(self.unit['extended_extent'])
        for change in [{'extra':True},{'omitted_byte_xref_evidence':original['omitted_byte_xref_evidence'][:-1]},{'omitted_byte_xref_evidence':[original['omitted_byte_xref_evidence'][0]]*18}]:
            self.unit['extended_extent']=copy.deepcopy(original);self.unit['extended_extent'].update(change)
            with self.subTest(change=change),self.assertRaises(ValueError):self.validate()

    def test_every_retained_evidence_subject_operation_load_language_and_profile(self):
        original=copy.deepcopy(self.evidence)
        for path in self.paths:
            for mode in ['subject','operation','load','language','profile','format']:
                self.evidence=copy.deepcopy(original);e=self.evidence[path]
                if mode=='subject':e['subject']['digest']['sha256']='0'*64
                elif mode=='operation':e['operation']='other'
                elif mode=='profile':e['analysis_profile']['digest']='other'
                else:e['analysis_profile']['parameters'][{'load':'load_segment','language':'language_id','format':'target_format'}[mode]]='other'
                with self.subTest(path=path,mode=mode),self.assertRaises(ValueError):self.validate()

    def test_each_omitted_byte_requires_its_own_empty_global_xref_result(self):
        original=copy.deepcopy(self.evidence);paths=self.unit['extended_extent']['omitted_byte_xref_evidence']
        for path in paths:
            for mode in ['incoming','address','identity']:
                self.evidence=copy.deepcopy(original);e=self.evidence[path]
                if mode=='incoming':e['normalized_result']=['0x10010']
                elif mode=='address':e['parameters']['address']='0x167fb'
                else:e['evidence_id']=self.evidence[self.paths[0]]['evidence_id']
                with self.subTest(path=path,mode=mode),self.assertRaises(ValueError):self.validate()

    def test_incoming_reference_to_each_omitted_byte_is_rejected(self):
        original=copy.deepcopy(self.body['incoming_references'])
        for at in OMITTED:
            self.body['incoming_references']=original+[{'target_address':hex(at)}]
            with self.subTest(at=at),self.assertRaises(ValueError):self.validate()

    def test_body_exact_three_ranges_and_reachable_count(self):
        original=copy.deepcopy(self.body['procedure'])
        for field,value in [('available',False),('contains_entry',False),('non_contiguous',False),('total_bytes',239),('span_bytes',221),('ranges',[{'start':'0x167fb','end':'0x168e9'}])]:
            self.body['procedure']=copy.deepcopy(original);self.body['procedure']['body'][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.validate()

    def test_cfg_must_be_exact_closed_nonoverlapping_and_cover_all_live_bytes(self):
        original=copy.deepcopy(self.body['basic_blocks'])
        for mode in ['remove','duplicate','extend','table_edge','dead_edge','outside','drop_edge','change_case']:
            blocks=copy.deepcopy(original)
            if mode=='remove':blocks.pop()
            elif mode=='duplicate':blocks.append(copy.deepcopy(blocks[-1]))
            elif mode=='extend':blocks[0]['end']='0x16811'
            elif mode=='drop_edge':blocks[0]['successors'].pop()
            elif mode=='change_case':next(b for b in blocks if b['start']=='0x16889')['successors'][0]='0x1681d'
            else:blocks[0]['successors'].append({'table_edge':'0x1688e','dead_edge':'0x1687c','outside':'0x168ea'}[mode])
            self.body['basic_blocks']=blocks
            with self.subTest(mode=mode),self.assertRaises(ValueError):self.validate()

    def test_every_cfg_block_boundary_edge_and_retained_range_boundary_is_bound(self):
        original_blocks=copy.deepcopy(self.body['basic_blocks'])
        for index,block in enumerate(original_blocks):
            for field in ['start','end']:
                blocks=copy.deepcopy(original_blocks);blocks[index][field]=hex(int(block[field],0)+1)
                self.body['basic_blocks']=blocks
                with self.subTest(block=index,field=field),self.assertRaises(ValueError):self.validate()
            for edge in range(len(block['successors'])):
                blocks=copy.deepcopy(original_blocks);blocks[index]['successors'].pop(edge)
                self.body['basic_blocks']=blocks
                with self.subTest(block=index,edge=edge),self.assertRaises(ValueError):self.validate()
        self.body['basic_blocks']=original_blocks
        original_ranges=copy.deepcopy(self.body['procedure']['body']['ranges'])
        for index,r in enumerate(original_ranges):
            for field in ['start','end']:
                ranges=copy.deepcopy(original_ranges);ranges[index][field]=hex(int(r[field],0)+1)
                self.body['procedure']['body']['ranges']=ranges
                with self.subTest(range=index,field=field),self.assertRaises(ValueError):self.validate()

    def test_raw_span_must_be_exact_complete694_original_bytes(self):
        original=copy.deepcopy(self.raw)
        for mode in ['address','length','returned','requested','complete','truncate','extend','linked_truncate','linked_mutable']:
            self.evidence[self.unit['extended_extent']['raw_span_evidence']]=copy.deepcopy(original);self.linked=type(self).linked
            if mode=='address':self.raw['parameters']['address']='0x167fc'
            elif mode=='length':self.raw['parameters']['length']=239
            elif mode=='returned':self.raw['normalized_result']['returned_bytes']=239
            elif mode=='requested':self.raw['normalized_result']['requested_bytes']=239
            elif mode=='complete':self.raw['normalized_result']['complete']=False
            elif mode=='truncate':self.raw['normalized_result']['bytes_hex']=self.raw['normalized_result']['bytes_hex'][:-2]
            elif mode=='extend':self.raw['normalized_result']['bytes_hex']+='90'
            elif mode=='linked_truncate':self.linked=self.linked[:-1]
            else:self.linked=bytearray(self.linked)
            with self.subTest(mode=mode),self.assertRaises(ValueError):self.validate()

    def test_next_entry_body_must_be_adjacent_complete455_and_contiguous(self):
        original=copy.deepcopy(self.following['procedure'])
        for field,value in [('available',False),('contains_entry',False),('non_contiguous',True),('total_bytes',454),('span_bytes',454),('ranges',[{'start':'0x168eb','end':'0x16ab0'}])]:
            self.following['procedure']=copy.deepcopy(original);self.following['procedure']['body'][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.validate()

    def test_codeview_symbol_extent_offset_and_segment_required(self):
        original=copy.deepcopy(self.emitted)
        for field,value in [('symbol','_other'),('boundary','next_public_or_segment_end'),('size',221),('end',238),('offset',True),('offset',-1),('segment',0),('fixups',[])]:
            self.emitted=copy.deepcopy(original);self.emitted[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.validate()

    def test_nonzero_actual_object_public_offset_is_supported(self):
        self.emitted['offset']+=100;self.emitted['end']+=100
        self.emitted['fixups']=[dataclasses.replace(f,offset=f.offset+100)for f in self.emitted['fixups']]
        self.validate()

    def test_each_of9_own_CODE_fixups_cannot_be_missing_or_corrupted(self):
        original=copy.deepcopy(self.emitted)
        required={table-START-2 for _,_,table,_,_ in SWITCHES}|{at-START for _,_,table,resume,_ in SWITCHES for at in range(table,resume,2)}
        for f in original['fixups']:
            if f.offset-original['offset'] not in required:continue
            for mode in ['missing','width','kind','relative','target','frame','displacement','segment']:
                self.emitted=copy.deepcopy(original)
                if mode=='missing':self.emitted['fixups']=[x for x in self.emitted['fixups']if x.offset!=f.offset]
                else:
                    changes={'width':{'width':4},'kind':{'location_type':3},'relative':{'segment_relative':False},'target':{'target':(2,1)},'frame':{'frame':(0,99)},'displacement':{'displacement':1},'segment':{'segment':99}}[mode]
                    self.emitted['fixups']=[dataclasses.replace(x,**changes)if x.offset==f.offset else x for x in self.emitted['fixups']]
                with self.subTest(offset=f.offset,mode=mode),self.assertRaises(ValueError):self.validate()

    def test_extra_fixup_cannot_overlap_gap_table_or_other_fixup_or_leave_procedure(self):
        original=copy.deepcopy(self.emitted);f=original['fixups'][0]
        for offset in [-1,SIZE-1,0x1687c-START,0x1688f-START,0x1689d-START,f.offset-original['offset']]:
            self.emitted=copy.deepcopy(original);self.emitted['fixups'].append(dataclasses.replace(f,offset=original['offset']+offset))
            with self.subTest(offset=offset),self.assertRaises(ValueError):self.validate()
