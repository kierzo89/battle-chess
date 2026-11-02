#include "motion.h"
#include "history.h"
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
static BCMove pick(BCPosition *p,int from,int to){BCMoveList l;bc_generate_legal(p,&l);for(size_t i=0;i<l.count;i++)if(l.moves[i].from==from&&l.moves[i].to==to)return l.moves[i];abort();}
int main(void){
 BCPosition p;bc_position_initial(&p);BCMove a;assert(!bc_finale_attack(&p,-1,&a));
 int from[]={21,100,22,115},to[]={37,68,54,55};for(int i=0;i<4;i++)assert(bc_play(&p,pick(&p,from[i],to[i])));
 for(unsigned side=0;side<2;side++){
  BCPosition q=p;if(side){uint8_t packed[33]={0};BCBoard mirrored=p.board;memset(mirrored.cells,0,sizeof mirrored.cells);
   for(int s=0;s<120;s++)if(!(s&0x88)){mirrored.cells[s^112]=p.board.cells[s];mirrored.cells[s^112].side^=1;}
   mirrored.side=1;bc_pack(&mirrored,packed);assert(bc_unpack(&q.board,packed));q.ep=-1;}
  BCPosition before=q;assert(bc_finale_attack(&q,-1,&a));assert(a.capture==1);assert(!bc_play(&q,a));BCStagePlan plan;assert(!bc_stage_plan(&q,a,&plan));
  BCMotion *m=calloc(1,sizeof *m);assert(m&&bc_motion_finale(m,&q,a.from,0,NULL,NULL,NULL));
  unsigned ticks=0,capture_frames=0;while(m->active&&ticks<20000){ticks+=2;bc_motion_tick(m,ticks,false);assert(!m->failed);for(unsigned i=0;i<m->battle.count;i++)capture_frames+=m->battle.actors[i].image==BC_ACTOR_CAPTURE;}
  assert(!m->active&&m->battle.done&&capture_frames);assert(!memcmp(&before,&q,sizeof q));
  unsigned kings=0;for(unsigned i=0;i<m->battle.count;i++)kings+=m->battle.actors[i].visible&&m->battle.actors[i].piece.kind==1&&m->battle.actors[i].piece.side==q.board.side;assert(!kings);free(m);
 }
 puts("PASS: both losing colours, king battle, legal-state preservation, normal move gate rejects king capture.");
}
