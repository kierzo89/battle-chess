"""Complete mixed CODE/PUBLIC DATA owner and exact DATA2 extraction gates."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys
import tempfile
import shutil
from unittest import mock
import unittest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
import owned_data16 as p
from omf import Public, Segment, read_omf
from reference import build_reference


def owner_unit():
    return {'language': 'c', 'backend': 'msc500-omf', 'flags': ['/AS', '/Zi'],
            'symbol': '_configure_serial', 'image_offset': '0xdcca', 'size': 24,
            'externals': {'__chkstk': 60586}, 'owned_data': p.serial_descriptor()}


def data_unit(symbol):
    offset = {'_serial_irq': 0, '_serial_base': 2}[symbol]
    return {'language': 'c-data', 'backend': 'msc500-owned-data-omf', 'flags': ['/AS', '/Zi'],
            'symbol': symbol, 'image_offset': hex(0x5fadc + offset), 'size': 2,
            'data_address': {'segment': 0x5cc2, 'offset': 0x2ebc + offset},
            'reference_region': 'exepack-expanded', 'externals': {},
            'rea_evidence': 'evidence/rea-serial-initialized-' + ('irq' if offset == 0 else 'base') + '.json',
            'owned_data': p.serial_descriptor()}


@unittest.skipUnless((PROJECT / 'build/byte-io-serial-initialized/SERINIT.OBJ').exists()
                     and (PROJECT.parent / 'CHESS.EXE').exists(), 'Retained compiler object and original required')
class OwnedPublicDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.obj = read_omf((PROJECT / 'build/byte-io-serial-initialized/SERINIT.OBJ').read_bytes())
        cls.reference = build_reference((PROJECT.parent / 'CHESS.EXE').read_bytes())
        cls.primary = json.loads((PROJECT / p.serial_descriptor()['rea_evidence']).read_text())

    def check(self, obj=None, desc=None, reference=None, project=None):
        unit = owner_unit()
        if desc is not None: unit['owned_data'] = desc
        return p.validate(unit, obj or self.obj, project or PROJECT, reference or self.reference)

    def test_real_complete_allocation_and_two_exact_publics(self):
        before = deepcopy(self.obj)
        owned, data, proof = self.check()
        self.assertEqual(data, bytes.fromhex('0400f803'))
        self.assertEqual(proof['public_extents']['_serial_irq']['bytes_hex'], '0400')
        self.assertEqual(proof['public_extents']['_serial_base']['bytes_hex'], 'f803')
        self.assertEqual(proof['complete_MZ_sites'], [])
        self.assertEqual(proof['source_data_credit'], 0)
        self.assertEqual(self.obj, before)
        self.assertEqual([(x['object_offset'], x['original_addend']) for x in proof['code_references']],
                         [(330, 2), (336, 0)])

    def test_descriptor_negative_cases(self):
        changes = [('segment', 3), ('group', True), ('size', 2), ('image_offset', '0x5fade'),
                   ('owner_symbol', '_available_bytes_dc91'), ('rea_evidence', '../outside.json'),
                   ('data_address', {'segment': 0x5cc2, 'offset': 0x2ebe}),
                   ('publics', {'_serial_irq': {'offset': 0, 'size': 4}})]
        for key, value in changes:
            desc = p.serial_descriptor(); desc[key] = value
            with self.subTest(key=key), self.assertRaises(p.OwnedDataError): self.check(desc=desc)
        desc = p.serial_descriptor();desc['extra'] = True
        with self.assertRaises(p.OwnedDataError):self.check(desc=desc)

    def test_data_shape_negative_cases(self):
        for mutation in (lambda s: setattr(s, 'length', 6),
                         lambda s: setattr(s, 'attributes', 0x28),
                         lambda s: setattr(s, 'class_name', 'CONST'),
                         lambda s: setattr(s, 'unsupported_data', True),
                         lambda s: setattr(s, 'chunks', [(1, b'\x00\xf8\x03')]),
                         lambda s: setattr(s, 'chunks', [(0, b'\x04\x00')]),
                         lambda s: setattr(s, 'chunks', [(0, b'\x04\x00'), (1, b'\x00\xf8\x03')]),
                         lambda s: setattr(s, 'chunks', [(0, b'\x05\x00\xf8\x03')])):
            obj = deepcopy(self.obj);mutation(obj.segments[2])
            with self.subTest(mutation=mutation), self.assertRaises(p.OwnedDataError): self.check(obj=obj)

    def test_public_negative_cases(self):
        for change in ({'offset': 1}, {'group': 0}, {'type_index': 0x80}, {'segment': 3}):
            obj=deepcopy(self.obj);obj.publics['_serial_irq']=replace(obj.publics['_serial_irq'], **change)
            with self.subTest(change=change), self.assertRaises(p.OwnedDataError): self.check(obj=obj)
        obj=deepcopy(self.obj);del obj.publics['_serial_base']
        with self.assertRaises(p.OwnedDataError):self.check(obj=obj)
        obj=deepcopy(self.obj);obj.publics['_alias']=Public('_alias',2,0,1,0x81)
        with self.assertRaises(p.OwnedDataError):self.check(obj=obj)

    def test_each_CODE_public_must_be_ungrouped(self):
        for name, public in self.obj.publics.items():
            if public.segment != 1:
                continue
            obj = deepcopy(self.obj)
            obj.publics[name] = replace(public, group=1)
            with self.subTest(symbol=name), self.assertRaises(p.OwnedDataError):
                self.check(obj=obj)

    def test_group_negative_cases(self):
        payloads=(b'\x02\xff\x03\xff\x04', # missing DATA
                  b'\x02\xff\x03\xff\x04\xff\x02\xff\x02', # repeated
                  b'\x02\xff\x01\xff\x02\xff\x03', # CODE included
                  b'\x03\xff\x03\xff\x04\xff\x02', # not DGROUP
                  b'\x02\x00\x02', b'\x02\xff\x7f')
        for payload in payloads:
            obj=deepcopy(self.obj);obj.records=[(k,o,payload if k==0x9a else raw) for k,o,raw in obj.records]
            with self.subTest(payload=payload), self.assertRaises(p.OwnedDataError):self.check(obj=obj)
        obj=deepcopy(self.obj);obj.records += [(0x9a,99999,b'\x02\xff\x02')]
        with self.assertRaises(p.OwnedDataError):self.check(obj=obj)

    def test_owner_allocation_and_extra_data_negative_cases(self):
        for mutation in (lambda obj: obj.procedures['_configure_serial'].update(length=22),
                         lambda obj: setattr(obj.segments[1], 'length', 346),
                         lambda obj: setattr(obj.segments[4], 'length', 2),
                         lambda obj: obj.segments.update({7: Segment(7,2,0,0,0,0x48,
                                           [(0,b'\x00\x00')],name='_MORE',class_name='DATA')}),
                         lambda obj: obj.records.append((0xb0,99999,b'')),
                         lambda obj: obj.records.append((0xa2,99999,b''))):
            obj=deepcopy(self.obj);mutation(obj)
            with self.subTest(mutation=mutation),self.assertRaises(p.OwnedDataError):self.check(obj=obj)

    def test_internal_field_negative_cases(self):
        index=next(i for i,f in enumerate(self.obj.fixups) if f.segment==1 and f.offset==330)
        for change in ({'offset': 329}, {'width': 4}, {'location_type': 2}, {'segment_relative': False},
                       {'frame': (5,None)}, {'target': (0,3)}, {'displacement': 1}):
            obj=deepcopy(self.obj);obj.fixups[index]=replace(obj.fixups[index],**change)
            with self.subTest(change=change),self.assertRaises(p.OwnedDataError):self.check(obj=obj)
        obj=deepcopy(self.obj);del obj.fixups[index]
        with self.assertRaises(p.OwnedDataError):self.check(obj=obj)
        obj=deepcopy(self.obj);obj.fixups.append(obj.fixups[index])
        with self.assertRaises(p.OwnedDataError):self.check(obj=obj)
        obj=deepcopy(self.obj);obj.fixups.append(replace(obj.fixups[index],segment=2,offset=0))
        with self.assertRaises(p.OwnedDataError):self.check(obj=obj)
        for raw_addend in (1,3,4):
            obj=deepcopy(self.obj)
            for j,(off,data) in enumerate(obj.segments[1].chunks):
                if off<=330 and 332<=off+len(data):
                    data=bytearray(data);data[330-off:332-off]=raw_addend.to_bytes(2,'little')
                    obj.segments[1].chunks[j]=(off,bytes(data));break
            with self.subTest(addend=raw_addend),self.assertRaises(p.OwnedDataError):self.check(obj=obj)

    def test_primary_and_reference_negative_cases(self):
        for mutate in (lambda e:e['parameters'].update(length=2),
                       lambda e:e['normalized_result'].update(complete=False),
                       lambda e:e['normalized_result'].update(bytes_hex='0400'),
                       lambda e:e['normalized_result'].update(address='0x6fade'),
                       lambda e:e['subject']['digest'].update(sha256='0'*64),
                       lambda e:e['analysis_profile']['parameters'].update(load_segment='0x2000')):
            evidence=deepcopy(self.primary);mutate(evidence)
            with tempfile.TemporaryDirectory() as temp:
                root=Path(temp);(root/'evidence').mkdir()
                (root/p.serial_descriptor()['rea_evidence']).write_text(json.dumps(evidence))
                with self.subTest(mutate=mutate),self.assertRaises(p.OwnedDataError):self.check(project=root)
        for change in ({'original_sha256':'0'*64}, {'carrier_sha256':'0'*64},
                       {'relocations':tuple(self.reference['relocations'])+(0x5fadc,)},
                       {'image': self.reference['image'][:0x5fadc]+b'\x05'+self.reference['image'][0x5fadd:]}):
            reference=dict(self.reference,**change)
            with self.subTest(change=list(change)),self.assertRaises(p.OwnedDataError):self.check(reference=reference)


    def test_pure_layout_has_no_target_or_filesystem_reads(self):
        with mock.patch.object(Path, 'read_bytes', side_effect=AssertionError('filesystem access')):
            data, proof = p.validate_layout(self.obj, p.serial_descriptor())
        self.assertEqual(data, b'\x04\x00\xf8\x03')
        self.assertNotIn('original_sha256', proof)
        self.assertEqual(proof['whole_CODE_CV_union_size'], 344)

    def test_unit_language_backend_flags_and_code_owner_metadata(self):
        alternatives = [{'language': 'runtime'}, {'language': 'c-data'}, {'backend': 'msc510-omf'},
                        {'flags': ['/AS', '/Zl', '/Zi']}, {'flags': ['/AS']},
                        {'symbol': '_available_bytes_dc91'}, {'size': 22}, {'size': True},
                        {'image_offset': '0xdccb'}, {'image_offset': 0xdcca},
                        {'externals': {'_serial_irq': 0x2ebc}}]
        for changes in alternatives:
            with self.subTest(changes=changes),self.assertRaises(p.OwnedDataError):
                p.validate(dict(owner_unit(), **changes), self.obj, PROJECT, self.reference)
        with self.assertRaises(p.OwnedDataError):p.extract_public(owner_unit(),self.obj,PROJECT,self.reference)
        for ref in (None, {}, {'image': b''}):
            with self.assertRaises(p.OwnedDataError):p.validate(owner_unit(),self.obj,PROJECT,ref)

    def test_both_publics_require_full_owner_and_own_exact_primary(self):
        for symbol, expected in (('_serial_irq', b'\x04\x00'), ('_serial_base', b'\xf8\x03')):
            unit=data_unit(symbol);before=deepcopy(self.obj)
            data,info=p.extract_public(unit,self.obj,PROJECT,self.reference)
            self.assertEqual(data,expected)
            self.assertEqual(info['boundary'],'complete_owned_public_int16')
            self.assertEqual(info['owned_data_proof']['size'],4)
            self.assertEqual(info['public']['offset'],0 if symbol=='_serial_irq' else 2)
            self.assertEqual(info['authored_c_function_count'],0)
            self.assertEqual(self.obj,before)
            for which in ('whole','child'):
                with tempfile.TemporaryDirectory() as temp:
                    root=Path(temp);(root/'evidence').mkdir()
                    whole=p.serial_descriptor()['rea_evidence'];child=unit['rea_evidence']
                    for relative in (whole,child):
                        e=json.loads((PROJECT/relative).read_text())
                        if relative == (whole if which=='whole' else child):
                            e['normalized_result']['complete']=False
                        (root/relative).write_text(json.dumps(e))
                    with self.subTest(symbol=symbol,which=which),self.assertRaises(p.OwnedDataError):
                        p.extract_public(unit,self.obj,root,self.reference)

    def test_public_metadata_cannot_borrow_neighbor_or_whole_owner_extent(self):
        alternatives=[{'backend':'msc500-data-omf'}, {'flags':['/AS','/Zl','/Zi']},
                      {'symbol':'_missing'}, {'symbol':'_serial_base'}, {'size':4}, {'size':True},
                      {'image_offset':'0x5fade'}, {'image_offset':0x5fadc},
                      {'reference_region':'packed'}, {'data_address':{'segment':0x5cc2,'offset':0x2ebe}},
                      {'data_address':None}, {'rea_evidence':'evidence/rea-serial-initialized-base.json'},
                      {'rea_evidence':p.serial_descriptor()['rea_evidence']}, {'externals':{'_time':1}}]
        for changes in alternatives:
            with self.subTest(changes=changes),self.assertRaises(p.OwnedDataError):
                p.extract_public(dict(data_unit('_serial_irq'),**changes),self.obj,PROJECT,self.reference)

    def test_link_default_rejects_owned_fields_and_optin_preserves_full_CODE344(self):
        from link16 import link_function, LinkError
        proposed=json.loads((PROJECT/'build/byte-io-serial-initialized/source-context-proposal.json').read_text())
        owner=next(u for u in proposed['units'] if u['symbol']=='_configure_serial')
        with self.assertRaises(LinkError):
            link_function(self.obj,owner['symbol'],int(owner['image_offset'],0),owner['externals'])
        before=deepcopy(self.obj);whole=bytearray();logs=[]
        raw_code=p.complete_bytes(self.obj.segments[1])
        for unit in proposed['units']:
            origin=int(unit['image_offset'],0)
            opts={'owned_data':p.serial_descriptor()} if unit['symbol']=='_configure_serial' else {}
            with mock.patch.object(Path,'read_bytes',side_effect=AssertionError('linker read target/filesystem')):
                linked,log=link_function(self.obj,unit['symbol'],origin,unit['externals'],**opts)
            self.assertEqual(linked,self.reference['image'][origin:origin+unit['size']])
            info=self.obj.function_info(unit['symbol'])
            self.assertEqual(len(linked),info['size'])
            self.assertEqual(len(log),len(info['fixups']))
            for emitted in log:
                f=next(f for f in info['fixups'] if f.offset==emitted['object_offset'])
                self.assertEqual(emitted['raw_fixupp'],f.raw.hex())
                self.assertEqual(emitted['width'],f.width)
                self.assertEqual(emitted['original_addend'],int.from_bytes(raw_code[f.offset:f.offset+2],'little'))
                self.assertEqual(emitted['image_offset'],origin+f.offset-info['offset'])
            whole.extend(linked);logs.extend(log)
        self.assertEqual(bytes(whole),self.reference['image'][0xdb8a:0xdce2])
        self.assertEqual(len(whole),344)
        mz={x['mz_segment_relocation_image_offset'] for x in logs if 'mz_segment_relocation_image_offset' in x}
        self.assertEqual(mz,{x for x in self.reference['relocations'] if 0xdb8a<=x<0xdce2})
        owned=[x for x in logs if x['object_offset'] in (330,336)]
        self.assertEqual([(x['object_offset'],x['original_addend'],x['encoded_value']) for x in owned],
                         [(330,2,0x2ebe),(336,0,0x2ebc)])
        self.assertEqual([x['owned_data_public'] for x in owned],['_serial_base','_serial_irq'])
        self.assertTrue(all(x['target_symbol'] is None for x in owned))
        self.assertTrue(all('mz_segment_relocation_image_offset' not in x for x in owned))
        self.assertEqual(self.obj,before)

    def test_link_optin_rejects_malformed_owner_descriptor(self):
        from link16 import link_function, LinkError
        for changes in ({'size':2},{'group':True},{'segment':3},{'extra':True},
                        {'publics':{'_serial_irq':{'offset':0,'size':4}}}):
            desc=dict(p.serial_descriptor(),**changes)
            with self.subTest(changes=changes),self.assertRaises(LinkError):
                link_function(self.obj,'_configure_serial',0xdcca,{'__chkstk':60586},owned_data=desc)

    @unittest.skipUnless(shutil.which('dosbox') and (PROJECT/'toolchains/msc500/CL.EXE').exists(),
                         'Pinned Microsoft C5 and DOSBox required')
    def test_fresh_genuine_source_accepted_without_filename_or_object_hash_assumption(self):
        from msc import compile_c
        source=PROJECT/'src/byte_io_serial_match.c'
        compiled=compile_c(source,['/AS','/Zi'],compiler='msc500')
        obj=read_omf(compiled.object_bytes);before=deepcopy(obj)
        desc,data,proof=p.validate(owner_unit(),obj,PROJECT,self.reference)
        self.assertEqual(data,b'\x04\x00\xf8\x03')
        self.assertEqual(proof['owner']['offset'],320)
        self.assertEqual(proof['owner']['size'],24)
        for symbol in ('_serial_irq','_serial_base'):
            self.assertEqual(len(p.extract_public(data_unit(symbol),obj,PROJECT,self.reference)[0]),2)
        self.assertEqual(obj,before)

if __name__=='__main__': unittest.main()
