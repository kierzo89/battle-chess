#include "motion.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "../../matching/src/promote_ui_match.c"
Move current,history,observed;int ready;static unsigned calls;
int apply_bb0e(Move move,int suppress){assert(suppress==1);observed=move;calls++;return 9;}
static void put(uint8_t data[33],unsigned square,unsigned kind){unsigned i=(square>>4)*8+(square&7);if(i&1)data[1+i/2]|=kind;else data[1+i/2]|=kind<<4;}
int main(void){
 unsigned cases=0;
 for(unsigned kind=1;kind<=6;kind++)for(unsigned special=0;special<2;special++){
  history=(Move){.from=20,.to=36,.special=special};history.kind.byte.low=kind;
  calls=0;ready=0;int promoted=promote_ui_9371();
  assert(promoted==(int)(special&&kind>=2&&kind<=5));
  assert(calls==(unsigned)promoted);
 }

 for(unsigned side=0;side<2;side++)for(unsigned capture=0;capture<2;capture++)for(unsigned kind=2;kind<=5;kind++){
  unsigned from=side?16:96,to=(side?0:112)+capture;
  uint8_t packed[33]={0};put(packed,4,1);put(packed,116,9);put(packed,from,6+side*8);
  if(capture)put(packed,to,3+(1-side)*8);
  BCPosition p={0};assert(bc_unpack(&p.board,packed));p.board.side=side;p.ep=-1;p.fullmove=1;
  BCMoveList l;bc_generate_legal(&p,&l);BCMove m={0};
  for(size_t i=0;i<l.count;i++)if(l.moves[i].from==from&&l.moves[i].to==to&&l.moves[i].kind==kind)m=l.moves[i];
  assert(m.special&&m.kind==kind);
  history=(Move){.from=from,.to=to,.special=1};history.kind.byte.low=kind;history.kind.byte.high=m.capture;
  calls=0;ready=0;assert(promote_ui_9371()==1&&calls==1&&ready==9);
  assert(observed.from==(int)from&&observed.to==(int)to&&!observed.special&&observed.kind.byte.low==6&&observed.kind.byte.high==m.capture);
  BCStagePlan plan;assert(bc_stage_plan(&p,m,&plan));
  unsigned capture_tasks=0;for(unsigned i=0;i<plan.count;i++)capture_tasks+=plan.commands[i].operation==5;
  assert(capture_tasks==capture*2);
  BCMotion motion;assert(bc_motion_begin(&motion,&p,m,0,true)&&motion.battle_mode);
  bool pawn=false;unsigned tick=2;
  while(motion.active&&tick<6000){
   int id=motion.battle.actor_map[from];if(id>=0&&motion.battle.actors[id].piece.kind==6)pawn=true;
   bc_motion_tick(&motion,tick,false);assert(!motion.failed);tick+=2;
  }
  assert(pawn&&!motion.active&&motion.battle.done);
  int id=motion.battle.actor_map[to];assert(id>=0&&motion.battle.actors[id].visible&&motion.battle.actors[id].piece.kind==kind);
  assert(motion.battle.actor_map[from]<0);
  if(capture)assert(motion.battle.capture.animation_counter==4);
  assert(p.board.cells[from].kind==6);cases++;
 }
 printf("PASS: %u promotion animations, both colours/four choices/quiet and capture; recovered caller normalization, pawn motion and final selected sprite.\n",cases);
}
