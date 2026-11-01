"""Whole owned CONST gates and genuine D9C6 code/field preservation."""
import copy
import dataclasses
import hashlib
import json
from pathlib import Path
import shutil
import sys
import unittest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from owned_const16 import validate, OwnedConstError
from omf import read_omf, Public
from reference import build_reference
from link16 import link_function, LinkError


def descriptor():
    return {'segment': 3, 'group': 1, 'size': 24, 'image_offset': '0x61dbb',
            'data_address': {'segment': 0x5cc2, 'offset': 0x519b},
            'rea_evidence': 'evidence/rea-dialog-label-full24.json'}


def fixture_unit():
    proposal = json.loads((PROJECT / 'build/dialog-label-data/consumer-proposed-unit.json').read_text())
    return dict(proposal['unit'], owned_const=descriptor())


@unittest.skipUnless((PROJECT / 'build/dialog-label-data/literal-consumer-GsOs.obj').exists()
                     and (PROJECT.parent / 'CHESS.EXE').exists(), 'Retained independent C object and pinned original required')
class OwnershipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = (PROJECT / 'build/dialog-label-data/literal-consumer-GsOs.obj').read_bytes()
        cls.obj = read_omf(cls.raw)
        cls.unit = fixture_unit()
        cls.context = build_reference((PROJECT.parent / 'CHESS.EXE').read_bytes())

    def test_complete_original_24bytes_all_fields_and_object_stay_unchanged(self):
        obj, unit = copy.deepcopy(self.obj), copy.deepcopy(self.unit)
        before, original_unit = copy.deepcopy(obj), copy.deepcopy(unit)
        owned, data, proof = validate(unit, obj, PROJECT, self.context)
        self.assertEqual(owned, descriptor())
        self.assertEqual(data, b'Cancel\0Done\0Cancel\0Done\0')
        self.assertEqual(len(data), 24)
        self.assertEqual(data, self.context['image'][0x61dbb:0x61dd3])
        self.assertEqual(proof['size'], 24)
        self.assertEqual(proof['complete_MZ_sites'], [])
        self.assertEqual([(f['object_offset'], f['original_addend']) for f in proof['code_references']],
                         [(97, 0), (142, 7), (248, 12), (321, 19)])
        self.assertEqual(proof['source_data_credit'], 0)
        self.assertTrue(proof['requires_enclosing_CONST_alignment_context'])
        self.assertFalse(proof['standalone_source_link_layout_proved'])
        self.assertEqual(proof['owner_CODE_bytes_outside_procedure'], 1)
        self.assertFalse(proof['omf_records_or_fields_modified'])
        self.assertEqual(obj, before)
        self.assertEqual(unit, original_unit)

    def test_descriptor_missing_extra_boolean_wrong_index_size_or_backend_fails(self):
        alternatives = [None, {}, dict(descriptor(), extra=True), dict(descriptor(), segment=True),
                        dict(descriptor(), group=False), dict(descriptor(), size=23),
                        dict(descriptor(), segment=1), dict(descriptor(), group=2),
                        dict(descriptor(), image_offset=0x61dbb)]
        for d in alternatives:
            with self.subTest(descriptor=d), self.assertRaises(OwnedConstError):
                validate(dict(self.unit, owned_const=d), self.obj, PROJECT, self.context)
        for changes in [{'language': 'runtime'}, {'backend': 'msc510-omf'}, {'size': 374}, {'symbol': '_missing'}]:
            with self.subTest(changes=changes), self.assertRaises(OwnedConstError):
                validate(dict(self.unit, **changes), self.obj, PROJECT, self.context)
        with self.assertRaises(OwnedConstError):
            validate(self.unit, self.obj, PROJECT, None)

    def test_full_const_holes_overlaps_reserved_tail_and_attributes_fail(self):
        for change in ['hole', 'overlap', 'tail', 'size', 'attributes', 'iterated', 'identity']:
            obj = copy.deepcopy(self.obj); c = obj.segments[3]; data = c.chunks[0][1]
            if change == 'hole': c.chunks = [(1, data[1:])]
            elif change == 'overlap': c.chunks = [(0, data), (23, data[-1:])]
            elif change == 'tail': c.chunks = [(0, data[:-1])]
            elif change == 'size': c.length = 23
            elif change == 'attributes': c.attributes = 0x58
            elif change == 'iterated': c.unsupported_data = True
            elif change == 'identity': c.class_name = 'DATA'
            with self.subTest(change=change), self.assertRaises(OwnedConstError):
                validate(self.unit, obj, PROJECT, self.context)

    def test_const_public_fixup_extra_allocations_and_communals_fail(self):
        for change in ['public', 'fixup', 'BSS', 'DATA', 'otherCODE', 'COMDEF', 'LIDATA']:
            obj = copy.deepcopy(self.obj)
            if change == 'public': obj.publics['_extra'] = Public('_extra', 3, 0, 1, 0)
            elif change == 'fixup': obj.fixups.append(dataclasses.replace(obj.fixups[0], segment=3, offset=0))
            elif change == 'BSS': obj.segments[4].length = 2
            elif change == 'DATA': obj.segments[2].length = 2
            elif change == 'otherCODE': obj.segments[4].name = 'OTHER_TEXT'; obj.segments[4].class_name = 'CODE'
            elif change == 'COMDEF': obj.records.append((0xb0, 99999, b''))
            elif change == 'LIDATA': obj.records.append((0xa2, 99999, b''))
            with self.subTest(change=change), self.assertRaises(OwnedConstError):
                validate(self.unit, obj, PROJECT, self.context)

    def test_missing_ambiguous_wrong_group_or_members_fail(self):
        for change in ['missing', 'duplicate', 'member', 'code', 'name']:
            obj = copy.deepcopy(self.obj); group = next(r for r in obj.records if r[0] == 0x9a)
            obj.records.remove(group)
            if change == 'duplicate': obj.records += [group, group]
            elif change == 'member': obj.records.append((0x9a, group[1], b'\x02\xff\x04\xff\x02'))
            elif change == 'code': obj.records.append((0x9a, group[1], group[2] + b'\xff\x01'))
            elif change == 'name': obj.names[2] = 'OTHER'; obj.records.append(group)
            with self.subTest(change=change), self.assertRaises(OwnedConstError):
                validate(self.unit, obj, PROJECT, self.context)

    def test_own_const_fields_require_exact_group_offset16_shape_and_inbounds_addend(self):
        for change in ['frame', 'width', 'location', 'mode', 'displacement', 'owner', 'addend', 'no_refs']:
            obj = copy.deepcopy(self.obj)
            i = next(i for i, f in enumerate(obj.fixups) if f.target == (0, 3)); f = obj.fixups[i]
            if change == 'frame': obj.fixups[i] = dataclasses.replace(f, frame=(5, None))
            elif change == 'width': obj.fixups[i] = dataclasses.replace(f, width=4)
            elif change == 'location': obj.fixups[i] = dataclasses.replace(f, location_type=5)
            elif change == 'mode': obj.fixups[i] = dataclasses.replace(f, segment_relative=False)
            elif change == 'displacement': obj.fixups[i] = dataclasses.replace(f, displacement=24)
            elif change == 'owner': obj.fixups[i] = dataclasses.replace(f, offset=375)
            elif change == 'no_refs': obj.fixups = [f for f in obj.fixups if f.target != (0, 3)]
            elif change == 'addend':
                chunks = []
                for start, raw in obj.segments[1].chunks:
                    raw = bytearray(raw)
                    if start <= f.offset and f.offset + 2 <= start + len(raw): raw[f.offset-start:f.offset-start+2] = b'\x18\0'
                    chunks.append((start, bytes(raw)))
                obj.segments[1].chunks = chunks
            with self.subTest(change=change), self.assertRaises(OwnedConstError):
                validate(self.unit, obj, PROJECT, self.context)

    def test_primary_original_placement_pins_and_mz_scope_are_required(self):
        for change in ['frame', 'offset', 'origin', 'evidence', 'outside', 'reference', 'MZ']:
            u, context = copy.deepcopy(self.unit), copy.deepcopy(self.context)
            d = u['owned_const']
            if change == 'frame': d['data_address']['segment'] -= 1
            elif change == 'offset': d['data_address']['offset'] -= 1
            elif change == 'origin': d['image_offset'] = '0x61dbc'
            elif change == 'evidence': d['rea_evidence'] = 'evidence/rea-save-name-next-consumers-d9c6.json'
            elif change == 'outside': d['rea_evidence'] = '../CHESS.EXE'
            elif change == 'reference': context['carrier_sha256'] = '0' * 64
            elif change == 'MZ': context['relocations'] += (0x61dbb,)
            with self.subTest(change=change), self.assertRaises(OwnedConstError):
                validate(u, self.obj, PROJECT, context)

    def test_changed_independent_const_or_primary_profile_is_rejected(self):
        obj = copy.deepcopy(self.obj)
        at, data = obj.segments[3].chunks[0]
        obj.segments[3].chunks = [(at, bytes([data[0] ^ 1]) + data[1:])]
        with self.assertRaisesRegex(OwnedConstError, 'source raw-byte'):
            validate(self.unit, obj, PROJECT, self.context)
        import tempfile
        evidence = json.loads((PROJECT / descriptor()['rea_evidence']).read_text())
        for change in ['subject', 'loader', 'length', 'bytes']:
            e = copy.deepcopy(evidence)
            if change == 'subject': e['subject']['digest']['sha256'] = '0' * 64
            elif change == 'loader': e['analysis_profile']['parameters']['load_segment'] = '0x2000'
            elif change == 'length': e['parameters']['length'] -= 1
            elif change == 'bytes': e['normalized_result']['bytes_hex'] = '00' * 24
            with tempfile.TemporaryDirectory() as temporary:
                project = Path(temporary); (project / 'proof.json').write_text(json.dumps(e))
                u = dict(self.unit, owned_const=dict(descriptor(), rea_evidence='proof.json'))
                with self.subTest(change=change), self.assertRaises(OwnedConstError):
                    validate(u, self.obj, project, self.context)

    def test_default_linker_still_rejects_then_explicit_owner_matches_all375_and_four_mz(self):
        u, obj = self.unit, self.obj; origin = int(u['image_offset'], 0)
        with self.assertRaises(LinkError):
            link_function(obj, u['symbol'], origin, u['externals'])
        owned, _, _ = validate(u, obj, PROJECT, self.context)
        code, log = link_function(obj, u['symbol'], origin, u['externals'], owned_const=owned)
        self.assertEqual(len(code), 375)
        self.assertEqual(code, self.context['image'][origin:origin + 375])
        fields = [f for f in log if f['mode'] == 'segment_relative_owned_const']
        self.assertEqual(len(log), 40)
        self.assertEqual([f['object_offset'] for f in fields], [97, 142, 248, 321])
        emitted = sorted(f['mz_segment_relocation_image_offset'] for f in log if 'mz_segment_relocation_image_offset' in f)
        original = sorted(s for s in self.context['relocations'] if origin <= s < origin + 375)
        self.assertEqual(emitted, original)
        self.assertEqual(emitted, [0xd9f6, 0xda66, 0xda8d, 0xdb33])
        self.assertEqual(obj.segments[1].length, 376)  # all emitted compiler bytes remain available
        self.assertEqual(obj.segments[1].chunks[-1][1][-1:], b'\x90')
        self.assertNotEqual(self.context['image'][origin + 375:origin + 376], b'\x90')


@unittest.skipUnless(shutil.which('dosbox') and (PROJECT / 'toolchains/msc500').exists(), 'Pinned MSC5/DOSBox required')
class FreshCompilerTests(unittest.TestCase):
    def test_fresh_genuine375_plus_complete_owned24_without_rewriting_omf_fields(self):
        from msc import compile_c
        u = fixture_unit(); source = PROJECT / u['source']
        before = source.read_bytes()
        compiled = compile_c(source, u['flags'], compiler='msc500')
        obj = read_omf(compiled.object_bytes); original_obj = copy.deepcopy(obj)
        context = build_reference((PROJECT.parent / 'CHESS.EXE').read_bytes())
        owned, data, provenance = validate(u, obj, PROJECT, context)
        code, log = link_function(obj, u['symbol'], int(u['image_offset'], 0), u['externals'], owned_const=owned)
        self.assertEqual(obj, original_obj)
        self.assertEqual(source.read_bytes(), before)
        self.assertEqual(hashlib.sha256(before).hexdigest(), compiled.source_sha256)
        self.assertEqual(len(code), 375)
        self.assertEqual(code, context['image'][0xd9c6:0xdb3d])
        self.assertEqual(len(data), 24)
        self.assertEqual(len(log), 40)
        self.assertEqual(provenance['source_data_credit'], 0)
        import check
        import tempfile
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            built = check.build_unit(u, context['image'], PROJECT, 'nasm', output=output, reference=context)
            self.assertEqual(built['status'], 'c_matched', built)
            self.assertEqual(built['owned_const_data_credit'], 0)
            self.assertEqual(built['owned_const_proof']['size'], 24)
            self.assertTrue(built['owned_const_proof']['requires_enclosing_CONST_alignment_context'])
            self.assertFalse(built['owned_const_proof']['standalone_source_link_layout_proved'])


if __name__ == '__main__':
    unittest.main()
