typedef unsigned char Byte;
typedef struct {Byte width,height;signed char x,y;char huge *pixels;} Frame;
typedef struct Actor {int x,y,old_x,old_y,flag;Byte colour,square;int left,right,top,bottom;Frame *frame;void far *resource;struct Actor *next;} Actor;
typedef struct {int kind,code,status,reserved,x,y;} Event;
/* A queued event is copied as ten actual words. Only its prefix is decoded here. */
typedef struct {int words[10];} EventImage20;
extern void far graphics_rect_110d_0003(int,int,int,int);
void rect_2079(int left,int top,int right,int bottom)
{
 graphics_rect_110d_0003(left,top,right,top);
 graphics_rect_110d_0003(right,top,right,bottom);
 graphics_rect_110d_0003(left,bottom,right,bottom);
 graphics_rect_110d_0003(left,top,left,bottom);
}
extern Byte board_action_active_0056;
extern int cursor_kind_0ef4,cursor_actor_57d0,editor_piece_008a;
extern unsigned selected_square_0efa;
extern Actor actors[];
extern int *command_cursor_0070;
extern void input_update_0886(void),detach_actor(Actor *),refresh_panel_1d51(void);
extern void outline_piece_578c(int,int,int,int,unsigned),place_piece_22c5(int,int);
extern Event *next_event_184d(void);
extern int *far write_command_fd4e(int *);
void board_action_20d5(void)
{
 unsigned a=9;
 Event *b;
 int c,d;
 board_action_active_0056=1;input_update_0886();
 if(cursor_kind_0ef4&&actors[cursor_actor_57d0].frame)detach_actor(actors+cursor_actor_57d0);
 for(;;) {
  c=editor_piece_008a>=6?295:7;
  d=editor_piece_008a%6*24+4;
  b=next_event_184d();
  switch(b->kind) {
  case 7:
   if(!a)outline_piece_578c(c,d,18,24,0);
   switch(b->status) {
   case 128:
    if(c==7){if(--editor_piece_008a<0)editor_piece_008a=5;}
    else{if(--editor_piece_008a<6)editor_piece_008a=11;}
    break;
   case 130:case 131:editor_piece_008a=(editor_piece_008a+6)%12;break;
   case 129:
    if(c==7){if(++editor_piece_008a>5)editor_piece_008a=0;}
    else{if(++editor_piece_008a>11)editor_piece_008a=6;}
    break;
   case 27:
    outline_piece_578c(c,d,18,24,0);refresh_panel_1d51();selected_square_0efa=255;board_action_active_0056=0;return;
   }
   break;
  case 4:
   if(b->status==1) {
    outline_piece_578c(c,d,18,24,0);
    place_piece_22c5(c+2,d);
    *(EventImage20 *)command_cursor_0070=*(EventImage20 *)b;
    command_cursor_0070=write_command_fd4e(command_cursor_0070);
    refresh_panel_1d51();selected_square_0efa=255;board_action_active_0056=0;return;
   }
   break;
  case 3:outline_piece_578c(c,d,18,24,a);a^=9;break;
  }
 }
}
