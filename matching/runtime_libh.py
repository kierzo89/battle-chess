"""Fresh authentic-LINK backend for independently pinned LIBH runtime members.

No reference executable or expected bytes enter this runner. Archived objects
are passed unchanged to pinned Microsoft LINK in a fresh isolated DOS drive.
The C compiler's strict OMF reader is not relaxed for overlapping library data.
"""
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import re
import struct
import subprocess
import tempfile

from library16 import LibraryError, extract_member
from msc import compiler_config, validate_toolchain
from omf import _Cursor
from setup_libh import helper_config, validate_helpers
from setup_runtime import runtime_config, validate_runtime

HERE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class RuntimeLinkResult:
    image: bytes
    object_bytes: bytes
    provenance: dict


def member_layout(data):
    """Validate a narrow library object layout without synthesizing code bytes.

    Overlapping LEDATA writes are recorded, never merged here. Authentic LINK
    alone interprets them. Initially only a single initialized CODE segment,
    zero-length other segments, no externals and no FIXUPP are admitted.
    """
    position, ended, names = 0, False, ['']
    segments, publics, writes = {}, {}, []
    module_name = None
    while position < len(data):
        start = position
        if ended or position + 3 > len(data):
            raise LibraryError('invalid authentic-link object record boundary')
        kind, length = data[position], int.from_bytes(data[position + 1:position + 3], 'little')
        if length < 1 or position + 3 + length > len(data):
            raise LibraryError('truncated authentic-link object record')
        record = data[position:position + 3 + length]
        if sum(record) & 255:
            raise LibraryError('authentic-link object checksum mismatch')
        position += 3 + length
        cursor = _Cursor(record[3:-1])
        if kind == 0x80:
            if start != 0 or module_name is not None:
                raise LibraryError('authentic-link object requires one initial THEADR')
            module_name = cursor.name()
            cursor.finish()
        elif module_name is None:
            raise LibraryError('authentic-link object lacks THEADR')
        elif kind == 0x96:
            while cursor:
                names.append(cursor.name())
        elif kind == 0x98:
            attributes = cursor.byte()
            if attributes & 3 or attributes >> 5 == 0:
                raise LibraryError('unsupported authentic-link segment attributes')
            size = cursor.word()
            segment = {'index': len(segments) + 1, 'length': size,
                       'name_index': cursor.index(), 'class_index': cursor.index(),
                       'overlay_index': cursor.index(), 'attributes': attributes}
            cursor.finish()
            segments[segment['index']] = segment
        elif kind == 0x90:
            group, segment = cursor.index(), cursor.index()
            if segment == 0:
                raise LibraryError('absolute authentic-link publics unsupported')
            while cursor:
                name, offset, type_index = cursor.name(), cursor.word(), cursor.index()
                if name in publics:
                    raise LibraryError('duplicate authentic-link public')
                publics[name] = {'segment': segment, 'offset': offset, 'group': group, 'type_index': type_index}
        elif kind == 0xa0:
            segment, offset = cursor.index(), cursor.word()
            content = cursor.take(len(cursor.data) - cursor.pos)
            if segment not in segments or offset + len(content) > segments[segment]['length']:
                raise LibraryError('authentic-link LEDATA outside declared segment')
            overlaps = [{'start': max(offset, w['offset']),
                         'end': min(offset + len(content), w['offset'] + w['length'])}
                        for w in writes if w['segment'] == segment
                        and offset < w['offset'] + w['length'] and w['offset'] < offset + len(content)]
            writes.append({'record_offset': start, 'segment': segment, 'offset': offset,
                           'length': len(content), 'sha256': hashlib.sha256(content).hexdigest(), 'overlaps': overlaps})
        elif kind == 0x8a:
            if cursor.take(len(cursor.data) - cursor.pos) != b'\0':
                raise LibraryError('unsupported authentic-link MODEND start address')
            ended = True
        elif kind in (0x88, 0x9a):
            # Comments and groups remain unchanged for LINK to consume. There
            # are no external placements, data allocations or fixups here.
            pass
        else:
            raise LibraryError(f'unsupported authentic-link object record {kind:#x}; no externals/fixups admitted')
    if module_name is None or not ended:
        raise LibraryError('authentic-link object requires THEADR/MODEND')
    for segment in segments.values():
        try:
            segment['name'] = names[segment.pop('name_index')]
            segment['class_name'] = names[segment.pop('class_index')]
            names[segment.pop('overlay_index')]
        except IndexError as exc:
            raise LibraryError('authentic-link segment has undefined LNAMES index') from exc
    code = [segment for segment in segments.values() if segment['class_name'] == 'CODE' and segment['length']]
    if len(code) != 1 or any(s['length'] for s in segments.values() if s not in code):
        raise LibraryError('authentic-link backend requires exactly one nonempty CODE segment')
    selected = code[0]
    present = bytearray(selected['length'])
    for write in writes:
        if write['segment'] == selected['index']:
            present[write['offset']:write['offset'] + write['length']] = b'\1' * write['length']
    if not all(present):
        raise LibraryError('authentic-link CODE segment has uninitialized holes')
    for public in publics.values():
        if public['segment'] not in segments or public['offset'] > segments[public['segment']]['length']:
            raise LibraryError('authentic-link public outside declared segment')
    return {'module_name': module_name, 'segment': selected, 'publics': publics, 'data_writes': writes}


def load_member(member_id, project=HERE):
    """Check independent library/member pins and the complete public extent."""
    project = Path(project).resolve()
    config = helper_config(project)
    matches = [m for m in config['members'] if m['id'] == member_id]
    if len(matches) != 1:
        raise LibraryError('authentic-link member id must identify one pinned member')
    profile = matches[0]
    library_profile = profile.get('library_profile', 'libh')
    runtime_config_hash = None
    if library_profile == 'runtime500':
        supplied = runtime_config(project)
        runtime_config_hash = hashlib.sha256((project / 'config/runtime500.json').read_bytes()).hexdigest()
        # Only the existing independently pinned runtime profile is eligible.
        # Member identity and extent still come from the helper registry.
        fields = ('archive_url', 'archive_sha256', 'library_name', 'library_size',
                  'library_sha256', 'destination')
        config = dict(config, **{key: supplied[key] for key in fields})
        validator = validate_runtime
    elif library_profile == 'libh':
        validator = validate_helpers
    else:
        raise LibraryError('unknown authentic-link library profile')
    directory = (project / config['destination']).resolve()
    if not directory.is_relative_to(project):
        raise LibraryError('helper installation outside matching project')
    library = validator(directory, config)
    member = extract_member(library, profile['name'], config['library_sha256'],
                            profile['member_sha256'], validate_object=False)
    if member.offset != profile['library_offset']:
        raise LibraryError('authentic-link library member offset mismatch')
    layout = member_layout(member.data)
    layout['library_profile'] = library_profile
    layout['runtime_config_sha256'] = runtime_config_hash
    public = layout['publics'].get(profile['symbol'])
    if (layout['module_name'] != profile['name'] or layout['segment']['index'] != profile['segment']
            or layout['segment']['length'] != profile['code_size']
            or public is None or public['segment'] != profile['segment'] or public['offset'] != 0):
        raise LibraryError('authentic-link independent segment/public extent mismatch')
    return config, profile, member, layout


def mz_output(data, declared_code_size):
    """Return the entire declared MZ image and every emitted relocation site."""
    if len(data) < 28 or data[:2] != b'MZ':
        raise LibraryError('authentic LINK did not produce an MZ executable')
    tail, pages, count, paragraphs = struct.unpack_from('<4H', data, 2)
    if not pages or tail > 511:
        raise LibraryError('invalid authentic LINK MZ size')
    size = (pages - 1) * 512 + (tail or 512)
    header = paragraphs * 16
    table = int.from_bytes(data[24:26], 'little')
    if size != len(data) or not 28 <= header <= size or table < 28 or table + 4 * count > header:
        raise LibraryError('authentic LINK MZ bounds/overlay mismatch')
    image = bytes(data[header:])
    if len(image) != declared_code_size:
        raise LibraryError('complete authentic LINK image differs from independently declared CODE size')
    relocations = []
    for index in range(count):
        offset, segment = struct.unpack_from('<HH', data, table + index * 4)
        site = segment * 16 + offset
        if site + 2 > len(image) or site in relocations:
            raise LibraryError('invalid/duplicate authentic LINK MZ relocation site')
        relocations.append(site)
    if relocations:
        raise LibraryError('relocatable authentic-link helper members are not supported yet')
    return image, tuple(relocations), {'header_bytes': header, 'file_bytes': size,
                                     'minalloc': int.from_bytes(data[10:12], 'little'),
                                     'maxalloc': int.from_bytes(data[12:14], 'little')}


def link_member(member_id, project=HERE, dosbox='dosbox', timeout=30):
    """Freshly link one independent helper; accepts no reference bytes."""
    project = Path(project).resolve()
    config, profile, member, layout = load_member(member_id, project)
    if config['linker_profile'] != 'msc510' or config['linker_name'] != 'LINK.EXE':
        raise LibraryError('authentic-link backend requires the pinned official LINK profile')
    manifest_hash, hashes = validate_toolchain(project / 'toolchains/msc510', compiler='msc510')
    tool_profile = compiler_config('msc510')
    entry = next(e for e in tool_profile['files'] if e['name'] == config['linker_name'])
    if entry['sha256'] != config['linker_sha256'] or entry['size'] != config['linker_size']:
        raise LibraryError('authentic LINK config differs from independent toolchain pin')
    linker = (project / 'toolchains/msc510/LINK.EXE').read_bytes()
    if hashlib.sha256(linker).hexdigest() != config['linker_sha256']:
        raise LibraryError('authentic LINK tool hash mismatch')
    with tempfile.TemporaryDirectory(prefix='bc-libh-link-') as temp:
        root = Path(temp)
        if any(c in str(root) for c in '\r\n"'):
            raise LibraryError('DOSBox helper mount path has unsupported characters')
        drive, tools = root / 'drive', root / 'tools'
        drive.mkdir()
        tools.mkdir()
        (drive / 'UNIT.OBJ').write_bytes(member.data)
        (tools / 'LINK.EXE').write_bytes(linker)
        command = ('T:\\LINK', '/NOD', 'UNIT.OBJ,UNIT.EXE,UNIT.MAP;')
        batch = ('@echo off\r\n' + ' '.join(command) + ' > LINK.LOG\r\n'
                 'if errorlevel 1 goto failed\r\necho success > SUCCESS.TXT\r\ngoto done\r\n'
                 ':failed\r\necho failed > FAILED.TXT\r\n:done\r\nexit\r\n')
        (drive / 'BUILD.BAT').write_bytes(batch.encode('ascii'))
        conf = root / 'dosbox.conf'
        conf.write_text('[sdl]\nfullscreen=false\noutput=surface\n[mixer]\nnosound=true\n'
                        '[cpu]\ncore=normal\ncycles=max\n[autoexec]\nmount c "' + str(drive)
                        + '"\nmount t "' + str(tools) + '" -ro\nc:\nBUILD.BAT\n')
        try:
            completed = subprocess.run([str(dosbox), '-conf', str(conf), '-noconsole'],
                         env=dict(os.environ, SDL_VIDEODRIVER='dummy', SDL_AUDIODRIVER='dummy'),
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise RuntimeError('Authentic helper LINK failed or timed out') from exc
        log = (drive / 'LINK.LOG').read_bytes().decode('cp437') if (drive / 'LINK.LOG').exists() else ''
        if (completed.returncode or not (drive / 'SUCCESS.TXT').exists() or (drive / 'FAILED.TXT').exists()
                or not (drive / 'UNIT.EXE').exists() or not (drive / 'UNIT.MAP').exists()):
            raise RuntimeError('Authentic helper LINK failed:\n' + log + '\n' + completed.stdout.decode(errors='replace'))
        executable = (drive / 'UNIT.EXE').read_bytes()
        map_text = (drive / 'UNIT.MAP').read_bytes().decode('cp437')
    image, relocations, mz = mz_output(executable, layout['segment']['length'])
    maps = re.findall(r'^\s*([0-9A-F]+)H\s+([0-9A-F]+)H\s+([0-9A-F]+)H\s+(\S+)\s+CODE\s*$', map_text, re.M)
    if len(maps) != 1 or int(maps[0][0], 16) != 0 or int(maps[0][2], 16) != len(image):
        raise LibraryError('authentic LINK map disagrees with complete CODE image')
    provenance = {'classification': 'independently_supplied_runtime_library_authentic_LINK',
                  'authored_c_credit': 0, 'member_id': member_id, 'source': 'config/runtime_libh.json',
                  'config_sha256': hashlib.sha256((project / 'config/runtime_libh.json').read_bytes()).hexdigest(),
                  'library_profile': layout['library_profile'],
                  'runtime_config_sha256': layout['runtime_config_sha256'],
                  'library_sha256': config['library_sha256'], 'archive_url': config['archive_url'],
                  'archive_sha256': config['archive_sha256'], 'member_sha256': member.sha256,
                  'library_member_offset': member.offset, 'linker_sha256': hashes['LINK.EXE'],
                  'linker_toolchain_manifest_sha256': manifest_hash,
                  'linker_repository': tool_profile['repository'], 'linker_commit': tool_profile['commit'],
                  'build_command': list(command), 'linker_log': log, 'linker_map': map_text,
                  'linked_executable_sha256': hashlib.sha256(executable).hexdigest(),
                  'linked_image_sha256': hashlib.sha256(image).hexdigest(), 'mz': mz,
                  'mz_relocations': list(relocations), 'reference_executable_read_or_mounted': False,
                  'segment': layout['segment'], 'publics': layout['publics'],
                  'independent_data_writes': layout['data_writes']}
    return RuntimeLinkResult(image, member.data, provenance)
