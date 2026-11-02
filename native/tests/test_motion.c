#include "motion.h"
#include <assert.h>
#include <string.h>
#include <stdio.h>
static void put(uint8_t data[33],unsigned square,unsigned kind){unsigned i=(square>>4)*8+(square&7);if(i&1)data[1+i/2]|=kind;else data[1+i/2]|=kind<<4;}
int main(void){
 BCPosition p;bc_position_initial(&p);BCPosition original=p;BCMoveList list;bc_generate_legal(&p,&list);
 for(size_t i=0;i<list.count;i++){
  BCMotion m;assert(bc_motion_begin(&m,&p,list.moves[i],100,false));assert(m.active&&m.frame==1);
  assert(bc_motion_hidden_square(&m)==list.moves[i].from);
  bc_motion_tick(&m,101,false);assert(m.frame==1);
  bc_motion_tick(&m,102,true);assert(m.frame==1);
  for(unsigned step=1;step<8;step++){bc_motion_tick(&m,100+2*step,false);assert(m.active&&m.frame==step+1);}
  for(unsigned tick=116;m.active&&tick<400;tick+=2){bc_motion_tick(&m,tick,false);
   if(m.active&&list.moves[i].kind==5){assert(m.display.cells[2].kind==4&&m.display.cells[5].kind==4);}
  }
  assert(!m.active);assert(!memcmp(&p,&original,sizeof p));
 }
 /* Exercise every opening move with the retained turn/walk/terminal-turn
  * program, including three-leg knight paths and complete visual transfer. */
 for(size_t i=0;i<list.count;i++){
  BCMotion m;assert(bc_motion_begin(&m,&p,list.moves[i],0,true));
  bool turned=false,walked=false;
  for(unsigned tick=2;m.active&&tick<1000;tick+=2){
   turned|=m.operation==2;walked|=m.operation==1;
   bc_motion_tick(&m,tick,false);
  }
  assert(!m.active&&!m.failed&&turned&&walked);
  BCPosition after=p;assert(bc_play(&after,list.moves[i]));
  for(unsigned sq=0;sq<120;sq++)if(!(sq&0x88)){
   assert(m.display.cells[sq].kind==after.board.cells[sq].kind);
   if(after.board.cells[sq].kind)assert(m.display.cells[sq].side==after.board.cells[sq].side);
  }
  assert(m.facing[list.moves[i].to]==4);
 }
 uint8_t data[33]={0};put(data,4,1);put(data,0,3);put(data,7,3);put(data,116,9);
 memset(&p,0,sizeof p);assert(bc_unpack(&p.board,data));p.ep=-1;p.fullmove=1;p.castle[0]=3;
 bc_generate_legal(&p,&list);unsigned castles=0;
 for(size_t i=0;i<list.count;i++)if(list.moves[i].special&&list.moves[i].kind==1){
  castles++;BCMotion m;assert(bc_motion_begin(&m,&p,list.moves[i],0,true));assert(m.count>=4);
  unsigned t=2;while(m.active&&bc_motion_piece(&m).kind==1&&t<400){bc_motion_tick(&m,t,false);t+=2;}
  assert(m.active&&bc_motion_piece(&m).kind==3);
  assert(m.display.cells[list.moves[i].to].kind==1&&m.display.cells[4].kind==0);
  while(m.active&&t<400){bc_motion_tick(&m,t,false);t+=2;}
  assert(!m.active);
 }
 assert(castles==2);
 BCMotion m;BCMove capture={0,16,0,3,6};assert(!bc_motion_begin(&m,&p,capture,0,false));assert(!m.active);
 BCMove invalid={0,119,0,3,0};assert(!bc_motion_begin(&m,&p,invalid,0,false));
 puts("PASS: 20 legal opening motions, countdown/input gate, both sequential castles, state preservation and capture exclusion.");return 0;
}
