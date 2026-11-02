"""Pin recovered BB0E and adapt its command sinks without changing its paths."""
import argparse,hashlib,re
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
s=(a.root/'matching/src/animation_stage_match.c').read_text()
if hashlib.sha256(s.encode()).hexdigest()!='b12558abe504d0e99530a23cbf15a2049793cbb77fd6def0745e8dfd2569fa40':raise ValueError('Unpinned animation stage source')
s=s[s.index('unsigned animation_stage('):]
# Call arities are explicit. Do not read an omitted DOS stack argument.
s=re.sub(r'append_command_5fbd\(([^;]*?)\)',lambda m:'append'+str(len(m[1].split(',')))+'('+m[1]+')',s)
header='''#include "stage.h"
#include <string.h>
typedef uint8_t Byte;
typedef union {uint16_t word;struct {Byte kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
static _Thread_local Byte animation_busy,record_latch,cells[64],animation_done;
static const Byte capture_types_11ac[7]={0,4,1,5,6,2,3};
static _Thread_local int current_side,modes[2];
static _Thread_local BCStagePlan *plan;
static _Thread_local unsigned flushed;
static void record_dfac(Move *m){(void)m;}
static int emit(unsigned parent,unsigned op,unsigned square,unsigned arg,unsigned extra,bool known){
 if(plan->count>=BC_STAGE_MAX){plan->failed=true;return 0;}
 unsigned id=plan->count++;plan->commands[id]=(BCStageCommand){parent,op,square,arg,extra,known};return (int)id;
}
static int begin_command_60d3(unsigned op,unsigned square,unsigned arg){return emit(255,op,square,arg,0,false);}
static int append4(unsigned parent,unsigned op,unsigned square,unsigned arg){return emit(parent,op,square,arg,0,false);}
static int append5(unsigned parent,unsigned op,unsigned square,unsigned arg,unsigned extra){return emit(parent,op,square,arg,extra,true);}
static void poll_input(int flag){(void)flag;}
static int obtain_input(void){
 /* Model completed transfer state for recursive castling/en-passant planning.
  * This is not an animation executor and does not resolve unknown fields. */
 for(;flushed<plan->count;flushed++){
  BCStageCommand c=plan->commands[flushed];
  if(c.operation==3&&c.square!=c.argument){cells[c.argument]=cells[c.square];cells[c.square]=0;}
 }
 animation_done=1;return 0;
}
'''
table=(a.root/'matching/src/data/capture_record_mapping_11ac.c').read_bytes()
if hashlib.sha256(table).hexdigest()!='57655210c3d430cabaab49f0de5a52f81a7828839d604504011145ca0fcbe1c7':raise ValueError('Unpinned capture mapping')
mapping=(a.root/'matching/src/data/game_kind_map.c').read_bytes()
if hashlib.sha256(mapping).hexdigest()!='205edda8d4dbed06035b90c85b1b35288084eedd538acbbb6f8d815b114b5f20':raise ValueError('Unpinned piece mapping')
promotion=(a.root/'matching/src/promote_ui_match.c').read_bytes()
if hashlib.sha256(promotion).hexdigest()!='cdb59b04186ad701f31b4a27169524c2acce56ee4501e07b4fdc456580da70ff':raise ValueError('Unpinned promotion normalization')
footer='''
bool bc_stage_plan(const BCPosition *before,BCMove move,BCStagePlan *out){
 if(!before||!out)return false;
 memset(out,0,sizeof *out);BCPosition check=*before;
 if(!bc_play(&check,move))return false;
 /* Original9371 calls BB0E with pawn kind and cleared promotion flag. */
 if(move.special&&move.kind>=2&&move.kind<=5){move.kind=6;move.special=0;}
 const Byte map[7]={0,2,5,6,1,3,4};
 for(unsigned i=0;i<64;i++){unsigned sq=((7-i/8)*16)+(i%8);BCCell c=before->board.cells[sq];cells[i]=c.kind?(map[c.kind]|(c.side?64:0)):0;}
 plan=out;flushed=0;animation_busy=record_latch=animation_done=0;current_side=0;modes[0]=modes[1]=0;
 Move original={move.to,move.from,move.special,{0}};original.detail.bytes.kind=move.kind;original.detail.bytes.capture=move.capture;
 (void)animation_stage(original,1);plan=NULL;return !out->failed;
}
'''
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(header+s+footer)
