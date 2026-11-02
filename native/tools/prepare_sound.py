"""Package native-verified amplitude nibbles, preserving original slot mapping."""
from pathlib import Path
import argparse,json,hashlib,struct
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
pins={r['path']:r['sha256'] for r in json.loads((a.root/'verification/asset-snapshot.json').read_text())['files']}
def read(path):
 b=(a.root/path).read_bytes()
 if hashlib.sha256(b).hexdigest()!=pins[path]:raise ValueError('Asset identity: '+path)
 return b
r=json.loads(read('assets/recovered/audio-report.json'));records=sorted((x for x in r['records'] if x['mode']==0),key=lambda x:x['mode_slot'])
if [x['mode_slot'] for x in records]!=list(range(15)):raise ValueError('Sound slot mapping')
out=bytearray(b'BCA1')
for x in records:
 data=read('assets/recovered/audio/'+x['sample_file'])
 if len(data)!=x['samples'] or hashlib.sha256(data).hexdigest()!=x['sample_sha256'] or max(data)>15:raise ValueError('Sample extent or identity')
 trace=json.loads(read('assets/recovered/audio/'+x['native_trace']['path']))
 commands=bytes.fromhex(trace['commands_hex'])
 if commands[:2]!=bytes((0x81,0)) or commands[2:]!=bytes(0x90|(15-v) for v in data):raise ValueError('Original port amplitude command stream differs')
 out+=struct.pack('<II',x['header_pitch_denominator'],len(data))+data
# This bundle retains source amplitudes and timing words, not a measured WAV.
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(out)
