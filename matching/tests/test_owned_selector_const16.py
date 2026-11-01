"""Future complete800 selector gate tests; outside the frozen C217 canonical suite."""
import copy
import dataclasses
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

M = Path(__file__).resolve().parents[1]
D = M/'build/book-selector-context-stage'
sys.path.insert(0, str(M))
from omf import read_omf, Public
from reference import build_reference
import owned_selector_const16 as gate
import link16

class SelectorGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = (M/'build/book-scan-843f/positive800.obj').read_bytes()
        cls.obj = read_omf(cls.raw)
        cls.unit = next(u for u in json.loads((M/'build/book-scan-843f/proposed800-units.json').read_text()) if u['symbol']=='_accept_hint_82db')
        cls.reference = build_reference((M.parent/'CHESS.EXE').read_bytes())

    def validate(self, unit=None, obj=None, reference=None, project=M):
        return gate.validate(self.unit if unit is None else unit,
            self.obj if obj is None else obj, project,
            self.reference if reference is None else reference)

    def test_entire_800_code_and_two_byte_selector_all_actual_fields_mz(self):
        before = copy.deepcopy(self.obj)
        descriptor, data, p = self.validate()
        self.assertEqual(data, bytes.fromhex('091f'))
        self.assertEqual(p['complete_CODE_bytes'], 800)
        self.assertEqual(len(p['complete_CODE_fields']), 117)
        self.assertEqual(p['CODE_MZ_sites'], [0x82d0, 0x82e6, 0x837c])
        self.assertEqual(p['complete_MZ_sites'], [0x619c6])
        self.assertEqual(p['source_data_credit'], 0)
        self.assertFalse(p['original_global_MAP_proved'])
        self.assertEqual(before, self.obj)

    def test_every_code_byte_compared_including_other_two_functions(self):
        for at in range(800):
            obj = copy.deepcopy(self.obj)
            chunks = []
            for start, body in obj.segments[1].chunks:
                body = bytearray(body)
                if start <= at < start+len(body):
                    body[at-start] ^= 1
                chunks.append((start, bytes(body)))
            obj.segments[1].chunks = chunks
            with self.subTest(at=at), self.assertRaises(ValueError):
                self.validate(obj=obj)

    def test_each_selector_addend_byte_rejected(self):
        for raw in (b'\1\0', b'\0\1'):
            obj = copy.deepcopy(self.obj)
            obj.segments[3].chunks = [(0, raw)]
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                self.validate(obj=obj)

    def test_changed_const_fixup_shapes_are_rejected(self):
        changes = [dict(offset=1), dict(width=4), dict(location_type=1),
                   dict(segment_relative=False), dict(frame=(1, 1)),
                   dict(target=(2, 65535)), dict(displacement=1)]
        for change in changes:
            obj = copy.deepcopy(self.obj)
            index = next(i for i, f in enumerate(obj.fixups) if f.segment == 3)
            obj.fixups[index] = dataclasses.replace(obj.fixups[index], **change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.validate(obj=obj)

    def test_missing_duplicate_const_and_owner_fields_rejected(self):
        for segment in (1, 3):
            for operation in ('missing', 'duplicate'):
                obj = copy.deepcopy(self.obj)
                index = next(i for i, f in enumerate(obj.fixups)
                             if (f.target == (0, 3) if segment == 1 else f.segment == 3))
                if operation == 'missing':
                    obj.fixups.pop(index)
                else:
                    obj.fixups.append(obj.fixups[index])
                with self.subTest(segment=segment, op=operation), self.assertRaises(ValueError):
                    self.validate(obj=obj)

    def test_owner_reference_frame_location_target_extent_addend_rejected(self):
        for change in (dict(offset=135), dict(width=4), dict(location_type=2),
                       dict(segment_relative=False), dict(frame=(5, None)),
                       dict(displacement=1), dict(target=(0, 2))):
            obj = copy.deepcopy(self.obj)
            index = next(i for i, f in enumerate(obj.fixups) if f.target == (0, 3))
            obj.fixups[index] = dataclasses.replace(obj.fixups[index], **change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.validate(obj=obj)

    def test_complete_allocations_and_anonymous_identity(self):
        for op in ('hole', 'overlap', 'tail', 'extra_data', 'attributes', 'public', 'LIDATA', 'COMMON'):
            obj = copy.deepcopy(self.obj)
            if op == 'hole': obj.segments[3].chunks = [(1, b'\0')]
            if op == 'overlap': obj.segments[3].chunks.append((0, b'\0'))
            if op == 'tail': obj.segments[1].length += 1
            if op == 'extra_data': obj.segments[2].length = 2
            if op == 'attributes': obj.segments[3].attributes = 0x58
            if op == 'public': obj.publics['_selector'] = Public('_selector', 3, 0, 1, 0)
            if op == 'LIDATA': obj.records.append((0xa2, 99999, b''))
            if op == 'COMMON': obj.records.append((0xb0, 99999, b''))
            with self.subTest(op=op), self.assertRaises(ValueError):
                self.validate(obj=obj)

    def test_descriptor_profile_placement_and_far_target_are_closed(self):
        changes = [dict(kind='other'), dict(segment=True), dict(group=2), dict(size=1),
                   dict(target_symbol='_other'), dict(image_offset='0x619c7'),
                   dict(data_address=dict(segment=0x5cc2, offset=0x4da7)), dict(extra=1)]
        for change in changes:
            u = copy.deepcopy(self.unit)
            u['owned_selector_const'].update(change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.validate(unit=u)
        for target in (0, dict(segment=0x1f09, offset=1), dict(segment=0x1f08, offset=0)):
            u = copy.deepcopy(self.unit);u['externals']['_splash_buffer'] = target
            with self.subTest(target=target), self.assertRaises(ValueError):
                self.validate(unit=u)

    def test_unit_owner_profile_and_exclusive_contract(self):
        for change in (dict(symbol='_load_book_82a5'), dict(size=168), dict(image_offset='0x82da'),
                       dict(language='asm'), dict(backend='msc510-omf'), dict(flags=['/AS', '/Zi']),
                       dict(owned_const={}), dict(owned_data={}), dict(owned_bss={}), dict(extended_extent={})):
            u = copy.deepcopy(self.unit);u.update(change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.validate(unit=u)

    def test_native_mz_sets_and_unchanged_comparison_provenance_required(self):
        for op in ('missing_const_MZ', 'extra_CODE_MZ', 'carrier', 'original'):
            r = copy.deepcopy(self.reference)
            if op == 'missing_const_MZ': r['relocations'] = tuple(x for x in r['relocations'] if x != 0x619c6)
            if op == 'extra_CODE_MZ': r['relocations'] += (0x82a4,)
            if op == 'carrier': r['carrier_sha256'] = '0'*64
            if op == 'original': r['original_sha256'] = '0'*64
            with self.subTest(op=op), self.assertRaises(ValueError):
                self.validate(reference=r)

    def test_original_literal_gate_remains_closed_to_selector_relocations(self):
        import owned_const16
        u = copy.deepcopy(self.unit)
        u['owned_const'] = {k:v for k,v in u['owned_selector_const'].items()
                            if k in ('segment', 'group', 'size', 'image_offset', 'data_address', 'rea_evidence')}
        with self.assertRaisesRegex(ValueError, 'no fixups'):
            owned_const16.validate(u, self.obj, M, self.reference)
        with self.assertRaisesRegex(ValueError, 'relocation-free'):
            link16.link_function(self.obj, u['symbol'], 0x82db, u['externals'], owned_const=u['owned_const'])

    def test_layout_validation_has_no_reference_reads(self):
        from unittest.mock import patch
        with patch.object(Path, 'read_bytes', side_effect=AssertionError('Reference read during layout/generation')):
            self.assertEqual(gate.validate_layout(self.obj, self.unit['owned_selector_const'], self.unit['externals']), 0x4da6)

    def test_actual_group_and_all_three_codeview_extents_required(self):
        for op in ('missing_group', 'duplicate_group', 'wrong_name', 'missing_proc', 'short_proc', 'foreign_public'):
            obj = copy.deepcopy(self.obj)
            if op == 'missing_group': obj.records = [r for r in obj.records if r[0] != 0x9a]
            if op == 'duplicate_group': obj.records += [r for r in obj.records if r[0] == 0x9a]
            if op == 'wrong_name': obj.names[2] = 'OTHER'
            if op == 'missing_proc': del obj.procedures['_empty_82a4']
            if op == 'short_proc': obj.procedures['_scan_book_843f']['length'] = 213
            if op == 'foreign_public': obj.publics['_alias'] = Public('_alias', 1, 0, 0, 0)
            with self.subTest(op=op), self.assertRaises(ValueError):
                self.validate(obj=obj)

    def test_complete_primary_identity_loader_length_and_scope_required(self):
        for key in ('rea_evidence', 'code_evidence'):
            original = json.loads((M/self.unit['owned_selector_const'][key]).read_text())
            for op in ('subject', 'load', 'language', 'operation', 'length', 'incomplete', 'byte'):
                evidence = copy.deepcopy(original)
                if op == 'subject': evidence['subject']['digest']['sha256'] = '0'*64
                if op == 'load': evidence['analysis_profile']['parameters']['load_segment'] = '0x1001'
                if op == 'language': evidence['analysis_profile']['parameters']['language_id'] = 'x86:LE:32:default'
                if op == 'operation': evidence['operation'] = 'other'
                if op == 'length': evidence['parameters']['length'] -= 1
                if op == 'incomplete': evidence['normalized_result']['complete'] = False
                if op == 'byte':
                    raw = bytearray.fromhex(evidence['normalized_result']['bytes_hex']);raw[0] ^= 1
                    evidence['normalized_result']['bytes_hex'] = raw.hex()
                with tempfile.TemporaryDirectory() as folder:
                    root = Path(folder);u = copy.deepcopy(self.unit)
                    for field in ('rea_evidence', 'code_evidence'):
                        raw = evidence if field == key else json.loads((M/u['owned_selector_const'][field]).read_text())
                        name = field+'.json';(root/name).write_text(json.dumps(raw));u['owned_selector_const'][field] = name
                    with self.subTest(key=key, op=op), self.assertRaises(ValueError):
                        self.validate(unit=u, project=root)

    def test_low_level_linker_exclusivity_and_owner_are_enforced(self):
        d = self.unit['owned_selector_const']
        for kwargs in (dict(owned_const={}), dict(owned_data={}), dict(owned_bss={})):
            with self.subTest(kwargs=kwargs), self.assertRaisesRegex(ValueError, 'one procedure'):
                link16.link_function(self.obj, self.unit['symbol'], 0x82db,
                    self.unit['externals'], owned_selector_const=d, **kwargs)
        with self.assertRaisesRegex(ValueError, 'CodeView owner'):
            link16.link_function(self.obj, '_load_book_82a5', 0x82a5,
                self.unit['externals'], owned_selector_const=d)

    def test_skip_owner_requires_separate_strict_union_extent(self):
        skip = json.loads((M/'build/book-skip-extent-stage/proposed-skip-unit.json').read_text())
        gate.validate_unit_metadata(skip)
        for extent in (None, {}, {'kind': 'other'}):
            u = copy.deepcopy(skip);u['extended_extent'] = extent
            with self.subTest(extent=extent), self.assertRaises(ValueError):
                gate.validate_unit_metadata(u)
        for name in gate.OWNERS-{'_skip_book_8577'}:
            u = copy.deepcopy(self.unit);u['symbol'] = name
            u['size'] = gate.PROCEDURES[name][1]
            u['image_offset'] = hex(0x82a4+gate.PROCEDURES[name][0])
            gate.validate_unit_metadata(u)
            u['extended_extent'] = skip['extended_extent']
            with self.subTest(name=name), self.assertRaises(ValueError):
                gate.validate_unit_metadata(u)

if __name__ == '__main__':
    unittest.main(verbosity=2)
