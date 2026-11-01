#include "stage.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
static BCMove select_move(BCPosition *p,unsigned from,unsigned to){BCMoveList l;bc_generate_legal(p,&l);for(size_t i=0;i<l.count;i++)if(l.moves[i].from==from&&l.moves[i].to==to)return l.moves[i];assert(0);return (BCMove){0};}
static void targets(BCStagePlan *plan,const unsigned *expected,unsigned n){unsigned j=0;for(unsigned i=0;i<plan->count;i++){BCStageCommand c=plan->commands[i];assert(c.parent==255||c.parent<i);if(c.operation==1){assert(j<n&&c.argument==expected[j++]);assert(!c.extra_known);}}assert(j==n);}
int main(void){
 BCPosition p;bc_position_initial(&p);BCPosition before=p;BCStagePlan plan;
 assert(bc_stage_plan(&p,select_move(&p,20,52),&plan));const unsigned pawn[]={44,36};targets(&plan,pawn,2);
 assert(bc_stage_plan(&p,select_move(&p,1,34),&plan));const unsigned knight[]={58,50,42};targets(&plan,knight,3);
 assert(!memcmp(&p,&before,sizeof p));
 /* Build a real capture and verify both actor branches and explicit extras. */
 assert(bc_play(&p,select_move(&p,20,52)));assert(bc_play(&p,select_move(&p,99,67)));
 assert(bc_stage_plan(&p,select_move(&p,52,67),&plan));unsigned captures=0,known=0;
 for(unsigned i=0;i<plan.count;i++){BCStageCommand c=plan.commands[i];assert(c.parent==255||c.parent<i);if(c.operation==5)captures++;if(c.extra_known){assert(c.operation==7);known++;}}
 assert(captures==2&&known==3);
 /* Broader generated legal histories exercise construction, not rendering. */
 unsigned seed=6,plans=0;
 for(unsigned turn=0;turn<100;turn++){
  BCMoveList l;bc_generate_legal(&p,&l);if(!l.count)break;
  for(size_t i=0;i<l.count;i++){
   BCMove m=l.moves[i];if(m.special&&m.kind!=1&&m.kind!=6)continue;
   assert(bc_stage_plan(&p,m,&plan));assert(plan.count&&plan.count<BC_STAGE_MAX);
   for(unsigned j=0;j<plan.count;j++){BCStageCommand c=plan.commands[j];assert(c.square<64&&c.operation>=1&&c.operation<=8);assert(c.parent==255||c.parent<j);}
   plans++;
  }
  seed=seed*1664525u+1013904223u;assert(bc_play(&p,l.moves[seed%l.count]));
 }
 printf("PASS: recovered pawn/knight paths, capture branches/unknown extras; %u legal command plans.\n",plans);
}
