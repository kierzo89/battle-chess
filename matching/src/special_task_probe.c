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
 union {struct {Byte from,to,kind,framecounter,stage,inverted,x,y;int target_y;} bytes;
        struct {int word14,word16,word18,x,y;} words;} detail;
} AnimationTask;


extern int command_active,motion_x,motion_y;
extern int *frame_lists[];
extern int task_ready_772d(AnimationTask *),pop_value(void);
extern void compose_frame_3b3a(Frame *,int,Frame *),interpolate_position_5ebc(int,int,int,int,int,int);
int special_task_6bf9(register AnimationTask *task)
{
 register Actor *a;Frame *b;
 if(task->state){task->state--;return 0;}
 task->state=0;a=task->actor;
 if(!task->detail.bytes.stage) {
  task->detail.words.word14=a->old_x;task->detail.words.word16=a->old_y;
  task->detail.bytes.stage=6;task->detail.bytes.inverted=0;
 }
 b=a->frame;
 interpolate_position_5ebc(task->detail.words.word14,task->detail.words.word16,task->detail.words.word14+(signed char)task->detail.bytes.x,task->detail.words.word16+(signed char)task->detail.bytes.y,task->detail.bytes.stage,task->detail.bytes.inverted++);
 attach_actor(motion_x,motion_y,a->colour,b,a);a->flag=0;
 if(task->detail.bytes.stage+1==task->detail.bytes.inverted) {
  a->old_x=task->detail.words.word14+(signed char)task->detail.bytes.x;a->old_y=task->detail.words.word16+(signed char)task->detail.bytes.y;return 1;
 }
 return 0;
}
