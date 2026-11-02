"""Developer-only original-machine compositor check for a crossing queen turn.
Requires the preserved reconstruction's Unicorn oracle; no emulator at runtime.
Writes portable evidence for the native test suite. Never changes reference.
"""
from pathlib import Path
import argparse,sys,importlib.util,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--reference',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
root=Path(__file__).resolve().parents[2]
pins={r['path']:r['sha256'] for r in json.loads((root/'verification/asset-snapshot.json').read_text())['files']}
def read(path):
 b=(root/path).read_bytes();assert hashlib.sha256(b).hexdigest()==pins[path];return b
def mod(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
oracle_path=args.reference/'asset_recovery/compositor_v1/oracle.py';oracle=mod('turn_native_compositor',oracle_path)
base='assets/recovered/metadata/bank2-records/'
records={(r['pair'],r['record']):r for r in json.loads(read(base+'report.json'))['records']}
seqfolder='assets/recovered/animations/pair-04-list-21/'
seq=json.loads(read(seqfolder+'sequence.json'));initial=seq['frames'][0]
a=tuple(initial[k] for k in ('width','height','anchor_x','anchor_y'));ap=read(seqfolder+initial['packed_file'])
# Original queen turn5->1 takes negative steps, skipping entries0/1 on
# continuation. The first crossing21->20 exposes the differing retained pixel.
steps=[(21,f['delta_record']) for f in seq['frames'][1:]]
for listing in (20,19,18):
 seq=json.loads(read(f'assets/recovered/animations/pair-04-list-{listing:02d}/sequence.json'))
 steps.extend((listing,f['delta_record']) for f in seq['frames'][2:])
rows=[]
for listing,index in steps:
 r=records[4,index];b=tuple(r[k] for k in ('width','height','anchor_x','anchor_y'));bp=read(base+r['packed_file'])
 ap,proof=oracle.run(a,ap,b,bp);a=tuple(proof['descriptor'])
 rows.append({'list':listing,'delta_record':index,'proof':proof})
result={'scope':'Queen graphics kind5, turn5->1 negative; original compositor/fill/blitter for every emitted delta, retained730C selection contract. Not whole original game execution.', 'initial_sequence':'pair-04-list-21','rows':rows,'oracle_sha256':hashlib.sha256(oracle_path.read_bytes()).hexdigest(),'canonical_credit_added':0}
args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print(f'PASS {len(rows)} original compositor calls, including divergent queen continuation')
