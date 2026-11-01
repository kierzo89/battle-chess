/* 6167 command executor; both original dispatch switches retained. */
typedef unsigned char Byte;
typedef struct {Byte width,height;signed char x,y;char huge *pixels;} Frame;
typedef struct Actor {int x,y,old_x,old_y,flag;Byte colour,square;int left,right,top,bottom;Frame *frame;void far *resource;struct Actor *next;} Actor;
typedef struct {Byte operation,state,child,next,square,argument,extra,reserved;} Command;
typedef struct AnimationTask {
 int word0;Byte state,pad3;Byte *control;Actor *actor;Byte operation,command;struct AnimationTask *next;int sequence;
 union {struct {Byte from,to,kind,pad17,stage,inverted,x,y;int target_y;} bytes;
        struct {int word14,word16,word18,x,y;} words;} detail;
} AnimationTask;
typedef struct {int far *begin,far *end;int **list_begin,**list_end,*words;unsigned frame_begin,frame_end;int last_use;} AssetGroup;
extern Command commands[];
extern Actor actors[];
extern Byte cells[],actor_map[],capture_pending,animation_counter,asset_group_requested[],selected_left,selected_right;
extern int command_active,arena_fallback,*screen_x,*screen_y;
extern AssetGroup asset_groups[];
extern int *frame_lists[];
extern Byte *piece_controls[][24];
typedef union {struct {Byte *left,*right;} named;Byte *by_side[2];} CurrentControls;
extern CurrentControls current_controls;
extern Byte step_x[][2],step_y[][2];
extern AnimationTask *allocate_task_3b0c(void);
extern void release_task_3ae3(AnimationTask *),manage_asset_arena(void),detach_actor(Actor *),schedule_task_6796(AnimationTask *);
void run_command_6167(Byte command)
{
 Byte a,b;register Command *c;register AnimationTask *d;Byte e;int f;Byte g,h;int i;Byte j;
 c=&commands[command];a=c->square;b=c->argument;e=c->extra;c->state=1;
 d=allocate_task_3b0c();d->command=command;d->actor=&actors[actor_map[a]];d->word0=0;d->operation=c->operation;d->state=0;
 {Byte k;k=cells[a];g=k&7;h=(k&56)>>3;}
 if(command_active) {
  f=0;
  switch(c->operation) {
  case 7:
   if(a!=b&&e>1)d->operation=1;else {f=1;break;}
  case 1:
   d->sequence=g+16;d->detail.bytes.from=d->actor->square;d->actor->square=b;d->detail.bytes.to=b;d->detail.bytes.kind=0;schedule_task_6796(d);break;
  case 8:
   d->sequence=g+16;d->detail.bytes.x=step_x[b][0];d->detail.bytes.y=step_y[b][0];d->detail.bytes.stage=0;schedule_task_6796(d);break;
  case 3:
   d->sequence=b;d->detail.words.word14=255;
   if(a!=b) {
    if(capture_pending){animation_counter+=capture_pending*4;capture_pending=0;detach_actor(&actors[actor_map[b]]);}
    cells[b]=cells[a];cells[a]=0;actor_map[b]=actor_map[a];
   }
   schedule_task_6796(d);break;
  case 5:capture_pending=1;
  case 2:case 4:case 6:f=1;break;
  }
  if(c->next!=255)run_command_6167(c->next);
  if(f) {
   commands[d->command].state=0;j=d->command;release_task_3ae3(d);
   {Byte child;child=commands[j].child;if(child!=255)run_command_6167(child);}
  }
 }else {
  switch(c->operation) {
  case 1:
   d->sequence=asset_groups[g-1].list_begin-frame_lists;
   i=(g==1||g==3||g==6)?h>>1:h;d->sequence+=i;
   d->control=piece_controls[g][h];d->detail.bytes.from=d->actor->square;d->actor->square=b;d->detail.bytes.to=b;d->detail.bytes.kind=0;schedule_task_6796(d);break;
  case 5:
   d->sequence=b?0x1052:0x103e;d->detail.bytes.from=b;capture_pending++;
   if(capture_pending==2&&arena_fallback){arena_fallback=1;asset_group_requested[selected_left-1]=255;asset_group_requested[selected_right-1]=255;manage_asset_arena();}
   d->control=current_controls.by_side[b];schedule_task_6796(d);break;
  case 4:
   d->sequence=asset_groups[g-1].list_begin-frame_lists;
   if(g==1||g==3||g==6)d->sequence+=h>>1;else d->sequence+=h;
   d->control=piece_controls[g][h];d->detail.bytes.x=step_x[b][0];d->detail.bytes.y=step_y[b][0];d->detail.bytes.stage=0;schedule_task_6796(d);break;
  case 8:
   d->sequence=asset_groups[g-1].list_begin-frame_lists;
   if(g==1||g==3||g==6)d->sequence+=h>>1;else d->sequence+=h;
   d->detail.bytes.x=step_x[b][0];d->detail.bytes.y=step_y[b][0];d->detail.bytes.stage=0;schedule_task_6796(d);break;
  case 7:
   d->sequence=asset_groups[g-1].list_begin-frame_lists;d->actor->square=b;d->detail.bytes.inverted=0;
   if(g==1||g==3||g==6)d->sequence+=h>>1;else d->sequence+=h;
   d->control=piece_controls[g][h];
   if(e==1){d->detail.words.x=screen_x[b]+9;d->detail.words.y=screen_y[b>>3]-5;if(h>=4&&h<=6)d->detail.bytes.inverted=1;}
   else if(e==0){d->detail.words.x=screen_x[b]-9;d->detail.words.y=screen_y[b>>3]+5;}
   else {d->detail.words.x=screen_x[b];d->detail.words.y=screen_y[b>>3];}
   d->detail.bytes.stage=0;schedule_task_6796(d);break;
  case 2:
   d->detail.bytes.from=(cells[a]>>3)&7;d->detail.bytes.to=b;d->detail.bytes.kind=g;d->sequence=0;
   cells[a]=(cells[a]&71)|(b<<3);schedule_task_6796(d);break;
  case 3:
   d->sequence=b;d->detail.words.word14=255;
   if(a!=b){
    if(capture_pending){capture_pending=0;d->detail.words.word14=actor_map[b];}
    cells[b]=cells[a];cells[a]=0;actor_map[b]=actor_map[a];
    for(i=0;i<8;asset_group_requested[i++]=255);
   }
   schedule_task_6796(d);break;
  case 6:
   d->sequence=(asset_groups[g-1].list_begin-frame_lists)+b+14;
   if(b>1)cells[a]=(d->actor->x>160?56:24)|(cells[a]&71);
   else cells[a]=(cells[a]&71)|(b<<5);
   schedule_task_6796(d);break;
  }
  if(c->next!=255)run_command_6167(c->next);
 }
}
