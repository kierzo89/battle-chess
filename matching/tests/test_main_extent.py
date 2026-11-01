"""Strict fixed main0010 proof with full-context and ownership mutations."""
import copy
import dataclasses
import json
from pathlib import Path
import sys
import tempfile
import unittest
PROJECT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT))
from main_extent import ORIGINAL_SHA256,START,SIZE,GAP,END,MZ_SITES,NEXT_MZ
from extent import validate_extended_extent
from msc import compile_c
from omf import read_omf
from link16 import link_function
class MainExtentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit=json.loads((PROJECT/'evidence/main-0010-policy-unit.json').read_text())
        r=compile_c(PROJECT/cls.unit['source'],cls.unit['flags'],compiler='msc500')
        o=read_omf(r.object_bytes);cls.info=o.function_info('_main');cls.linked,cls.logs=link_function(o,'_main',16,cls.unit['externals'])
        validate_extended_extent(cls.unit,PROJECT,ORIGINAL_SHA256,cls.info,cls.linked)
        assert {f['mz_segment_relocation_image_offset']for f in cls.logs if 'mz_segment_relocation_image_offset'in f}==MZ_SITES
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.project=Path(self.tmp.name)/'matching';self.project.mkdir()
        (self.project.parent/'CHESS.EXE').write_bytes((PROJECT.parent/'CHESS.EXE').read_bytes())
        self.unit=copy.deepcopy(type(self).unit);self.info=copy.deepcopy(type(self).info);self.linked=type(self).linked
        self.paths=[self.unit['rea_evidence']]
        for k,v in self.unit['extended_extent'].items():
            if k!='kind':self.paths.extend(v if isinstance(v,list)else[v])
        self.es={p:json.loads((PROJECT/p).read_text())for p in self.paths};self.written={}
        for e in self.es.values():
            e.pop('raw_result',None)
            if e['operation']=='analyze_function':
                n=e['normalized_result'];e['normalized_result']={k:n[k]for k in ['procedure','basic_blocks','incoming_references']}
    def e(self,k):return self.es[self.unit['extended_extent'][k]]
    @property
    def native(self):return self.es[self.unit['rea_evidence']]['normalized_result']
    def validate(self):
        for p,e in self.es.items():
            t=json.dumps(e)
            if self.written.get(p)!=t:
                path=self.project/p;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(t);self.written[p]=t
        return validate_extended_extent(self.unit,self.project,ORIGINAL_SHA256,self.info,self.linked)
    def test_fresh580_CV575_native_and_full_next_context(self):
        r=self.validate();self.assertEqual(r['span_bytes'],580);self.assertEqual(r['reachable_body_bytes'],575)
        self.assertEqual(r['closed_cfg_blocks'],32);self.assertEqual(r['compiler_fixups'],80)
        self.assertEqual(r['gap_hex'],'5e8be55dc3');self.assertEqual(r['next_complete_span_bytes'],1439)
        self.assertEqual(r['next_closed_cfg_blocks'],145);self.assertEqual(set(r['original_MZ_sites']),MZ_SITES)
    def test_every_context_byte_rejects_agreeing_linked_original_and_loaded_mutants(self):
        raw=self.e('original_raw_evidence')['normalized_result'];loaded=self.e('expanded_raw_evidence')['normalized_result']
        original=bytes.fromhex(raw['bytes_hex']);expanded=bytes.fromhex(loaded['bytes_hex'])
        for at in range(2019):
            b=bytearray(original);b[at]^=1;raw['bytes_hex']=b.hex()
            c=bytearray(expanded);c[at]^=1;loaded['bytes_hex']=c.hex();self.linked=bytes(b[:580])
            with self.subTest(at=at),self.assertRaises(ValueError):self.validate()
    def test_each_linked_byte_rejected_without_masking(self):
        for at in range(580):
            b=bytearray(type(self).linked);b[at]^=1;self.linked=bytes(b)
            with self.subTest(at=at),self.assertRaises(ValueError):self.validate()
    def test_all11_loaded_relocation_words_require_real_loader_addition(self):
        n=self.e('expanded_raw_evidence')['normalized_result'];raw=self.e('original_raw_evidence')['normalized_result'];b=bytes.fromhex(n['bytes_hex']);original=bytes.fromhex(raw['bytes_hex'])
        for site in MZ_SITES|NEXT_MZ:
            at=site-16;c=bytearray(b);c[at:at+2]=original[at:at+2];n['bytes_hex']=c.hex()
            with self.subTest(site=site),self.assertRaises(ValueError):self.validate()
    def test_original_binary_pin(self):
        p=self.project.parent/'CHESS.EXE';b=bytearray(p.read_bytes());b[10]^=1;p.write_bytes(b)
        with self.assertRaises(ValueError):self.validate()
    def test_fixed_unit_identity_and_proof_fields(self):
        old=copy.deepcopy(self.unit)
        for d in [{'id':'other'},{'symbol':'_other'},{'size':575},{'image_offset':'0x11'},{'backend':'msc400-omf'},{'language':'asm'},{'flags':['/AS','/Gs','/Zi']},{'code_address':{'segment':0,'offset':16}}]:
            self.unit=copy.deepcopy(old);self.unit.update(d)
            with self.subTest(d=d),self.assertRaises(ValueError):self.validate()
        self.unit=copy.deepcopy(old);self.unit['externals']['__chkstk']=0xecab
        with self.assertRaises(ValueError):self.validate()
        self.unit=copy.deepcopy(old);self.unit['extended_extent']['extra']=True
        with self.assertRaises(ValueError):self.validate()
    def test_all_evidence_subject_operation_profile_and_identity(self):
        original=copy.deepcopy(self.es)
        for p in self.paths:
            for mode in ['subject','operation','digest','load_segment','language_id','target_format','identity']:
                self.es=copy.deepcopy(original);e=self.es[p]
                if mode=='subject':e['subject']['digest']['sha256']='0'*64
                elif mode=='operation':e['operation']='other'
                elif mode=='digest':e['analysis_profile']['digest']='other'
                elif mode=='identity':e['evidence_id']=original[self.paths[(self.paths.index(p)+1)%len(self.paths)]]['evidence_id']
                else:e['analysis_profile']['parameters'][mode]='other'
                with self.subTest(p=p,mode=mode),self.assertRaises(ValueError):self.validate()
    def test_both_native_extents_all_fields(self):
        old=copy.deepcopy(self.es)
        for p in [self.unit['rea_evidence'],self.unit['extended_extent']['next_entry_evidence']]:
            for k,v in [('available',False),('contains_entry',False),('total_bytes',1),('span_bytes',1),('ranges',[])]:
                self.es=copy.deepcopy(old);self.es[p]['normalized_result']['procedure']['body'][k]=v
                with self.subTest(p=p,k=k),self.assertRaises(ValueError):self.validate()
            self.es=copy.deepcopy(old);self.es[p]['parameters']['procedure']='0x10000'
            with self.assertRaises(ValueError):self.validate()
    def test_every_main_and_next_CFG_block_range_and_edge(self):
        old=copy.deepcopy(self.es)
        for p in [self.unit['rea_evidence'],self.unit['extended_extent']['next_entry_evidence']]:
            blocks=old[p]['normalized_result']['basic_blocks']
            for at,b in enumerate(blocks):
                for k in ['start','end','successors']:
                    self.es=copy.deepcopy(old);self.es[p]['normalized_result']['basic_blocks'][at][k]=['0x1024f']if k=='successors'else hex(int(b[k],0)+1)
                    with self.subTest(p=p,at=at,k=k),self.assertRaises(ValueError):self.validate()
    def test_all10_global_gap_xrefs_are_exact_empty_queries(self):
        old=copy.deepcopy(self.es)
        for k in ['original_gap_xrefs','expanded_gap_xrefs']:
            for p in self.unit['extended_extent'][k]:
                for mode in ['incoming','address','filter']:
                    self.es=copy.deepcopy(old)
                    if mode=='incoming':self.es[p]['normalized_result']=['0x10010']
                    elif mode=='address':self.es[p]['parameters']['address']='0x1024a'
                    else:self.es[p]['parameters']['filter']='empty'
                    with self.subTest(p=p,mode=mode),self.assertRaises(ValueError):self.validate()
    def test_each_gap_byte_incoming_reference_rejected(self):
        original=copy.deepcopy(self.native['incoming_references'])
        for at in range(GAP,END):
            self.native['incoming_references']=original+[{'target_address':hex(at)}]
            with self.subTest(at=at),self.assertRaises(ValueError):self.validate()
    def test_jumpback_decoder_target_and_complete_bytes(self):
        original=copy.deepcopy(self.e('jump_evidence'))
        for k,v in [('bytes','eb00'),('length',3),('status','undecodable'),('procedure','0x1024a'),('mnemonic','CALL')]:
            self.es[self.unit['extended_extent']['jump_evidence']]=copy.deepcopy(original);self.e('jump_evidence')['normalized_result'][k]=v
            with self.subTest(k=k),self.assertRaises(ValueError):self.validate()
        self.es[self.unit['extended_extent']['jump_evidence']]=copy.deepcopy(original);self.e('jump_evidence')['normalized_result']['flow']['direct_destinations']=['0x1024f']
        with self.assertRaises(ValueError):self.validate()
    def test_unknown_epilogue_decoder_observations_not_fabricated(self):
        old=copy.deepcopy(self.es)
        for p in self.unit['extended_extent']['epilogue_decoder_evidence']:
            for k,v in [('status','decoded'),('length',1),('bytes','5e'),('address','0x1024a')]:
                self.es=copy.deepcopy(old);self.es[p]['normalized_result'][k]=v
                with self.subTest(p=p,k=k),self.assertRaises(ValueError):self.validate()
    def test_raw_context_queries_complete_counts_and_status(self):
        old=copy.deepcopy(self.es)
        for k in ['original_raw_evidence','expanded_raw_evidence']:
            for f,v in [('complete',False),('returned_bytes',2018),('requested_bytes',2018),('address','0x10011')]:
                self.es=copy.deepcopy(old);self.e(k)['normalized_result'][f]=v
                with self.subTest(k=k,f=f),self.assertRaises(ValueError):self.validate()
    def test_fresh_CV_all_fields(self):
        old=copy.deepcopy(self.info)
        for k,v in [('size',575),('end',575),('offset',-1),('segment',0),('symbol','_other'),('boundary','other')]:
            self.info=copy.deepcopy(old);self.info[k]=v
            with self.subTest(k=k),self.assertRaises(ValueError):self.validate()
    def test_each_fixup_missing_duplicate_or_invalid(self):
        old=copy.deepcopy(self.info)
        for at,f in enumerate(old['fixups']):
            for mode in ['missing','duplicate','outside','frame','target','width','location','relative','displacement','segment']:
                self.info=copy.deepcopy(old)
                if mode=='missing':self.info['fixups'].pop(at)
                elif mode=='duplicate':self.info['fixups'][at]=old['fixups'][(at+1)%80]
                else:
                    d={'outside':{'offset':580},'frame':{'frame':(0,1)},'target':{'target':(0,1)},'width':{'width':1},'location':{'location_type':1 if f.location_type==5 else 4},'relative':{'segment_relative':not f.segment_relative},'displacement':{'displacement':1},'segment':{'segment':2}}[mode]
                    self.info['fixups'][at]=dataclasses.replace(f,**d)
                with self.subTest(at=at,mode=mode),self.assertRaises(ValueError):self.validate()
    def test_production_REA_gate_is_narrow_and_does_not_grant_carrier_to_ordinary_C(self):
        from check import validate_rea_extent
        from main_extent import CARRIER_SHA256
        self.validate()  # Persist independently authenticated evidence fixture.
        expected=self.es[self.unit['rea_evidence']]['evidence_id']
        self.assertEqual(validate_rea_extent(self.unit,self.project,ORIGINAL_SHA256),expected)
        old=copy.deepcopy(self.unit)
        for delta in [{'id':'other'},{'language':'runtime'},{'extended_extent':{'kind':'unrecognized'}}]:
            self.unit=copy.deepcopy(old);self.unit.update(delta)
            with self.subTest(delta=delta),self.assertRaises(ValueError):validate_rea_extent(self.unit,self.project,ORIGINAL_SHA256)
        self.unit=copy.deepcopy(old)
        with self.assertRaises(ValueError):validate_rea_extent(self.unit,self.project,'0'*64)
        path=self.project/self.unit['rea_evidence'];e=copy.deepcopy(self.es[self.unit['rea_evidence']])
        e['subject']['digest']['sha256']=ORIGINAL_SHA256;path.write_text(json.dumps(e))
        with self.assertRaises(ValueError):validate_rea_extent(self.unit,self.project,ORIGINAL_SHA256)
        self.unit['extended_extent']={'kind':'unrecognized'}
        with self.assertRaises(ValueError):validate_rea_extent(self.unit,self.project,ORIGINAL_SHA256)
        e['subject']['digest']['sha256']=CARRIER_SHA256;path.write_text(json.dumps(e))
        self.unit=copy.deepcopy(old);self.unit.pop('extended_extent')
        with self.assertRaises(ValueError):validate_rea_extent(self.unit,self.project,ORIGINAL_SHA256)
        self.unit['extended_extent']={'kind':'text_input_expanded_1064_v1'}
        with self.assertRaises(ValueError):validate_rea_extent(self.unit,self.project,ORIGINAL_SHA256)
if __name__=='__main__':unittest.main()
