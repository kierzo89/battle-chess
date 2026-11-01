#!/usr/bin/env python3
"""Explicitly install a pinned Microsoft compiler profile.

msc510: Microsoft's MIT-licensed MS-DOS repository tools.
msc400/msc500: historical proprietary installation disks preserved by PCjs; no MIT
or redistribution-permission claim is attached to this separate profile.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import struct
import tempfile
import urllib.request

from msc import (COMPILERS, compiler_config, default_toolchain,
                 manifest_fields, validate_toolchain)


def _download(url, expected, size=None):
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read(16 * 1024 * 1024)
    if hashlib.sha256(data).hexdigest() != expected or (size is not None and len(data) != size):
        raise ValueError('Downloaded input does not match pinned hash: ' + url)
    return data


def archive_files(raw, names):
    """Extract selected root files from pinned PCjs CHS/dword FAT12 media."""
    media = json.loads(raw)
    info = media['imageInfo']
    cylinders, heads = info['cylinders'], info['heads']
    sectors_per_track = info.get('trackDefault', 9)
    sector_size = info.get('sectorDefault', 512)
    total = cylinders * heads * sectors_per_track
    if sector_size != 512 or not 0 < total <= 8192:
        raise ValueError('Unsupported archive geometry')
    sectors = {}
    for cylinder in media['diskData']:
        for head in cylinder:
            for sector in head:
                c, h, s = sector['c'], sector['h'], sector['s']
                length = sector.get('l', sector_size)
                words = sector['d']
                if (not 0 <= c < cylinders or not 0 <= h < heads or
                        not 1 <= s <= sectors_per_track or length != sector_size or
                        not words or len(words) > length // 4):
                    raise ValueError('Invalid archive sector')
                key = c, h, s
                if key in sectors:
                    raise ValueError('Duplicate archive sector')
                data = b''.join(struct.pack('<I', word & 0xffffffff) for word in words)
                data += struct.pack('<I', words[-1] & 0xffffffff) * ((length - len(data)) // 4)
                sectors[key] = data
    if len(sectors) != total:
        raise ValueError('Missing archive sector')
    disk = b''.join(sectors[key] for key in sorted(sectors))
    bps = struct.unpack_from('<H', disk, 11)[0]
    spc = disk[13]
    reserved = struct.unpack_from('<H', disk, 14)[0]
    fat_count = disk[16]
    root_count = struct.unpack_from('<H', disk, 17)[0]
    fat_sectors = struct.unpack_from('<H', disk, 22)[0]
    if bps != sector_size or spc not in (1, 2, 4, 8, 16, 32, 64, 128) or not reserved or not fat_count or not fat_sectors:
        raise ValueError('Invalid FAT12 BPB')
    root_start = (reserved + fat_count * fat_sectors) * bps
    data_start = root_start + ((root_count * 32 + bps - 1) // bps) * bps
    if not root_start < data_start <= len(disk):
        raise ValueError('Invalid FAT12 layout')
    fat = disk[reserved * bps:(reserved + fat_sectors) * bps]
    files = {}
    for offset in range(root_start, root_start + root_count * 32, 32):
        entry = disk[offset:offset + 32]
        if entry[0] == 0:
            break
        if entry[0] == 0xe5 or entry[11] & 0x18:
            continue
        name = entry[:8].decode('ascii').rstrip() + '.' + entry[8:11].decode('ascii').rstrip()
        if name not in names:
            continue
        if name in files:
            raise ValueError('Duplicate archive file: ' + name)
        size = struct.unpack_from('<I', entry, 28)[0]
        cluster = struct.unpack_from('<H', entry, 26)[0]
        content, seen = bytearray(), set()
        while cluster < 0xff8:
            if not 2 <= cluster < 0xff0 or cluster in seen:
                raise ValueError('Invalid or looping FAT12 chain: ' + name)
            seen.add(cluster)
            start = data_start + (cluster - 2) * spc * bps
            if start + spc * bps > len(disk):
                raise ValueError('FAT12 cluster outside disk')
            content.extend(disk[start:start + spc * bps])
            fat_offset = cluster + cluster // 2
            if fat_offset + 2 > len(fat):
                raise ValueError('FAT12 entry outside table')
            word = int.from_bytes(fat[fat_offset:fat_offset + 2], 'little')
            cluster = word >> 4 if cluster & 1 else word & 0xfff
        if size > len(content):
            raise ValueError('Truncated archive file: ' + name)
        files[name] = bytes(content[:size])
    if set(files) != set(names):
        raise ValueError('Missing requested archive files: ' + ', '.join(sorted(set(names) - set(files))))
    return files


def install(destination=None, compiler='msc510'):
    config = compiler_config(compiler)
    destination = Path(destination if destination is not None else default_toolchain(compiler)).resolve()
    if destination.exists():
        validate_toolchain(destination, compiler)
        return destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.' + compiler + '-download-', dir=destination.parent) as tmp:
        stage = Path(tmp) / compiler
        stage.mkdir()
        if compiler == 'msc510':
            base = 'https://raw.githubusercontent.com/microsoft/MS-DOS/' + config['commit'] + '/'
            entries = [(entry['name'], config['path'] + '/' + entry['name'], entry['sha256'], entry['size'])
                       for entry in config['files']]
            entries.append(('LICENSE', config['license']['path'], config['license']['sha256'], None))
            for name, remote, expected, size in entries:
                (stage / name).write_bytes(_download(base + remote, expected, size))
        else:
            archive_dir = stage / 'archives'
            archive_dir.mkdir()
            for archive in config['archives']:
                raw = _download(archive['url'], archive['sha256'])
                (archive_dir / archive['name']).write_bytes(raw)
                entries = [entry for entry in config['files'] if entry['archive'] == archive['url']]
                for name, data in archive_files(raw, [entry['name'] for entry in entries]).items():
                    (stage / name).write_bytes(data)
        manifest = {key: config[key] for key in manifest_fields(compiler)}
        (stage / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
        validate_toolchain(stage, compiler)
        # Publish only a complete, hash-verified profile with accurate provenance.
        shutil.move(str(stage), str(destination))
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path)
    parser.add_argument('--compiler', choices=COMPILERS, default='msc510')
    args = parser.parse_args()
    print(install(args.destination, args.compiler))
