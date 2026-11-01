"""Reject modified source rather than silently claiming recovered provenance."""
from pathlib import Path
import importlib.util, tempfile, shutil
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('port_evaluation',ROOT/'native/tools/port_evaluation.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);(root/'matching/src/data').mkdir(parents=True);(root/'verification').mkdir()
    shutil.copy2(ROOT/'verification/source-snapshot.json',root/'verification/source-snapshot.json')
    source=Path('matching/src/full_evaluation_match.c')
    (root/source).write_bytes((ROOT/source).read_bytes()+b'\n/* mutation */\n')
    try:m.generate(root,root/'generated.c')
    except ValueError as error:assert 'Source differs' in str(error)
    else:raise AssertionError('Modified recovered source was admitted')
    assert not (root/'generated.c').exists()
print('PASS: generator rejects modified recovered source before creating output')
