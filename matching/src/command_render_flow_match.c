/* Rebuild visible board actors and interpolate a screen-space position. */
typedef unsigned char Byte;
typedef struct {Byte width,height;signed char x,y;char huge *pixels;} Frame;
typedef struct Actor {int x,y,old_x,old_y,flag;Byte colour,square;int left,right,top,bottom;Frame *frame;void far *resource;struct Actor *next;} Actor;
extern Actor actors[];
extern Frame frames[];
extern Byte cells[],actor_map[],*frame_index;
extern int *screen_x,*screen_y;
extern void attach_actor(int,int,int,Frame *,Actor *);
extern int motion_x,motion_y;

typedef struct {Byte operation,state,child,next,square,argument,extra,reserved;} Command;
typedef struct AnimationTask {
 int word0;Byte state,pad3;Byte *control;Actor *actor;Byte operation,command;struct AnimationTask *next;int sequence;
 union {struct {Byte from,to,kind,pad17,stage,inverted,x,y;int target_y;} bytes;
        struct {int word14,word16,word18,x,y;} words;} detail;
} AnimationTask;
typedef struct {int huge *begin,huge *end;int **list_begin,**list_end,*words;unsigned frame_begin,frame_end;int last_use;} AssetGroup;
extern Command commands[];
extern Actor actors[];
extern Byte cells[],actor_map[],capture_pending,animation_counter;
typedef union {struct {Byte loaded[6],requested[6],left,right;} named;Byte bytes[14];} AssetState;
extern AssetState asset_state;
extern int command_active,arena_fallback,*screen_x,*screen_y;
extern AssetGroup asset_groups[];
extern int *frame_lists[];
extern Byte *piece_controls[][24];
typedef union {struct {Byte *left,*right;} named;Byte *by_side[2];} CurrentControls;
extern CurrentControls current_controls;
extern Byte step_x[][2],step_y[][2];
extern AnimationTask *allocate_task_3b0c(void);
extern void release_task_3ae3(AnimationTask *),manage_asset_arena(void),detach_actor(Actor *),schedule_task_6796(AnimationTask *);
extern Command commands[32];
extern Byte command_cursor,command_root,cells[];
extern int command_active;
extern void manage_asset_arena(void),run_command_6167(Byte);
void advance_60bb(void);

void display_board_5e18(void)
{
 /* a: board cursor; b: actor index; c: square; d/e: coordinate cursors. */
 Byte *a;register int b,c;int *d,*e;
 b=0;d=screen_x;e=screen_y;a=cells;
 for(c=0;c<=63;c++) {
  if(*a) {
   actors[b].square=c;actor_map[c]=b;
   attach_actor(*d,*e,*a&64,&frames[frame_index[*a&63]],&actors[b++]);
  }
  d++;a++;if((c&7)==7)e++;
 }
}
void interpolate_position_5ebc(register int x,register int y,int to_x,int to_y,int steps,int step)
{
 /* a/b: remainders; c/d: whole steps; e/f: signed displacement. */
 int a,b,c,d,e,f;
 e=to_x-x;f=to_y-y;
 c=e/steps;d=f/steps;a=e%steps;b=f%steps;
 if(e>=0)motion_x=c*step+(a*step+steps/2)/steps+x;
 else motion_x=c*step+(a*step-steps/2)/steps+x;
 if(f>=0)motion_y=d*step+(b*step+steps/2)/steps+y;
 else motion_y=d*step+(b*step-steps/2)/steps+y;
}

int append_command_5fbd(Byte parent,Byte operation,Byte square,Byte argument,Byte extra)
{
 register Command *record;
 Byte next;
 if(operation==5) {
  if(argument)asset_state.named.right=cells[square]&7;
  else asset_state.named.left=cells[square]&7;
 }else if(operation!=8)asset_state.bytes[5+(cells[square]&7)]=1;
 command_cursor=(command_cursor+1)&31;
 next=commands[parent].child;
 if(next==255)commands[parent].child=command_cursor;
 else {
  while(next!=255) {
   parent=next;
   next=commands[parent].next;
  }
  commands[parent].next=command_cursor;
 }
 record=&commands[command_cursor];
 record->operation=operation;
 record->square=square;
 record->argument=argument;
 record->extra=extra;
 record->state=2;
 record->child=255;
 record->next=255;
 if(operation==3&&square!=argument) {
  if(!command_active)manage_asset_arena();
  advance_60bb();
 }
 return command_cursor;
}
void advance_60bb(void)
{
 run_command_6167(command_root);
}
int begin_command_60d3(Byte operation,Byte square,Byte argument,Byte extra)
{
 register Command *record;
 command_cursor=(command_cursor+1)&31;
 record=&commands[command_cursor];
 record->operation=operation;
 record->square=square;
 record->argument=argument;
 record->extra=extra;
 record->child=255;
 record->next=255;
 command_root=command_cursor;
 if(operation==5) {
  if(argument)asset_state.named.right=cells[square]&7;
  else asset_state.named.left=cells[square]&7;
 }else if(operation!=8)asset_state.bytes[5+(cells[square]&7)]=1;
 return command_root;
}

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
   if(capture_pending==2&&arena_fallback){arena_fallback=1;asset_state.named.requested[asset_state.named.left-1]=255;asset_state.named.requested[asset_state.named.right-1]=255;manage_asset_arena();}
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
    for(i=0;i<8;asset_state.bytes[6+i++]=255);
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
