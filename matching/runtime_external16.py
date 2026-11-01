"""Narrow authentic-LINK runtime backend for pinned ALDIV and real dependencies.

Overlapping library records are retained unchanged. No ordinary OMF admission,
reference input, target placement, source compilation, or C credit occurs here.
"""
from dataclasses import dataclass, asdict
import hashlib
import os
from pathlib import Path
import re
import struct
import subprocess
import tempfile
from types import SimpleNamespace

from library16 import LibraryError, extract_member
from msc import compiler_config, validate_toolchain
from omf import _Cursor, _fixupp, OMFError
from setup_libh import helper_config, validate_helpers

HERE = Path(__file__).resolve().parent
LIBRARY_SHA256 = '768bfe171ebcad6d44aeca830ec8d19b31f02ce84ab35c81fc48fcf3f1e14858'
LINKER_SHA256 = '124a3c800edc16b60f696d35a9dfec798b68b78fe2ca90c5988ea76bdeab1a8a'
SPECS = {
    'ALDIV': {'sha256': '18905d8050ba88e8a17003d80c15506a7c73e8005a460496e6612e472730a459',
              'offset': 8160, 'file_size': 203, 'size': 34,
              'publics': ['__aNFbldiv', '__aNNaldiv'], 'external': '__aNldiv',
              'field': 18, 'writes': [(0, 32), (31, 3)]},
    'LDIV': {'sha256': '6e210aff6aee94d45d3c8a9c8d91710fa77473eafbba5175ac64e9a064169af9',
             'offset': 7056, 'file_size': 308, 'size': 163,
             'publics': ['__aNldiv'], 'external': '__aNulmul',
             'field': 122, 'writes': [(0, 161), (160, 3)]},
    'LMUL': {'sha256': 'b0e033a1674414d4a985ad87daee47357fc7730ed67800f20ab4de7f6384bb1d',
             'offset': 7376, 'file_size': 200, 'size': 52,
             'publics': ['__aNlmul', '__aNulmul'], 'external': None,
             'field': None, 'writes': [(0, 25), (24, 26), (49, 3)]},
}


def _sha(data):
    return hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class RuntimeExternalResult:
    image: bytes
    object_bytes: bytes
    provenance: dict


def _layout(data, name):
    """Validate structural ownership; never merge or relocate LEDATA contents."""
    if name not in SPECS:
        raise LibraryError('unknown external runtime member')
    spec = SPECS[name]
    pos, ended, names = 0, False, ['']
    segments, publics, externals, groups, writes, records = [], {}, {}, [], [], []
    module = None
    obj, last, threads = SimpleNamespace(fixups=[]), None, {}
    try:
        while pos < len(data):
            start = pos
            if ended or pos + 3 > len(data):
                raise LibraryError('external runtime record boundary/trailing data')
            kind, length = data[pos], int.from_bytes(data[pos + 1:pos + 3], 'little')
            if length < 1 or pos + 3 + length > len(data):
                raise LibraryError('truncated external runtime record')
            raw = data[pos:pos + 3 + length]
            if sum(raw) & 255:
                raise LibraryError('external runtime record checksum mismatch')
            pos += 3 + length
            payload = raw[3:-1]
            records.append({'offset': start, 'kind': kind, 'length': len(raw), 'sha256': _sha(raw)})
            c = _Cursor(payload)
            if kind == 0x80:
                if start or module is not None:
                    raise LibraryError('external runtime requires one initial THEADR')
                module = c.name()
                c.finish()
            elif module is None:
                raise LibraryError('external runtime missing THEADR')
            elif kind == 0x88:
                if payload != b'\x00\xa3' + bytes([len('an' + name.lower())]) + ('an' + name.lower()).encode():
                    # ALDIV uses annaldiv rather than analdiv in the assembler name.
                    if name != 'ALDIV' or payload != b'\x00\xa3\x08annaldiv':
                        raise LibraryError('unexpected external runtime COMMENT')
            elif kind == 0x96:
                while c:
                    names.append(c.name())
            elif kind == 0x98:
                attributes, size = c.byte(), c.word()
                sn, cl, ov = c.index(), c.index(), c.index()
                c.finish()
                if not all(0 < i < len(names) for i in (sn, cl, ov)):
                    raise LibraryError('external runtime undefined LNAMES index')
                segments.append({'index': len(segments) + 1, 'attributes': attributes,
                                 'length': size, 'name': names[sn], 'class_name': names[cl],
                                 'overlay': names[ov]})
            elif kind == 0x9a:
                group_name = c.index()
                members = []
                while c:
                    if c.byte() != 0xff:
                        raise LibraryError('external runtime unsupported group component')
                    members.append(c.index())
                groups.append({'name': names[group_name], 'segments': members})
            elif kind == 0x8c:
                while c:
                    symbol, type_index = c.name(), c.index()
                    if type_index:
                        raise LibraryError('external runtime nonzero external type')
                    externals[len(externals) + 1] = symbol
            elif kind == 0x90:
                group, segment = c.index(), c.index()
                if not segment:
                    raise LibraryError('external runtime absolute public unsupported')
                while c:
                    symbol, offset, typ = c.name(), c.word(), c.index()
                    if symbol in publics:
                        raise LibraryError('duplicate external runtime public')
                    publics[symbol] = {'segment': segment, 'offset': offset, 'group': group, 'type_index': typ}
            elif kind == 0xa0:
                segment, offset = c.index(), c.word()
                content = c.take(len(c.data) - c.pos)
                if segment != 1 or offset + len(content) > spec['size']:
                    raise LibraryError('external runtime data outside whole CODE extent')
                overlaps = [{'start': max(offset, w['offset']),
                             'end': min(offset + len(content), w['offset'] + w['length'])}
                            for w in writes if max(offset, w['offset']) < min(offset + len(content), w['offset'] + w['length'])]
                writes.append({'record_offset': start, 'segment': segment, 'offset': offset,
                               'length': len(content), 'sha256': _sha(content), 'overlaps': overlaps})
                if spec['field'] is not None and offset <= spec['field'] < offset + len(content):
                    field = spec['field'] - offset
                    if content[field:field + 2] != b'\x00\x00' or field == 0 or content[field - 1] != 0xe8:
                        raise LibraryError('external runtime relative call requires zero source field')
                last = segment, offset, len(content)
            elif kind == 0x9c:
                _fixupp(obj, payload, last, threads, start)
            elif kind == 0x8a:
                if payload != b'\0':
                    raise LibraryError('external runtime MODEND start unsupported')
                ended = True
            else:
                raise LibraryError('unsupported external runtime allocation/record')
    except (OMFError, IndexError, UnicodeError) as exc:
        if isinstance(exc, LibraryError):
            raise
        raise LibraryError('malformed external runtime metadata: ' + str(exc)) from exc
    if not ended or module != name:
        raise LibraryError('external runtime module/THEADR/MODEND mismatch')
    if names != ['', '', 'CODE', 'DATA', 'DGROUP', '_DATA', '_TEXT']:
        raise LibraryError('external runtime LNAMES shape mismatch')
    expected_segments = [dict(index=1, attributes=0x48, length=spec['size'], name='_TEXT', class_name='CODE', overlay=''),
                         dict(index=2, attributes=0x48, length=0, name='_DATA', class_name='DATA', overlay='')]
    if segments != expected_segments or groups != [{'name': 'DGROUP', 'segments': [2]}]:
        raise LibraryError('external runtime whole allocation/group mismatch')
    if publics != {n: dict(segment=1, offset=0, group=0, type_index=0) for n in spec['publics']}:
        raise LibraryError('external runtime public extent/aliases mismatch')
    if [(w['offset'], w['length']) for w in writes] != spec['writes']:
        raise LibraryError('external runtime LEDATA ownership/hole/overlap mismatch')
    if any(w['overlaps'] != ([{'start': w['offset'], 'end': w['offset'] + 1}] if i else [])
           for i, w in enumerate(writes)):
        raise LibraryError('external runtime overwrite extent mismatch')
    expected_externals = {1: spec['external']} if spec['external'] else {}
    if externals != expected_externals:
        raise LibraryError('external runtime external dependency mismatch')
    if len(obj.fixups) != int(spec['field'] is not None):
        raise LibraryError('external runtime fixup count mismatch')
    for f in obj.fixups:
        if (f.segment, f.offset, f.width, f.location_type, f.segment_relative, f.frame, f.target, f.displacement) != (1, spec['field'], 2, 1, False, (0, 1), (2, 1), None):
            raise LibraryError('external runtime relative fixup shape mismatch')
        if any(w['record_offset'] > f.record_offset and w['offset'] < f.offset + 2 and f.offset < w['offset'] + w['length'] for w in writes):
            raise LibraryError('external runtime fixup overwritten by later data')
    kinds = [r['kind'] for r in records]
    expected = [0x80, 0x88, 0x96, 0x98, 0x98, 0x9a]
    expected += ([0x8c, 0xa0, 0x9c, 0xa0] if spec['external'] else [0xa0, 0xa0, 0xa0])
    expected += [0x90] * len(spec['publics']) + [0x8a]
    if kinds != expected:
        raise LibraryError('external runtime record ordering/count mismatch')
    return {'module_name': name, 'segment': segments[0], 'segments': segments, 'groups': groups,
            'publics': publics, 'externals': externals, 'fixups': [asdict(f) | {'raw': f.raw.hex()} for f in obj.fixups],
            'data_writes': writes, 'records': records}


def load_profile(member_id, project=HERE):
    """Load only known near_aldiv and its fully pinned genuine dependencies."""
    if member_id != 'near_aldiv':
        raise LibraryError('unknown external runtime profile')
    project = Path(project).resolve()
    config = helper_config(project)
    if (config.get('library_sha256') != LIBRARY_SHA256 or config.get('destination') != 'toolchains/runtime-libh'
            or config.get('library_name') != 'LIBH.LIB' or config.get('library_size') != 13689
            or config.get('archive_sha256') != '18a0c57eadf4eea0eb236a0e16f57019c6fd05789dfc52d857b84f6bf7edf58c'
            or config.get('archive_path') != '/LIB/LIBH.LIB'
            or config.get('linker_profile') != 'msc510' or config.get('linker_name') != 'LINK.EXE'
            or config.get('linker_sha256') != LINKER_SHA256 or config.get('linker_size') != 65539):
        raise LibraryError('external runtime requires independently pinned library/tool configuration')
    library = validate_helpers(project / config['destination'], config)
    members = {}
    for name, spec in SPECS.items():
        member = extract_member(library, name, LIBRARY_SHA256, spec['sha256'], validate_object=False)
        if member.offset != spec['offset'] or len(member.data) != spec['file_size']:
            raise LibraryError('external runtime independent member placement/size mismatch')
        layout = _layout(member.data, name)
        members[name] = dict(layout, object_bytes=member.data, object_sha256=member.sha256,
                             library_offset=member.offset, object_size=len(member.data))
    return dict(members['ALDIV'], id=member_id, name='ALDIV', symbol='__aNNaldiv', code_size=34,
                library_sha256=LIBRARY_SHA256, config=config,
                config_sha256=_sha((project / 'config/runtime_libh.json').read_bytes()), members=members)


def _output(executable, map_text, profile, order):
    """Account for the complete image, declared segments, alignment and MZ table."""
    if len(executable) < 28 or executable[:2] != b'MZ':
        raise LibraryError('external runtime LINK output is not MZ')
    h = struct.unpack_from('<14H', executable)
    if not h[2] or h[1] > 511:
        raise LibraryError('external runtime MZ size invalid')
    size, header, table = (h[2] - 1) * 512 + (h[1] or 512), h[4] * 16, h[12]
    if size != len(executable) or not 28 <= header <= size or table < 28 or table + h[3] * 4 > header or h[13]:
        raise LibraryError('external runtime MZ full image/overlay bounds invalid')
    image = executable[header:]
    mz = []
    for j in range(h[3]):
        off, seg = struct.unpack_from('<HH', executable, table + 4 * j)
        site = seg * 16 + off
        if site + 2 > len(image) or any(abs(site - s) < 2 for s in mz):
            raise LibraryError('external runtime MZ word bounds/overlap invalid')
        mz.append(site)
    if mz:
        raise LibraryError('external runtime unexpected MZ relocation')
    maps = re.findall(r'^\s*([0-9A-F]+)H\s+([0-9A-F]+)H\s+([0-9A-F]+)H\s+(\S+)\s+(\S+)\s*$', map_text, re.M)
    nonzero = [(int(a, 16), int(b, 16), int(n, 16), name, cl) for a, b, n, name, cl in maps if int(n, 16)]
    if len(nonzero) != 1 or nonzero[0][0] != 0 or nonzero[0][3:] != ('_TEXT', 'CODE'):
        raise LibraryError('external runtime MAP has unexpected complete allocation')
    expected_size, allocations = 0, []
    for name in order:
        alignment = (-expected_size) % 2
        if alignment:
            allocations.append({'classification': 'authentic_LINK_word_alignment', 'origin': expected_size,
                                'size': alignment, 'sha256': _sha(image[expected_size:expected_size + alignment])})
        expected_size += alignment
        n = profile['members'][name]['segment']['length']
        allocations.append({'name': name, 'origin': expected_size, 'size': n,
                            'sha256': _sha(image[expected_size:expected_size + n]),
                            'object_sha256': profile['members'][name]['object_sha256'],
                            'zero_length_DATA': profile['members'][name]['segments'][1]})
        expected_size += n
    if len(image) != expected_size or nonzero[0][:3] != (0, expected_size - 1, expected_size):
        raise LibraryError('external runtime complete CODE/alignment size mismatch')
    if [(int(a, 16), int(b, 16), int(n, 16), name, cl) for a, b, n, name, cl in maps] != [
            (0, expected_size - 1, expected_size, '_TEXT', 'CODE'),
            (expected_size, expected_size, 0, '_DATA', 'DATA')]:
        raise LibraryError('external runtime MAP zero DATA allocation mismatch')
    groups = re.findall(r'^\s*([0-9A-F]{4}):0\s+(\S+)\s*$', map_text, re.M)
    if groups != [(format(expected_size // 16, '04X'), 'DGROUP')]:
        raise LibraryError('external runtime MAP group frame mismatch')
    parts = map_text.split('Publics by Name')
    if len(parts) != 2 or len(parts[1].split('Publics by Value')) != 2:
        raise LibraryError('external runtime missing unique public MAP sections')
    rows = re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(\S+)\s*$', parts[1].split('Publics by Value')[0], re.M)
    publics = {}
    for seg, off, symbol in rows:
        if symbol in publics:
            raise LibraryError('external runtime duplicate MAP public')
        publics[symbol] = {'segment': int(seg, 16), 'offset': int(off, 16)}
    expected_publics = {}
    for a in allocations:
        if 'name' in a:
            expected_publics.update({n: {'segment': 0, 'offset': a['origin']} for n in profile['members'][a['name']]['publics']})
    if publics != expected_publics:
        raise LibraryError('external runtime MAP public extent/dependency mismatch')
    fields = []
    for a in allocations:
        if 'name' not in a:
            continue
        spec = SPECS[a['name']]
        if spec['external'] is None:
            continue
        field, origin = spec['field'], a['origin']
        target = publics[spec['external']]
        value = (target['offset'] - (origin + field + 2)) & 65535
        if image[origin + field:origin + field + 2] != value.to_bytes(2, 'little'):
            raise LibraryError('external runtime authentic field disagrees with actual MAP')
        fields.append({'member': a['name'], 'offset': field, 'image_offset': origin + field,
                       'location_type': 1, 'width': 2, 'mode': 'relative16',
                       'external': spec['external'], 'target': target,
                       'source_origin': origin, 'encoded_hex': value.to_bytes(2, 'little').hex()})
    selected = next(a for a in allocations if a.get('name') == 'ALDIV')
    origin = selected['origin']
    return image[origin:origin + 34], dict(full_image_sha256=_sha(image), full_image_size=len(image),
        full_image_hex=image.hex(), MZ_header=list(h), MZ_relocations=mz,
        complete_allocations=allocations, actual_publics=publics, actual_fixups=fields,
        member_origin=origin, member_MZ_relocations=[], member_size=34,
        member_sha256=_sha(image[origin:origin + 34]))


def build(member_id, project=HERE, *, dosbox='dosbox', timeout=30):
    """Fresh target-free generation from three unchanged independently pinned objects."""
    project = Path(project).resolve()
    profile = load_profile(member_id, project)
    config = profile['config']
    manifest, hashes = validate_toolchain(project / 'toolchains/msc510', compiler='msc510')
    toolspec = next(e for e in compiler_config('msc510')['files'] if e['name'] == 'LINK.EXE')
    if toolspec['sha256'] != LINKER_SHA256 or toolspec['size'] != 65539:
        raise LibraryError('external runtime independent LINK pin mismatch')
    linker = (project / 'toolchains/msc510/LINK.EXE').read_bytes()
    if _sha(linker) != LINKER_SHA256:
        raise LibraryError('external runtime LINK hash mismatch')
    order = ['ALDIV', 'LDIV', 'LMUL']
    command = ['T:\\LINK', '/NOD', '/NOFARCALLTRANSLATION', '/MAP',
               '+'.join(n + '.OBJ' for n in order) + ',UNIT.EXE,UNIT.MAP;']
    with tempfile.TemporaryDirectory(prefix='bc-runtime-external16-') as tmp:
        root = Path(tmp)
        if any(c in str(root) for c in '\r\n"'):
            raise LibraryError('external runtime unsupported mount path')
        drive, tools = root / 'drive', root / 'tools'
        drive.mkdir(); tools.mkdir()
        for name in order:
            (drive / (name + '.OBJ')).write_bytes(profile['members'][name]['object_bytes'])
        (tools / 'LINK.EXE').write_bytes(linker)
        batch = ('@echo off\r\n' + ' '.join(command) + ' > LINK.LOG\r\n'
                 'if errorlevel 1 goto failed\r\necho success > SUCCESS.TXT\r\ngoto done\r\n'
                 ':failed\r\necho failed > FAILED.TXT\r\n:done\r\nexit\r\n')
        (drive / 'BUILD.BAT').write_bytes(batch.encode('ascii'))
        conf = root / 'dosbox.conf'
        conf.write_text('[sdl]\noutput=surface\n[mixer]\nnosound=true\n[cpu]\ncycles=max\n[autoexec]\n'
                        'mount c "' + str(drive) + '"\nmount t "' + str(tools) + '" -ro\nc:\nBUILD.BAT\n')
        try:
            done = subprocess.run([str(dosbox), '-conf', str(conf), '-noconsole'],
                env=dict(os.environ, SDL_VIDEODRIVER='dummy', SDL_AUDIODRIVER='dummy'),
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise RuntimeError('external runtime authentic LINK failed/timed out') from exc
        log = (drive / 'LINK.LOG').read_bytes().decode('cp437') if (drive / 'LINK.LOG').exists() else ''
        if (done.returncode or not (drive / 'SUCCESS.TXT').exists() or (drive / 'FAILED.TXT').exists()
                or not (drive / 'UNIT.EXE').exists() or not (drive / 'UNIT.MAP').exists()):
            raise RuntimeError('external runtime authentic LINK failed: ' + log)
        executable = (drive / 'UNIT.EXE').read_bytes()
        map_text = (drive / 'UNIT.MAP').read_bytes().decode('cp437')
    image, output = _output(executable, map_text, profile, order)
    provenance = dict(output, classification='independently_supplied_runtime_library_authentic_LINK_external16',
        authored_c_credit=0, member_id=member_id, library_sha256=LIBRARY_SHA256,
        archive_url=config['archive_url'], archive_sha256=config['archive_sha256'],
        config_sha256=profile['config_sha256'], object_order=order,
        members={n: dict({k: v for k, v in profile['members'][n].items() if k != 'object_bytes'},
                         object_hex=profile['members'][n]['object_bytes'].hex()) for n in order},
        linker_sha256=hashes['LINK.EXE'], linker_toolchain_manifest_sha256=manifest,
        build_command=command, linker_log=log, linker_map=map_text,
        linked_executable_sha256=_sha(executable), linked_executable_hex=executable.hex(),
        reference_executable_read_or_mounted=False, mounted_inputs=[n + '.OBJ' for n in order] + ['BUILD.BAT', 'LINK.EXE'])
    return RuntimeExternalResult(image, profile['object_bytes'], provenance)


def relocate_for_comparison(unit, authentic):
    """Regenerate only ALDIV's one OMF call field at explicit destination placements.

    This is distinct from generation: it accepts no reference bytes. No other
    byte changes, and actual source field/public/MAP provenance is rechecked.
    """
    if not isinstance(authentic, RuntimeExternalResult):
        raise LibraryError('external runtime comparison requires authentic result')
    p = authentic.provenance
    if (p.get('member_id') != 'near_aldiv' or p.get('classification') != 'independently_supplied_runtime_library_authentic_LINK_external16'
            or p.get('reference_executable_read_or_mounted') is not False
            or p.get('linker_sha256') != LINKER_SHA256 or p.get('library_sha256') != LIBRARY_SHA256
            or len(authentic.image) != 34 or _sha(authentic.object_bytes) != SPECS['ALDIV']['sha256']):
        raise LibraryError('external runtime comparison authentic provenance mismatch')
    try:
        profile_members = {}
        for name, spec in SPECS.items():
            d = p['members'][name]
            raw = bytes.fromhex(d['object_hex'])
            expected = dict(_layout(raw, name), object_hex=raw.hex(), object_sha256=_sha(raw),
                            library_offset=spec['offset'], object_size=len(raw))
            if (_sha(raw) != spec['sha256'] or len(raw) != spec['file_size'] or d != expected):
                raise LibraryError('external runtime comparison member provenance mismatch')
            profile_members[name] = d
        exe = bytes.fromhex(p['linked_executable_hex'])
        image, verified = _output(exe, p['linker_map'], {'members': profile_members}, ['ALDIV', 'LDIV', 'LMUL'])
        if _sha(exe) != p['linked_executable_sha256'] or image != authentic.image:
            raise LibraryError('external runtime comparison full authentic image mismatch')
        for k, v in verified.items():
            if p.get(k) != v:
                raise LibraryError('external runtime comparison output provenance mismatch: ' + k)
    except (KeyError, TypeError, ValueError) as exc:
        raise LibraryError('external runtime comparison incomplete provenance') from exc
    if (not isinstance(unit, dict) or unit.get('symbol') != '__aNNaldiv'
            or type(unit.get('size')) is not int or unit['size'] != 34
            or not isinstance(unit.get('externals'), dict) or set(unit['externals']) != {'__aNldiv'}
            or unit.get('language', 'runtime') != 'runtime'
            or unit.get('member', 'near_aldiv') != 'near_aldiv'
            or unit.get('backend', 'msc500-authentic-external16') != 'msc500-authentic-external16'):
        raise LibraryError('external runtime comparison requires exact public/size/named binding')
    origin = unit.get('image_offset')
    if isinstance(origin, str):
        try:
            origin = int(origin, 0)
        except ValueError as exc:
            raise LibraryError('external runtime comparison invalid origin') from exc
    binding = unit['externals']['__aNldiv']
    if (not isinstance(binding, dict) or set(binding) != {'segment', 'offset'}
            or any(type(v) is not int or not 0 <= v <= 65535 for v in binding.values())
            or binding['segment'] != 0 or type(origin) is not int or not 0 <= origin <= 65536 - 34):
        raise LibraryError('external runtime comparison requires explicit same-frame 16-bit placement')
    value = (binding['offset'] - (origin + 18 + 2)) & 65535
    output = authentic.image[:18] + value.to_bytes(2, 'little') + authentic.image[20:]
    relocation = dict(object_offset=18, width=2, location_type=1, mode='relative16',
        external='__aNldiv', source_origin=p['member_origin'],
        source_target=p['actual_publics']['__aNldiv'], source_encoded_hex=authentic.image[18:20].hex(),
        comparison_origin=origin, comparison_target=binding,
        encoded_hex=value.to_bytes(2, 'little').hex(), mz_segment_relocations=[],
        formula='(target_offset - (origin + object_offset + width)) & 0xffff')
    return RuntimeExternalResult(output, authentic.object_bytes,
        dict(p, comparison_relocation=relocation, comparison_image_sha256=_sha(output)))
