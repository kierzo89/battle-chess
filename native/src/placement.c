#include "placement.h"
#include <string.h>
static bool coordinate(int v){return v>=-1024&&v<=1024;}
bool bc_placement_begin(BCPlacement *t,BCPlacementKind mode,unsigned kind,unsigned orientation,unsigned profile,int fx,int fy,int tx,int ty,bool active){
 if(!t)return false;
 memset(t,0,sizeof *t);t->sequence=bc_walk_sequence(kind,orientation,profile);
 if(mode<BC_EFFECT||mode>BC_OFFSET_FULL||!t->sequence||!coordinate(fx)||!coordinate(fy)||!coordinate(tx)||!coordinate(ty)){t->failed=true;return false;}
 t->steps=mode==BC_OFFSET_FULL?t->sequence->count:t->sequence->count/2;
 t->total=t->steps+(mode==BC_EFFECT);
 if(!t->steps||t->steps>128||t->total>t->sequence->count){t->failed=true;return false;}
 t->from_x=t->x=t->anchor_x=fx;t->from_y=t->y=t->anchor_y=fy;t->to_x=tx;t->to_y=ty;
 t->mode=mode;t->command_active=active;
 t->clock=(BCTaskClock){.control=t->sequence->control,.length=t->sequence->length};return true;
}
int bc_placement_tick(BCPlacement *t,unsigned colour,BCSoundEvent sound,void *context){
 if(!t||t->failed||!t->sequence)return -1;
 if(t->done)return 2;
 if(!bc_task_ready(&t->clock,t->command_active,colour,sound,context)){
  if(t->clock.failed){t->failed=true;return -1;}return 0;
 }
 t->frame=t->emitted;
 if(!bc_interpolate(t->from_x,t->from_y,t->to_x,t->to_y,t->steps,t->emitted,&t->x,&t->y)){t->failed=true;return -1;}
 if(++t->emitted==t->total){t->done=true;t->anchor_x=t->to_x;t->anchor_y=t->to_y;}
 return 1;
}
