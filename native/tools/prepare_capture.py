"""Retain original capture lists/control streams; no synthetic frame durations."""
from pathlib import Path
import argparse,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
pins={r['path']:r['sha256'] for r in json.loads((a.root/'verification/asset-snapshot.json').read_text())['files']}
def read(path):
 b=(a.root/path).read_bytes()
 if hashlib.sha256(b).hexdigest()!=pins[path]:raise ValueError('Asset identity: '+path)
 return json.loads(b)
r=read('assets/recovered/metadata/timing/report.json');text='#include "capture.h"\n';controls={};entries={}
for c in r['capture_controls']:
 data=bytes.fromhex(c['raw_hex'])
 if hashlib.sha256(data).hexdigest()!=c['sha256']:raise ValueError('Control identity')
 name=f"control_{c['alternate_profile']}_{c['table']}_{c['index']}"
 text+='static const uint8_t '+name+'[]={'+','.join(map(str,data))+'};\n'
 controls[c['table'],c['index']]=name
for s in r['capture_sequence_mapping']:
 side=int(s['side']=='right');kind=s['piece_kind'];opponent=s['opponent_kind'];pair=s['bank_pair']
 name=f'frames_{side}_{kind}_{opponent}';frames=[]
 for listing in s['bank_list_indices']:
  seq=read(f'assets/recovered/animations/pair-{pair:02d}-list-{listing:02d}/sequence.json')
  frames.extend('{'+f'{pair},{listing},{step}'+'}' for step in range(len(seq['frames'])))
 if len(frames)>512:raise ValueError('Sequence extent')
 text+='static const BCCaptureFrame '+name+'[]={'+','.join(frames or ['{0,0,0}'])+'};\n'
 for profile,table in enumerate(s['control_tables']):
  control=controls[table,s['control_record_index']]
  entries[side,kind,opponent,profile]='{'+f'{control},sizeof {control},{len(frames)},{name}'+'}'
text+='static const BCCaptureSequence sequences[2][6][6][2]={'+','.join('{'+','.join('{'+','.join('{'+','.join(entries[side,kind,opp,profile] for profile in range(2))+'}' for opp in range(1,7))+'}' for kind in range(1,7))+'}' for side in range(2))+'};\n'
text+='''const BCCaptureSequence *bc_capture_sequence(unsigned side,unsigned kind,unsigned opponent,unsigned profile){
 if(side>1||kind<1||kind>6||opponent<1||opponent>6||profile>1)return 0;
 const unsigned map[]={0,2,5,6,1,3,4};return &sequences[side][map[kind]-1][map[opponent]-1][profile];
}
'''
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
