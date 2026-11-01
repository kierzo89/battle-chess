/* Event, network packet, board and menu input dispatcher, native image0254.
 * next_event_184d consumes no stack arguments in its complete202B body.
 * This caller supplies none; older wait callers push one ignored word. */
typedef unsigned char Byte;
typedef union {unsigned word;struct{Byte kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
typedef struct {int kind,code,status,reserved,x,y;} Event;
typedef struct {Byte width,height;signed char x,y;char huge *pixels;} Frame;
typedef struct Actor {int x,y,old_x,old_y,flag;Byte colour,square;int left,right,top,bottom;Frame *frame;void far *resource;struct Actor *next;} Actor;
typedef struct {char *label;int command;Byte enabled,reserved;} MenuItem;
extern Byte menu_open_0044,menu_button_004a,previous_button_004b,modal_0054,text_input_active;
extern Byte highlight_flash_0057,highlight_colour_0058,mode_005a,pointer_hidden_0060,input_flag_0061;
extern Byte remote_move_ready_0062,remote_status_0063,search_active,check_8f44,animation_done;
extern Byte input_mask_11b4,remote_move_817a[2],remote_board_b082[33],flash_rank_b0a3;
extern int modes[2],current_side,waiting_0eee,menu_enabled_0ef0,board_input_0ef2,cursor_kind_0ef4;
extern unsigned selected_square_0efa,cursor_square_0efc,hover_square_0efe;
extern int pointer_x,pointer_y,paused,cursor_actor_57d0,cursor_colour_9850,last_key_8dcc;
extern Move current;
extern Actor actors[];
extern Frame cursor_frames_820e[];
extern Event *current_event;
extern MenuItem menu_items_108a[],menu_items_10a8[];
extern char remote_illegal_message_4be2[],remote_line_end_4bfe[];
extern void select_mode(int),input_update_0886(void),input_reset_e00f(void);
extern void far input_select_11ef_001e(void),far input_init_11ef_0000(void),far update_pointer_11ef_0030(void);
extern void far input_highlight_110d_0003(int,int,int,int);
extern int available_bytes_dc91(void),receive_packet_ddd3(Byte *),validate_current_8ca1(void);
extern void write_bytes_dbb5(Byte *,int);
extern int prompt_1296(char *,int,int),rand(void);
extern Event *next_event_184d(void);
extern void type_chat_14c1(int),board_pointer_0daf(int,int),board_action_20d5(void);
extern void attach_actor(int,int,int,Frame *,Actor *),detach_actor(Actor *);
extern void track_menu_512d(int,int),advance_menu_5381(void),initialize_menu_bar_4e5d(void);
extern unsigned finish_menu_5035(void);
extern Byte dispatch_tasks_67fb(void);
extern void select_pen_5b18(int),select_square_8c26(unsigned),outline_square_543a(unsigned,unsigned);
int obtain_input(void)
{
 /* a=packet read cursor, b=remote error message, c=board copy cursor;
  * d=returned menu command (SI), e=loop counter (DI), f=40-byte packet.
  * C5 retains genuine register homes and creates one CSE word naturally. */
 Byte *a;
 char *b;
 Byte *c;
 Byte f[40];
 register unsigned d=0;
 register int e;
 if(menu_open_0044)select_mode(1);
 else if(search_active)select_mode(3);
 else if(waiting_0eee&&modes[current_side]!=2) {
  if(check_8f44)select_mode(4);
  else select_mode(1);
 }else select_mode(2);
 if(!mode_005a&&check_8f44&&!pointer_hidden_0060) {
  input_init_11ef_0000();++pointer_hidden_0060;
 }
 if(!mode_005a&&!check_8f44&&pointer_hidden_0060) {
  input_select_11ef_001e();--pointer_hidden_0060;
 }
 if((modes[0]==2||modes[1]==2)&&!modal_0054&&!text_input_active&&!menu_open_0044) {
  if(available_bytes_dc91()) {
   receive_packet_ddd3(f);
   switch(f[0]) {
    case 0xa2:
     remote_move_817a[0]=f[2];remote_move_817a[1]=f[3];remote_move_ready_0062=1;
     input_reset_e00f();break;
    case 0xa1:
     e=33;a=f+2;c=remote_board_b082;
     for(;e;e--)*c++=*a++;
     input_flag_0061=1;break;
    case 0xa9:
     remote_status_0063=f[2];input_reset_e00f();break;
   }
  }
 }
 if(waiting_0eee&&modes[current_side]==2&&remote_move_ready_0062) {
  current.from=remote_move_817a[1];current.to=remote_move_817a[0];remote_move_ready_0062=0;
  if(!validate_current_8ca1()) {
   b=remote_illegal_message_4be2;
   prompt_1296(remote_illegal_message_4be2,12,0);
   write_bytes_dbb5((Byte *)b,27);
   write_bytes_dbb5((Byte *)remote_line_end_4bfe,1);
  }else if(!input_flag_0061) {waiting_0eee=0;return 6;}
 }
 rand();current_event=next_event_184d();
 switch(current_event->kind) {
  case 5:
   pointer_x=current_event->x;pointer_y=current_event->y;
   update_pointer_11ef_0030();break;
  case 6:
   last_key_8dcc=current_event->status;
   if(last_key_8dcc>=32&&last_key_8dcc<=127&&!text_input_active&&!menu_open_0044&&!modal_0054&&(modes[0]==2||modes[1]==2)) {
    type_chat_14c1(last_key_8dcc);return 0;
   }else {
   input_update_0886();
   for(e=0;e<4;e++) {
    if(menu_items_108a[e].reserved==last_key_8dcc&&menu_items_108a[e].enabled)return menu_items_108a[e].command;
   }
   if(last_key_8dcc==0xf3&&menu_items_10a8[0].enabled)return 10;
   return last_key_8dcc|0x2000;
   }
   break;
  case 3:
   if(cursor_kind_0ef4&&!paused) {
    if(actors[cursor_actor_57d0].frame)detach_actor(&actors[cursor_actor_57d0]);
    attach_actor(pointer_x,pointer_y+200,cursor_colour_9850,&cursor_frames_820e[cursor_kind_0ef4],&actors[cursor_actor_57d0]);
   }
   if(paused) {track_menu_512d(pointer_x,pointer_y);advance_menu_5381();}
   else {
    if(((waiting_0eee&&modes[current_side]!=2)||(board_input_0ef2&&!modal_0054))&&!text_input_active)board_pointer_0daf(pointer_x,pointer_y);
    if(!modal_0054&&!text_input_active)animation_done=dispatch_tasks_67fb();
   }
   if(menu_button_004a&&!previous_button_004b&&(previous_button_004b=menu_button_004a,menu_enabled_0ef0)&&!paused) {
    input_mask_11b4=0x18;input_update_0886();
    if(cursor_kind_0ef4&&actors[cursor_actor_57d0].frame)detach_actor(&actors[cursor_actor_57d0]);
    select_mode(1);initialize_menu_bar_4e5d();track_menu_512d(pointer_x,pointer_y);paused=1;menu_open_0044=1;
   }
   if(!menu_button_004a&&previous_button_004b&&(previous_button_004b=menu_button_004a,paused)) {
    paused=0;menu_open_0044=0;d=finish_menu_5035();input_mask_11b4=0x3f;
    if(d)select_mode(2);
    return d;
   }
   if(highlight_flash_0057) {
    highlight_colour_0058^=14;select_pen_5b18(highlight_colour_0058);
    input_highlight_110d_0003(flash_rank_b0a3*32+96,121,flash_rank_b0a3*32+128,123);
   }
   break;
  case 4:
   switch(current_event->status) {
    case 1:
     if(menu_button_004a)break;
      if(cursor_square_0efc!=255) {
       if(selected_square_0efa!=255) {
        if(!input_flag_0061) {
         current.from=(((cursor_square_0efc<<1)&112)^112)|(cursor_square_0efc&7);
         current.to=(((selected_square_0efa<<1)&112)^112)|(selected_square_0efa&7);
         input_update_0886();waiting_0eee=0;select_mode(2);return 6;
        }else input_update_0886();
       }else if(cursor_square_0efc==hover_square_0efe)input_update_0886();
      }else if(selected_square_0efa!=255) {
       if(board_input_0ef2)return 0x1002;
       else {
       select_square_8c26((((selected_square_0efa<<1)&112)^112)|(selected_square_0efa&7));
       outline_square_543a(selected_square_0efa,12);cursor_square_0efc=selected_square_0efa;selected_square_0efa=255;
       }
      }else return 0x1003;
     break;
    case 3:
     if(menu_enabled_0ef0)menu_button_004a=1;
     if(modal_0054)return 0x1004;
     break;
    case 2:menu_button_004a=0;break;
   }
   break;
  case 0x3d:
   if(board_input_0ef2)board_action_20d5();break;
 }
 return 0;
}
