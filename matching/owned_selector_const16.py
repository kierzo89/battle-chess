"""Separate, closed far-array selector CONST comparison gate. No generation."""
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
from omf import OMFError, OMFObject, _Cursor
from reference import validate_data_address, validate_expanded_read

KIND = 'book_far_array_selector_800_v1'
KEYS = {'kind', 'segment', 'group', 'size', 'image_offset', 'data_address',
        'rea_evidence', 'code_evidence', 'target_symbol'}
PROCEDURES = {'_empty_82a4': (0, 1), '_load_book_82a5': (1, 54),
              '_accept_hint_82db': (55, 169), '_prepare_hint_8384': (224, 187),
              '_scan_book_843f': (411, 214), '_rotate_book_8515': (625, 98),
              '_skip_book_8577': (723, 22), '_previous_book_858d': (745, 55)}
OWNERS = {'_accept_hint_82db', '_scan_book_843f', '_rotate_book_8515',
          '_skip_book_8577', '_previous_book_858d'}
CONST_REFERENCES = [134, 497, 522, 637, 658, 734, 766]

class SelectorConstError(OMFError):
    pass

def require(condition, message):
    if not condition:
        raise SelectorConstError(message)

def full_bytes(segment):
    result = bytearray()
    require(not segment.unsupported_data, 'selector CONST iterated/reserved data')
    for offset, body in sorted(segment.chunks):
        require(body and offset == len(result), 'selector allocation hole/overlap')
        result.extend(body)
    require(len(result) == segment.length, 'selector allocation uninitialized tail')
    return bytes(result)

def validate_unit_metadata(unit):
    if isinstance(unit, dict) and isinstance(unit.get('owned_selector_const'), dict) and unit['owned_selector_const'].get('kind') == 'shared_turn_book_literals78_v1':
        import shared_turn_book_literals78
        return shared_turn_book_literals78.validate_unit_metadata(unit)
    if isinstance(unit, dict) and isinstance(unit.get('owned_selector_const'), dict) and unit['owned_selector_const'].get('kind') == 'shared_turn_book_selector_2418_v1':
        import shared_turn_book_selector2418
        return shared_turn_book_selector2418.validate_unit_metadata(unit)
    if isinstance(unit, dict) and isinstance(unit.get('owned_selector_const'), dict) and unit['owned_selector_const'].get('kind') == 'pen_far_array_selector_560_v1':
        import pen_selector_const16
        return pen_selector_const16.validate_unit_metadata(unit)
    require(isinstance(unit, dict), 'selector C unit required')
    d = unit.get('owned_selector_const')
    require(isinstance(d, dict) and set(d) == KEYS and d.get('kind') == KIND,
            'selector exact descriptor/profile required')
    require(unit.get('language') == 'c' and unit.get('backend') == 'msc500-omf'
            and unit.get('symbol') in OWNERS and unit.get('size') == PROCEDURES[unit['symbol']][1]
            and unit.get('image_offset') == hex(0x82a4+PROCEDURES[unit['symbol']][0])
            and unit.get('flags') == ['/AS', '/Gs', '/Os', '/Zi']
            and not any(unit.get(k) is not None for k in ('owned_const', 'owned_data', 'owned_bss', 'code_address')),
            'selector exact C owner/profile and exclusive contract required')
    extent = unit.get('extended_extent')
    require((unit['symbol'] == '_skip_book_8577' and isinstance(extent, dict)
             and extent.get('kind') == 'book_skip_8577_v1')
            or (unit['symbol'] != '_skip_book_8577' and extent is None),
            'selector skip owner requires its separate strict extent contract')

def validate_layout(obj, descriptor, externals):
    if isinstance(descriptor, dict) and descriptor.get('kind') == 'shared_turn_book_literals78_v1':
        import shared_turn_book_literals78
        return shared_turn_book_literals78.validate_layout(obj, descriptor, externals)
    if isinstance(descriptor, dict) and descriptor.get('kind') == 'shared_turn_book_selector_2418_v1':
        import shared_turn_book_selector2418
        return shared_turn_book_selector2418.validate_layout(obj, descriptor, externals)
    if isinstance(descriptor, dict) and descriptor.get('kind') == 'pen_far_array_selector_560_v1':
        import pen_selector_const16
        return pen_selector_const16.validate_layout(obj, descriptor, externals)
    """Validate raw OMF ownership without reading any original/reference input."""
    d = descriptor
    require(isinstance(obj, OMFObject) and isinstance(d, dict) and set(d) == KEYS,
            'selector CONST exact descriptor required')
    require(d['kind'] == KIND and d['target_symbol'] == '_splash_buffer',
            'unreviewed selector CONST profile/target')
    require(all(type(d[k]) is int for k in ('segment', 'group', 'size'))
            and (d['segment'], d['group'], d['size']) == (3, 1, 2),
            'selector CONST exact indexes/size required')
    require(d['image_offset'] == '0x619c6' and d['data_address'] == {'segment': 0x5cc2, 'offset': 0x4da6}
            and all(type(v) is int for v in d['data_address'].values()),
            'selector CONST native placement identity')
    require(all(isinstance(d[k], str) and d[k] for k in ('rea_evidence', 'code_evidence')),
            'selector CONST primary paths required')
    require(isinstance(externals, dict) and externals.get(d['target_symbol']) == {'segment': 0x1f09, 'offset': 0}
            and all(type(v) is int for v in externals[d['target_symbol']].values()),
            'selector CONST explicit native far-array placement required')
    require(set(obj.segments) == {1, 2, 3, 4, 5, 6}, 'selector foreign/missing segment')
    expected = [(1, '_TEXT', 'CODE', 800, 0x48), (2, '_DATA', 'DATA', 0, 0x48),
                (3, 'CONST', 'CONST', 2, 0x48), (4, '_BSS', 'BSS', 0, 0x48)]
    require([(i, obj.segments[i].name, obj.segments[i].class_name,
              obj.segments[i].length, obj.segments[i].attributes) for i in range(1, 5)] == expected,
            'selector exact natural CODE800/CONST2 allocation required')
    require([(obj.segments[i].name, obj.segments[i].class_name) for i in (5, 6)] ==
            [('$$SYMBOLS', 'DEBSYM'), ('$$TYPES', 'DEBTYP')], 'selector debug segments changed')
    for index in (1, 2, 3, 4):
        full_bytes(obj.segments[index])
    require(not any(s.unsupported_data for s in obj.segments.values()),
            'selector iterated/reserved data forbidden')
    require(not any(k in (0xa2, 0xa3, 0xb0, 0xb8) for k, _, _ in obj.records),
            'selector LIDATA/COMMON forbidden')
    require(not any(p.segment == 3 for p in obj.publics.values()), 'selector CONST must be anonymous')
    require(set(obj.publics) == set(PROCEDURES), 'selector foreign/missing PUBLIC alias')
    require(set(obj.procedures) == set(PROCEDURES), 'selector complete eight-procedure context required')
    for name, (offset, size) in PROCEDURES.items():
        info = obj.function_info(name)
        require((info['segment'], info['offset'], info['size'], info['boundary']) ==
                (1, offset, size, 'codeview3_procedure'), 'selector independent CodeView extent changed')
    groups = []
    for kind, _, payload in obj.records:
        if kind != 0x9a:
            continue
        cursor = _Cursor(payload)
        name = cursor.index()
        require(0 < name < len(obj.names), 'selector invalid group name')
        members = []
        while cursor:
            require(cursor.byte() == 0xff, 'selector invalid group component')
            members.append(cursor.index())
        groups.append((obj.names[name], members))
    require(groups == [('DGROUP', [3, 4, 2])], 'selector actual DGROUP membership changed')
    const_fields = [f for f in obj.fixups if f.segment == 3]
    require(len(const_fields) == 1, 'selector complete CONST requires exactly one BASE16 field')
    field = const_fields[0]
    require((field.offset, field.width, field.location_type, field.segment_relative,
             field.frame, field.displacement) == (0, 2, 2, True, (5, None), None)
            and field.target[0] == 2 and obj.externals.get(field.target[1]) == d['target_symbol']
            and full_bytes(obj.segments[3]) == b'\0\0',
            'selector CONST raw BASE16/addend/target changed')
    refs = sorted((f for f in obj.fixups if f.target == (0, 3)), key=lambda f:f.offset)
    require([f.offset for f in refs] == CONST_REFERENCES,
            'selector requires all seven complete owner CODE references')
    for ref in refs:
        require((ref.segment, ref.width, ref.location_type, ref.segment_relative,
                 ref.frame, ref.displacement) == (1, 2, 1, True, (1, 1), None)
                and full_bytes(obj.segments[1])[ref.offset:ref.offset+2] == b'\0\0',
                'selector owner OFFSET16 field/addend changed')
    require(all(f.segment in (1, 3, 5, 6) for f in obj.fixups), 'selector foreign loaded relocation')
    return 0x4da6

def validate(unit, obj, project, reference, *, function_linker=None):
    if isinstance(unit, dict) and isinstance(unit.get('owned_selector_const'), dict) and unit['owned_selector_const'].get('kind') == 'shared_turn_book_literals78_v1':
        import shared_turn_book_literals78
        return shared_turn_book_literals78.validate(unit, obj, project, reference, function_linker=function_linker)
    if isinstance(unit, dict) and isinstance(unit.get('owned_selector_const'), dict) and unit['owned_selector_const'].get('kind') == 'shared_turn_book_selector_2418_v1':
        import shared_turn_book_selector2418
        return shared_turn_book_selector2418.validate(unit, obj, project, reference, function_linker=function_linker)
    if isinstance(unit, dict) and isinstance(unit.get('owned_selector_const'), dict) and unit['owned_selector_const'].get('kind') == 'pen_far_array_selector_560_v1':
        import pen_selector_const16
        return pen_selector_const16.validate(unit, obj, project, reference, function_linker=function_linker)
    """Authenticate entire CODE800 plus relocated CONST2; no extra byte credit."""
    require(isinstance(unit, dict) and isinstance(reference, dict),
            'selector C unit and pinned reference required')
    validate_unit_metadata(unit)
    d = unit.get('owned_selector_const')
    externals = unit.get('externals', {})
    base = validate_layout(obj, d, externals)
    project = Path(project).resolve()
    def primary(key):
        require(not Path(d[key]).is_absolute(), 'selector primary must be relative')
        path = (project/d[key]).resolve()
        require(path.is_relative_to(project), 'selector primary escapes project')
        raw = path.read_bytes()
        return json.loads(raw), hashlib.sha256(raw).hexdigest()
    data_unit = dict(d, reference_region='exepack-expanded')
    validate_data_address(data_unit, reference)
    # The independent compiler emits a zero addend and its genuine BASE16
    # external field. Applying that field uses only the explicit far placement.
    selector = externals[d['target_symbol']]['segment'].to_bytes(2, 'little')
    selector_evidence, selector_pin = primary('rea_evidence')
    selector_id = validate_expanded_read(selector_evidence, data_unit, selector, reference,
                                        emitted_mz_sites=[0x619c6])
    if function_linker is None:
        from link16 import link_function
        function_linker = link_function
    code, fields = bytearray(), []
    for name, (offset, size) in PROCEDURES.items():
        kwargs = {'owned_selector_const': d} if name in OWNERS else {}
        body, records = function_linker(obj, name, 0x82a4+offset, externals, **kwargs)
        require(len(body) == size and len(code) == offset, 'selector full natural CODE context changed')
        code.extend(body)
        fields.extend(records)
    sites = [r['mz_segment_relocation_image_offset'] for r in fields
             if 'mz_segment_relocation_image_offset' in r]
    code_evidence, code_pin = primary('code_evidence')
    code_id = validate_expanded_read(code_evidence,
        dict(image_offset='0x82a4', size=800, reference_region='exepack-expanded'),
        bytes(code), reference, emitted_mz_sites=sites)
    proof = dict(classification='complete_compiler_owned_far_array_selector_CONST_uncredited_context',
                 authored_c_function_credit=0, source_data_credit=0, size=2,
                 selector_bytes_hex=selector.hex(), complete_MZ_sites=[0x619c6],
                 complete_CODE_bytes=800, complete_CODE_fields=fields, CODE_MZ_sites=sites,
                 selector_primary_id=selector_id, selector_primary_sha256=selector_pin,
                 code_primary_id=code_id, code_primary_sha256=code_pin,
                 raw_CONST_fixup=asdict(next(f for f in obj.fixups if f.segment == 3)),
                 original_global_MAP_proved=False, omf_records_or_fields_modified=False)
    proof['raw_CONST_fixup']['raw'] = proof['raw_CONST_fixup']['raw'].hex()
    return d, selector, proof


def owner_symbols(descriptor):
    """Exact source-context owner dispatch; no generic ownership grant."""
    if isinstance(descriptor, dict) and descriptor.get("kind") == "pen_far_array_selector_560_v1":
        import pen_selector_const16
        return pen_selector_const16.OWNERS
    if isinstance(descriptor, dict) and descriptor.get("kind") == KIND:
        return OWNERS
    if isinstance(descriptor, dict) and descriptor.get('kind') == 'shared_turn_book_selector_2418_v1':
        import shared_turn_book_selector2418
        return shared_turn_book_selector2418.OWNERS
    if isinstance(descriptor, dict) and descriptor.get('kind') == 'shared_turn_book_literals78_v1':
        import shared_turn_book_literals78
        return shared_turn_book_literals78.OWNERS
    raise SelectorConstError("Unknown selector owner profile")
