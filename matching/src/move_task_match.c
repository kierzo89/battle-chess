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


extern int command_active,motion_x,motion_y;
extern int *frame_lists[];
extern int task_ready_772d(AnimationTask *),pop_value(void);
extern void compose_frame_3b3a(Frame *,int,Frame *),interpolate_position_5ebc(int,int,int,int,int,int);
int move_task_68ea(register AnimationTask *task)
{
 Frame *a,*b;register Actor *c;int *d;int e,f;
 if(!task_ready_772d(task))return 0;
 d=(int *)task->word0;c=task->actor;e=task->sequence;
 if(!task->detail.bytes.kind) {
  d=frame_lists[e];
  if(!command_active) {
   for(f=0;*d!=-1;f++,d++);
   task->detail.bytes.kind=f;d=frame_lists[e];
  }else task->detail.bytes.kind=8;
  task->detail.bytes.pad17=1;
  b=command_active?&frames[e]:&frames[*d++];
  motion_x=screen_x[task->detail.bytes.from];motion_y=screen_y[task->detail.bytes.from>>3];
  attach_actor(motion_x,motion_y,c->colour,b,c);c->flag=0;
 }else {
  if(task->detail.bytes.pad17>=task->detail.bytes.kind) {
   c->old_x=screen_x[task->detail.bytes.to];c->old_y=screen_y[task->detail.bytes.to>>3];return 1;
  }
  b=c->frame;
  if(!command_active){a=(Frame *)pop_value();compose_frame_3b3a(b,*d++,a);b=a;}
  interpolate_position_5ebc(screen_x[task->detail.bytes.from],screen_y[task->detail.bytes.from>>3],screen_x[task->detail.bytes.to],screen_y[task->detail.bytes.to>>3],task->detail.bytes.kind,task->detail.bytes.pad17++);
  attach_actor(motion_x,motion_y,c->colour,b,c);c->flag=!command_active;
 }
 task->word0=(int)d;return 0;
}
