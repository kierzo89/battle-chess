"""Strict numeric NASM initialized DATA, separately credited from C or code.

One entire WORD PUBLIC _DATA/DGROUP allocation is accepted. No extraction
bounds, target bytes, includes, binary insertion, code or relocation fields
enter this backend. The numeric source grammar is intentionally narrow.
"""
from dataclasses import asdict, dataclass
import hashlib
from pathlib import Path
import re
import shutil
import struct
import subprocess
import tempfile

from omf import OMFError, OMFObject, _Cursor, read_omf


class ASMDataError(OMFError):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def validate_unit(unit):
    if ((unit.get('language'), unit.get('backend')) != ('asm-data', 'nasm-data-omf')
            or unit.get('reference_region') != 'exepack-expanded'):
        raise ASMDataError('ASM DATA requires its separate backend and expanded region')
    for key in ('source_sha256', 'assembler_sha256'):
        if not isinstance(unit.get(key), str) or not re.fullmatch('[0-9a-f]{64}', unit[key]):
            raise ASMDataError('ASM DATA requires explicit source and assembler SHA-256 pins')
    symbols = unit.get('symbols')
    if (not isinstance(symbols, list) or not symbols
            or any(not isinstance(x, str) or not re.fullmatch('_[A-Za-z0-9_]+', x) for x in symbols)
            or len(set(symbols)) != len(symbols)):
        raise ASMDataError('ASM DATA requires the complete ordered public symbol list')
    for key in ('symbol', 'flags', 'externals', 'extended_extent', 'owned_const', 'owned_data', 'owned_bss', 'data_address', 'code_address'):
        if key in unit:
            raise ASMDataError('ASM DATA forbids partial extents, placement fixups and foreign ownership fields')


def parse_source(source):
    """Authenticate a numeric DD model, including every public's full payload."""
    try:
        text = source.decode('ascii')
    except (AttributeError, UnicodeDecodeError) as exc:
        raise ASMDataError('ASM DATA source must be ASCII bytes') from exc
    headers = ['bits 16', 'segment _data public align=2 class=data use16', 'group dgroup _data']
    declarations, labels, values = [], {}, []
    position = 0
    for line in text.splitlines():
        line = line.split(';', 1)[0].strip()
        if not line:
            continue
        if position < 3:
            if line.lower() != headers[position]:
                raise ASMDataError('ASM DATA requires the exact WORD PUBLIC _DATA/DGROUP prologue')
            position += 1
            continue
        m = re.fullmatch(r'global (_[A-Za-z0-9_]+)', line, re.I)
        if m:
            if m[1] in declarations:
                raise ASMDataError('ASM DATA duplicate global')
            declarations.append(m[1]); continue
        m = re.fullmatch(r'(_[A-Za-z0-9_]+):', line)
        if m:
            if m[1] in labels or len(values) * 4 in labels.values():
                raise ASMDataError('ASM DATA duplicate/aliased public label')
            labels[m[1]] = len(values) * 4; continue
        m = re.fullmatch(r'dd\s+(.+)', line, re.I)
        if m:
            if not labels:
                raise ASMDataError('ASM DATA cannot contain undeclared leading storage')
            for item in m[1].split(','):
                item = item.strip()
                if not re.fullmatch(r'-?(?:0x[0-9a-fA-F]+|[0-9]+)', item):
                    raise ASMDataError('ASM DATA accepts only explicit numeric DD values')
                value = int(item, 16 if 'x' in item.lower() else 10)
                if not -0x80000000 <= value <= 0xffffffff:
                    raise ASMDataError('ASM DATA numeric DD is outside 32-bit range')
                values.append(value & 0xffffffff)
            continue
        raise ASMDataError('ASM DATA forbids instructions, INCBIN, preprocessing, padding and reserved storage')
    if (position != 3 or not values or not declarations or declarations != list(labels)
            or list(labels.values())[0] != 0 or list(labels.values())[-1] >= 4 * len(values)):
        raise ASMDataError('ASM DATA requires complete ordered initialized public definitions')
    return {'symbols': declarations, 'offsets': labels, 'numeric_values': values}


def extract_data(obj, symbols):
    """Extract exactly one complete allocation, never a selected public slice."""
    if not isinstance(obj, OMFObject):
        raise ASMDataError('ASM DATA requires a strict-reader OMF object')
    if (len(obj.segments) != 1 or obj.fixups or obj.externals
            or any(k in (0xb0, 0xb8, 0xa2, 0x9c) for k, _, _ in obj.records)):
        raise ASMDataError('ASM DATA forbids other segments, FIXUPP, EXTDEF, COMM and LIDATA')
    segment = next(iter(obj.segments.values()))
    if ((segment.name, segment.class_name, segment.attributes) != ('_DATA', 'DATA', 0x48)
            or segment.unsupported_data or not 0 < segment.length <= 65535):
        raise ASMDataError('ASM DATA requires a complete initialized WORD PUBLIC _DATA segment')
    groups = []
    for kind, _, payload in obj.records:
        if kind not in (0x80, 0x88, 0x96, 0x98, 0x9a, 0x90, 0xa0, 0x8a):
            raise ASMDataError('ASM DATA forbids auxiliary aliases, types and unsupported records')
        if kind == 0x88 and not (payload.startswith(b'\0\0') or payload == b'\x40\xa2\x01'):
            raise ASMDataError('ASM DATA forbids linker-directive comments')
        if kind == 0x9a:
            cursor = _Cursor(payload); name = cursor.index(); members = []
            if not 0 < name < len(obj.names):
                raise ASMDataError('ASM DATA undefined group name')
            while cursor:
                if cursor.byte() != 0xff:
                    raise ASMDataError('ASM DATA requires explicit SEGDEF group membership')
                members.append(cursor.index())
            groups.append((obj.names[name], members))
        elif kind in (0x8a, 0x8b) and payload != b'\0':
            raise ASMDataError('ASM DATA forbids entry points')
    if groups != [('DGROUP', [segment.index])]:
        raise ASMDataError('ASM DATA requires exactly its one real DGROUP membership')
    publics = sorted(obj.publics.values(), key=lambda p: p.offset)
    if ([p.name for p in publics] != symbols or not publics or publics[0].offset != 0
            or len({p.offset for p in publics}) != len(publics)
            or any(p.segment != segment.index or p.group != 1 or p.type_index != 0
                   or not 0 <= p.offset < segment.length or p.offset % 4 for p in publics)):
        raise ASMDataError('ASM DATA requires every declared public, offset zero and DGROUP PUBDEF frames')
    data = bytearray()
    for offset, content in sorted(segment.chunks):
        if not content or offset != len(data) or offset + len(content) > segment.length:
            raise ASMDataError('ASM DATA has a hole, overlap or invalid LEDATA extent')
        data.extend(content)
    if len(data) != segment.length:
        raise ASMDataError('ASM DATA has an uninitialized allocation tail')
    return bytes(data), {'boundary': 'complete_asm_data_SEGDEF', 'segment': {'index': segment.index,
        'name': segment.name, 'class_name': segment.class_name, 'attributes': segment.attributes,
        'length': segment.length}, 'publics': [asdict(p) for p in publics],
        'group': 'DGROUP', 'sha256': digest(data), 'emitted_mz_sites': [],
        'authored_c_credit': 0, 'function_credit': 0}


@dataclass(frozen=True)
class Build:
    object_bytes: bytes
    data: bytes
    metadata: dict
    provenance: dict


def assemble(source: Path, unit: dict, nasm='nasm'):
    validate_unit(unit)
    source_bytes = source.read_bytes()
    if digest(source_bytes) != unit['source_sha256']:
        raise ASMDataError('ASM DATA source SHA-256 pin mismatch')
    model = parse_source(source_bytes)
    if model['symbols'] != unit['symbols']:
        raise ASMDataError('ASM DATA source globals differ from the complete declared symbol list')
    executable = shutil.which(nasm)
    if executable is None:
        raise ASMDataError('ASM DATA assembler is unavailable')
    executable = Path(executable).resolve()
    if digest(executable.read_bytes()) != unit['assembler_sha256']:
        raise ASMDataError('ASM DATA assembler SHA-256 pin mismatch')
    with tempfile.TemporaryDirectory(prefix='bc-asm-data-') as tmp:
        scratch = Path(tmp); (scratch / 'UNIT.ASM').write_bytes(source_bytes)
        command = [str(executable), '-f', 'obj', 'UNIT.ASM', '-o', 'UNIT.OBJ']
        result = subprocess.run(command, cwd=scratch, capture_output=True, text=True, timeout=30)
        output = scratch / 'UNIT.OBJ'
        if result.returncode or not output.is_file():
            raise ASMDataError('ASM DATA assembly failed: ' + (result.stderr or result.stdout).strip())
        object_bytes = output.read_bytes()
    if digest(executable.read_bytes()) != unit['assembler_sha256']:
        raise ASMDataError('ASM DATA assembler changed during compilation')
    obj = read_omf(object_bytes); data, metadata = extract_data(obj, unit['symbols'])
    # Independent numeric source model authenticates all emitted storage and
    # public positions; it never supplies output bytes to the comparison.
    if (data != b''.join(struct.pack('<I', x) for x in model['numeric_values'])
            or {p['name']: p['offset'] for p in metadata['publics']} != model['offsets']):
        raise ASMDataError('ASM DATA object differs from its complete numeric source model')
    return Build(object_bytes, data, metadata, {'source_sha256': digest(source_bytes),
        'assembler_sha256': unit['assembler_sha256'], 'assembler_path': str(executable),
        'build_command': command, 'assembler_log': result.stdout + result.stderr,
        'object_sha256': digest(object_bytes), 'object_format': 'OMF16',
        'fresh_directory': True, 'numeric_DD_values': len(model['numeric_values']),
        'authored_c_credit': 0, 'function_credit': 0})
