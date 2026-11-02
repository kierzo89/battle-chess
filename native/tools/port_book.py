"""Pinned original book scan/rotation/selection, with native replay adapters."""
import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
pins={r['path']:r['sha256'] for r in json.loads((a.root/'verification/source-snapshot.json').read_text())['files']}
def source(name):
 b=(a.root/name).read_bytes()
 if hashlib.sha256(b).hexdigest()!=pins[name]:raise ValueError('Source changed: '+name)
 return b.decode()
s=source('matching/src/book_context_match.c');weights=source('matching/src/data/book_weights.c')
asset='assets/recovered/bank1/startup-02.raw.bin';b=(a.root/asset).read_bytes()
ap={r['path']:r['sha256'] for r in json.loads((a.root/'verification/asset-snapshot.json').read_text())['files']}
if hashlib.sha256(b).hexdigest()!=ap[asset]:raise ValueError('Book data changed')
# Keep the actual bodies. DOS loading/graphics/history ownership becomes host context.
functions=s[s.index('void accept_hint_82db(void)'):s.index('extern unsigned char search_active;')]
functions+=s[s.index('void scan_book_843f(void)\n{'):]
pre='''#include "book.h"
#include <string.h>
typedef union {unsigned word;struct{unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
static _Thread_local int book_choice_offset,book_state_index,best,iteration,input_state,history_index,book_saved_index,book_matches;
static _Thread_local Move working_move,working_follow_8bb6,state_8d12,initial_move,history[43];
static _Thread_local BCPosition positions[44];
static _Thread_local BCMoveList generated;
static _Thread_local unsigned cursor,draw_value;
static _Thread_local bool failed;
static void rotate_book_8515(int),skip_book_8577(void),previous_book_858d(void);
static void graphics_end(void){}static void graphics_begin(void){}
static int book_rand(void){return (int)draw_value;}
#define rand book_rand
static BCMove host(Move m){return (BCMove){m.from,m.to,m.flag,m.detail.bytes.kind,m.detail.bytes.capture};}
static Move native(BCMove m){Move r={m.to,m.from,m.special,{0}};r.detail.bytes.kind=m.kind;r.detail.bytes.capture=m.capture;return r;}
static int equal_state(Move *a,Move *b){return a->from==b->from&&a->to==b->to&&a->flag==b->flag&&a->detail.bytes.kind==b->detail.bytes.kind&&a->detail.bytes.capture==b->detail.bytes.capture;}
static void generate_a348(void){
 BCMove prev=history_index>=0?host(history[history_index]):(BCMove){0};
 generated.count=0;cursor=0;
 if(!bc_book_order(&positions[history_index+1],history_index>=0?&prev:NULL,&generated))failed=true;
}
static void advance(void){state_8d12=cursor<generated.count?native(generated.moves[cursor++]):initial_move;}
static void notify_866d(Move m){
 positions[history_index+2]=positions[history_index+1];
 if(!bc_play(&positions[history_index+2],host(m)))failed=true;
 history_index++;
}
static void notify_86a1(Move m){(void)m;history_index--;}
'''
# Private functions and tables avoid collisions with independently generated order.
import re
functions=re.sub(r'^void ', 'static void ',functions,flags=re.M)
pre+= 'static const unsigned char splash_buffer[32000]={'+','.join(map(str,b))+'};\n'
pre+=weights.replace('char book_weights','static const char book_weights')+'\n'
post='''
bool bc_book_move(const BCPosition *root,const BCMove *past,size_t count,unsigned draw,BCMove *out){
 if(!root||!out||(!past&&count)||count>42||draw>15)return false;
 bc_position_initial(&positions[0]);
 for(size_t i=0;i<count;i++){
  positions[i+1]=positions[i];if(!bc_play(&positions[i+1],past[i]))return false;history[i]=native(past[i]);
 }
 const BCPosition *replay=&positions[count];
 uint8_t a[33],b[33];bc_pack(&root->board,a);bc_pack(&replay->board,b);
 if(memcmp(a,b,33)||memcmp(root->castle,replay->castle,2)||root->ep!=replay->ep||root->halfmove!=replay->halfmove||root->fullmove!=replay->fullmove)return false;
 /* Reject same visible board with incompatible original piece-list identities. */
 if(memcmp(root->board.pieces,replay->board.pieces,sizeof root->board.pieces)||memcmp(root->board.cells,replay->board.cells,sizeof root->board.cells))return false;
 initial_move=(Move){0};history_index=-1;book_saved_index=(int)count-2;
 book_choice_offset=book_matches=0;failed=false;
 scan_book_843f();
 if(failed||!book_matches||book_choice_offset<=0||book_choice_offset>=32000)return false;
 history_index=(int)count-1;draw_value=draw;accept_hint_82db();
 BCMove move=host(working_move);BCPosition check=*root;
 if(failed||!bc_play(&check,move))return false;
 *out=move;return true;
}
'''
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(pre+functions+post)
