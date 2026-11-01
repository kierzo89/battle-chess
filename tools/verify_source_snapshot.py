"""Verify the published source snapshot, not executable reproduction."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    inventory = json.loads((ROOT / 'verification/source-snapshot.json').read_text())
    for row in inventory['files']:
        path = ROOT / row['path']
        assert path.is_file() and not path.is_symlink(), row['path']
        assert sha(path) == row['sha256'], row['path']
    external = {row['path']: row['sha256'] for row in json.loads(
        (ROOT / 'verification/external-inputs.json').read_text())['inputs']}
    manifest = json.loads((ROOT / 'matching/build_pipeline/manifest.json').read_text())
    pins = [('matching/' + row['path'], row['sha256'])
            for row in manifest['engine_files'] + manifest['project_inputs']]
    bundle = '.reworkbench/staging/exact-build-driver-v2/'
    pins += [(bundle + row['path'], row['sha256']) for row in json.loads(
        (ROOT / bundle / 'bundle-manifest.json').read_text())['files']]
    for name, digest in pins:
        path = ROOT / name
        if path.is_file():
            assert sha(path) == digest, name
        else:
            assert external.get(name) == digest, 'Unaccounted required input: ' + name
    print(f"PASS: {len(inventory['files'])} published files intact; {len(pins)} pinned inputs accounted for.")
    print('External inputs remain required. This check is not a fresh executable build.')

if __name__ == '__main__':
    main()
