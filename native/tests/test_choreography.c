#include "choreography.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
static BCMove pick(BCPosition *p,unsigned from,unsigned to){BCMoveList l;bc_generate_legal(p,&l);for(size_t i=0;i<l.count;i++)if(l.moves[i].from==from&&l.moves[i].to==to)return l.moves[i];assert(0);return (BCMove){0};}
static void put(uint8_t data[33],unsigned square,unsigned kind){unsigned i=(square>>4)*8+(square&7);if(i&1)data[1+i/2]|=kind;else data[1+i/2]|=kind<<4;}
static void pairings(void){
 unsigned cases=0;
 for(unsigned kind=1;kind<=6;kind++)for(unsigned victim=2;victim<=6;victim++){
  uint8_t packed[33]={0};unsigned from=51,to=kind==3?67:kind==5?84:68;
  put(packed,kind==1?from:0,1);if(kind!=1)put(packed,from,kind);
  put(packed,119,9);put(packed,to,victim+8);
  BCPosition p={0};assert(bc_unpack(&p.board,packed));p.ep=-1;p.fullmove=1;
  BCMove m=pick(&p,from,to);BCChoreography g;assert(bc_choreography_begin(&g,&p,m,NULL));
  unsigned ticks=0;while(!g.done&&ticks++<3000){
   int status=bc_choreography_tick(&g);if(status<0)fprintf(stderr,"Pair %u vs %u failed tick%u\n",kind,victim,ticks);assert(status>=0);
  }
  assert(g.done&&g.capture.animation_counter==4&&g.capture.cleanup);
  assert(g.actor_map[from]<0&&g.actor_map[to]>=0&&g.actors[g.actor_map[to]].piece.kind==kind);
  unsigned visible=0;for(unsigned i=0;i<g.count;i++)visible+=g.actors[i].visible;
  assert(visible==(kind==1?2:3));cases++;
 }
 printf("PASS: %u legal attacker/victim kind pairings complete capture choreography.\n",cases);
}
int main(void){
 pairings();
 BCPosition p;bc_position_initial(&p);assert(bc_play(&p,pick(&p,20,52)));assert(bc_play(&p,pick(&p,99,67)));
 BCMove m=pick(&p,52,67);BCPosition original=p,after=p;assert(bc_play(&after,m));
 BCChoreography g;assert(bc_choreography_begin(&g,&p,m,NULL));
 unsigned frames[2]={0},ticks=0;bool paired=false;
 while(!g.done&&ticks++<2000){
  int result=bc_choreography_tick(&g);
  if(result<0)fprintf(stderr,"Choreography failed tick%u pending%u used%d\n",ticks,g.capture.pending,g.commands.used);
  assert(result>=0);
  unsigned active=0;
  for(unsigned i=0;i<g.count;i++)if(g.actors[i].visible&&g.actors[i].image==BC_ACTOR_CAPTURE){frames[g.actors[i].piece.side]++;active++;}
  paired|=active==2;
 }
 assert(g.done&&!g.failed&&paired&&frames[0]&&frames[1]);assert(g.capture.animation_counter==4&&g.capture.cleanup);
 unsigned visible=0;
 for(unsigned s=0;s<120;s++)if(!(s&0x88)){
  int id=g.actor_map[s];
  if(after.board.cells[s].kind){assert(id>=0&&g.actors[id].visible);assert(g.actors[id].piece.kind==after.board.cells[s].kind&&g.actors[id].piece.side==after.board.cells[s].side);}
  else assert(id<0);
 }
 for(unsigned i=0;i<g.count;i++)visible+=g.actors[i].visible;
 assert(visible==31&&!memcmp(&p,&original,sizeof p));
 printf("PASS: e4xd5 complete concurrent capture choreography, %u dispatches; both actors, one cleanup, exact final board and immutable input.\n",ticks);
}
