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
int effect_task_6ab1(register AnimationTask *task)
{
 Frame *a,*b;register Actor *c;int *d;int e;unsigned f;
 if(!task_ready_772d(task))return 0;
 d=(int *)task->word0;c=task->actor;e=task->sequence;
 if(!d) {
  d=frame_lists[e];task->detail.words.word14=c->old_x;task->detail.words.word16=c->old_y;
  for(f=0;*d!=-1;f++,d++);
  task->detail.bytes.stage=f>>1;task->detail.bytes.inverted=1;d=frame_lists[e];b=&frames[*d++];
  attach_actor(c->old_x,c->old_y,c->colour,b,c);c->flag=0;
 }else {
  b=c->frame;a=(Frame *)pop_value();compose_frame_3b3a(b,*d++,a);
  interpolate_position_5ebc(task->detail.words.word14,task->detail.words.word16,task->detail.words.word14+(signed char)task->detail.bytes.x,task->detail.words.word16+(signed char)task->detail.bytes.y,task->detail.bytes.stage,task->detail.bytes.inverted++);
  b=a;attach_actor(motion_x,motion_y,c->colour,b,c);c->flag=1;
 }
 if(task->detail.bytes.stage+1==task->detail.bytes.inverted) {
  c->old_x=task->detail.words.word14+(signed char)task->detail.bytes.x;c->old_y=task->detail.words.word16+(signed char)task->detail.bytes.y;return 1;
 }else {task->word0=(int)d;return 0;}
}
