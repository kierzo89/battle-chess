"""Narrow private-BSS ownership gates; no initialized-zero matching credit."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
M=next(p for p in Path(__file__).resolve().parents if(p/'config/units.json').is_file());sys.path.insert(0,str(M))
import owned_bss16 as p
from omf import read_omf,Public
from reference import build_reference
from msc import compile_c
from link16 import link_function,LinkError


def unit():
    # Fixed probe/object fixtures use their exact pre-coherence external map.
    units=json.loads((Path(__file__).resolve().parent/'fixtures/selection_private_bss_legacy_251.json').read_text())['units']
    u=deepcopy(next(u for u in units if u.get('symbol')=='_board_pointer_0daf'))
    u['owned_bss']=p.selection_descriptor()
    for name in p.selection_descriptor()['scalars']:u['externals'].pop(name,None)
    return u


class OwnedBSSTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.obj=read_omf((M/'build/selection-static/xor-first.OBJ').read_bytes())
        cls.ref=build_reference((M.parent/'CHESS.EXE').read_bytes())

    def check(self,obj=None,desc=None,reference=None,project=M):
        u=unit()
        if desc is not None:u['owned_bss']=desc
        return p.validate(u,self.obj if obj is None else obj,project,
                          self.ref if reference is None else reference)

    def test_real_complete_BSS_CODE_CV_fields_and_no_mutations(self):
        before=deepcopy(self.obj)
        desc,proof=self.check()
        self.assertEqual(desc,p.selection_descriptor())
        self.assertEqual(proof['size'],4)
        self.assertEqual(proof['BSS_initialized_bytes'],0)
        self.assertEqual(proof['BSS_byte_credit'],0)
        self.assertFalse(proof['zero_bytes_compared_or_generated'])
        self.assertEqual(proof['whole_CODE_CV_union_size'],578)
        self.assertEqual([(f['function_offset'],f['original_addend'])for f in proof['code_references']],list(p.FIELD_ADDENDS))
        self.assertEqual(proof['original_CRT_zero_range_exclusive'],[0x52cc,0xcbe0])
        self.assertEqual(self.obj,before)

    def test_both_bounded_declaration_orders_have_same_layout(self):
        other=read_omf((M/'build/selection-static/colour-first.OBJ').read_bytes())
        a=p.validate_layout(self.obj,p.selection_descriptor())
        b=p.validate_layout(other,p.selection_descriptor())
        self.assertEqual(a['whole_CODE_sha256'],b['whole_CODE_sha256'])
        self.assertEqual(a['code_references'],b['code_references'])
        self.assertEqual({k:v['offset']for k,v in b['private_scalar_debug_metadata'].items()},
                         {'selection_xor_52cc':0,'selection_colour_52ce':2})

    def test_pure_gate_performs_no_target_or_filesystem_read(self):
        with mock.patch.object(Path,'read_bytes',side_effect=AssertionError('read forbidden')):
            proof=p.validate_layout(self.obj,p.selection_descriptor())
        self.assertEqual(proof['BSS_initialized_bytes'],0)

    def test_descriptor_mutations(self):
        for key,value in [('size',2),('segment',3),('group',True),('image_offset','0x61eee'),
            ('data_address',{'segment':0x5cc2,'offset':0x52ce}),
            ('owner_symbol','_error_message'),('rea_evidence','../outside'),
            ('scalars',{'_selection_xor_52cc':{'offset':0,'size':4}}),('extra',0)]:
            d=p.selection_descriptor();d[key]=value
            with self.subTest(key=key),self.assertRaises(p.OwnedBSSError):self.check(desc=d)

    def test_uninitialized_BSS_and_no_other_allocations(self):
        for index,key,value in [(4,'length',6),(4,'chunks',[(0,b'\0'*4)]),
            (4,'chunks',[(4,b'')]),(4,'attributes',0x28),(4,'unsupported_data',True),
            (2,'length',2),(3,'length',2),(2,'chunks',[(0,b'\0\0')]),(4,'class_name','DATA')]:
            o=deepcopy(self.obj);setattr(o.segments[index],key,value)
            with self.subTest(index=index,key=key,value=value),self.assertRaises(p.OwnedBSSError):self.check(obj=o)
        for kind in(0xa2,0xa3,0xb0,0xb8):
            o=deepcopy(self.obj);o.records.append((kind,0,b''))
            with self.subTest(kind=kind),self.assertRaises(p.OwnedBSSError):self.check(obj=o)

    def test_COMPLETE_CODE_and_public_CV_union(self):
        for change in [('length',580),('chunks',[(1,b'\0'*577)]),('unsupported_data',True)]:
            o=deepcopy(self.obj);setattr(o.segments[1],*change)
            with self.subTest(change=change),self.assertRaises(p.OwnedBSSError):self.check(obj=o)
        for name in p.CODE_PROCEDURES:
            o=deepcopy(self.obj);o.publics[name]=replace(o.publics[name],group=1)
            with self.subTest(name=name),self.assertRaises(p.OwnedBSSError):self.check(obj=o)
            o=deepcopy(self.obj);o.procedures[name]['length']-=1
            with self.subTest(name=name,CV=True),self.assertRaises(p.OwnedBSSError):self.check(obj=o)

    def test_no_scalar_external_or_public_aliases(self):
        for name in p.selection_descriptor()['scalars']:
            o=deepcopy(self.obj);o.externals[max(o.externals)+1]=name
            with self.subTest(name=name),self.assertRaises(p.OwnedBSSError):self.check(obj=o)
            o=deepcopy(self.obj);o.publics[name]=Public(name,4,0,1,0x85)
            with self.subTest(name=name,public=True),self.assertRaises(p.OwnedBSSError):self.check(obj=o)

    def test_group_membership_and_duplicate_rejection(self):
        for payload in [None,b'\x01\xff\x02\xff\x03',b'\x01\xff\x03\xff\x04\xff\x04',
                        b'\x01\xff\x02\xff\x03\xff\x04']:
            o=deepcopy(self.obj);o.records=[r for r in o.records if r[0]!=0x9a]
            if payload is not None:o.records.append((0x9a,0,payload))
            with self.subTest(payload=payload),self.assertRaises(p.OwnedBSSError):self.check(obj=o)

    def test_each_owned_field_shape_missing_extra_overlap(self):
        indices=[i for i,f in enumerate(self.obj.fixups)if f.segment==1 and f.target==(0,4)]
        for i in indices:
            for values in [dict(width=4),dict(location_type=5),dict(segment_relative=False),
                           dict(frame=(5,None)),dict(target=(0,3)),dict(displacement=2),dict(offset=0)]:
                o=deepcopy(self.obj);o.fixups[i]=replace(o.fixups[i],**values)
                with self.subTest(index=i,values=values),self.assertRaises(p.OwnedBSSError):self.check(obj=o)
        o=deepcopy(self.obj);del o.fixups[indices[0]]
        with self.assertRaises(p.OwnedBSSError):self.check(obj=o)
        o=deepcopy(self.obj);o.fixups.append(o.fixups[indices[0]])
        with self.assertRaises(p.OwnedBSSError):self.check(obj=o)
        o=deepcopy(self.obj);o.fixups.append(replace(o.fixups[indices[0]],segment=4,offset=0))
        with self.assertRaises(p.OwnedBSSError):self.check(obj=o)

    def test_each_owned_addend_rejects_interior_and_wrong_scalar(self):
        for f in self.obj.fixups:
            if f.segment!=1 or f.target!=(0,4):continue
            for value in [1,4]:
                o=deepcopy(self.obj)
                for i,(at,raw) in enumerate(o.segments[1].chunks):
                    if at<=f.offset and f.offset+2<=at+len(raw):
                        b=bytearray(raw);b[f.offset-at:f.offset-at+2]=value.to_bytes(2,'little')
                        o.segments[1].chunks[i]=(at,bytes(b));break
                with self.subTest(field=f.offset,value=value),self.assertRaises(p.OwnedBSSError):self.check(obj=o)

    def test_static_debug_symbols_types_offsets_and_fixups(self):
        for name in ['selection_xor_52cc','selection_colour_52ce']:
            for replacement in ['x'+name[1:],name]:
                o=deepcopy(self.obj)
                for i,(at,raw)in enumerate(o.segments[5].chunks):
                    index=raw.find(name.encode())
                    if index>=0:
                        b=bytearray(raw)
                        if replacement!=name:b[index:index+len(name)]=replacement.encode()
                        else:b[index-3:index-1]=b'\x81\x00'
                        o.segments[5].chunks[i]=(at,bytes(b));break
                with self.subTest(name=name,replacement=replacement),self.assertRaises(p.OwnedBSSError):self.check(obj=o)
        o=deepcopy(self.obj);o.fixups=[f for f in o.fixups if not(f.segment==5 and f.target==(0,4))]
        with self.assertRaises(p.OwnedBSSError):self.check(obj=o)

    def test_unit_flags_identity_and_external_alias_gate(self):
        for key,value in [('flags',['/AS','/Gs','/Zi']),('symbol','_error_message'),
            ('language','c-data'),('backend','msc500-data-omf'),('size',512),('image_offset','0xdb0'),
            ('code_address',{'segment':0,'offset':0xdaf}),('owned_const',{}),('owned_data',{}),
            ('extended_extent',{}),('extended_extent',{'kind':'other'})]:
            u=unit();u[key]=value
            with self.subTest(key=key),self.assertRaises(p.OwnedBSSError):p.validate(u,self.obj,M,self.ref)
        u=unit();u['externals']['_selection_xor_52cc']=0x52cc
        with self.assertRaises(p.OwnedBSSError):p.validate(u,self.obj,M,self.ref)
        self.assertEqual(p.validate_unit_metadata(unit()),p.selection_descriptor())
        for bad in(None,[],{'owned_bss':p.selection_descriptor()}):
            with self.subTest(bad=bad),self.assertRaises(p.OwnedBSSError):p.validate_unit_metadata(bad)

    def test_context_CRT_primary_and_zero_bounds_not_fake_data(self):
        for key,value in [('original_sha256','0'*64),('carrier_sha256','0'*64),('image',b''),('relocations',())]:
            r=dict(self.ref);r[key]=value
            with self.subTest(key=key),self.assertRaises(p.OwnedBSSError):self.check(reference=r)
        for change in ['bounds','profile','subject','length','bytes']:
            with tempfile.TemporaryDirectory()as tmp:
                root=Path(tmp);d=root/'evidence';d.mkdir()
                e=json.loads((M/p.selection_descriptor()['rea_evidence']).read_text())
                if change=='bounds':e['normalized_result']['bytes_hex']=e['normalized_result']['bytes_hex'].replace('bfcc52','bfce52')
                if change=='profile':e['analysis_profile']['parameters']['load_segment']='0x2000'
                if change=='subject':e['subject']['digest']['sha256']='0'*64
                if change=='length':e['normalized_result']['returned_bytes']=178
                if change=='bytes':e['normalized_result']['bytes_hex']='00'*179
                (root/p.selection_descriptor()['rea_evidence']).write_text(json.dumps(e))
                with self.subTest(change=change),self.assertRaises(p.OwnedBSSError):self.check(project=root)

    def test_fresh_genuine_C5_compile_passes_structural_and_native_gates(self):
        r=compile_c(M/'src/probes/selection-static/xor-first.c',['/AS','/Zi'],compiler='msc500')
        o=read_omf(r.object_bytes)
        _,proof=self.check(obj=o)
        self.assertEqual(proof['size'],4)
        self.assertEqual(r.object_bytes,(M/'build/selection-static/xor-first.OBJ').read_bytes())

    def test_authentic_LINK_two_order_complete_field_execution_evidence(self):
        e=json.loads((M/'evidence/selection-static-control.json').read_text())
        self.assertEqual(len(e['authentic_target_free_trials']),2)
        for trial in e['authentic_target_free_trials']:
            self.assertTrue(trial['executed_successfully'])
            self.assertTrue(trial['private_BSS_precedes_COMMON'])
            self.assertEqual(trial['private_BSS']['size'],4)
            self.assertFalse(trial['original_read_or_mounted'])
        for case in e['native_source_comparisons']:
            self.assertEqual(case['complete_CODE_bytes'],578)
            self.assertEqual(case['complete_MZ_sites'],[0xf35,0xf64])

    def test_optional_linker_owner_matches_full513_and_exact_MZ(self):
        u=unit()
        with self.assertRaises(LinkError):
            link_function(self.obj,u['symbol'],0xdaf,u['externals'])
        body,fields=link_function(self.obj,u['symbol'],0xdaf,u['externals'],
                                  owned_bss=p.selection_descriptor())
        self.assertEqual(len(body),513)
        self.assertEqual(body,self.ref['image'][0xdaf:0xfb0])
        owned=[f for f in fields if f['mode']=='segment_relative_owned_bss']
        self.assertEqual(len(owned),13)
        self.assertEqual(sorted(f['mz_segment_relocation_image_offset']for f in fields
                         if 'mz_segment_relocation_image_offset'in f),[0xf35,0xf64])
        self.assertEqual({f['owned_bss_scalar']for f in owned},
                         {'_selection_xor_52cc','_selection_colour_52ce'})

    def test_optional_linker_rejects_other_owner_and_combined_storage(self):
        u=unit()
        for kwargs in [dict(owned_bss=p.selection_descriptor(),owned_const={}),
                       dict(owned_bss=p.selection_descriptor(),owned_data={})]:
            with self.subTest(kwargs=kwargs),self.assertRaises(LinkError):
                link_function(self.obj,u['symbol'],0xdaf,u['externals'],**kwargs)
        with self.assertRaises(LinkError):
            link_function(self.obj,'_error_message',0xd8d,u['externals'],
                          owned_bss=p.selection_descriptor())

    def test_whole_three_procedures_all65_fields_and_four_DOS_load_bases(self):
        units=[u for u in json.loads((Path(__file__).resolve().parent/'fixtures/selection_private_bss_legacy_251.json').read_text())['units']
               if u.get('symbol')in p.CODE_PROCEDURES]
        self.assertEqual(len(units),3)
        units.sort(key=lambda u:int(u['image_offset'],0))
        full=bytearray();fields=[]
        with mock.patch.object(Path,'read_bytes',side_effect=AssertionError('linker must be pure')):
            for u in units:
                ext=dict(u['externals'])
                kwargs={}
                if u['symbol']=='_board_pointer_0daf':
                    for name in p.selection_descriptor()['scalars']:ext.pop(name,None)
                    kwargs['owned_bss']=p.selection_descriptor()
                b,logs=link_function(self.obj,u['symbol'],int(u['image_offset'],0),ext,**kwargs)
                full.extend(b);fields.extend(logs)
        original=self.ref['image'][0xd6e:0xfb0]
        self.assertEqual(bytes(full),original);self.assertEqual(len(full),578)
        self.assertEqual(len(fields),65)
        owned=[f for f in fields if f['mode']=='segment_relative_owned_bss']
        self.assertEqual(len(owned),13)
        self.assertTrue(all(f['target_symbol']is None for f in owned))
        self.assertEqual({f['owned_bss_scalar']for f in owned},set(p.selection_descriptor()['scalars']))
        sites=sorted(f['mz_segment_relocation_image_offset']for f in fields
                     if 'mz_segment_relocation_image_offset'in f)
        self.assertEqual(sites,[0xf35,0xf64])
        self.assertEqual(sites,sorted(n for n in self.ref['relocations']if 0xd6e<=n<0xfb0))
        for load in(0,1,0x1000,0xffff):
            emitted=bytearray(full);observed=bytearray(original)
            for site in sites:
                at=site-0xd6e
                for b in(emitted,observed):
                    value=int.from_bytes(b[at:at+2],'little')
                    b[at:at+2]=((value+load)&0xffff).to_bytes(2,'little')
            with self.subTest(load=load):
                self.assertEqual(emitted,observed)
                for f in owned:
                    at=f['image_offset']-0xd6e
                    self.assertEqual(emitted[at:at+2],full[at:at+2])

    def test_production_fresh_build_unit_matches_full_owner_zero_BSS_credit(self):
        import check
        u=unit();u['source']='src/probes/selection-static/xor-first.c'
        with tempfile.TemporaryDirectory()as tmp:
            result=check.build_unit(u,self.ref['image'],M,'nasm',c_cache={},
                                    output=Path(tmp),reference=self.ref)
        self.assertEqual(result['status'],'c_matched',result.get('error'))
        self.assertEqual(result['owned_bss_additional_credit'],0)
        self.assertEqual(result['owned_bss_proof']['BSS_byte_credit'],0)
        self.assertEqual(result['emitted_procedure']['size'],513)
        self.assertEqual(len(result['relocations']),60)
        # Independently retain fresh coverage of the current coherent owner source.
        current=deepcopy(next(u for u in json.loads((M/'config/units.json').read_text())
                              if u.get('symbol')=='_board_pointer_0daf'))
        self.assertIn('_graphics_begin',current['externals'])
        self.assertIn('_graphics_end',current['externals'])
        self.assertNotIn('_input_select_11ef_001e',current['externals'])
        self.assertNotIn('_input_init_11ef_0000',current['externals'])
        with tempfile.TemporaryDirectory()as tmp:
            fresh=check.build_unit(current,self.ref['image'],M,'nasm',c_cache={},
                                   output=Path(tmp),reference=self.ref)
        self.assertEqual(fresh['status'],'c_matched',fresh.get('error'))
        self.assertEqual(fresh['owned_bss_additional_credit'],0)
        self.assertEqual(fresh['owned_bss_proof']['BSS_byte_credit'],0)
        self.assertEqual(fresh['emitted_procedure']['size'],513)
        self.assertEqual(len(fresh['relocations']),60)


if __name__=='__main__':unittest.main()
