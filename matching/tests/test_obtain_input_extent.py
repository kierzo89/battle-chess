"""Fixed0254 proof: fresh full source plus meaningful ownership mutations."""
import copy
import dataclasses
import json
from pathlib import Path
import sys
import tempfile
import unittest
PROJECT=next(p for p in Path(__file__).resolve().parents if(p/'config/units.json').is_file())
sys.path.insert(0,str(PROJECT))
from obtain_input_extent import validate_obtain_input_extent,ORIGINAL_SHA256,START,END,SIZE,NEXT_SIZE,GAPS,MZ_SITES,INTERIOR_TARGETS,FIXUPS
from msc import compile_c
from omf import read_omf
from link16 import link_function

class ObtainInputExtentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        canonical=json.loads((PROJECT/'config/units.json').read_text())
        cls.unit=next((u for u in canonical if u['id']=='obtain_input_0254'),None)
        if cls.unit is None:
            cls.unit=json.loads((PROJECT/'evidence/obtain-input-extent-unit.json').read_text())
        r=compile_c(PROJECT/cls.unit['source'],cls.unit['flags'],compiler='msc500')
        o=read_omf(r.object_bytes);cls.info=o.function_info('_obtain_input')
        cls.linked,cls.logs=link_function(o,'_obtain_input',0x254,cls.unit['externals'])
        cls.proof=validate_obtain_input_extent(cls.unit,PROJECT,ORIGINAL_SHA256,cls.info,cls.linked)
        assert len(cls.linked)==SIZE and {f['mz_segment_relocation_image_offset']for f in cls.logs if 'mz_segment_relocation_image_offset'in f}==MZ_SITES
        # A second genuine source context has the same181 fields at public0.
        r=compile_c(PROJECT/'src/probes/obtain_input_0254_match.c',['/AS','/Zi'],compiler='msc500')
        o=read_omf(r.object_bytes);cls.standalone=o.function_info('_obtain_input')
        # This retained standalone source predates canonical graphics name coherence.
        # Bind its genuine historical EXTDEFs with its immutable original map.
        cls.standalone_unit=json.loads((PROJECT/'evidence/obtain-input-extent-unit.json').read_text())
        cls.standalone_linked,_=link_function(o,'_obtain_input',0x254,cls.standalone_unit['externals'])
        validate_obtain_input_extent(cls.standalone_unit,PROJECT,ORIGINAL_SHA256,cls.standalone,cls.standalone_linked)
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.project=Path(self.tmp.name)/'matching';self.project.mkdir()
        (self.project.parent/'CHESS.EXE').write_bytes((PROJECT.parent/'CHESS.EXE').read_bytes())
        self.unit=copy.deepcopy(type(self).unit);self.info=copy.deepcopy(type(self).info);self.linked=type(self).linked;self.sha=ORIGINAL_SHA256
        self.paths=[self.unit['rea_evidence']]
        for k,v in self.unit['extended_extent'].items():
            if k!='kind':self.paths.extend(v if isinstance(v,list)else[v])
        self.es={p:json.loads((PROJECT/p).read_text())for p in self.paths};self.written={}
        for e in self.es.values():
            e.pop('raw_result',None)
            if e['operation']=='analyze_function':
                n=e['normalized_result'];e['normalized_result']={k:n[k]for k in ['procedure','basic_blocks','incoming_references','outgoing_references']}
    def e(self,key):return self.es[self.unit['extended_extent'][key]]
    def validate(self):
        for p,e in self.es.items():
            t=json.dumps(e)
            if self.written.get(p)!=t:
                q=self.project/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t);self.written[p]=t
        return validate_obtain_input_extent(self.unit,self.project,self.sha,self.info,self.linked)
    def test_fresh_group_and_standalone_full1439_proof(self):
        p=self.validate();self.assertEqual(p['span_bytes'],1439);self.assertEqual(p['reachable_body_bytes'],1424)
        self.assertEqual(p['closed_cfg_blocks'],145);self.assertEqual(p['gap_bytes'],15)
        self.assertEqual(p['empty_global_xrefs'],15);self.assertEqual(p['compiler_fixups'],181)
        self.assertEqual(p['native_terminating_predecessors'],7);self.assertEqual(p['decoded_interior_targets'],2)
        self.assertEqual(p['dead_to_dead_chain'],['0x1048e','0x104e5','0x107e9'])
        self.assertEqual(p['next_complete_span_bytes'],75);self.assertEqual(p['next_closed_cfg_blocks'],9)
        self.assertEqual(set(p['original_MZ_sites']),MZ_SITES)
        self.info=copy.deepcopy(type(self).standalone);self.linked=type(self).standalone_linked
        self.unit=copy.deepcopy(type(self).standalone_unit)
        self.assertEqual(self.validate()['body_sha256'],p['body_sha256'])
    def test_each_full1514_original_context_byte_even_with_agreeing_C(self):
        raw=self.e('raw_span_evidence')['normalized_result'];original=bytes.fromhex(raw['bytes_hex'])
        for at in range(SIZE+NEXT_SIZE):
            b=bytearray(original);b[at]^=1;raw['bytes_hex']=b.hex();self.linked=bytes(b[:SIZE])
            with self.subTest(at=at),self.assertRaises(ValueError):self.validate()
    def test_each_full1439_linked_byte_has_no_mask(self):
        for at in range(SIZE):
            b=bytearray(type(self).linked);b[at]^=1;self.linked=bytes(b)
            with self.subTest(at=at),self.assertRaises(ValueError):self.validate()
    def test_raw_read_extent_flags_parameters_and_lengths(self):
        old=copy.deepcopy(self.es)
        for k,v in [('complete',False),('address','0x10255'),('requested_bytes',1439),('returned_bytes',1439),('bytes_hex','00')]:
            self.es=copy.deepcopy(old);self.e('raw_span_evidence')['normalized_result'][k]=v
            with self.subTest(k=k),self.assertRaises(ValueError):self.validate()
        for params in [{'address':'0x10254','length':1439},{'address':'0x10254','length':1514,'filter':True}]:
            self.es=copy.deepcopy(old);self.e('raw_span_evidence')['parameters']=params
            with self.assertRaises(ValueError):self.validate()
    def test_pinned_original_binary_and_target_sha(self):
        self.sha='0'*64
        with self.assertRaises(ValueError):self.validate()
        self.sha=ORIGINAL_SHA256;p=self.project.parent/'CHESS.EXE';b=bytearray(p.read_bytes());b[-1]^=1;p.write_bytes(b)
        with self.assertRaises(ValueError):self.validate()
    def test_fixed_unit_identity_and_only_known_metadata(self):
        old=copy.deepcopy(self.unit)
        for d in [{'id':'other'},{'language':'asm'},{'backend':'msc400-omf'},{'symbol':'_other'},{'image_offset':'0x255'},{'size':1424},{'flags':['/AS','/Gs','/Zi']},{'code_address':{'segment':0,'offset':0x254}}]:
            self.unit=copy.deepcopy(old);self.unit.update(d)
            with self.subTest(d=d),self.assertRaises(ValueError):self.validate()
        self.unit=copy.deepcopy(old);self.unit['externals']['__chkstk']=0xecab
        with self.assertRaises(ValueError):self.validate()
        for key in ['unknown','extra']:
            self.unit=copy.deepcopy(old)
            if key=='unknown':self.unit['extended_extent']['kind']='ordinary_noncontiguous'
            else:self.unit['extended_extent']['extra']=True
            with self.assertRaises(ValueError):self.validate()
    def test_all_evidence_subject_profile_operation_and_distinct_ids(self):
        old=copy.deepcopy(self.es)
        for at,p in enumerate(self.paths):
            for mode in ['subject','operation','digest','load_segment','language_id','target_format','format','architecture','identity']:
                self.es=copy.deepcopy(old);e=self.es[p]
                if mode=='subject':e['subject']['digest']['sha256']='0'*64
                elif mode=='operation':e['operation']='other'
                elif mode=='digest':e['analysis_profile']['digest']='other'
                elif mode=='identity':e['evidence_id']=old[self.paths[(at+1)%len(self.paths)]]['evidence_id']
                elif mode in ['format','architecture']:e['subject'][mode]='other'
                else:e['analysis_profile']['parameters'][mode]='other'
                with self.subTest(p=p,mode=mode),self.assertRaises(ValueError):self.validate()
    def test_evidence_cannot_escape_project(self):
        self.unit['extended_extent']['raw_span_evidence']='../CHESS.EXE'
        with self.assertRaises(ValueError):self.validate()
    def test_body_and_full_next_native_extent_fields(self):
        old=copy.deepcopy(self.es)
        for p in [self.unit['rea_evidence'],self.unit['extended_extent']['next_entry_evidence']]:
            for k,v in [('available',False),('contains_entry',False),('non_contiguous',None),('ranges',[]),('total_bytes',1),('span_bytes',1)]:
                self.es=copy.deepcopy(old);self.es[p]['normalized_result']['procedure']['body'][k]=v
                with self.subTest(p=p,k=k),self.assertRaises(ValueError):self.validate()
            self.es=copy.deepcopy(old);self.es[p]['parameters']['procedure']='0x10000'
            with self.assertRaises(ValueError):self.validate()
            self.es=copy.deepcopy(old);self.es[p]['normalized_result']['procedure']['address']='0x10000'
            with self.assertRaises(ValueError):self.validate()
    def test_every_native_and_next_CFG_block_range_and_successor(self):
        old=copy.deepcopy(self.es)
        for p in [self.unit['rea_evidence'],self.unit['extended_extent']['next_entry_evidence']]:
            for at,b in enumerate(old[p]['normalized_result']['basic_blocks']):
                for key in ['start','end','successors']:
                    self.es=copy.deepcopy(old);self.es[p]['normalized_result']['basic_blocks'][at][key]=['0x10393']if key=='successors'else hex(int(b[key],0)+1)
                    with self.subTest(p=p,at=at,key=key),self.assertRaises(ValueError):self.validate()
            for mode in ['remove','duplicate','disconnect']:
                self.es=copy.deepcopy(old);blocks=self.es[p]['normalized_result']['basic_blocks']
                if mode=='remove':blocks.pop()
                elif mode=='duplicate':blocks.append(copy.deepcopy(blocks[0]))
                else:
                    for b in blocks:b['successors']=[]
                with self.assertRaises(ValueError):self.validate()
    def test_all15_global_gap_queries_empty_unfiltered_and_exact(self):
        old=copy.deepcopy(self.es)
        for p in self.unit['extended_extent']['gap_xref_evidence']:
            for mode in ['incoming','address','filter']:
                self.es=copy.deepcopy(old)
                if mode=='incoming':self.es[p]['normalized_result']=['0x10254']
                elif mode=='address':self.es[p]['parameters']['address']='0x10254'
                else:self.es[p]['parameters']['filter']='empty'
                with self.subTest(p=p,mode=mode),self.assertRaises(ValueError):self.validate()
    def test_native_incoming_and_outgoing_edges_cannot_enter_any_gap_byte(self):
        old=copy.deepcopy(self.es)
        for key in ['incoming_references','outgoing_references']:
            for a,(raw,*_)in GAPS.items():
                for dest in range(a,a+len(bytes.fromhex(raw))):
                    self.es=copy.deepcopy(old);self.es[self.unit['rea_evidence']]['normalized_result'][key].append({'target_address':hex(dest)})
                    with self.subTest(key=key,dest=dest),self.assertRaises(ValueError):self.validate()
    def test_each_gap_decoder_retains_explicit_unknown(self):
        old=copy.deepcopy(self.es)
        for p in self.unit['extended_extent']['gap_decoder_evidence']:
            for key,value in [('status','decoded'),('address','0x10254'),('bytes','eb00'),('length',2),('mnemonic','JMP'),('procedure','0x10254')]:
                self.es=copy.deepcopy(old);self.es[p]['normalized_result'][key]=value
                with self.subTest(p=p,key=key),self.assertRaises(ValueError):self.validate()
            for key,value in [('kind','jump'),('conditional',True),('computed',True),('direct_destinations',['0x107e9'])]:
                self.es=copy.deepcopy(old);self.es[p]['normalized_result']['flow'][key]=value
                with self.assertRaises(ValueError):self.validate()
    def test_every_preceding_live_jump_and_two_interior_targets(self):
        old=copy.deepcopy(self.es)
        for k in ['preceding_jump_evidence','interior_target_evidence']:
            for p in self.unit['extended_extent'][k]:
                for key,value in [('status','undecodable'),('address','0x10254'),('bytes','eb00'),('length',1),('mnemonic','CALL'),('procedure','0x10010')]:
                    self.es=copy.deepcopy(old);self.es[p]['normalized_result'][key]=value
                    with self.subTest(p=p,key=key),self.assertRaises(ValueError):self.validate()
                for key,value in [('kind','fallthrough'),('conditional',True),('computed',True),('direct_destinations',['0x10393'])]:
                    self.es=copy.deepcopy(old);self.es[p]['normalized_result']['flow'][key]=value
                    with self.subTest(p=p,key=key),self.assertRaises(ValueError):self.validate()
    def test_gap_proof_lists_cannot_remove_duplicate_or_retarget_records(self):
        old=copy.deepcopy(self.unit);old_es=copy.deepcopy(self.es)
        for k in ['gap_xref_evidence','gap_decoder_evidence','preceding_jump_evidence','interior_target_evidence']:
            for mode in ['missing','duplicate','retarget']:
                self.unit=copy.deepcopy(old);self.es=copy.deepcopy(old_es);entries=self.unit['extended_extent'][k]
                if mode=='missing':entries.pop()
                elif mode=='duplicate':entries[0]=entries[-1]
                else:
                    p=entries[0];self.es[p]['parameters']['address']='0x10254'
                with self.subTest(k=k,mode=mode),self.assertRaises(ValueError):self.validate()
    def test_full_CV_metadata_rejects_partial_or_unknown_offsets(self):
        old=copy.deepcopy(self.info)
        for key,value in [('symbol','_other'),('boundary','public_next'),('size',1424),('offset',1),('end',1),('segment',2),('segment',True)]:
            self.info=copy.deepcopy(old);self.info[key]=value
            with self.subTest(key=key,value=value),self.assertRaises(ValueError):self.validate()
    def test_every181_field_type_frame_target_width_displacement_and_segment(self):
        old=copy.deepcopy(self.info)
        for at,f in enumerate(old['fixups']):
            for changes in [dict(offset=f.offset+1),dict(segment=2),dict(frame=(0,1)),dict(target=(0,1)),dict(target=(2,0)),dict(width=1),dict(location_type=2),dict(segment_relative=not f.segment_relative),dict(displacement=1)]:
                self.info=copy.deepcopy(old);self.info['fixups'][at]=dataclasses.replace(f,**changes)
                with self.subTest(at=at,changes=changes),self.assertRaises(ValueError):self.validate()
    def test_missing_extra_duplicate_and_out_of_bounds_fields(self):
        old=copy.deepcopy(self.info)
        for mode in ['missing','extra','duplicate','before','after']:
            self.info=copy.deepcopy(old);f=self.info['fixups']
            if mode=='missing':f.pop()
            elif mode=='extra':f.append(f[0])
            elif mode=='duplicate':f[0]=f[1]
            else:f[0]=dataclasses.replace(f[0],offset=self.info['offset']+(-1 if mode=='before'else SIZE))
            with self.subTest(mode=mode),self.assertRaises(ValueError):self.validate()
    def test_CV_source_incomplete_or_excess_output_rejected(self):
        for b in [type(self).linked[:-1],type(self).linked+b'\x90',bytearray(type(self).linked)]:
            self.linked=b
            with self.assertRaises(ValueError):self.validate()

if __name__=='__main__':unittest.main()
