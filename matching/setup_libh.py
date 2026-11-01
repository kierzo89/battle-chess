#!/usr/bin/env python3
"""Explicitly install the independently pinned MSC5.00 LIBH runtime library."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import struct
import tempfile

from setup_toolchain import _download

HERE = Path(__file__).resolve().parent
FIELDS = ('archive_url', 'archive_sha256', 'archive_path', 'library_name', 'library_size', 'library_sha256')


def helper_config(project=HERE):
    return json.loads((Path(project) / 'config/runtime_libh.json').read_text())


def archive_member(raw, path):
    """Read one root/nested FAT12 file from a PCjs CHS/dword disk JSON."""
    media = json.loads(raw)
    info = media['imageInfo']
    cylinders, heads = info['cylinders'], info['heads']
    tracks, size = info.get('trackDefault', 9), info.get('sectorDefault', 512)
    if size != 512 or not 0 < cylinders * heads * tracks <= 8192:
        raise ValueError('Unsupported helper archive geometry')
    sectors = {}
    for cylinder in media['diskData']:
        for head in cylinder:
            for sector in head:
                c, h, s = sector['c'], sector['h'], sector['s']
                words = sector['d']
                if (not 0 <= c < cylinders or not 0 <= h < heads or not 1 <= s <= tracks
                        or sector.get('l', size) != size or not words or len(words) > size // 4):
                    raise ValueError('Invalid helper archive sector')
                key = c, h, s
                if key in sectors:
                    raise ValueError('Duplicate helper archive sector')
                content = b''.join(struct.pack('<I', word & 0xffffffff) for word in words)
                content += struct.pack('<I', words[-1] & 0xffffffff) * ((size - len(content)) // 4)
                sectors[key] = content
    if len(sectors) != cylinders * heads * tracks:
        raise ValueError('Missing helper archive sector')
    disk = b''.join(sectors[key] for key in sorted(sectors))
    bps, spc = int.from_bytes(disk[11:13], 'little'), disk[13]
    reserved, fats = int.from_bytes(disk[14:16], 'little'), disk[16]
    roots, fat_size = int.from_bytes(disk[17:19], 'little'), int.from_bytes(disk[22:24], 'little')
    if bps != 512 or spc not in (1, 2, 4, 8, 16, 32, 64, 128) or not reserved or not fats or not fat_size:
        raise ValueError('Invalid helper FAT12 BPB')
    root = (reserved + fats * fat_size) * bps
    data_start = root + ((roots * 32 + bps - 1) // bps) * bps
    if not root < data_start <= len(disk):
        raise ValueError('Invalid helper FAT12 layout')
    fat = disk[reserved * bps:(reserved + fat_size) * bps]

    def chain(cluster):
        content, seen = bytearray(), set()
        while cluster < 0xff8:
            if not 2 <= cluster < 0xff0 or cluster in seen:
                raise ValueError('Invalid or looping helper FAT12 chain')
            seen.add(cluster)
            start = data_start + (cluster - 2) * spc * bps
            if start + spc * bps > len(disk):
                raise ValueError('Helper FAT12 cluster outside disk')
            content.extend(disk[start:start + spc * bps])
            offset = cluster + cluster // 2
            if offset + 2 > len(fat):
                raise ValueError('Helper FAT12 entry outside table')
            word = int.from_bytes(fat[offset:offset + 2], 'little')
            cluster = word >> 4 if cluster & 1 else word & 0xfff
        return bytes(content)

    parts = path.strip('/').split('/')
    if not parts or any(not part or part in ('.', '..') for part in parts):
        raise ValueError('Invalid helper archive member path')
    directory = disk[root:root + roots * 32]
    for index, part in enumerate(parts):
        found = []
        for offset in range(0, len(directory), 32):
            entry = directory[offset:offset + 32]
            if len(entry) != 32 or entry[0] == 0:
                break
            if entry[0] == 0xe5 or entry[11] & 0x08:
                continue
            name = entry[:8].decode('ascii').rstrip()
            extension = entry[8:11].decode('ascii').rstrip()
            name += '.' + extension if extension else ''
            if name == part:
                found.append(entry)
        if len(found) != 1:
            raise ValueError('Helper archive member path is absent or ambiguous')
        entry = found[0]
        content = chain(int.from_bytes(entry[26:28], 'little'))
        if index != len(parts) - 1:
            if not entry[11] & 0x10:
                raise ValueError('Helper archive path traverses a regular file')
            directory = content
        else:
            if entry[11] & 0x10:
                raise ValueError('Helper archive member is a directory')
            length = int.from_bytes(entry[28:32], 'little')
            if length > len(content):
                raise ValueError('Truncated helper archive file')
            return content[:length]


def validate_helpers(destination, config):
    destination = Path(destination)
    manifest = json.loads((destination / 'manifest.json').read_text())
    if manifest != {key: config[key] for key in FIELDS}:
        raise ValueError('Helper runtime manifest differs from pinned configuration')
    data = (destination / config['library_name']).read_bytes()
    if len(data) != config['library_size'] or hashlib.sha256(data).hexdigest() != config['library_sha256']:
        raise ValueError('Helper runtime library differs from pinned configuration')
    return data


def install(destination=None, archive=None):
    config = helper_config()
    destination = Path(destination or HERE / config['destination']).resolve()
    if destination.exists():
        validate_helpers(destination, config)
        return destination
    raw = Path(archive).read_bytes() if archive else _download(config['archive_url'], config['archive_sha256'])
    if hashlib.sha256(raw).hexdigest() != config['archive_sha256']:
        raise ValueError('Helper archive SHA-256 mismatch')
    library = archive_member(raw, config['archive_path'])
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.libh-', dir=destination.parent) as temp:
        stage = Path(temp) / 'runtime-libh'
        stage.mkdir()
        (stage / config['library_name']).write_bytes(library)
        (stage / config['archive_name']).write_bytes(raw)
        (stage / 'manifest.json').write_text(json.dumps({key: config[key] for key in FIELDS}, indent=2) + '\n')
        validate_helpers(stage, config)
        shutil.move(str(stage), destination)
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path)
    parser.add_argument('--archive', type=Path)
    args = parser.parse_args()
    print(install(args.destination, args.archive))
