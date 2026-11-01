"""Authenticate one genuine mixed C CODE344/PUBLIC DATA4 owner contribution.

The strict layout gate is target-free and never links or edits OMF fields.
Reference gates compare independently emitted complete storage. DATA2 extraction
requires both the complete owner read and that public's own primary read.
The shared ownership proof has zero separate DATA/function matching credit.
"""
from dataclasses import asdict
import hashlib
import json
from pathlib import Path

try:
    from .omf import OMFError, OMFObject, _Cursor
    from .reference import validate_data_address, validate_expanded_read
except ImportError:
    from omf import OMFError, OMFObject, _Cursor
    from reference import validate_data_address, validate_expanded_read


class OwnedDataError(OMFError):
    pass


def sha(data):
    return hashlib.sha256(data).hexdigest()


def serial_descriptor():
    """Return a fresh, closed descriptor for the complete serial allocation."""
    return {'segment': 2, 'group': 1, 'size': 4, 'image_offset': '0x5fadc',
            'data_address': {'segment': 0x5cc2, 'offset': 0x2ebc},
            'rea_evidence': 'evidence/rea-serial-link-defaults-expanded.json',
            'owner_symbol': '_configure_serial',
            'publics': {'_serial_irq': {'offset': 0, 'size': 2},
                        '_serial_base': {'offset': 2, 'size': 2}}}


def groups_of(obj):
    groups = []
    for kind, _, payload in obj.records:
        if kind != 0x9a:
            continue
        c = _Cursor(payload)
        index = c.index()
        if not 0 < index < len(obj.names):
            raise OwnedDataError('undefined group name')
        members = []
        while c:
            if c.byte() != 0xff:
                raise OwnedDataError('non-SEGDEF group component')
            member = c.index()
            if member not in obj.segments or member in members:
                raise OwnedDataError('missing or repeated group segment')
            members.append(member)
        groups.append({'index': len(groups) + 1, 'name': obj.names[index], 'segments': members})
    return groups


def complete_bytes(segment):
    data = bytearray()
    for offset, content in sorted(segment.chunks):
        if not content or offset != len(data) or offset + len(content) > segment.length:
            raise OwnedDataError('hole/overlap/invalid complete initialized segment')
        data.extend(content)
    if len(data) != segment.length:
        raise OwnedDataError('uninitialized segment tail')
    return bytes(data)


def _validate_layout(obj, desc):
    """Return all owned DATA bytes and proof; no bytes/OMF fields are changed."""
    if not isinstance(obj, OMFObject):
        raise OwnedDataError('Owned DATA requires a strict-reader OMF object')
    if not isinstance(desc, dict):
        raise OwnedDataError('Owned DATA requires an exact explicit descriptor')
    if json.dumps(desc, sort_keys=True) != json.dumps(serial_descriptor(), sort_keys=True):
        raise OwnedDataError('descriptor must identify the complete strict serial ownership contract')
    if any(kind in (0xa2, 0xa3, 0xb0, 0xb8) for kind, _, _ in obj.records):
        raise OwnedDataError('iterated/communal allocations forbidden')
    data = obj.segments.get(desc['segment'])
    if (data is None or (data.name, data.class_name, data.length, data.attributes) !=
            ('_DATA', 'DATA', 4, 0x48) or data.unsupported_data):
        raise OwnedDataError('complete genuine word-aligned PUBLIC DATA4 required')
    owner = obj.function_info(desc['owner_symbol'])
    code = obj.segments.get(owner['segment'])
    if (owner['boundary'] != 'codeview3_procedure' or owner['offset'] != 320 or
            owner['size'] != 24 or code.length != 344 or
            (code.name, code.class_name, code.attributes) != ('_TEXT', 'CODE', 0x48)):
        raise OwnedDataError('complete genuine configure_serial CV owner and CODE344 required')
    if code.unsupported_data:
        raise OwnedDataError('iterated CODE forbidden')
    # All genuine publics/procedures must cover the entire CODE allocation.
    code_publics = [p for p in obj.publics.values() if p.segment == code.index]
    expected_code = {'_initialize_io': (0, 43), '_write_bytes_dbb5': (43, 46),
                     '_read_bytes_dbe3': (89, 156), '_discard_bytes_dc7f': (245, 18),
                     '_available_bytes_dc91': (263, 57), '_configure_serial': (320, 24)}
    if {p.name for p in code_publics} != set(expected_code):
        raise OwnedDataError('all six genuine CODE publics required, no aliases')
    for p in code_publics:
        if p.group != 0:
            raise OwnedDataError('CODE PUBLIC must remain outside DGROUP')
        info = obj.function_info(p.name)
        if (info['boundary'] != 'codeview3_procedure' or
                (info['offset'], info['size']) != expected_code[p.name]):
            raise OwnedDataError('independent CV union must cover full CODE344 without tails')
    complete_bytes(code)
    for other in obj.segments.values():
        if other.index in (data.index, code.index):
            continue
        debug = (other.name, other.class_name, other.attributes) in (
            ('$$SYMBOLS', 'DEBSYM', 0x20), ('$$TYPES', 'DEBTYP', 0x20))
        empty = ((other.name, other.class_name) in (('CONST', 'CONST'), ('_BSS', 'BSS'))
                 and other.length == 0 and other.attributes == 0x48
                 and not other.chunks and not other.unsupported_data)
        if not debug and not empty:
            raise OwnedDataError('extra allocation or unknown segment forbidden')
    groups = groups_of(obj)
    if (len(groups) != 1 or groups[0]['index'] != desc['group'] or
            groups[0]['name'] != 'DGROUP' or set(groups[0]['segments']) != {2, 3, 4} or
            len(groups[0]['segments']) != 3):
        raise OwnedDataError('one actual matching DGROUP of DATA/CONST/BSS required')
    actual_publics = {p.name: p for p in obj.publics.values() if p.segment == data.index}
    if set(actual_publics) != set(desc['publics']):
        raise OwnedDataError('exact complete public DATA ownership required, no aliases')
    for name, extent in desc['publics'].items():
        p = actual_publics[name]
        if (p.offset != extent['offset'] or p.group != desc['group'] or
                p.type_index != 0x81 or extent['size'] != 2):
            raise OwnedDataError('ordinary int PUBLIC must have exact own DATA2 bounds and DGROUP')
    if any(p.segment not in (code.index, data.index) for p in obj.publics.values()):
        raise OwnedDataError('public outside owned CODE/DATA forbidden')
    if any(f.segment == data.index for f in obj.fixups):
        raise OwnedDataError('owned DATA4 must have no fixups')
    raw_data = complete_bytes(data)
    fields = []
    # Every code reference to this owned segment must remain a genuine
    # internal group-framed OFFSET16, never rewritten into external aliases.
    for f in obj.fixups:
        if f.segment != code.index:
            continue
        is_owned = f.target == (0, data.index) or f.frame == (1, desc['group']) or (f.target[0] == 2 and
                     obj.externals.get(f.target[1]) in actual_publics)
        if not is_owned:
            continue
        if (f.target != (0, data.index) or f.frame != (1, desc['group']) or
                f.width != 2 or f.location_type != 1 or not f.segment_relative or
                f.displacement not in (None, 0) or
                not owner['offset'] <= f.offset or f.offset + 2 > owner['end']):
            raise OwnedDataError('owned reference must be genuine complete owner group OFFSET16')
        raw_code = complete_bytes(code)
        addend = int.from_bytes(raw_code[f.offset:f.offset + 2], 'little')
        if addend not in {v['offset'] for v in desc['publics'].values()}:
            raise OwnedDataError('owned addend must start a complete int public, never interior')
        fields.append({'object_offset': f.offset, 'function_offset': f.offset - owner['offset'],
                       'original_addend': addend, 'raw_fixupp': f.raw.hex(),
                       'width': f.width, 'location_type': f.location_type,
                       'segment_relative': f.segment_relative, 'displacement': f.displacement,
                       'frame': list(f.frame), 'target': list(f.target),
                       'record_offset': f.record_offset})
    if sorted((f['object_offset'], f['original_addend']) for f in fields) != [(330, 2), (336, 0)]:
        raise OwnedDataError('all and only two authentic configure_serial DATA fields required')
    public_extents = {name: dict(extent, bytes_hex=raw_data[extent['offset']:extent['offset'] + 2].hex())
                      for name, extent in desc['publics'].items()}
    proof = {'classification': 'complete_compiler_owned_PUBLIC_DATA',
             'size': len(raw_data), 'bytes_hex': raw_data.hex(), 'sha256': sha(raw_data),
             'segment': {k: v for k, v in asdict(data).items() if k != 'chunks'},
             'group': groups[0], 'owner': {k: v for k, v in owner.items() if k != 'fixups'},
             'code_references': sorted(fields, key=lambda f: f['object_offset']),
             'public_extents': public_extents,
             'data_writes': [{'offset': off, 'size': len(raw), 'sha256': sha(raw)}
                             for off, raw in sorted(data.chunks)],
             'owner_CODE_SEGDEF_size': code.length, 'whole_CODE_CV_union_size': 344,
             'complete_MZ_sites': [], 'source_data_credit': 0,
             'omf_records_or_fields_modified': False,
             'historical_source_ownership_unknown': True}
    return raw_data, proof


def validate_layout(obj, descriptor):
    """Pure structural gate: no target, evidence, filesystem or linker reads."""
    try:
        return _validate_layout(obj, descriptor)
    except OwnedDataError:
        raise
    except (OMFError, KeyError, TypeError, ValueError, IndexError, AttributeError) as exc:
        raise OwnedDataError('Owned DATA structural validation failed: ' + str(exc)) from exc


def _read_primary(project, relative):
    project = Path(project).resolve()
    if not isinstance(relative, str) or Path(relative).is_absolute():
        raise OwnedDataError('Owned DATA primary evidence must be project-relative')
    path = (project / relative).resolve()
    if not path.is_relative_to(project):
        raise OwnedDataError('Owned DATA primary evidence escaped project')
    raw = path.read_bytes()
    return json.loads(raw), sha(raw)


def _unit_metadata(unit):
    if not isinstance(unit, dict) or unit.get('flags') != ['/AS', '/Zi']:
        raise OwnedDataError('Owned DATA requires exact shared Microsoft C5 /AS /Zi flags')
    desc = unit.get('owned_data')
    if not isinstance(desc, dict) or json.dumps(desc, sort_keys=True) != json.dumps(serial_descriptor(), sort_keys=True):
        raise OwnedDataError('Owned DATA requires exact complete serial descriptor')
    desc = json.loads(json.dumps(desc))
    if unit.get('language') == 'c':
        if (unit.get('backend') != 'msc500-omf' or unit.get('symbol') != '_configure_serial' or
                type(unit.get('size')) is not int or unit['size'] != 24 or
                not isinstance(unit.get('image_offset'), str) or int(unit['image_offset'], 0) != 0xdcca):
            raise OwnedDataError('Owned DATA CODE unit must be complete configure_serial at DCCA24')
        if any(name in unit.get('externals', {}) for name in desc['publics']):
            raise OwnedDataError('Owned PUBLIC DATA may not be assigned external alias placements')
        return desc, None
    if unit.get('language') != 'c-data' or unit.get('backend') != 'msc500-owned-data-omf':
        raise OwnedDataError('Owned DATA public requires the explicit mixed-object C DATA backend')
    symbol = unit.get('symbol')
    public = desc['publics'].get(symbol)
    if public is None:
        raise OwnedDataError('Owned DATA public is not one of the two complete int definitions')
    expected_origin = int(desc['image_offset'], 0) + public['offset']
    expected_address = {'segment': desc['data_address']['segment'],
                        'offset': desc['data_address']['offset'] + public['offset']}
    expected_primary = {'_serial_irq': 'evidence/rea-serial-initialized-irq.json',
                        '_serial_base': 'evidence/rea-serial-initialized-base.json'}[symbol]
    if (type(unit.get('size')) is not int or unit['size'] != 2 or
            not isinstance(unit.get('image_offset'), str) or int(unit['image_offset'], 0) != expected_origin or
            unit.get('reference_region') != 'exepack-expanded' or
            json.dumps(unit.get('data_address'), sort_keys=True) != json.dumps(expected_address, sort_keys=True) or
            unit.get('rea_evidence') != expected_primary or unit.get('externals', {}) != {}):
        raise OwnedDataError('Owned DATA public requires exact own DATA2/image/DGROUP/primary metadata')
    return desc, public



def validate_unit_metadata(unit):
    """Validate the closed owner/public registry role before compiling anything."""
    try:
        return _unit_metadata(unit)
    except OwnedDataError:
        raise
    except (KeyError, TypeError, ValueError, IndexError, AttributeError) as exc:
        raise OwnedDataError('Owned DATA unit metadata validation failed: ' + str(exc)) from exc


def _validate(unit, obj, project, reference):
    if not isinstance(reference, dict):
        raise OwnedDataError('Owned DATA requires the pinned original/expanded reference context')
    desc, public = validate_unit_metadata(unit)
    data, proof = validate_layout(obj, desc)
    owner_unit = dict(desc, reference_region='exepack-expanded')
    frame, offset = validate_data_address(owner_unit, reference)
    primary, primary_hash = _read_primary(project, desc['rea_evidence'])
    evidence_id = validate_expanded_read(primary, owner_unit, data, reference)
    proof.update(descriptor=desc, rea_evidence_id=evidence_id,
                 rea_evidence_sha256=primary_hash, data_frame=frame, data_offset=offset,
                 original_sha256=reference['original_sha256'], carrier_sha256=reference['carrier_sha256'])
    if public is not None:
        # Validate the entire parent first. The selected child's exact bounds
        # are established by ordinary int PUBDEF metadata, never target slicing.
        selected = data[public['offset']:public['offset'] + public['size']]
        validate_data_address(unit, reference)
        child_primary, child_hash = _read_primary(project, unit['rea_evidence'])
        child_evidence_id = validate_expanded_read(child_primary, unit, selected, reference)
        proof['selected_public'] = {'symbol': unit['symbol'], 'offset': public['offset'],
            'size': public['size'], 'bytes_hex': selected.hex(), 'sha256': sha(selected),
            'rea_evidence_id': child_evidence_id, 'rea_evidence_sha256': child_hash,
            'image_offset': unit['image_offset'], 'data_address': dict(unit['data_address'])}
    return desc, data, proof


def validate(unit, obj, project, reference):
    """Return (closed descriptor, complete DATA4 bytes, full ownership proof).

    Accepts only the C configure owner or one of its two C-DATA registry rows.
    All paths validate the full allocation. DATA paths additionally validate
    their own independent complete DATA2 primary evidence.
    """
    try:
        return _validate(unit, obj, project, reference)
    except OwnedDataError:
        raise
    except (OMFError, OSError, KeyError, TypeError, ValueError, IndexError, AttributeError) as exc:
        raise OwnedDataError('Owned DATA reference/unit validation failed: ' + str(exc)) from exc


def extract_public(unit, obj, project, reference):
    """Return (exact generated DATA2 bytes, metadata) after both primary gates."""
    if not isinstance(unit, dict) or unit.get('language') != 'c-data':
        raise OwnedDataError('Owned DATA extraction requires a C-DATA public unit')
    desc, data, proof = validate(unit, obj, project, reference)
    selected = proof['selected_public']
    raw = data[selected['offset']:selected['offset'] + selected['size']]
    metadata = {'boundary': 'complete_owned_public_int16', 'symbol': unit['symbol'],
                'size': len(raw), 'sha256': sha(raw), 'public': asdict(obj.publics[unit['symbol']]),
                'owned_data': desc, 'owned_data_proof': proof, 'emitted_mz_sites': [],
                'authored_c_function_count': 0}
    return raw, metadata
