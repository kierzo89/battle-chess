#include "commands.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
typedef struct {unsigned left[4],started,completed,visits[1024],n;BCCommands *q;} Context;
static bool start(void *opaque,unsigned slot,unsigned command,const BCStageCommand *c){
 Context *x=opaque;assert(x->q->used<=4);
 if(c->parent!=255)assert(x->q->state[c->parent]==2);
 x->left[slot]=c->argument;x->started++;(void)command;return true;
}
static int step(void *opaque,unsigned slot,unsigned command,const BCStageCommand *c){
 Context *x=opaque;assert(x->n<1024);x->visits[x->n++]=command;(void)c;
 if(x->left[slot]){x->left[slot]--;return 0;}
 x->completed++;return 1;
}
int main(void){
 /* Parent0 launches sibling1/2; finishing1 reuses its slot for3 at the
  * tail, so original post-release traversal does NOT visit2 until next call. */
 BCStagePlan p={.count=5};p.commands[0]=(BCStageCommand){255,2,0,0,0,false};
 p.commands[1]=(BCStageCommand){0,2,0,0,0,false};p.commands[2]=(BCStageCommand){0,2,1,0,0,false};
 p.commands[3]=(BCStageCommand){1,2,0,0,0,false};p.commands[4]=(BCStageCommand){255,3,0,0,0,false};
 BCCommands q;Context x={.q=&q};assert(bc_commands_begin(&q,&p,start,&x));
 assert(x.started==1);assert(bc_commands_tick(&q,start,step,&x)==0);
 assert(x.n==2&&x.visits[0]==0&&x.visits[1]==2); /* reused0 now sibling1, next is2 */
 assert(bc_commands_tick(&q,start,step,&x)==0);
 assert(x.n==3&&x.visits[2]==1); /* child3 replaces1 at tail */
 while(!q.done)assert(bc_commands_tick(&q,start,step,&x)>=0);
 const unsigned expected[]={0,2,1,3,4};assert(x.n==5&&!memcmp(x.visits,expected,sizeof expected));
 assert(x.started==5&&x.completed==5&&q.used==0);
 /* Refuse overflow and malformed topology without inventing extra slots. */
 p.count=6;for(unsigned i=1;i<6;i++)p.commands[i]=(BCStageCommand){0,2,0,1,0,false};
 memset(&x,0,sizeof x);x.q=&q;assert(bc_commands_begin(&q,&p,start,&x));
 assert(bc_commands_tick(&q,start,step,&x)==-1&&q.failed);
 p.count=2;p.commands[1].parent=1;assert(!bc_commands_begin(&q,&p,start,&x));
 /* Exercise actual recovered capture dependencies rather than only a
  * synthetic graph. Task durations are test substitutes, not animation proof. */
 BCPosition board;bc_position_initial(&board);
 const unsigned from[]={20,99,52},to[]={52,67,67};
 for(unsigned turn=0;turn<3;turn++){
  BCMoveList legal;bc_generate_legal(&board,&legal);bool found=false;
  for(size_t j=0;j<legal.count;j++)if(legal.moves[j].from==from[turn]&&legal.moves[j].to==to[turn]){
   if(turn==2){
    assert(bc_stage_plan(&board,legal.moves[j],&p));
    unsigned captures=0;
    for(unsigned k=0;k<p.count;k++){captures+=p.commands[k].operation==5;p.commands[k].argument=p.commands[k].operation%3;}
    assert(captures==2);memset(&x,0,sizeof x);x.q=&q;
    assert(bc_commands_begin(&q,&p,start,&x));
    unsigned ticks=0;while(!q.done&&ticks++<1000)assert(bc_commands_tick(&q,start,step,&x)>=0);
    assert(q.done&&x.started==p.count&&x.completed==p.count);
   }
   assert(bc_play(&board,legal.moves[j]));found=true;break;
  }
  assert(found);
 }
 puts("PASS: dependency starts, four-slot reuse traversal, serialized roots, overflow and malformed parent rejection.");
}
