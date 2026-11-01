"""Pinned OMF library inputs and restricted whole-segment runtime relocation.

This is a library backend, never C reconstruction. It reads no reference EXE,
accepts no replacement bytes, and returns every byte of a complete LEDATA
segment. Placements are explicit linker inputs; unsupported forms fail closed.
"""
from dataclasses import dataclass
import hashlib

try:
    from .omf import OMFError, read_omf
except ImportError:
    from omf import OMFError, read_omf


class LibraryError(OMFError):
    pass


@dataclass(frozen=True)
class LibraryMember:
    name: str
    offset: int
    data: bytes
    library_sha256: str

    @property
    def sha256(self):
        return hashlib.sha256(self.data).hexdigest()


def extract_member(data, name, library_sha256, member_sha256, *, validate_object=True):
    """Extract one independently pinned module from a DOS OMF library.

    The complete library digest is mandatory. Member boundaries follow OMF
    records through MODEND and library page alignment, never a byte search.
    ``validate_object=False`` is reserved for independently pinned library
    members passed unchanged to authentic LINK; strict OMF validation remains
    the default. Container record checksums are always checked.
    The header and dictionary are container metadata; object checksums are
    checked during the scan and the selected member uses the strict OMF parser.
    """
    digest = hashlib.sha256(data).hexdigest()
    if digest != library_sha256:
        raise LibraryError('library SHA-256 pin mismatch')
    if len(data) < 10 or data[0] != 0xf0:
        raise LibraryError('missing LIBHDR')
    page = int.from_bytes(data[1:3], 'little') + 3
    dictionary = int.from_bytes(data[3:7], 'little')
    pages = int.from_bytes(data[7:9], 'little')
    if page < 16 or page & (page - 1) or not page <= dictionary <= len(data):
        raise LibraryError('invalid library page or dictionary bounds')
    if dictionary + pages * 512 > len(data):
        raise LibraryError('truncated library dictionary')
    position, found = page, []
    while position < dictionary and data[position] != 0xf1:
        start = position
        if data[position] != 0x80:
            raise LibraryError('expected page-aligned THEADR')
        module_name = None
        while True:
            if position + 3 > dictionary:
                raise LibraryError('truncated library object record')
            kind = data[position]
            length = int.from_bytes(data[position + 1:position + 3], 'little')
            end = position + 3 + length
            if not length or end > dictionary:
                raise LibraryError('invalid library object record bounds')
            record = data[position:end]
            if sum(record) & 255:
                raise LibraryError('library object record checksum mismatch')
            if position == start:
                if length < 2 or record[3] + 2 != length:
                    raise LibraryError('invalid library THEADR name')
                module_name = record[4:-1].decode('latin1')
            position = end
            if kind == 0x8a:
                break
        if module_name == name:
            found.append(LibraryMember(name, start, bytes(data[start:position]), digest))
        position = (position + page - 1) // page * page
    if position >= dictionary or data[position] != 0xf1:
        raise LibraryError('missing LIBEND before dictionary')
    if position + 3 > dictionary or position + 3 + int.from_bytes(data[position + 1:position + 3], 'little') != dictionary:
        raise LibraryError('invalid LIBEND bounds')
    if not found:
        raise LibraryError('member name must identify exactly one library object')
    # OMF libraries may contain distinct modules with the same THEADR name
    # (SLIBC has two MEMCPY members). The mandatory independent member digest
    # selects identity; ambiguous duplicate copies still fail closed.
    selected = [member for member in found if member.sha256 == member_sha256]
    if not selected:
        raise LibraryError('member SHA-256 pin mismatch')
    if len(selected) != 1:
        raise LibraryError('member name and SHA-256 must identify exactly one library object')
    member = selected[0]
    if type(validate_object) is not bool:
        raise LibraryError('validate_object must be a boolean')
    if validate_object:
        read_omf(member.data)
    return member


def _word(value):
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 0xffff:
        raise LibraryError('placement requires explicit 16-bit integers')
    return value


def _placement(value):
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise LibraryError('placement requires (frame paragraph, offset)')
    return _word(value[0]), _word(value[1])


def link_segment(obj, segment, segments, groups, externals):
    """Link a complete initialized segment, returning bytes and fixup log.

    ``segments`` maps object SEGDEF indexes to (frame paragraph, base offset).
    ``groups`` maps GRPDEF indexes to frame paragraphs. ``externals`` maps names
    to (frame paragraph, offset). All paragraphs are relative to the MZ image,
    with no DOS load base applied. Only OFFSET16 and BASE16 forms present in
    the selected C5.00 runtime members are supported. Holes are rejected.
    """
    segments = {k: _placement(v) for k, v in segments.items()}
    groups = {k: _word(v) for k, v in groups.items()}
    externals = {k: _placement(v) for k, v in externals.items()}
    if segment not in obj.segments or segment not in segments:
        raise LibraryError('missing segment or explicit segment placement')
    seg = obj.segments[segment]
    if seg.unsupported_data:
        raise LibraryError('iterated data is unsupported')
    paragraph, base = segments[segment]
    if base + seg.length > 65536:
        raise LibraryError('segment extent crosses destination frame')
    result = bytearray()
    for offset, content in sorted(seg.chunks):
        if offset != len(result):
            raise LibraryError('hole or overlap in segment LEDATA')
        result.extend(content)
    if len(result) != seg.length:
        raise LibraryError('hole in segment LEDATA')

    def address(method, datum):
        if method == 0 and datum in segments:
            return segments[datum]
        if method == 1 and datum in groups:
            return groups[datum], 0
        if method == 2:
            name = obj.externals.get(datum)
            if name in externals:
                return externals[name]
            raise LibraryError(f'missing external placement: {name or datum}')
        raise LibraryError(f'unsupported or unresolved address method: {(method, datum)}')

    used, log = set(), []
    for fixup in sorted((f for f in obj.fixups if f.segment == segment), key=lambda f: f.offset):
        if fixup.width != 2 or fixup.location_type not in (1, 2):
            raise LibraryError('only OFFSET16 and BASE16 locations are supported')
        at = fixup.offset
        if at < 0 or at + 2 > len(result):
            raise LibraryError('fixup outside complete segment')
        if {at, at + 1} & used:
            raise LibraryError('overlapping fixup fields')
        used.update((at, at + 1))
        target_paragraph, target_offset = address(*fixup.target)
        frame_paragraph = (target_paragraph if fixup.frame == (5, None)
                           else address(*fixup.frame)[0])
        addend = int.from_bytes(result[at:at + 2], 'little')
        displacement = 0 if fixup.displacement is None else _word(fixup.displacement)
        place = paragraph * 16 + base + at
        if fixup.location_type == 2:
            if not fixup.segment_relative or displacement:
                raise LibraryError('BASE16 requires segment-relative mode and zero displacement')
            if fixup.target[0] != 1 or fixup.frame != fixup.target:
                raise LibraryError('BASE16 requires matching explicit group frame and target')
            value = target_paragraph + addend
            mode = 'base16'
        elif fixup.segment_relative:
            value = target_paragraph * 16 + target_offset + displacement - frame_paragraph * 16 + addend
            mode = 'offset16'
        else:
            if target_paragraph != paragraph:
                raise LibraryError('self-relative target must share code frame')
            value = target_paragraph * 16 + target_offset + displacement + addend - (place + 2)
            mode = 'relative16'
        encoded = value & 65535
        result[at:at + 2] = encoded.to_bytes(2, 'little')
        log.append({'segment': segment, 'object_offset': at, 'image_offset': place,
                    'mode': mode, 'frame': list(fixup.frame), 'target': list(fixup.target),
                    'target_symbol': obj.externals.get(fixup.target[1]) if fixup.target[0] == 2 else None,
                    'target_paragraph': target_paragraph, 'target_offset': target_offset,
                    'frame_paragraph': frame_paragraph, 'original_addend': addend,
                    'displacement': displacement, 'arithmetic_result': value,
                    'encoded_value': encoded, 'raw_fixupp': fixup.raw.hex(),
                    'record_offset': fixup.record_offset,
                    'mz_relocation_image_offset': place if mode == 'base16' else None})
    return bytes(result), log


def main():
    """Generate runtime artifacts from a pinned library and placement manifest."""
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--library', required=True, type=Path)
    parser.add_argument('--profile', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    profile = json.loads(args.profile.read_text())
    library = args.library.read_bytes()
    artifacts = []
    # Resolve everything before writing outputs, so missing inputs cannot leave
    # a misleading mixture of fresh and stale member artifacts.
    for module in profile['members']:
        member = extract_member(library, module['name'], profile['library_sha256'],
                                module['member_sha256'])
        if member.offset != module['library_offset']:
            raise LibraryError('library member offset mismatch')
        obj = read_omf(member.data)
        segments = {int(k): v for k, v in module['segments'].items()}
        groups = {int(k): v for k, v in module['groups'].items()}
        linked, fixups = link_segment(obj, module['segment'], segments, groups, module['externals'])
        artifacts.append((member, linked, fixups, module))
    artifact_ids = [module.get('id', member.name) for member, _, _, module in artifacts]
    if (any(not isinstance(value, str) or not value or any(c in value for c in '/\\')
            or value in ('.', '..') for value in artifact_ids)
            or len(set(artifact_ids)) != len(artifact_ids)):
        raise LibraryError('runtime artifact ids must be valid and unique')
    args.output.mkdir(parents=True, exist_ok=True)
    report = {'classification': 'independently supplied runtime library; zero authored-C credit',
              'library_sha256': profile['library_sha256'],
              'profile_sha256': hashlib.sha256(args.profile.read_bytes()).hexdigest(),
              'reference_executable_read': False, 'members': []}
    for member, linked, fixups, module in artifacts:
        artifact_id = module.get('id', member.name)
        if not isinstance(artifact_id, str) or not artifact_id or any(c in artifact_id for c in '/\\') or artifact_id in ('.', '..'):
            raise LibraryError('invalid runtime artifact id')
        (args.output / (artifact_id + '.obj')).write_bytes(member.data)
        (args.output / (artifact_id + '.bin')).write_bytes(linked)
        report['members'].append({'id': artifact_id, 'name': member.name, 'member_sha256': member.sha256,
                                  'library_offset': member.offset, 'object_size': len(member.data),
                                  'segment_size': len(linked), 'linked_sha256': hashlib.sha256(linked).hexdigest(),
                                  'placements': module, 'fixups': fixups})
    (args.output / 'GENERATED.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'generated_runtime_bytes': sum(len(a[1]) for a in artifacts),
                      'authored_c_bytes': 0, 'output': str(args.output)}, indent=2))


if __name__ == '__main__':
    main()
