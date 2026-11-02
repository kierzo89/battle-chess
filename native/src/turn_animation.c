#include "turn_animation.h"
#include <string.h>
static unsigned graphics(unsigned kind){const unsigned map[]={0,2,5,6,1,3,4};return kind<=6?map[kind]:0;}
bool bc_turn_begin(BCTurnAnimation *t,unsigned kind,unsigned from,unsigned to,unsigned profile){
 memset(t,0,sizeof *t);unsigned g=graphics(kind);
 bool collapsed=g==1||g==3||g==6;
 if(!g||from>7||to>7||profile>1||(collapsed&&((from^to)&1))){t->failed=true;return false;}
 t->kind=kind;t->from=from;t->to=to;t->profile=profile;t->step=collapsed?2:1;return true;
}
int bc_turn_tick(BCTurnAnimation *t,unsigned colour,BCSoundEvent sound,void *context){
 if(t->failed)return -1;
 if(t->done)return 2;
 if(t->direction&&!bc_task_ready(&t->clock,false,colour,sound,context)){
  if(t->clock.failed){t->failed=true;return -1;}return 0;
 }
 if(t->sequence&&t->frame+1<t->sequence->count){t->frame++;return 1;}
 unsigned skip=0;
 if(t->direction){
  t->from=(t->from+t->direction*(int)t->step)&7;
  unsigned g=graphics(t->kind);if(g==1||g==2||g==5)skip=2;
 }
 if(t->from==t->to){t->done=true;return 2;}
 if(!t->direction)t->direction=((t->to-t->from)&4)?-1:1;
 t->sequence=bc_turn_sequence(t->kind,t->from,t->direction,t->profile);
 if(!t->sequence||skip>=t->sequence->count){t->failed=true;return -1;}
 t->frame=skip;
 t->clock=(BCTaskClock){.control=t->sequence->control,.length=t->sequence->length};
 (void)bc_task_ready(&t->clock,false,colour,sound,context);
 if(t->clock.failed){t->failed=true;return -1;}
 return 1;
}
