"""Fresh C and independent authentic LINK controls for near-pointer DATA."""
import copy
import dataclasses
import json
from pathlib import Path
import sys
import tempfile
import unittest
PROJECT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT))
from msc import compile_c
from omf import read_omf,Segment,Public
from cdata import extract_data,CDataError
from cdata_pointer import link_pointer_data,CDataPointerError

class CDataPointerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.compiler=compile_c(PROJECT/'src/probes/main_menu_pointer_data.c',['/AS','/Zl','/Zi'],compiler='msc500')
        cls.original=read_omf(cls.compiler.object_bytes)
        cls.experiment=json.loads((PROJECT/'evidence/main-menu-pointer-data-experiment.json').read_text())
        cls.authentic=json.loads((PROJECT/'evidence/menu-pointer-authentic-link-experiment.json').read_text())
    def setUp(self):
        self.obj=copy.deepcopy(type(self).original);self.bindings=copy.deepcopy(self.experiment['externals'])
        self.frame=0x5cc2;self.origin=self.frame*16+0x114a;self.symbol='_main_menus_114a'
    def link(self):return link_pointer_data(self.obj,self.symbol,self.origin,self.frame,self.bindings)
    @property
    def data(self):return self.obj.segments[2]
    def test_complete_fresh20_DATA_public_DGROUP_and_all8_fixups(self):
        b,m=self.link();self.assertEqual(b.hex(),self.experiment['full_data_hex'])
        self.assertEqual(m['boundary'],'complete_omf_pointer_data_segment');self.assertEqual(m['segment']['length'],20)
        self.assertEqual(m['public']['offset'],0);self.assertEqual(len(m['relocations']),8)
        self.assertEqual(m['emitted_mz_sites'],[]);self.assertEqual(m['authored_c_function_count'],0)
        self.assertEqual(m['debug']['validated_debug_fixups'],8);self.assertEqual(len(m['debug']['type_records']),17)
        json.dumps(m) # Metadata must remain a complete JSON-safe provenance object.
    def test_independently_authentic_LINK_both_orders_whole_DATA(self):
        runs=self.authentic['runs'];self.assertEqual([r['object_order']for r in runs],[['MENUDATA','MENUHARN'],['MENUHARN','MENUDATA']])
        for r in runs:
            self.assertEqual(r['linker_sha256'],'124a3c800edc16b60f696d35a9dfec798b68b78fe2ca90c5988ea76bdeab1a8a')
            self.assertTrue(r['whole_DATA_exact_authentic_LINK']);self.assertTrue(r['harness_exit_zero']);self.assertFalse(r['reference_read_or_mounted'])
            self.frame=r['dgroup_frame'];self.origin=r['data_image_offset']
            self.bindings={n:r['publics'][n][1]for n in self.experiment['externals']}
            self.assertTrue(all(r['publics'][n][0]==self.frame for n in self.bindings))
            b,m=self.link();self.assertEqual(b.hex(),r['linked_DATA_hex']);self.assertEqual(len(b),20)
            self.assertEqual(m['emitted_mz_sites'],r['data_mz_sites']);self.assertEqual(m['emitted_mz_sites'],[])
            self.assertEqual(m['dgroup_offset'],r['publics'][self.symbol][1])
    def test_each_DATA_byte_is_preserved_or_relocated_without_masking(self):
        original=copy.deepcopy(self.obj);baseline,_=self.link()
        for at in range(20):
            self.obj=copy.deepcopy(original);b=bytearray(self.data.chunks[0][1]);b[at]^=1;self.data.chunks=[(0,bytes(b))]
            actual,_=self.link();self.assertNotEqual(actual,baseline)
            if at>=16:self.assertEqual(actual[at],baseline[at]^1)
            else:
                field=at//2*2;self.assertEqual((int.from_bytes(actual[field:field+2],'little')-int.from_bytes(baseline[field:field+2],'little'))&65535,1<<(8*(at%2)))
    def test_distinct_origins_addends_displacements_and_explicit_DGROUP_frame(self):
        fs=self.obj.fixups;at=next(i for i,f in enumerate(fs)if f.segment==2 and f.offset==0)
        fs[at]=dataclasses.replace(fs[at],frame=(1,1),displacement=3)
        b=bytearray(self.data.chunks[0][1]);b[:2]=(7).to_bytes(2,'little');self.data.chunks=[(0,bytes(b))]
        self.origin=self.frame*16+0x2222;b,m=self.link()
        self.assertEqual(int.from_bytes(b[:2],'little'),self.bindings['_menu_label_5094']+10)
        self.assertEqual(m['relocations'][0]['image_offset'],self.origin)
        self.assertEqual(m['relocations'][0]['original_addend'],7);self.assertEqual(m['relocations'][0]['displacement'],3)
    def test_frame_origin_and_all_bindings_are_explicit_bounded_no_extra(self):
        original=dict(self.bindings)
        for delta in [{'missing':1},{'extra':1},{'invalid':True},{'overflow':65536},{'mapping':(1,2)},{'startup':1}]:
            self.bindings=dict(original)
            key=next(iter(self.bindings))
            if 'missing'in delta:self.bindings.pop(key)
            elif 'extra'in delta:self.bindings['_other']=1
            elif 'startup'in delta:self.bindings['__acrtused']=0
            else:self.bindings[key]=next(iter(delta.values()))
            with self.subTest(delta=delta),self.assertRaises(CDataPointerError):self.link()
        self.bindings=original
        for frame,origin in [(True,self.origin),(-1,self.origin),(65536,self.origin),(0,-1),(self.frame,self.frame*16-1),(self.frame,self.frame*16+65530),(self.frame,self.frame*16+1)]:
            self.frame,self.origin=frame,origin
            with self.subTest(frame=frame,origin=origin),self.assertRaises(CDataPointerError):self.link()
    def test_external_marker_only_unreferenced_exception(self):
        old=copy.deepcopy(self.obj)
        self.obj.externals[10]='_unreferenced'
        with self.assertRaises(CDataPointerError):self.link()
        self.obj=copy.deepcopy(old);self.obj.externals[10]='__acrtused'
        with self.assertRaises(CDataPointerError):self.link()
        self.obj=copy.deepcopy(old);self.obj.externals[10]=self.obj.externals[2]
        with self.assertRaises(CDataPointerError):self.link()
        self.obj=copy.deepcopy(old);self.obj.externals.pop(1);self.link()
    def test_selected_public_and_all_other_publics_are_normal_DATA(self):
        old=copy.deepcopy(self.obj)
        for change in [{'offset':2},{'segment':1},{'group':0}]:
            self.obj=copy.deepcopy(old);self.obj.publics[self.symbol]=dataclasses.replace(self.obj.publics[self.symbol],**change)
            with self.subTest(change=change),self.assertRaises(CDataPointerError):self.link()
        self.obj=copy.deepcopy(old);self.obj.publics['_foreign']=Public('_foreign',1,0,0,0)
        with self.assertRaises(CDataPointerError):self.link()
        self.obj=copy.deepcopy(old);self.obj.publics['_at_end']=Public('_at_end',2,20,1,0)
        with self.assertRaises(CDataPointerError):self.link()
        self.obj=copy.deepcopy(old);self.obj.publics['_second']=Public('_second',2,16,1,0);self.link()
    def test_SEGDEF_public_alignment_size_and_uninitialized_tail(self):
        old=copy.deepcopy(self.obj)
        for key,value in [('attributes',0x40),('attributes',0x49),('name','OTHER'),('class_name','CODE'),('length',0),('length',65536),('length',22),('unsupported_data',True)]:
            self.obj=copy.deepcopy(old);setattr(self.data,key,value)
            with self.subTest(key=key,value=value),self.assertRaises(CDataPointerError):self.link()
    def test_holes_overlaps_partial_and_other_initialized_allocations(self):
        old=copy.deepcopy(self.obj)
        for chunks in [[(1,bytes(19))],[(0,bytes(18))],[(0,bytes(20)),(0,b'\0')],[(0,b'')],[(0,bytes(21))]]:
            self.obj=copy.deepcopy(old);self.data.chunks=chunks
            with self.subTest(chunks=chunks),self.assertRaises(CDataPointerError):self.link()
        for index in [1,3,4]:
            self.obj=copy.deepcopy(old);self.obj.segments[index].length=1;self.obj.segments[index].chunks=[(0,b'\0')]
            with self.subTest(index=index),self.assertRaises(CDataPointerError):self.link()
    def test_exact_DGROUP_and_no_unsupported_allocation_or_comment_record(self):
        old=copy.deepcopy(self.obj)
        for mode in ['missing','duplicate','member','unknown','communal','lidata','backpatch','comment']:
            self.obj=copy.deepcopy(old)
            if mode=='missing':self.obj.records=[r for r in self.obj.records if r[0]!=0x9a]
            elif mode=='duplicate':self.obj.records.append(next(r for r in self.obj.records if r[0]==0x9a))
            elif mode=='member':self.obj.records=[(t,a,b'\2\xff\2')if t==0x9a else(t,a,p)for t,a,p in self.obj.records]
            elif mode=='unknown':self.obj.records=[(t,a,b'\2\xff\x7f')if t==0x9a else(t,a,p)for t,a,p in self.obj.records]
            else:self.obj.records.append(({'communal':0xb0,'lidata':0xa2,'backpatch':0xb2,'comment':0x88}[mode],9999,b'unknown'))
            with self.subTest(mode=mode),self.assertRaises((CDataPointerError,ValueError)):self.link()
    def test_each_near_DATA_fixup_requires_exact_supported_ownership(self):
        old=copy.deepcopy(self.obj)
        for at,f in enumerate(old.fixups):
            if f.segment!=2:continue
            for change in [{'width':4},{'location_type':2},{'segment_relative':False},{'frame':(0,2)},{'frame':(1,2)},{'target':(0,2)},{'target':(2,999)},{'offset':19},{'offset':-1},{'displacement':-1},{'displacement':65536}]:
                self.obj=copy.deepcopy(old);self.obj.fixups[at]=dataclasses.replace(f,**change)
                with self.subTest(at=at,change=change),self.assertRaises(CDataPointerError):self.link()
        self.obj=copy.deepcopy(old);self.obj.fixups.append(old.fixups[0])
        with self.assertRaises(CDataPointerError):self.link()
    def test_near_pointer_overflow_rejected_without_modulo(self):
        self.bindings['_menu_label_5094']=65535;b=bytearray(self.data.chunks[0][1]);b[:2]=(1).to_bytes(2,'little');self.data.chunks=[(0,bytes(b))]
        with self.assertRaises(CDataPointerError):self.link()
    def test_debug_FIXUPP_not_generic_exception(self):
        old=copy.deepcopy(self.obj)
        for at,f in enumerate(old.fixups):
            if f.segment==2:continue
            for change in [{'width':2},{'location_type':1},{'segment_relative':False},{'frame':(1,1)},{'target':(2,1)},{'offset':f.offset+1},{'segment':6},{'displacement':1}]:
                self.obj=copy.deepcopy(old);self.obj.fixups[at]=dataclasses.replace(f,**change)
                with self.subTest(at=at,change=change),self.assertRaises(CDataPointerError):self.link()
            self.obj=copy.deepcopy(old);self.obj.fixups.pop(at)
            with self.subTest(missing=at),self.assertRaises(CDataPointerError):self.link()
        self.obj=copy.deepcopy(old);self.obj.segments[5].chunks=[(0,self.obj.segments[5].chunks[0][1][24:])];self.obj.segments[5].length-=24
        self.obj.fixups=[dataclasses.replace(f,offset=f.offset-24)if f.segment==5 else f for f in self.obj.fixups if not(f.segment==5 and f.offset==2)]
        with self.assertRaises(CDataPointerError):self.link()
        self.obj=copy.deepcopy(old);self.obj.fixups.append(old.fixups[-1])
        with self.assertRaises(CDataPointerError):self.link()
    def test_debug_records_types_names_and_holes_are_validated(self):
        old=copy.deepcopy(self.obj)
        for segment,at,value in [(5,1,1),(5,0,255),(5,8,1),(5,9,ord('X')),(5,2,1),(5,6,255),(6,0,2),(6,3,255),(6,1,255)]:
            self.obj=copy.deepcopy(old);s=self.obj.segments[segment];b=bytearray(s.chunks[0][1]);b[at]=value;s.chunks=[(0,bytes(b))]
            with self.subTest(segment=segment,at=at),self.assertRaises(CDataPointerError):self.link()
        self.obj=copy.deepcopy(old);self.obj.segments[5].chunks=[(1,self.obj.segments[5].chunks[0][1][1:])]
        with self.assertRaises(CDataPointerError):self.link()
    def test_segment_named_debug_cannot_hide_CODE_or_unowned_symbols(self):
        old=copy.deepcopy(self.obj)
        for change in [('name','$$FAKE'),('class_name','CODE'),('attributes',0x48),('length',193)]:
            self.obj=copy.deepcopy(old);setattr(self.obj.segments[5],*change)
            with self.subTest(change=change),self.assertRaises(CDataPointerError):self.link()
    def test_existing_relocation_free_DATA_policy_remains_strict(self):
        with self.assertRaises(CDataError):extract_data(self.obj,self.symbol)
if __name__=='__main__':unittest.main()
