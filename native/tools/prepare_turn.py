"""Generate original turn sequence descriptors from authenticated assets."""
from pathlib import Path
import argparse,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
pins={r['path']:r['sha256'] for r in json.loads((a.root/'verification/asset-snapshot.json').read_text())['files']}
def read(path):
 b=(a.root/path).read_bytes()
 if hashlib.sha256(b).hexdigest()!=pins[path]:raise ValueError('Asset identity: '+path)
 return json.loads(b)
text='#include "turn_animation.h"\n';entries={}
for item in read('assets/recovered/metadata/timing/report.json')['piece_controls']:
 if item['operation_family']!='turn':continue
 profile,kind,orientation,direction=(item[k] for k in ('profile','piece_kind','orientation','turn_direction'))
 name=f'turn_{profile}_{kind}_{orientation}_{int(direction>0)}';data=bytearray()
 for event in item['ready_events']:
  for d in event['dispatch']:data.extend((128|d['asset'],d['argument']+64))
  data.append(255 if event['terminal'] else event['delay'])
 if hashlib.sha256(data).hexdigest()!=item['stream_sha256']:raise ValueError('Control reconstruction')
 pair,seq=item['bank_pair'],item['bank_list_index']
 record=read(f'assets/recovered/animations/pair-{pair:02d}-list-{seq:02d}/sequence.json')
 tokens=[record['initial_frame']['native_global_index']]+[100+x for x in record['delta_indices']]
 if not 1<=len(tokens)<=64 or len(tokens)!=len(record['frames']):raise ValueError('Frame bound')
 text+='static const uint8_t '+name+'[]={'+','.join(map(str,data))+'};\n'
 text+='static const unsigned '+name+'_tokens[]={'+','.join(map(str,tokens))+'};\n'
 entries[profile,kind,orientation,direction]='{'+f'{name},sizeof {name},{pair},{seq},{len(tokens)},{name}_tokens'+'}'
text+='static const BCTurnSequence sequences[2][6][8][2]={\n'
for profile in range(2):
 text+='{'+','.join('{'+','.join('{'+','.join(entries[profile,kind,ori,d] for d in (-1,1))+'}' for ori in range(8))+'}' for kind in range(1,7))+'},\n'
text+='''};
const BCTurnSequence *bc_turn_sequence(unsigned kind,unsigned orientation,int direction,unsigned profile){
 if(kind<1||kind>6||orientation>7||profile>1||(direction!=-1&&direction!=1))return 0;
 const unsigned map[]={0,2,5,6,1,3,4};return &sequences[profile][map[kind]-1][orientation][direction>0];
}
'''
text+='static const BCTurnSequence faces[4]={\n'
face_entries=[]
for arg in range(4):
 record=read(f'assets/recovered/animations/pair-05-list-{14+arg:02d}/sequence.json')
 tokens=[record['initial_frame']['native_global_index']]+[100+x for x in record['delta_indices']]
 face_entries.append(tokens)
# Place the token arrays before the face descriptor table.
text=text.removesuffix('static const BCTurnSequence faces[4]={\n')
for arg,tokens in enumerate(face_entries):text+='static const unsigned face_'+str(arg)+'[]={'+','.join(map(str,tokens))+'};\n'
text+='static const BCTurnSequence faces[4]={'+','.join('{0,0,5,'+str(14+i)+','+str(len(t))+',face_'+str(i)+'}' for i,t in enumerate(face_entries))+'};\n'
text+='const BCTurnSequence *bc_face_sequence(unsigned arg){return arg<4?&faces[arg]:0;}\n'
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
