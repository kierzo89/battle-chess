"""Fail-closed complete signum proof, including both unreachable return jumps."""
import copy
import dataclasses
import json
from pathlib import Path
import sys
import tempfile
import unittest

PROJECT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT))
from extent import validate_extended_extent
from msc import compile_c
from omf import read_omf
from link16 import link_function

TARGET='c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'

class SignumExtentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        b=compile_c(PROJECT/'src/sign_5c8b_probe.c',['/AS','/Zi'],compiler='msc500')
        o=read_omf(b.object_bytes)
        cls.fresh_info=o.function_info('_sign_5c8b')
        cls.fresh_linked,_=link_function(o,'_sign_5c8b',0x5c8b,{'__chkstk':0xecaa})

    def setUp(self):
        self.scratch=tempfile.TemporaryDirectory();self.addCleanup(self.scratch.cleanup)
        self.project=Path(self.scratch.name)
        self.paths={'body':'evidence/rea_pen_sign_5c8b.json','raw':'evidence/rea_pen_sign_fullspan.json','next':'evidence/rea_after_pen_sign_5cb5.json'}
        self.paths.update({'xref'+str(i):'evidence/rea_pen_sign_gap_xrefs_'+a+'.json'for i,a in enumerate(['15c9e','15c9f','15cab','15cac'])})
        self.evidence={k:json.loads((PROJECT/p).read_text())for k,p in self.paths.items()}
        self.unit={'id':'sign_5c8b','language':'c','backend':'msc500-omf','flags':['/AS','/Zi'],'symbol':'_sign_5c8b','image_offset':'0x5c8b','size':42,'externals':{'__chkstk':0xecaa},'rea_evidence':self.paths['body'],'extended_extent':{'kind':'signed_signum_return_gaps_v1','raw_span_evidence':self.paths['raw'],'next_entry_evidence':self.paths['next'],'gap_xref_evidence':[self.paths['xref'+str(i)]for i in range(4)]}}
        self.emitted=copy.deepcopy(self.fresh_info);self.linked=self.fresh_linked

    def validate(self):
        for k,p in self.paths.items():
            path=self.project/p;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(self.evidence[k]))
        return validate_extended_extent(self.unit,self.project,TARGET,self.emitted,self.linked)

    def test_real_fresh_full_CV_emission_and_both_dead_jumps(self):
        r=self.validate();self.assertEqual(r['span_bytes'],42);self.assertEqual(r['reachable_body_bytes'],38)
        self.assertEqual(r['gap_hex'],['eb11','eb04']);self.assertEqual(len(r['gap_xref_evidence_ids']),4)

    def test_nonzero_enclosing_object_offset_is_validated_against_fixup(self):
        self.emitted['offset']+=334;self.emitted['end']+=334
        self.emitted['fixups']=[dataclasses.replace(f,offset=f.offset+334)for f in self.emitted['fixups']]
        self.validate()

    def test_every_byte_rejected_when_raw_and_linked_agree_on_a_mutant(self):
        original=self.linked
        for at in range(42):
            self.linked=original[:at]+bytes([original[at]^1])+original[at+1:]
            self.evidence['raw']['normalized_result']['bytes_hex']=self.linked.hex()+bytes.fromhex(self.evidence['raw']['normalized_result']['bytes_hex'])[42:].hex()
            with self.subTest(at=at),self.assertRaises(ValueError):self.validate()

    def test_fixed_function_language_profile_and_site_are_mandatory(self):
        original=copy.deepcopy(self.unit)
        for change in [{'language':'asm'},{'backend':'nasm'},{'id':'another'},{'symbol':'_another'},{'image_offset':'0x5c8c'},{'size':38},{'size':44},{'flags':['/AS','/Os','/Zi']},{'code_address':{'segment':0,'offset':0x5c8b}}]:
            self.unit=copy.deepcopy(original);self.unit.update(change)
            with self.subTest(change=change),self.assertRaises(ValueError):self.validate()

    def test_exact_proof_fields_and_four_xrefs_are_mandatory(self):
        original=copy.deepcopy(self.unit['extended_extent'])
        for change in [{'extra':True},{'gap_xref_evidence':original['gap_xref_evidence'][:3]},{'gap_xref_evidence':[original['gap_xref_evidence'][0]]*4}]:
            self.unit['extended_extent']=copy.deepcopy(original);self.unit['extended_extent'].update(change)
            with self.subTest(change=change),self.assertRaises(ValueError):self.validate()

    def test_every_evidence_target_operation_and_profile_is_bound(self):
        original=copy.deepcopy(self.evidence)
        for key in self.paths:
            for mode in ['target','operation','language','load','profile']:
                self.evidence=copy.deepcopy(original);e=self.evidence[key]
                if mode=='target':e['subject']['digest']['sha256']='0'*64
                elif mode=='operation':e['operation']='other'
                elif mode=='language':e['analysis_profile']['parameters']['language_id']='x86:LE:32:default'
                elif mode=='load':e['analysis_profile']['parameters']['load_segment']='0x2000'
                else:e['analysis_profile']['digest']='changed'
                with self.subTest(key=key,mode=mode),self.assertRaises(ValueError):self.validate()

    def test_reachable_ranges_counts_and_entry_must_be_exact(self):
        original=copy.deepcopy(self.evidence['body']['normalized_result']['procedure'])
        for field,value in [('available',False),('contains_entry',False),('non_contiguous',False),('total_bytes',42),('span_bytes',38),('ranges',[{'start':'0x15c8b','end':'0x15cb4'}])]:
            self.evidence['body']['normalized_result']['procedure']=copy.deepcopy(original)
            self.evidence['body']['normalized_result']['procedure']['body'][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.validate()

    def test_cfg_must_have_exactly_six_closed_blocks(self):
        blocks=copy.deepcopy(self.evidence['body']['normalized_result']['basic_blocks'])
        for mode in ['remove','extra','gap','outside','wrong_end']:
            b=copy.deepcopy(blocks)
            if mode=='remove':b.pop()
            elif mode=='extra':b.append(copy.deepcopy(b[-1]))
            elif mode=='gap':b[0]['successors'].append('0x15c9e')
            elif mode=='outside':b[-1]['successors']=['0x15cb5']
            else:b[1]['end']='0x15c9f'
            self.evidence['body']['normalized_result']['basic_blocks']=b
            with self.subTest(mode=mode),self.assertRaises(ValueError):self.validate()

    def test_each_global_gap_reference_or_wrong_address_is_rejected(self):
        original=copy.deepcopy(self.evidence)
        for i in range(4):
            for mode in ['reference','address','identity']:
                self.evidence=copy.deepcopy(original);e=self.evidence['xref'+str(i)]
                if mode=='reference':e['normalized_result']=['0x10010']
                elif mode=='address':e['parameters']['address']='0x15c8b'
                else:e['evidence_id']=self.evidence['xref'+str((i+1)%4)]['evidence_id']
                with self.subTest(i=i,mode=mode),self.assertRaises(ValueError):self.validate()

    def test_retained_incoming_reference_cannot_enter_either_gap(self):
        original=copy.deepcopy(self.evidence['body']['normalized_result']['incoming_references'])
        for at in ['0x15c9e','0x15c9f','0x15cab','0x15cac']:
            self.evidence['body']['normalized_result']['incoming_references']=original+[{'target_address':at}]
            with self.subTest(at=at),self.assertRaises(ValueError):self.validate()

    def test_raw_length_completeness_address_and_full_next_context(self):
        original=copy.deepcopy(self.evidence['raw'])
        for field,value in [('complete',False),('address','0x15c8c'),('returned_bytes',42),('requested_bytes',42)]:
            self.evidence['raw']=copy.deepcopy(original);self.evidence['raw']['normalized_result'][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.validate()
        self.evidence['raw']=copy.deepcopy(original);self.evidence['raw']['parameters']['length']=42
        with self.assertRaises(ValueError):self.validate()
        self.evidence['raw']=copy.deepcopy(original);d=self.evidence['raw']['normalized_result'];d['bytes_hex']=d['bytes_hex'][:88];d['returned_bytes']=d['requested_bytes']=44;self.evidence['raw']['parameters']['length']=44
        with self.assertRaises(ValueError):self.validate()

    def test_adjacent_function_must_be_complete_contiguous_and_consistent(self):
        original=copy.deepcopy(self.evidence['next']['normalized_result']['procedure'])
        for field,value in [('available',False),('contains_entry',False),('non_contiguous',True),('total_bytes',146),('span_bytes',146),('ranges',[{'start':'0x15cb6','end':'0x15d47'}])]:
            self.evidence['next']['normalized_result']['procedure']=copy.deepcopy(original);self.evidence['next']['normalized_result']['procedure']['body'][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.validate()

    def test_every_adjacent_body_byte_is_authenticated_independently(self):
        raw=self.evidence['raw']['normalized_result']
        original=bytes.fromhex(raw['bytes_hex'])
        for at in range(42,189):
            mutant=original[:at]+bytes([original[at]^1])+original[at+1:]
            raw['bytes_hex']=mutant.hex()
            with self.subTest(raw_offset=at),self.assertRaises(ValueError):self.validate()

    def test_compiler_extent_and_sole_real_stack_probe_fixup_are_mandatory(self):
        original=copy.deepcopy(self.emitted)
        for field,value in [('symbol','_other'),('boundary','public'),('size',38),('end',41),('offset',1),('fixups',[])]:
            self.emitted=copy.deepcopy(original);self.emitted[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.validate()
        self.emitted=copy.deepcopy(original);f=self.emitted['fixups'][0]
        for change in [{'offset':f.offset+1},{'width':4},{'location_type':3},{'segment_relative':True},{'frame':(0,1)},{'target':(0,1)},{'displacement':1}]:
            self.emitted=copy.deepcopy(original);self.emitted['fixups']=[dataclasses.replace(f,**change)]
            with self.subTest(change=change),self.assertRaises(ValueError):self.validate()

    def test_wrong_linked_span_and_stack_probe_binding_are_rejected(self):
        original=self.linked
        for blob in [original[:-1],original+b'\x90',bytearray(original)]:
            self.linked=blob
            with self.subTest(length=len(blob)),self.assertRaises(ValueError):self.validate()
        self.linked=original;self.unit['externals']['__chkstk']=0xecab
        with self.assertRaises(ValueError):self.validate()
