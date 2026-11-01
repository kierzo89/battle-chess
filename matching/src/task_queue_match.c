typedef unsigned char Byte;
typedef struct {Byte width,height;signed char x,y;char huge *pixels;} Frame;
typedef struct Actor {int x,y,old_x,old_y,flag;Byte colour,square;int left,right,top,bottom;Frame *frame;void far *resource;struct Actor *next;} Actor;
extern Actor actors[];
extern Frame frames[];
extern Byte cells[],actor_map[],*frame_index;
extern int *screen_x,*screen_y;
extern void attach_actor(int,int,int,Frame *,Actor *);


typedef struct {Byte operation,state,child,next,square,argument,extra,reserved;} Command;
typedef struct AnimationTask {
 int word0;Byte state,pad3;Byte *control;Actor *actor;Byte operation,command;struct AnimationTask *next;int sequence;
 union {struct {Byte from,to,kind,pad17,stage,inverted,x,y;int target_y;} bytes;
        struct {int word14,word16,word18,x,y;} words;} detail;
} AnimationTask;

extern AnimationTask *active_tasks;
extern Command commands[];
extern void release_task_3ae3(AnimationTask *),run_command_6167(Byte);
extern int move_task_68ea(AnimationTask *),turn_task_730c(AnimationTask *),transfer_task_758c(AnimationTask *),effect_task_6ab1(AnimationTask *),capture_task_75f6(AnimationTask *),face_task_724d(AnimationTask *),offset_task_70ef(AnimationTask *),special_task_6bf9(AnimationTask *);
void schedule_task_6796(register AnimationTask *task)
{
 register AnimationTask *a;
 a=active_tasks;
 if(!a)active_tasks=task;
 else {while(a->next)a=a->next;a->next=task;}
 task->next=0;
}
void unlink_task_67cb(register AnimationTask *task)
{
 register AnimationTask **a;
 a=&active_tasks;while(*a!=task)a=&(*a)->next;
 *a=task->next;release_task_3ae3(task);
}
int dispatch_tasks_67fb(void)
{
 register AnimationTask *a;register int b;Byte c;
 b=0;a=active_tasks;if(!a)return 1;
 while(a) {
  switch(a->operation) {
  case 1:b=move_task_68ea(a);break;
  case 7:b=offset_task_70ef(a);break;
  case 8:b=special_task_6bf9(a);break;
  case 3:b=transfer_task_758c(a);break;
  case 2:b=turn_task_730c(a);break;
  case 4:b=effect_task_6ab1(a);break;
  case 6:b=face_task_724d(a);break;
  case 5:b=capture_task_75f6(a);break;
  }
  if(b){commands[a->command].state=0;c=a->command;unlink_task_67cb(a);{Byte child;child=commands[c].child;if(child!=255)run_command_6167(child);}}
  a=a->next;
 }
 return 0;
}
