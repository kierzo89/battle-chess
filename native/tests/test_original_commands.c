#include "commands.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
#define huge
#define far
#include "../../matching/src/task_queue_match.c"
AnimationTask *active_tasks;
Command commands[BC_STAGE_MAX];
static AnimationTask records[4],*pool[4];
static unsigned used,durations[BC_STAGE_MAX],remaining[4],events[4096],event_count,dispatch;
void release_task_3ae3(AnimationTask *t){assert(used);pool[--used]=t;}
void run_command_6167(Byte id){
 assert(used<4);AnimationTask *t=pool[used++];memset(t,0,sizeof *t);
 t->operation=commands[id].operation;t->command=id;remaining[t-records]=durations[id];
 commands[id].state=1;schedule_task_6796(t);
 if(commands[id].next!=255)run_command_6167(commands[id].next);
}
static int tick(AnimationTask *t){
 assert(event_count<4096);events[event_count++]=(dispatch<<8)|t->command;
 unsigned *left=&remaining[t-records];if(*left){--*left;return 0;}return 1;
}
#define HANDLER(name) int name(AnimationTask *t){return tick(t);}
HANDLER(move_task_68ea) HANDLER(turn_task_730c) HANDLER(transfer_task_758c)
HANDLER(effect_task_6ab1) HANDLER(capture_task_75f6) HANDLER(face_task_724d)
HANDLER(offset_task_70ef) HANDLER(special_task_6bf9)
static unsigned actual[4096],actual_count,left[4];
static bool begin(void *ctx,unsigned slot,unsigned id,const BCStageCommand *c){(void)ctx;(void)c;left[slot]=durations[id];return true;}
static int advance(void *ctx,unsigned slot,unsigned id,const BCStageCommand *c){
 (void)ctx;(void)c;assert(actual_count<4096);actual[actual_count++]=(dispatch<<8)|id;
 if(left[slot]){left[slot]--;return 0;}return 1;
}
int main(void){
 unsigned seed=19;
 for(unsigned trial=0;trial<1000;trial++){
  BCStagePlan p={.count=25};p.commands[0]=(BCStageCommand){255,1,0,0,0,false};
  /* Two independent branches with twelve dependent nodes each. */
  for(unsigned i=1;i<p.count;i++)p.commands[i]=(BCStageCommand){i<3?0:i-2,(i%8)+1,0,0,0,false};
  memset(commands,0,sizeof commands);
  for(unsigned i=0;i<p.count;i++){
   seed=seed*1664525u+1013904223u;durations[i]=(seed>>16)%5;
   commands[i].operation=p.commands[i].operation;commands[i].child=commands[i].next=255;
  }
  for(unsigned i=1;i<p.count;i++){
   unsigned parent=p.commands[i].parent;
   Byte *link=&commands[parent].child;while(*link!=255)link=&commands[*link].next;*link=i;
  }
  memset(records,0,sizeof records);for(unsigned i=0;i<4;i++)pool[i]=&records[i];
  active_tasks=NULL;used=event_count=actual_count=0;run_command_6167(0);
  BCCommands q;assert(bc_commands_begin(&q,&p,begin,NULL));
  for(dispatch=0;dispatch<1000;dispatch++){
   int expected=dispatch_tasks_67fb();int got=bc_commands_tick(&q,begin,advance,NULL);
   assert(got==expected&&actual_count==event_count&&!memcmp(events,actual,event_count*sizeof *events));
   assert(q.used==(int)used);
   if(expected)break;
  }
  assert(dispatch<1000&&q.done);
 }
 puts("PASS: 1000 two-branch command programs match unchanged recovered queue C on every dispatch, visit order, idle return and slot count.");
}
