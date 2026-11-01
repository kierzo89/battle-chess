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
typedef union {struct {Byte loaded[6],requested[6],left,right;} named;Byte bytes[14];} AssetState;
extern AssetState asset_state;
extern Byte capture_pending,animation_counter;
extern void restore_active_arena(void),manage_asset_arena(void),remove_actor_5934(Actor *),dispatch_c83a(int,int,int);
int transfer_task_758c(register AnimationTask *task)
{
 attach_actor(task->actor->old_x,task->actor->old_y,task->actor->colour,&frames[frame_index[cells[task->sequence]&63]],task->actor);
 if(task->detail.words.word14!=255)remove_actor_5934(&actors[task->detail.words.word14]);
 task->actor->flag=0;return 1;
}
int capture_task_75f6(register AnimationTask *task)
{
 Byte *a;Frame *b,*c;register Actor *d;int *e;
 if(capture_pending==1)return 0;
 if(task->state==255) {
  if(capture_pending==4) {
   if(task->detail.bytes.from) {
    animation_counter+=capture_pending;
    if(!command_active){restore_active_arena();asset_state.bytes[5+asset_state.named.right]=1;asset_state.named.left=asset_state.named.right=255;manage_asset_arena();}
   }
   return 1;
  }else return 0;
 }
 if(!task_ready_772d(task))return 0;
 e=(int *)task->word0;d=task->actor;a=(Byte *)task->sequence;
 if(!e) {
  if(*a==255){task->state=255;capture_pending++;return 0;}
  e=frame_lists[*a++];c=&frames[*e++];attach_actor(d->x,d->y,d->colour,c,d);d->flag=0;
 }else {
  c=d->frame;b=(Frame *)pop_value();compose_frame_3b3a(c,*e++,b);c=b;
  attach_actor(d->x,d->y,d->colour,c,d);d->flag=1;
 }
 if(*e==-1)e=0;
 task->word0=(int)e;task->sequence=(int)a;return 0;
}
int task_ready_772d(register AnimationTask *task)
{
 Byte a;
 if(task->state){task->state--;return 0;}
 if(!command_active) {
  while((a=*task->control)>127&&a!=255) {
   dispatch_c83a(a&15,task->actor->colour,task->control[1]-64);task->control+=2;
  }
  if(*task->control==255)task->state=0;
  else task->state=*task->control++;
 }else task->state=0;
 return 1;
}

/* Existing queue routine, using the common wire-order Move8 fields. */
typedef union {unsigned word;struct {Byte kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
extern Byte cells[],actor_map[],kind_map[];
extern Actor actors[];
extern void detach_actor(Actor *);
extern void queue_piece(int,int,int,int);
void queue_move(register Move *move)
{
    /* Six original frame bytes have no observed reads/writes. */
    int a,b,c;
    Byte d,e; /* transformed source and destination */
    Move f;
    if (move->flag && move->detail.bytes.kind == 1) {
        f.to = move->to;
        f.from = move->from;
        f.flag = 0;
        f.detail.bytes.kind = move->detail.bytes.kind;
        f.detail.bytes.capture = 0;
        queue_move(&f);
        if (((Byte)move->to & 7) == 6) {
            f.to = (move->to & 0xf0) | 5;
            f.from = (move->from & 0xf0) | 7;
        } else {
            f.to = (move->to & 0xf0) | 3;
            f.from = move->from & 0xf0;
        }
        f.detail.bytes.kind = 3;
        f.detail.bytes.capture = 0;
        f.flag = 0;
        move = &f;
    }
    e = (((move->from >> 1) & 0x38) ^ 0x38) | (move->from & 7);
    d = (((move->to >> 1) & 0x38) ^ 0x38) | (move->to & 7);
    if (cells[d]) detach_actor(&actors[actor_map[d]]);
    detach_actor(&actors[actor_map[e]]);
    queue_piece(kind_map[move->detail.bytes.kind],cells[e]&64,actor_map[e],d);
    cells[e] = 0;
    if (move->flag && move->detail.bytes.kind == 6) {
        e = (e & 0x38) | (d & 7);
        detach_actor(&actors[actor_map[e]]);
        cells[e] = 0;
    }
}
