"""Reconstruct lossless original move controls, bounded by retained hashes."""
from pathlib import Path
import argparse,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
pins={r['path']:r['sha256'] for r in json.loads((a.root/'verification/asset-snapshot.json').read_text())['files']}
def read(path):
 b=(a.root/path).read_bytes()
 if hashlib.sha256(b).hexdigest()!=pins[path]:raise ValueError('Asset identity: '+path)
 return json.loads(b)
r=read('assets/recovered/metadata/timing/report.json');text='#include "walk.h"\n';entries={}
for item in r['piece_controls']:
 if item['operation_family']!='move_or_effect':continue
 profile,kind,orientation=item['profile'],item['piece_kind'],item['orientation']
 name=f'control_{profile}_{kind}_{orientation}';data=bytearray()
 for event in item['ready_events']:
  for d in event['dispatch']:data.extend((128|d['asset'],d['argument']+64))
  data.append(255 if event['terminal'] else event['delay'])
 if hashlib.sha256(data).hexdigest()!=item['stream_sha256']:raise ValueError('Control reconstruction')
 pair,seq=item['bank_pair'],item['bank_list_index']
 frames=read(f'assets/recovered/animations/pair-{pair:02d}-list-{seq:02d}/sequence.json')['frames']
 if not 0<len(frames)<=64:raise ValueError('Frame bound')
 text+='static const uint8_t '+name+'[]={'+','.join(map(str,data))+'};\n'
 entries[profile,kind,orientation]='{'+f'{name},sizeof {name},{pair},{seq},{len(frames)}'+'}'
text+='static const BCWalk sequences[2][6][8]={\n'
for profile in range(2):
 text+='{'+','.join('{'+','.join(entries[profile,kind,ori] for ori in range(8))+'}' for kind in range(1,7))+'},\n'
text+='''};
const BCWalk *bc_walk_sequence(unsigned kind,unsigned orientation,unsigned profile){
 if(kind<1||kind>6||orientation>7||profile>1)return 0;
 const unsigned map[7]={0,2,5,6,1,3,4};return &sequences[profile][map[kind]-1][orientation];
}
'''
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
