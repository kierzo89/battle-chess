"""Reproduce the reviewed exact executable from pinned source providers."""
from pathlib import Path
import hashlib, json, runpy, sys
ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / '.reworkbench/staging/exact-build-driver-v2'
EXPECTED = '7bd2a762b329ef8d9af414d99e13d733460db8d7c2cfd97dabd8d2184edf64ff'
if hashlib.sha256((BUNDLE / 'bundle-manifest.json').read_bytes()).hexdigest() != EXPECTED:
    raise SystemExit('Reviewed build bundle changed; explicit review required')
for item in json.loads((BUNDLE / 'bundle-manifest.json').read_text())['files']:
    path = BUNDLE / item['path']
    if not path.resolve().is_relative_to(BUNDLE.resolve()) or hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
        raise SystemExit('Reviewed source or script changed: ' + item['path'])
sys.path.insert(0, str(BUNDLE))
runpy.run_path(str(BUNDLE / 'build_exact.py'), run_name='__main__')
