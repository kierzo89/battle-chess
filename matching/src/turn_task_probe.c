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
typedef struct {int huge *begin,huge *end;int **list_begin,**list_end,*words;unsigned frame_begin,frame_end;int last_use;} AssetGroup;
extern AssetGroup asset_groups[];
extern Byte *piece_controls[][24];
int turn_task_730c(register AnimationTask *task)
{
 Frame *a,*b;unsigned c;Byte d;register Actor *e;int *f;int g;
 if(task->sequence&&!task_ready_772d(task))return 0;
 f=(int *)task->word0;e=task->actor;g=task->detail.bytes.from;d=task->detail.bytes.kind;
 if(!f) {
  if(task->sequence) {
   if(((task->sequence+g)&7)==task->detail.bytes.to)return 1;
   g=(task->sequence+g)&7;c=task->sequence>0?g+8:g+16;
   if(d==3||d==6||d==1)c>>=1;
   if(d==2||d==5||d==1) {
    f=asset_groups[d-1].list_begin[c];f+=2;
    b=e->frame;a=(Frame *)pop_value();compose_frame_3b3a(b,*f++,a);b=a;
    attach_actor(e->old_x,e->old_y,e->colour,b,e);e->flag=1;
   }else {
    f=asset_groups[d-1].list_begin[c];b=&frames[*f++];
    attach_actor(e->x,e->y,e->colour,b,e);e->flag=0;
   }
  }else {
   if(task->detail.bytes.to==g)return 1;
   task->sequence=((task->detail.bytes.to-g)&4)?-1:1;
   c=task->sequence>0?g+8:g+16;
   if(d==3||d==6||d==1){task->sequence<<=1;f=asset_groups[d-1].list_begin[c>>1];}
   else f=asset_groups[d-1].list_begin[c];
   b=&frames[*f++];attach_actor(e->old_x,e->old_y,e->colour,b,e);e->flag=0;
  }
  task->control=piece_controls[d][2*g+(task->sequence<0?0:1)+8];task->state=0;task_ready_772d(task);
 }else {
  b=e->frame;a=(Frame *)pop_value();compose_frame_3b3a(b,*f++,a);b=a;
  attach_actor(e->x,e->y,e->colour,b,e);e->flag=1;
 }
 if(*f==-1)f=0;
 task->word0=(int)f;task->detail.bytes.from=g;return 0;
}
