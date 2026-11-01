"""Complete fixed75F6 ordinary C proof, including the dead conditional-arm skip."""
import copy
import dataclasses
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

PROJECT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT))
from capture_task_extent import TARGET_SHA256,BODY_SHA256,NEXT_SHA256,START,END,SIZE,NEXT_SIZE,GAP,FIXUP_FIELDS
from extent import validate_extended_extent
from msc import compile_c
from omf import read_omf
from link16 import link_function
from exepack import unpack_exepack

class CaptureTaskExtentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        units=json.loads((PROJECT/'config/units.json').read_text())
        cls.unit=next((u for u in units if u['id']=='capture_task_75f6'),None)
        if cls.unit is None:cls.unit=json.loads((PROJECT/'evidence/capture-task-75f6-policy-unit.json').read_text())['unit']
        r=compile_c(PROJECT/cls.unit['source'],cls.unit['flags'],compiler='msc500')
        o=read_omf(r.object_bytes);cls.info=o.function_info(cls.unit['symbol'])
        cls.linked,_=link_function(o,cls.unit['symbol'],START-0x10000,cls.unit['externals'])
        validate_extended_extent(cls.unit,PROJECT,TARGET_SHA256,cls.info,cls.linked)
        original=(PROJECT.parent/'CHESS.EXE').read_bytes()
        assert hashlib.sha256(original).hexdigest()==TARGET_SHA256
        image=unpack_exepack(original).image;at=START-0x10000;end=END-0x10000
        assert image[at:end+NEXT_SIZE]==original[512+at:512+end+NEXT_SIZE]
        assert hashlib.sha256(image[at:end]).hexdigest()==BODY_SHA256
        assert hashlib.sha256(image[end:end+NEXT_SIZE]).hexdigest()==NEXT_SHA256

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.project=Path(self.temp.name);self.unit=copy.deepcopy(type(self).unit)
        self.emitted=copy.deepcopy(type(self).info);self.linked=type(self).linked
        m=self.unit['extended_extent'];self.paths=[self.unit['rea_evidence'],m['raw_span_evidence'],m['next_entry_evidence']]+m['gap_xref_evidence']
        self.evidence={p:json.loads((PROJECT/p).read_text())for p in self.paths};self.written={}
        for e in self.evidence.values():
            e.pop('raw_result',None)
            if e['operation']=='analyze_function':
                n=e['normalized_result'];e['normalized_result']={k:n[k]for k in ['procedure','basic_blocks','incoming_references']}

    def validate(self):
        for p,e in self.evidence.items():
            data=json.dumps(e)
            if self.written.get(p)!=data:
                path=self.project/p;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(data);self.written[p]=data
        return validate_extended_extent(self.unit,self.project,TARGET_SHA256,self.emitted,self.linked)

    @property
    def body(self):return self.evidence[self.unit['rea_evidence']]['normalized_result']
    @property
    def raw(self):return self.evidence[self.unit['extended_extent']['raw_span_evidence']]
    @property
    def following(self):return self.evidence[self.unit['extended_extent']['next_entry_evidence']]['normalized_result']

    def test_fresh_full311_CV_all20_fixups_and_complete130_context(self):
        r=self.validate();self.assertEqual(r['span_bytes'],311);self.assertEqual(r['reachable_body_bytes'],309)
        self.assertEqual(r['closed_cfg_blocks'],20);self.assertEqual(r['gap_hex'],'eb05')
        self.assertEqual(r['next_complete_body_bytes'],130);self.assertEqual(r['compiler_OFFSET16_fixups'],20)

    def test_dead_skip_targets_continuation_while_predecessor_returns_to_epilogue(self):
        r=self.validate()
        self.assertEqual(r['dead_skip_target'],'0x17657')
        self.assertEqual(r['live_return_epilogue'],'0x17727')
        self.assertNotEqual(r['dead_skip_target'],r['live_return_epilogue'])
        g=GAP-START
        self.assertEqual(self.linked[g-3],0xe9)
        self.assertEqual(self.linked[g:g+7],bytes.fromhex('eb052bc0e9d000'))

    def test_each_of311_linked_and_raw_agreeing_mutants_is_rejected(self):
        original=self.linked;context=bytes.fromhex(self.raw['normalized_result']['bytes_hex'])[SIZE:]
        for at in range(SIZE):
            self.linked=original[:at]+bytes([original[at]^1])+original[at+1:]
            self.raw['normalized_result']['bytes_hex']=(self.linked+context).hex()
            with self.subTest(at=at),self.assertRaises(ValueError):self.validate()

    def test_each_of130_next_body_mutants_is_rejected(self):
        original=bytes.fromhex(self.raw['normalized_result']['bytes_hex'])
        for at in range(SIZE,SIZE+NEXT_SIZE):
            b=bytearray(original);b[at]^=1;self.raw['normalized_result']['bytes_hex']=b.hex()
            with self.subTest(at=at),self.assertRaises(ValueError):self.validate()

    def test_fixed_function_profile_target_and_stack_probe_binding(self):
        original=copy.deepcopy(self.unit)
        for change in [{'id':'other'},{'symbol':'_other'},{'language':'asm'},{'backend':'msc400-omf'},{'flags':['/AS','/Os','/Zi']},{'image_offset':'0x75f7'},{'size':309},{'code_address':{'segment':0,'offset':0x75f6}}]:
            self.unit=copy.deepcopy(original);self.unit.update(change)
            with self.subTest(change=change),self.assertRaises(ValueError):self.validate()
        self.unit=copy.deepcopy(original);self.unit['externals']['__chkstk']=0xecab
        with self.assertRaises(ValueError):self.validate()
        self.unit=copy.deepcopy(original)
        with self.assertRaises(ValueError):validate_extended_extent(self.unit,self.project,'0'*64,self.emitted,self.linked)

    def test_exact_proof_fields_and_both_global_xrefs(self):
        original=copy.deepcopy(self.unit['extended_extent'])
        for change in [{'extra':True},{'gap_xref_evidence':original['gap_xref_evidence'][:1]},{'gap_xref_evidence':[original['gap_xref_evidence'][0]]*2}]:
            self.unit['extended_extent']=copy.deepcopy(original);self.unit['extended_extent'].update(change)
            with self.subTest(change=change),self.assertRaises(ValueError):self.validate()

    def test_each_evidence_target_operation_load_language_format_and_profile(self):
        original=copy.deepcopy(self.evidence)
        for path in self.paths:
            for mode in ['subject','operation','load_segment','language_id','target_format','digest']:
                self.evidence=copy.deepcopy(original);e=self.evidence[path]
                if mode=='subject':e['subject']['digest']['sha256']='0'*64
                elif mode=='operation':e['operation']='other'
                elif mode=='digest':e['analysis_profile']['digest']='other'
                else:e['analysis_profile']['parameters'][mode]='other'
                with self.subTest(path=path,mode=mode),self.assertRaises(ValueError):self.validate()

    def test_both_gap_bytes_require_distinct_empty_xref_records(self):
        original=copy.deepcopy(self.evidence)
        for path in self.unit['extended_extent']['gap_xref_evidence']:
            for mode in ['incoming','address','identity']:
                self.evidence=copy.deepcopy(original);e=self.evidence[path]
                if mode=='incoming':e['normalized_result']=['0x10000']
                elif mode=='address':e['parameters']['address']=hex(START)
                else:e['evidence_id']=self.evidence[self.paths[0]]['evidence_id']
                with self.subTest(path=path,mode=mode),self.assertRaises(ValueError):self.validate()

    def test_incoming_reference_cannot_enter_either_dead_jump_byte(self):
        original=copy.deepcopy(self.body['incoming_references'])
        for at in [GAP,GAP+1]:
            self.body['incoming_references']=original+[{'target_address':hex(at)}]
            with self.subTest(at=at),self.assertRaises(ValueError):self.validate()

    def test_exact_two_ranges_and309_reachable_count(self):
        original=copy.deepcopy(self.body['procedure'])
        for field,value in [('available',False),('contains_entry',False),('non_contiguous',False),('total_bytes',311),('span_bytes',309),('ranges',[{'start':hex(START),'end':hex(END-1)}])]:
            self.body['procedure']=copy.deepcopy(original);self.body['procedure']['body'][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.validate()
        self.body['procedure']=copy.deepcopy(original)
        ranges=original['body']['ranges']
        for index,r in enumerate(ranges):
            for field in ['start','end']:
                b=copy.deepcopy(ranges);b[index][field]=hex(int(r[field],0)+1);self.body['procedure']['body']['ranges']=b
                with self.subTest(range=index,field=field),self.assertRaises(ValueError):self.validate()

    def test_every_CFG_block_boundary_and_edge_is_bound(self):
        original=copy.deepcopy(self.body['basic_blocks'])
        for index,b in enumerate(original):
            for field in ['start','end']:
                blocks=copy.deepcopy(original);blocks[index][field]=hex(int(b[field],0)+1);self.body['basic_blocks']=blocks
                with self.subTest(block=index,field=field),self.assertRaises(ValueError):self.validate()
            for edge in range(len(b['successors'])):
                blocks=copy.deepcopy(original);blocks[index]['successors'].pop(edge);self.body['basic_blocks']=blocks
                with self.subTest(block=index,edge=edge),self.assertRaises(ValueError):self.validate()

    def test_CFG_rejects_extra_missing_overlapping_or_gap_blocks_and_nonclosed_edges(self):
        original=copy.deepcopy(self.body['basic_blocks'])
        for mode in ['remove','extra','overlap','gap','outside','cycle']:
            blocks=copy.deepcopy(original)
            if mode=='remove':blocks.pop()
            elif mode=='extra':blocks.append(copy.deepcopy(blocks[-1]))
            elif mode=='overlap':blocks[1]['start']=blocks[0]['start']
            else:blocks[0]['successors']=[{'gap':hex(GAP),'outside':hex(END),'cycle':hex(START)}[mode]]
            self.body['basic_blocks']=blocks
            with self.subTest(mode=mode),self.assertRaises(ValueError):self.validate()

    def test_exact_complete441_raw_and_full_linked_bytes_required(self):
        original=copy.deepcopy(self.raw)
        for mode in ['address','length','returned','requested','complete','truncate','extend','linked_truncate','linked_mutable']:
            self.evidence[self.unit['extended_extent']['raw_span_evidence']]=copy.deepcopy(original);self.linked=type(self).linked
            if mode=='address':self.raw['parameters']['address']=hex(START+1)
            elif mode=='length':self.raw['parameters']['length']=SIZE
            elif mode=='returned':self.raw['normalized_result']['returned_bytes']=SIZE
            elif mode=='requested':self.raw['normalized_result']['requested_bytes']=SIZE
            elif mode=='complete':self.raw['normalized_result']['complete']=False
            elif mode=='truncate':self.raw['normalized_result']['bytes_hex']=self.raw['normalized_result']['bytes_hex'][:-2]
            elif mode=='extend':self.raw['normalized_result']['bytes_hex']+='90'
            elif mode=='linked_truncate':self.linked=self.linked[:-1]
            else:self.linked=bytearray(self.linked)
            with self.subTest(mode=mode),self.assertRaises(ValueError):self.validate()

    def test_adjacent_next_function_is_complete_contiguous130(self):
        original=copy.deepcopy(self.following['procedure'])
        for field,value in [('available',False),('contains_entry',False),('non_contiguous',True),('total_bytes',129),('span_bytes',129),('ranges',[{'start':hex(END+1),'end':hex(END+NEXT_SIZE-1)}])]:
            self.following['procedure']=copy.deepcopy(original);self.following['procedure']['body'][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.validate()

    def test_fresh_CV_symbol_boundary_complete_size_offsets_segment_and_fixups(self):
        original=copy.deepcopy(self.emitted)
        for field,value in [('symbol','_other'),('boundary','next_public_or_segment_end'),('size',309),('end',310),('offset',True),('offset',-1),('segment',0),('fixups',[])]:
            self.emitted=copy.deepcopy(original);self.emitted[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.validate()

    def test_nonzero_natural_public_offset_supported(self):
        self.emitted['offset']+=100;self.emitted['end']+=100
        self.emitted['fixups']=[dataclasses.replace(f,offset=f.offset+100)for f in self.emitted['fixups']]
        self.validate()

    def test_every_actual_OFFSET16_field_required_and_wrong_mode_frame_target_rejected(self):
        original=copy.deepcopy(self.emitted)
        self.assertEqual({f.offset-original['offset']for f in original['fixups']},set(FIXUP_FIELDS))
        for f in original['fixups']:
            for mode in ['missing','width','kind','relative','frame','target','displacement','segment']:
                self.emitted=copy.deepcopy(original)
                if mode=='missing':self.emitted['fixups']=[x for x in self.emitted['fixups']if x.offset!=f.offset]
                else:
                    change={'width':{'width':4},'kind':{'location_type':3},'relative':{'segment_relative':not f.segment_relative},'frame':{'frame':(0,1)},'target':{'target':(0,1)},'displacement':{'displacement':1},'segment':{'segment':99}}[mode]
                    self.emitted['fixups']=[dataclasses.replace(x,**change)if x.offset==f.offset else x for x in self.emitted['fixups']]
                with self.subTest(offset=f.offset,mode=mode),self.assertRaises(ValueError):self.validate()

    def test_duplicate_overlapping_outofbounds_or_gap_fixups_rejected(self):
        original=copy.deepcopy(self.emitted);f=original['fixups'][0]
        for at in [-1,SIZE-1,GAP-START,GAP+1-START,original['fixups'][1].offset-original['offset'],f.offset-original['offset']+1]:
            self.emitted=copy.deepcopy(original);self.emitted['fixups'][0]=dataclasses.replace(f,offset=original['offset']+at)
            with self.subTest(at=at),self.assertRaises(ValueError):self.validate()
        self.emitted=copy.deepcopy(original);self.emitted['fixups'].append(copy.deepcopy(f))
        with self.assertRaises(ValueError):self.validate()
