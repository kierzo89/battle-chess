#include "capture.h"
#include <string.h>
bool bc_capture_begin(BCCapture *t,BCCaptureSync *s,unsigned side,unsigned kind,unsigned opponent,unsigned profile,bool command_active){
 if(!t)return false;
 memset(t,0,sizeof *t);
 t->sequence=bc_capture_sequence(side,kind,opponent,profile);
 if(!s||s->pending>=2||!t->sequence||(s->registered&(1u<<side))){t->failed=true;return false;}
 t->side=side;t->command_active=command_active;
 t->clock=(BCTaskClock){.control=t->sequence->control,.length=t->sequence->length};
 s->registered|=1u<<side;s->pending++;return true;
}
int bc_capture_tick(BCCapture *t,BCCaptureSync *s,unsigned colour,BCSoundEvent sound,void *context,BCCaptureFrame *frame){
 if(!t||!s||!frame||t->failed||!t->sequence||s->pending<1||s->pending>4)return -1;
 if(t->done)return 2;
 if(s->pending==1)return 0;
 if(t->terminal){
  if(s->pending!=4)return 0;
  if(t->side){s->animation_counter+=s->pending;if(!t->command_active)s->cleanup=true;}
  t->done=true;return 2;
 }
 if(!bc_task_ready(&t->clock,t->command_active,colour,sound,context)){
  if(t->clock.failed){t->failed=true;return -1;}return 0;
 }
 if(t->cursor==t->sequence->count){t->terminal=true;s->pending++;return 0;}
 *frame=t->sequence->frames[t->cursor++];return 1;
}
