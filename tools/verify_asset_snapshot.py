"""Verify the published asset snapshot and independently reconstruct both banks."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    'ALLCANM1': (185726, 'aa50ef9fb55e5271526e25ccc6e60b2908f00440c3f33380d13d27ecd4cbc564'),
    'ALLCANM2': (339592, '114a46f323f6766396eba42bd741768e415ded55685ee0778f127a48377c084d'),
}

def main():
    manifest = json.loads((ROOT / 'verification/asset-snapshot.json').read_text())
    for row in manifest['files']:
        path = ROOT / row['path']
        if path.is_symlink() or not path.is_file():
            raise ValueError(f'Missing or symlink input: {row["path"]}')
        data = path.read_bytes()
        if len(data) != row['size'] or hashlib.sha256(data).hexdigest() != row['sha256']:
            raise ValueError(f'Asset hash mismatch: {row["path"]}')
    with tempfile.TemporaryDirectory(prefix='battle-chess-assets-') as temp:
        output = Path(temp) / 'banks'
        subprocess.run([sys.executable, '-I', '-B',
                        str(ROOT / 'assets/bank-rebuild/rebuild.py'),
                        '--output', str(output)], cwd=temp, check=True,
                       capture_output=True, text=True, timeout=120)
        for name, (size, digest) in EXPECTED.items():
            data = (output / name).read_bytes()
            if len(data) != size or hashlib.sha256(data).hexdigest() != digest:
                raise ValueError(f'Rebuilt bank mismatch: {name}')
    print(f'PASS: {len(manifest["files"])} asset files intact; both banks rebuilt byte-exactly.')

if __name__ == '__main__':
    main()
