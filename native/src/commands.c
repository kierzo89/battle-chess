#include "commands.h"
#include <string.h>
static bool start_chain(BCCommands *q,int command,BCCommandStart start,void *ctx){
 while(command>=0){
  if(q->used>=4||q->state[command]!=0){q->failed=true;return false;}
  int slot=q->pool[q->used++];q->slots[slot]=(BCCommandSlot){command,-1};q->state[command]=1;
  if(!start(ctx,(unsigned)slot,(unsigned)command,&q->plan.commands[command])){q->failed=true;return false;}
  if(q->head<0)q->head=slot;
  else {int tail=q->head;while(q->slots[tail].next>=0)tail=q->slots[tail].next;q->slots[tail].next=slot;}
  command=q->sibling[command];
 }
 return true;
}
static bool root(BCCommands *q,int id,BCCommandStart start,void *ctx){
 q->root=id;q->next_root=(int)q->plan.count;
 for(unsigned i=(unsigned)id+1;i<q->plan.count;i++)if(q->plan.commands[i].parent==255){q->next_root=(int)i;break;}
 return start_chain(q,id,start,ctx);
}
bool bc_commands_begin(BCCommands *q,const BCStagePlan *plan,BCCommandStart start,void *ctx){
 if(!q)return false;
 memset(q,0,sizeof *q);q->head=-1;
 if(!plan||!start||plan->failed||!plan->count||plan->count>BC_STAGE_MAX){q->failed=true;return false;}
 q->plan=*plan;int first=0;
 for(unsigned i=0;i<plan->count;i++)q->child[i]=q->sibling[i]=-1;
 for(unsigned i=0;i<plan->count;i++){
  BCStageCommand c=plan->commands[i];
  if(c.operation<1||c.operation>8||c.square>=64){q->failed=true;return false;}
  if(c.parent==255){first=(int)i;continue;}
  if(c.parent>=i||c.parent<first){q->failed=true;return false;}
  int *link=&q->child[c.parent];while(*link>=0)link=&q->sibling[*link];*link=(int)i;
 }
 if(plan->commands[0].parent!=255){q->failed=true;return false;}
 for(int i=0;i<4;i++)q->pool[i]=i;
 return root(q,0,start,ctx);
}
int bc_commands_tick(BCCommands *q,BCCommandStart start,BCCommandStep step,void *ctx){
 if(!q||q->failed||!start||!step)return -1;
 if(q->done)return 1;
 if(q->head<0){
  if(q->next_root==(int)q->plan.count){q->done=true;return 1;}
  return root(q,q->next_root,start,ctx)?0:-1;
 }
 int slot=q->head;
 while(slot>=0){
  int command=q->slots[slot].command;
  int result=step(ctx,(unsigned)slot,(unsigned)command,&q->plan.commands[command]);
  if(result<0||result>1){q->failed=true;return -1;}
  if(result){
   q->state[command]=2;int *link=&q->head;
   while(*link!=slot)link=&q->slots[*link].next;
   *link=q->slots[slot].next;q->pool[--q->used]=slot;
   if(!start_chain(q,q->child[command],start,ctx))return -1;
  }
  /* Deliberately read AFTER child allocation. The original released record
   * may have been reused and its next field overwritten by schedule6796. */
  slot=q->slots[slot].next;
 }
 return 0;
}
