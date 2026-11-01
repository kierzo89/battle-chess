/* Scan at most the actual menu-item count, wrapping in the requested direction. */
typedef unsigned char Byte;
typedef struct {char *label;int command;Byte enabled,reserved;} MenuItem;
extern int menu_rows;
int choose_action_2008(int index,int step,MenuItem *items)
{
 int count;
 if(!step)step=-1;
 for(count=0;count!=menu_rows;count++) {
  if(items[index].enabled)return index;
  index+=step;
  index=index>=menu_rows?0:index;
  index=index<0?menu_rows-1:index;
 }
 return 255;
}

typedef struct {Byte width,height;signed char x,y;char huge *pixels;} Frame;
typedef struct Actor {int x,y,old_x,old_y,flag;Byte colour,square;int left,right,top,bottom;Frame *frame;void far *resource;struct Actor *next;} Actor;
typedef struct {int kind,code,status,reserved,x,y,data[4];} Event;
/* A queued event is copied as ten actual words. Only its prefix is decoded here. */
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
extern void outline_piece_578c(int,int,int,int,unsigned),position_command_22c5(int,int);
extern Event *next_event_184d(void);
extern int *far write_command_fd4e(int *);
void board_action_20d5(void)
{
 /* a=blink colour; b=event prefix; c=piece-bank x; d=piece-row y. */
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
   switch((unsigned)b->status) {
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
    position_command_22c5(c+2,d);
    *(Event *)command_cursor_0070=*b;
    command_cursor_0070=write_command_fd4e(command_cursor_0070);
    refresh_panel_1d51();selected_square_0efa=255;board_action_active_0056=0;return;
   }
   break;
  case 3:outline_piece_578c(c,d,18,24,a);a^=9;break;
  }
 }
 /* Native compiler output also retains this unreachable final cleanup. */
 board_action_active_0056=0;
}

/* Queue one position event and advance the real command ring cursor. */
extern int *command_cursor_0070;
extern int *far write_command_fd4e(int *);
void position_command_22c5(int x,int y)
{
 *(long *)command_cursor_0070=5L;
 command_cursor_0070[4]=x;
 command_cursor_0070[5]=y;
 command_cursor_0070=write_command_fd4e(command_cursor_0070);
}

extern void far input_poll_11ef_00b9(void);
extern int input_x_005c,input_y_005e,pointer_x,pointer_y,buttons_8d04,previous_buttons_9888;
extern int *command_cursor_0070;
extern unsigned long current_ticks_9884,last_event_ticks_b07a;
extern Event event_tick_0072;
extern Byte modal_0054;
extern void position_command_22c5(int,int);
extern void input_control_1c77(char);
extern int *far write_command_fd4e(int *);
extern long ticks_ea5b(void);
extern int poll_event(Byte *,Byte *,Byte *);
void pump_input_2301(void)
{
 /* a=scan byte; b=changed-button mask; c=ASCII byte; d=modifier flags. */
 char a,c,d;
 int b;
 input_poll_11ef_00b9();
 if(input_x_005c!=pointer_x||input_y_005e!=pointer_y)position_command_22c5(input_x_005c,input_y_005e);
 if(previous_buttons_9888!=buttons_8d04) {
  for(b=1;b!=3;b++) {
   if((b&buttons_8d04)!=(b&previous_buttons_9888)) {
    *(long *)command_cursor_0070=4L;
    command_cursor_0070[2]=((buttons_8d04>>(b-1))&1)+(b&2);
    command_cursor_0070=write_command_fd4e(command_cursor_0070);
   }
  }
  previous_buttons_9888=buttons_8d04;
 }
 current_ticks_9884=ticks_ea5b();
 if(current_ticks_9884-last_event_ticks_b07a>1) {
  *(Event *)command_cursor_0070=event_tick_0072;
  command_cursor_0070=write_command_fd4e(command_cursor_0070);
  last_event_ticks_b07a=current_ticks_9884;
 }
 if(poll_event((Byte *)&d,(Byte *)&c,(Byte *)&a)) {
  *(long *)command_cursor_0070=6L;
  d&=0x2f;
  if(!(d&4)) {
   if(!(d&8)) {
    if(modal_0054) {
     if(c==13) {
      *(long *)command_cursor_0070=4L;
      command_cursor_0070[2]=1;
      command_cursor_0070=write_command_fd4e(command_cursor_0070);
     }else if(c==27) {
      *(long *)command_cursor_0070=4L;
      command_cursor_0070[2]=3;
      command_cursor_0070=write_command_fd4e(command_cursor_0070);
      *(Event *)command_cursor_0070=event_tick_0072;
      command_cursor_0070=write_command_fd4e(command_cursor_0070);
      *(long *)command_cursor_0070=4L;
      command_cursor_0070[2]=2;
      command_cursor_0070=write_command_fd4e(command_cursor_0070);
     }
    }else {
     if(a==60) {
      command_cursor_0070[2]=32;
      command_cursor_0070=write_command_fd4e(command_cursor_0070);
     }else {
      if(command_cursor_0070[2]=(c>='a'&&c<='z')?c-32:c)command_cursor_0070=write_command_fd4e(command_cursor_0070);
     }
    }
   }else input_control_1c77(a);
  }
 }
}

/* Load the selected archive bank into the 70,000-byte huge byte buffer. */
extern unsigned char mode_11aa;
extern unsigned long far *asset_lengths, far *asset_offsets;
extern unsigned char huge asset_buffer[];
extern char asset_overflow[];
extern void select_asset_file(int), seek_asset(long);
extern void read_asset(unsigned char huge *, long);
extern int prompt_1296(char *, int, int);
extern void exit_07f3();

void load_asset_bank(void)
{
    unsigned long a;
    int b, c;
    select_asset_file(0);
    if (mode_11aa) { b=15; c=31; }
    else { b=0; c=15; }
    a=0;
    for (;b!=c;b++) {
        if (a+asset_lengths[b]>70000UL) {
            prompt_1296(asset_overflow,12,0);
            exit_07f3();
        }
        seek_asset(asset_offsets[b]);
        read_asset(asset_buffer+a,asset_lengths[b]);
        a+=asset_lengths[b];
    }
}
