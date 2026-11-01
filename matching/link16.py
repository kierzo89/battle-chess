"""Restricted, deterministic OMF16 relocation of a compiler function.

External placements are explicit 16-bit offsets supplied by the caller: code
segment offsets for near calls and DGROUP offsets for segment-relative data.
No executable is read and no bytes or relocation fields are masked. Only the
OFFSET16, explicit far BASE16/FAR16 pointers, absolute words and validated
own-public-CODE offsets are supported.
"""

try:
    from .omf import OMFError, _Cursor
except ImportError:
    from omf import OMFError, _Cursor


class LinkError(OMFError):
    pass


def _address(value, description):
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 0xffff:
        raise LinkError(f'{description} must be an explicit 16-bit integer offset')
    return value


def _function_bytes(obj, info):
    """Copy every byte of the independently established compiler extent."""
    start, end = info['offset'], info['end']
    result, position = bytearray(), start
    for offset, data in sorted(obj.segments[info['segment']].chunks):
        left, right = max(start, offset), min(end, offset + len(data))
        if left >= right:
            continue
        if left != position:
            raise LinkError(f'hole or overlap in function LEDATA at {position:#x}')
        result.extend(data[left - offset:right - offset])
        position = right
    if position != end:
        raise LinkError(f'hole in function LEDATA at {position:#x}')
    return result


def _owned_const_placement(obj, descriptor):
    """Validate one complete literal CONST allocation; no reference bytes enter."""
    keys = {'segment', 'group', 'size', 'image_offset', 'data_address', 'rea_evidence'}
    if not isinstance(descriptor, dict) or set(descriptor) != keys:
        raise LinkError('owned CONST requires an exact complete allocation descriptor')
    index, group, size = (descriptor[k] for k in ('segment', 'group', 'size'))
    if (any(type(v) is not int or v <= 0 for v in (index, group, size))
            or index not in obj.segments or size > 65536):
        raise LinkError('owned CONST invalid segment/group/complete size')
    address = descriptor['data_address']
    if not isinstance(address, dict) or set(address) != {'segment', 'offset'}:
        raise LinkError('owned CONST requires explicit DGROUP segment:offset')
    frame = _address(address['segment'], 'owned CONST DGROUP frame')
    base = _address(address['offset'], 'owned CONST group-relative offset')
    try:
        physical = int(descriptor['image_offset'], 0)
    except (ValueError, TypeError) as exc:
        raise LinkError('owned CONST requires explicit physical image placement') from exc
    if (physical != frame * 16 + base or base + size > 65536
            or not isinstance(descriptor['rea_evidence'], str) or not descriptor['rea_evidence']):
        raise LinkError('owned CONST placement/extent identity mismatch')
    segment = obj.segments[index]
    if ((segment.name, segment.class_name, segment.attributes) != ('CONST', 'CONST', 0x48)
            or segment.length != size or segment.unsupported_data
            or any(p.segment == index for p in obj.publics.values())
            or any(f.segment == index for f in obj.fixups)):
        raise LinkError('owned CONST requires complete relocation-free anonymous initialized CONST')
    end = 0
    for offset, body in sorted(segment.chunks):
        if not body or offset != end or end + len(body) > size:
            raise LinkError('owned CONST has a hole, overlap or invalid LEDATA')
        end += len(body)
    if end != size:
        raise LinkError('owned CONST has an uninitialized allocation tail')
    groups = []
    for kind, _, payload in obj.records:
        if kind != 0x9a:
            continue
        cursor = _Cursor(payload); name = cursor.index(); members = []
        if not 0 < name < len(obj.names):
            raise LinkError('owned CONST undefined group name')
        while cursor:
            if cursor.byte() != 0xff:
                raise LinkError('owned CONST requires SEGDEF group members')
            member = cursor.index()
            if (member not in obj.segments or member in members
                    or obj.segments[member].class_name not in ('DATA', 'CONST', 'BSS')):
                raise LinkError('owned CONST invalid/duplicate DGROUP member')
            members.append(member)
        groups.append((len(groups) + 1, obj.names[name], members))
    if len(groups) != 1 or groups[0][:2] != (group, 'DGROUP') or index not in groups[0][2]:
        raise LinkError('owned CONST requires its real unique DGROUP membership')
    return base


def link_function(obj, symbol, origin, externals, *, image_origin=None, owned_const=None, owned_data=None, owned_bss=None, owned_selector_const=None):
    """Return (linked bytes, JSON-serializable relocation log).

    ``origin`` places this public function in the destination code segment.
    The object's code-segment placement is therefore origin-public.offset.
    Optional ``image_origin`` supplies the public's linear image offset for
    a nonzero real-mode CS. It must differ by a valid paragraph base. Near and
    own-CODE arithmetic remains in the 16-bit CS frame; log/MZ positions use
    image offsets. External near targets are still explicit CS offsets.
    CV3 procedure length is used when available; otherwise the entire next
    public/segment-end extent, including compiler padding, is retained.

    Segment-relative external offsets are asserted by the caller to be in
    DGROUP. FAR16 pointer externals instead require a dictionary with explicit
    ``offset`` and ``segment`` integers. Their segment fields are reported as
    MZ load-relocation positions; this function does not apply a DOS load base.
    Separate OFFSET16/BASE16 references may select the offset/segment of that
    same explicit far placement. BASE16 admits only frame=target, external
    targets and zero target displacement. Absolute ABI words use the distinct
    mapping ``{'absolute': value}``; they never emit loader relocations.
    Own-CODE OFFSET16 fixups may name this same public-combine CODE SEGDEF
    with frame=target or an explicit matching SEGDEF frame. Both refer to the
    combined CS frame at offset zero, so the fragment placement is retained in
    the encoded offset. Self-relative external offsets are asserted to be in
    this code segment. Arbitrary cross-segment addresses require a fuller linker and
    are deliberately unsupported by this API. The optional owned_const descriptor
    admits only an initialized anonymous CONST contribution in its real DGROUP.
    Its OFFSET16 fields retain their original group/segment targets; callers
    must separately authenticate the complete allocation and original placement.
    """
    _address(origin, 'function origin')
    if image_origin is None:
        image_origin = origin
    if (type(image_origin) is not int or not 0 <= image_origin <= 0x10ffef
            or image_origin < origin or (image_origin - origin) % 16
            or image_origin - origin > 0xffff0):
        raise LinkError('image origin must identify an explicit real-mode CS paragraph mapping')
    image_delta = image_origin - origin
    if not isinstance(externals, dict):
        raise LinkError('external placements must be a dictionary')
    for name, value in externals.items():
        if not isinstance(name, str):
            raise LinkError('external placement names must be strings')
        if isinstance(value, dict):
            if set(value) == {'absolute'}:
                _address(value['absolute'], f'external {name} absolute value')
            elif set(value) == {'offset', 'segment'}:
                _address(value['offset'], f'external {name} offset')
                _address(value['segment'], f'external {name} segment')
            else:
                raise LinkError(f'external {name} requires explicit far or absolute placement')
        else:
            _address(value, f'external {name}')
    if sum(x is not None for x in (owned_const, owned_data, owned_bss, owned_selector_const)) > 1:
        raise LinkError('one procedure may have only one explicit storage ownership contract')
    bss_base = None
    if owned_bss is not None:
        try:
            from .owned_bss16 import validate_layout
        except ImportError:
            from owned_bss16 import validate_layout
        try:
            validate_layout(obj, owned_bss)
        except OMFError as exc:
            raise LinkError('owned BSS layout: ' + str(exc)) from exc
        if symbol != owned_bss['owner_symbol']:
            raise LinkError('owned BSS descriptor must belong to this procedure')
        bss_base = _address(owned_bss['data_address']['offset'], 'owned BSS base')
    data_base = None
    if owned_data is not None:
        try:
            from .owned_data16 import validate_layout
        except ImportError:
            from owned_data16 import validate_layout
        try:
            validate_layout(obj, owned_data)
        except OMFError as exc:
            raise LinkError('owned DATA layout: ' + str(exc)) from exc
        if symbol != owned_data['owner_symbol']:
            raise LinkError('owned DATA descriptor must belong to this procedure')
        data_base = _address(owned_data['data_address']['offset'], 'owned DATA base')
    info = obj.function_info(symbol)
    const_contract = owned_const if owned_const is not None else owned_selector_const
    if owned_selector_const is not None:
        from owned_selector_const16 import validate_layout, owner_symbols
        if symbol not in owner_symbols(owned_selector_const):
            raise LinkError('selector CONST descriptor requires its CodeView owner')
        const_base = validate_layout(obj, owned_selector_const, externals)
    else:
        const_base = _owned_const_placement(obj, owned_const) if owned_const is not None else None
    if const_contract is not None and not any(f.target == (0, const_contract['segment']) for f in info['fixups']):
        raise LinkError('owned CONST descriptor has no actual procedure reference')
    start, end = info['offset'], info['end']
    if origin + info['size'] > 0x10000:
        raise LinkError('function extent crosses the destination code segment boundary')
    code_base = origin - start
    if code_base < 0:
        raise LinkError('function origin precedes its object segment offset')
    result = _function_bytes(obj, info)
    log, used = [], set()
    for fixup in sorted(info['fixups'], key=lambda f: (f.offset, f.record_offset)):
        far_pointer = fixup.location_type == 3 and fixup.width == 4
        base16 = fixup.location_type == 2 and fixup.width == 2
        loader_offset16 = fixup.location_type == 5 and fixup.width == 2
        if not (far_pointer or base16 or loader_offset16) and (fixup.location_type != 1 or fixup.width != 2):
            raise LinkError('only OFFSET16, external loader OFFSET16, BASE16 or FAR16 pointer FIXUPP locations are supported')
        # Microsoft 16-bit OMF LOC5 is a loader-resolved OFFSET16 (TIS1.1,
        # FIXUPP). Admit only the compiler's independently LINK-tested far
        # function-address shape; all target/frame/extent checks still apply.
        if loader_offset16 and (not fixup.segment_relative or fixup.target[0] != 2):
            raise LinkError('loader OFFSET16 requires segment-relative external far target')
        if (far_pointer or base16) and (not fixup.segment_relative or fixup.target[0] != 2):
            raise LinkError('BASE16/FAR16 requires segment-relative external target')
        own_const_offset = (const_contract is not None and fixup.segment_relative
                            and fixup.location_type == 1 and fixup.width == 2
                            and fixup.target == (0, const_contract['segment']))
        own_data_offset = (owned_data is not None and fixup.segment_relative
                           and fixup.location_type == 1 and fixup.width == 2
                           and fixup.target == (0, owned_data['segment']))
        own_bss_offset = (owned_bss is not None and fixup.segment_relative
                          and fixup.location_type == 1 and fixup.width == 2
                          and fixup.target == (0, owned_bss['segment']))
        own_code_offset = (not (far_pointer or base16) and fixup.segment_relative
                           and fixup.target == (0, info['segment']))
        if own_const_offset:
            if fixup.frame != (1, const_contract['group']):
                raise LinkError('owned CONST OFFSET16 requires its explicit DGROUP frame')
        elif own_data_offset:
            if fixup.frame != (1, owned_data['group']):
                raise LinkError('owned DATA OFFSET16 requires its actual DGROUP frame')
        elif own_bss_offset:
            if fixup.frame != (1, owned_bss['group']):
                raise LinkError('owned BSS OFFSET16 requires its actual DGROUP frame')
        elif own_code_offset:
            segment = obj.segments[info['segment']]
            # TIS OMF 1.1 SEGDEF: C=2,4,7 append as PUBLIC; C=6 is COMMON.
            # Only a relocatable, 16-bit public CODE contribution has the
            # combined CS frame assumed by this restricted linker.
            combine, alignment = (segment.attributes >> 2) & 7, segment.attributes >> 5
            if (segment.class_name.upper() != 'CODE' or combine not in (2, 4, 7)
                    or alignment not in (1, 2, 3, 4, 5) or segment.attributes & 1
                    or obj.publics[symbol].group != 0):
                raise LinkError('own CODE OFFSET16 requires ungrouped relocatable 16-bit public CODE SEGDEF')
            # TIS FIXUPP F0 names a SEGDEF frame; F5 uses the target frame.
            # For this same PUBLIC CODE contribution both are the combined
            # logical CS frame, whose offset is zero (not code_base).
            if fixup.frame not in ((5, None), (0, info['segment'])):
                raise LinkError(f'unsupported own CODE FIXUPP frame {fixup.frame!r}')
        elif fixup.frame != (5, None):
            raise LinkError(f'unsupported FIXUPP frame {fixup.frame!r}')
        if not start <= fixup.offset or fixup.offset + fixup.width > end:
            raise LinkError('relocation crosses the compiler function extent')
        field = fixup.offset - start
        if any(i in used for i in range(field, field + fixup.width)):
            raise LinkError('overlapping relocation fields')
        used.update(range(field, field + fixup.width))
        method, datum = fixup.target
        target_name = None
        if method == 2:
            target_name = obj.externals.get(datum)
            if target_name is None or target_name not in externals:
                raise LinkError(f'missing explicit external placement: {target_name or datum}')
            target = externals[target_name]
        elif own_const_offset:
            target = const_base
        elif own_data_offset:
            target = data_base
        elif own_bss_offset:
            target = bss_base
        elif method == 0 and datum == info['segment'] and (not fixup.segment_relative or own_code_offset):
            # Only the function's own code-segment placement is known.
            target = code_base
        else:
            raise LinkError(f'unsupported FIXUPP target {fixup.target!r}')
        far_offset, absolute = False, False
        if loader_offset16 and (not isinstance(target, dict) or set(target) != {'offset', 'segment'}):
            raise LinkError('loader OFFSET16 requires explicit offset and segment placement')
        if far_pointer or base16:
            if not isinstance(target, dict) or set(target) != {'offset', 'segment'}:
                raise LinkError('FAR16 pointer requires explicit offset and segment placement')
            target_segment = target['segment']
            target = target_segment if base16 else target['offset']
        elif isinstance(target, dict):
            if not fixup.segment_relative:
                raise LinkError('self-relative code requires an integer external placement')
            if set(target) == {'absolute'}:
                target, absolute = target['absolute'], True
            else:
                target_segment = target['segment']
                target, far_offset = target['offset'], True
        addend = int.from_bytes(result[field:field + 2], 'little')
        displacement = fixup.displacement if fixup.displacement is not None else 0
        if not isinstance(displacement, int) or not 0 <= displacement <= 0xffff:
            raise LinkError('unsupported relocation displacement')
        if base16 and displacement:
            raise LinkError('BASE16 target displacement is not supported')
        if own_const_offset and (displacement != 0 or addend >= const_contract['size']):
            raise LinkError('owned CONST field must address its complete initialized allocation')
        if own_data_offset and (displacement != 0 or addend not in
                {p['offset'] for p in owned_data['publics'].values()}):
            raise LinkError('owned DATA field must address a complete owned int public')
        if own_bss_offset and (displacement != 0 or addend not in
                {p['offset'] for p in owned_bss['scalars'].values()}):
            raise LinkError('owned BSS field must address one complete private unsigned word')
        value = target + addend + displacement
        code_place = code_base + fixup.offset
        place = image_delta + code_place
        if not fixup.segment_relative:
            value -= code_place + 2
        encoded = value & 0xffff
        result[field:field + 2] = encoded.to_bytes(2, 'little')
        entry = {
            'segment': fixup.segment, 'object_offset': fixup.offset,
            'function_offset': field, 'image_offset': place, 'width': fixup.width,
            'mode': ('far16_pointer' if far_pointer else
                     'segment_base16' if base16 else
                     'far_offset16' if far_offset else
                     'absolute16' if absolute else
                     'segment_relative_owned_selector_const' if own_const_offset and owned_selector_const is not None else
                     'segment_relative_owned_const' if own_const_offset else
                     'segment_relative_owned_data' if own_data_offset else
                     'segment_relative_owned_bss' if own_bss_offset else
                     'segment_relative_code' if own_code_offset else
                     'segment_relative_dgroup' if fixup.segment_relative else 'self_relative_code'),
            'frame_method': fixup.frame[0], 'target_method': method,
            'target_index': datum, 'target_symbol': target_name,
            'target_offset': target, 'original_addend': addend,
            'target_displacement': displacement, 'arithmetic_result': value,
            'encoded_value': encoded, 'encoded_hex': encoded.to_bytes(2, 'little').hex(),
            'code_segment_origin': code_base,
            'record_offset': fixup.record_offset, 'raw_fixupp': fixup.raw.hex(),
        }
        if own_const_offset:
            entry.update(owned_const_segment=const_contract['segment'],
                         owned_const_group=const_contract['group'],
                         owned_const_size=const_contract['size'],
                         owned_const_image_offset=const_contract['image_offset'],
                         owned_const_data_address=dict(const_contract['data_address']))
        elif own_data_offset:
            entry.update(owned_data_segment=owned_data['segment'],
                         owned_data_group=owned_data['group'],
                         owned_data_size=owned_data['size'],
                         owned_data_image_offset=owned_data['image_offset'],
                         owned_data_data_address=dict(owned_data['data_address']),
                         owned_data_public=next(name for name,p in owned_data['publics'].items()
                                                if p['offset'] == addend))
        elif own_bss_offset:
            entry.update(owned_bss_segment=owned_bss['segment'],
                         owned_bss_group=owned_bss['group'],
                         owned_bss_size=owned_bss['size'],
                         owned_bss_image_offset=owned_bss['image_offset'],
                         owned_bss_data_address=dict(owned_bss['data_address']),
                         owned_bss_scalar=next(name for name,p in owned_bss['scalars'].items()
                                                if p['offset'] == addend))
        elif own_code_offset:
            entry.update(code_frame_segment=info['segment'], code_frame_offset=0)
        if image_delta:
            entry.update(code_offset=code_place, code_frame_image_base=image_delta,
                         code_segment_image_origin=image_delta + code_base)
        if far_offset:
            entry.update(target_segment=target_segment)
        if loader_offset16:
            entry.update(loader_resolved_offset16=True, location_type=5)
        if base16:
            entry.update(target_segment=target_segment,
                         encoded_segment_value=encoded,
                         mz_segment_relocation_image_offset=place,
                         fields=[{'kind': 'segment16', 'image_offset': place,
                                  'original_addend': addend, 'encoded_value': encoded}])
        if far_pointer:
            segment_addend = int.from_bytes(result[field + 2:field + 4], 'little')
            segment_value = (target_segment + segment_addend) & 0xffff
            result[field + 2:field + 4] = segment_value.to_bytes(2, 'little')
            entry.update(encoded_hex=bytes(result[field:field + 4]).hex(),
                         target_segment=target_segment, original_segment_addend=segment_addend,
                         encoded_segment_value=segment_value,
                         mz_segment_relocation_image_offset=place + 2,
                         fields=[{'kind': 'offset16', 'image_offset': place,
                                  'original_addend': addend, 'encoded_value': encoded},
                                 {'kind': 'segment16', 'image_offset': place + 2,
                                  'original_addend': segment_addend, 'encoded_value': segment_value}])
        log.append(entry)
    return bytes(result), log
