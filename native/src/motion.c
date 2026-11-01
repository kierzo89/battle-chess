#include "motion.h"
#include "stage.h"
#include "geometry.h"
#include <string.h>
static int x(const BCMotion *m,unsigned square){int x=0,y=0;(void)bc_geometry_anchor(m->perspective,square,&x,&y);return x;}
static int y(const BCMotion *m,unsigned square){int x=0,y=0;(void)bc_geometry_anchor(m->perspective,square,&x,&y);return y;}
bool bc_motion_begin(BCMotion *m,const BCPosition *before,BCMove move,uint64_t tick,bool perspective){
 memset(m,0,sizeof *m);m->perspective=perspective;
 if(move.capture)return false;
 BCPosition verify=*before;if(!bc_play(&verify,move))return false;
 BCStagePlan plan;if(!bc_stage_plan(before,move,&plan))return false;
 m->display=before->board;uint8_t position[120];
 for(unsigned i=0;i<120;i++)position[i]=(uint8_t)i;
 for(unsigned i=0;i<plan.count;i++){
  BCStageCommand c=plan.commands[i];if(c.operation!=1)continue;
  unsigned source=((7-c.square/8)*16)+(c.square%8);
  unsigned target=((7-c.argument/8)*16)+(c.argument%8);
  if(m->count>=32)return false;
  m->origins[m->count]=(uint8_t)source;
  m->moves[m->count++]=(BCMove){position[source],target,0,before->board.cells[source].kind,0};
  position[source]=(uint8_t)target;
 }
 if(!m->count)return false;
 m->last_tick=tick;m->active=true;m->x=x(m,move.from);m->y=y(m,move.from);
 /* Initial attach is visible immediately; the next ready call emits step1. */
 m->frame=1;return true;
}
void bc_motion_tick(BCMotion *m,uint64_t tick,bool pending){
 if(!m->active||!bc_presentation_tick(tick,&m->last_tick,pending))return;
 BCMove move=m->moves[m->index];
 if(m->frame<8){(void)bc_interpolate(x(m,move.from),y(m,move.from),x(m,move.to),y(m,move.to),8,m->frame++,&m->x,&m->y);return;}
 /* Only a completed actor transfers occupancy. Intermediate waypoints can
  * cross occupied squares (knight); never erase an unrelated display piece. */
 unsigned origin=m->origins[m->index];
 if(m->index+1==m->count||m->origins[m->index+1]!=origin){
  m->display.cells[move.to]=m->display.cells[origin];m->display.cells[origin].kind=0;
 }
 if(++m->index==m->count){m->active=false;return;}
 move=m->moves[m->index];m->frame=1;m->x=x(m,move.from);m->y=y(m,move.from);
}
int bc_motion_hidden_square(const BCMotion *m){return m->active?m->origins[m->index]:-1;}
BCCell bc_motion_piece(const BCMotion *m){return m->active?m->display.cells[m->origins[m->index]]:(BCCell){0};}
