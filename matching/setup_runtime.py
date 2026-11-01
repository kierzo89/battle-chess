#!/usr/bin/env python3
"""Explicitly install the independently pinned historical MSC5.00 runtime."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

from setup_toolchain import _download, archive_files

HERE = Path(__file__).resolve().parent


def runtime_config(project=HERE):
    return json.loads((Path(project) / 'config/runtime500.json').read_text())


def validate_runtime(destination, config):
    destination = Path(destination)
    manifest = json.loads((destination / 'manifest.json').read_text())
    fields = ('archive_url', 'archive_sha256', 'library_name', 'library_size', 'library_sha256')
    if manifest != {k: config[k] for k in fields}:
        raise ValueError('Runtime manifest does not match pinned configuration')
    data = (destination / config['library_name']).read_bytes()
    if len(data) != config['library_size'] or hashlib.sha256(data).hexdigest() != config['library_sha256']:
        raise ValueError('Runtime library does not match pinned configuration')
    return data


def install(destination=None, archive=None):
    config = runtime_config()
    destination = Path(destination or HERE / config['destination']).resolve()
    if destination.exists():
        validate_runtime(destination, config)
        return destination
    raw = Path(archive).read_bytes() if archive else _download(config['archive_url'], config['archive_sha256'])
    if hashlib.sha256(raw).hexdigest() != config['archive_sha256']:
        raise ValueError('Runtime archive SHA-256 mismatch')
    library = archive_files(raw, [config['library_name']])[config['library_name']]
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.runtime500-', dir=destination.parent) as temp:
        stage = Path(temp) / 'runtime500'
        stage.mkdir()
        (stage / config['library_name']).write_bytes(library)
        (stage / config['archive_name']).write_bytes(raw)
        fields = ('archive_url', 'archive_sha256', 'library_name', 'library_size', 'library_sha256')
        (stage / 'manifest.json').write_text(json.dumps({k: config[k] for k in fields}, indent=2) + '\n')
        validate_runtime(stage, config)
        shutil.move(str(stage), destination)
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path)
    parser.add_argument('--archive', type=Path, help='Use a locally preserved pinned PCjs disk JSON')
    args = parser.parse_args()
    print(install(args.destination, args.archive))
