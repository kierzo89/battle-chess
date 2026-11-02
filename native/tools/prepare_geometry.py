"""Retain verified original coordinate values as native const data."""
from pathlib import Path
import argparse,json,hashlib,struct
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
e=json.loads((a.root/'native/evidence/rea-board-coordinates.json').read_text())
b=bytes.fromhex(e['normalized_result']['bytes_hex'])
if hashlib.sha256(b).hexdigest()!='c0a97dc159f44fd9f98eb0b2bbe8caa30f895f97b080960f1a3176118246bebd':raise ValueError('Coordinate evidence changed')
arrays=[]
for name,offset,count in [('square_y_flat',486,9),('square_x_flat',504,81),('square_y_tilted',666,9),('square_x_tilted',684,81),('screen_x_flat',846,64),('screen_y_flat',974,8),('screen_x_tilted',990,64),('screen_y_tilted',1118,8)]:
 values=struct.unpack_from('<'+str(count)+'h',b,offset-486)
 arrays.append('static const int '+name+'['+str(count)+']={'+','.join(map(str,values))+'};')
text='#include "geometry.h"\n'+'\n'.join(arrays)+'''
int bc_geometry_hit(bool perspective,int x,int y){
 const int *ys=perspective?square_y_flat:square_y_tilted;
 const int *xs=perspective?square_x_flat:square_x_tilted;
 unsigned row=0,col=0;
 while(row<9&&ys[row]<=y)row++;
 if(!row||row==9)return -1;
 row--;xs+=row*9;
 while(col<9&&xs[col]<=x)col++;
 if(!col||col==9)return -1;
 return (int)((7-row)*16+col-1);
}
bool bc_geometry_anchor(bool perspective,unsigned square,int *x,int *y){
 if(!x||!y||square>=120||(square&0x88))return false;
 unsigned row=7-(square>>4),column=square&7;
 *x=(perspective?screen_x_flat:screen_x_tilted)[row*8+column];
 *y=(perspective?screen_y_flat:screen_y_tilted)[row];return true;
}
'''
# queue_piece_7AA7 maps engine kind through game_kind_map before choosing facing.
# Keep source-derived frame selection in ordinary C with pinned tables.
for filename,digest in [('game_kind_map.c','205edda8d4dbed06035b90c85b1b35288084eedd538acbbb6f8d815b114b5f20')]:
 raw=(a.root/'matching/src/data'/filename).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=digest:raise ValueError('Piece mapping changed')
source=(a.root/'matching/src/queue_piece_match.c').read_bytes()
if hashlib.sha256(source).hexdigest()!='cf929768281d5083f974334333df537ef658fe794f6502793f6f34856a272066':raise ValueError('Standing-frame source changed')
frame=(a.root/'matching/src/data/frame_index_flat_0166.c').read_text()
# Snapshot independently authenticates frame table before generating runtime data.
pins={v['path']:v['sha256'] for v in json.loads((a.root/'verification/source-snapshot.json').read_text())['files']}
path='matching/src/data/frame_index_flat_0166.c'
if hashlib.sha256(frame.encode()).hexdigest()!=pins[path]:raise ValueError('Frame index changed')
text+='static const '+frame[frame.index('unsigned char'):]
text+='''
unsigned bc_geometry_facing(unsigned kind,unsigned side,unsigned square){
 if(kind<1||kind>6||side>1||square>=120||(square&0x88))return 99;
 const unsigned map[7]={0,2,5,6,1,3,4};unsigned k=map[kind],facing;
 if(k==6)facing=(square&7)<4?3:7;
 else if(k==1)facing=(square&7)<4?(side?1:3):(side?7:5);
 else facing=side?0:4;
 return facing;
}
unsigned bc_geometry_faced_frame(unsigned kind,unsigned facing){
 const unsigned map[7]={0,2,5,6,1,3,4};
 if(kind<1||kind>6||facing>7)return 99;
 return frame_index_flat[(facing<<3)|map[kind]];
}
unsigned bc_geometry_frame(unsigned kind,unsigned side,unsigned square){
 return bc_geometry_faced_frame(kind,bc_geometry_facing(kind,side,square));
}
'''
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
