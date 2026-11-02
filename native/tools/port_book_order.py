"""Generate recovered A348 book move ordering with explicit host context."""
import argparse, hashlib, json, re
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
name='matching/src/move_engine_9a50_full_match.c'
pins={r['path']:r['sha256'] for r in json.loads((a.root/'verification/source-snapshot.json').read_text())['files']}
data=(a.root/name).read_bytes()
if hashlib.sha256(data).hexdigest()!=pins[name]:raise ValueError('Move source not pinned')
asset='assets/recovered/bank1/startup-02.raw.bin'
asset_pins={r['path']:r['sha256'] for r in json.loads((a.root/'verification/asset-snapshot.json').read_text())['files']}
if hashlib.sha256((a.root/asset).read_bytes()).hexdigest()!=asset_pins[asset]:raise ValueError('Opening book asset not pinned')
s=data.decode();s=s[s.index('void append_move(void)'):]
s=re.sub(r'^void ', 'static void ', s, flags=re.M)
pre='''#include "book_order.h"
#include <string.h>
#include <stdlib.h>
typedef union {uint16_t word;struct{uint8_t kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
typedef struct {int from,to;} Castle;
static _Thread_local BCCell board[120];
static _Thread_local BCPiece pieces[2][16];
static _Thread_local Move candidate_move,move_list[80],history[1];
static const Castle castle[2][2]={{{2,4},{6,4}},{{114,116},{118,116}}};
static const int pawn_step[2]={16,-16},steps[8]={1,-1,16,-16,17,-17,15,-15},knight_steps[8]={14,-14,18,-18,31,-31,33,-33};
static _Thread_local int current_side,opponent,history_index,piece_counts[2],side_piece_counts[2],move_count,state_index;
static _Thread_local const BCPosition *position;
static int abs_i16(int x){return abs(x);}
static int piece_attacks(int kind,int side,int from,int to){return bc_piece_attacks(&position->board,kind,side,from,to);}
static int legal_move(int to,int from,int flag,MoveKind detail){
 if(flag&&detail.bytes.kind==6)return position->ep==to&&!(from&0x88)&&board[from].kind==6&&board[from].side==current_side;
 BCMoveList legal;bc_generate_legal(position,&legal);
 for(size_t i=0;i<legal.count;i++){BCMove m=legal.moves[i];if(m.to==to&&m.from==from&&m.special==flag&&m.kind==detail.bytes.kind&&m.capture==detail.bytes.capture)return 1;}
 return 0;
}
'''
post='''
bool bc_book_order(const BCPosition *p,const BCMove *previous,BCMoveList *out){
 if(!p||!out||p->board.side>1)return false;
 /* Recovered quiet pawn generator assumes no unpromoted pawn on last rank. */
 for(int x=0;x<120;x++)if(!(x&0x88)&&p->board.cells[x].kind==6&&(x<8||x>=112))return false;
 position=p;memcpy(board,p->board.cells,sizeof board);memcpy(pieces,p->board.pieces,sizeof pieces);
 current_side=p->board.side;opponent=current_side^1;history_index=0;
 for(int c=0;c<2;c++){piece_counts[c]=p->board.last_nonpawn[c];side_piece_counts[c]=p->board.last_piece[c];}
 history[0]=(Move){0};candidate_move=(Move){0};
 if(previous){history[0].to=previous->to;history[0].from=previous->from;history[0].detail.bytes.kind=previous->kind;}
 generate_a348();out->count=move_count;
 for(int i=0;i<move_count;i++){Move m=move_list[i];out->moves[i]=(BCMove){m.from,m.to,m.flag,m.detail.bytes.kind,m.detail.bytes.capture};}
 position=NULL;return true;
}
'''
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(pre+s+post)
