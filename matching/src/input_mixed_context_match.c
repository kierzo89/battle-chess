/* Fill a modal region, then draw its three inset border rectangles. */
extern void far graphics_begin(void),far graphics_end(void);
extern void far graphics_rect_110d_0003(int,int,int,int);
extern void select_pen_5b18(int),rect_2079(int,int,int,int);
void fill_region_1780(register int left,register int top,int right,int bottom,int colour)
{
 graphics_begin();
 select_pen_5b18(colour);
 graphics_rect_110d_0003(left,top,right,bottom);
 rect_2079(left,top,right,bottom);
 select_pen_5b18(14);
 for(colour=0;colour<3;colour++)rect_2079(++left,++top,--right,--bottom);
 graphics_end();
}

/* The event template is copied as ten words by the native input dispatcher. */
typedef struct {int kind,code,status,reserved,x,y,data[4];} Event;
extern unsigned char mode_005a;
extern int *command_head_006e,*command_cursor_0070;
extern unsigned long current_ticks_9884,last_event_ticks_b07a;
extern Event event_tick_0072;
extern void pump_input_2301(void);
extern int handle_input_1917(char,char,char);
extern int *far write_command_fd4e(int *);
extern int poll_event();
extern long ticks_ea5b(void);
Event *next_event_184d(void)
{
 char a,b,c;
 Event *d;
 d=0;
 if(mode_005a) {
  do pump_input_2301();while(command_head_006e==command_cursor_0070);
  d=(Event *)command_head_006e;
  command_head_006e=write_command_fd4e(command_head_006e);
  return d;
 }
 do {
  current_ticks_9884=ticks_ea5b();
  if(command_head_006e!=command_cursor_0070) {
   d=(Event *)command_head_006e;
   command_head_006e=write_command_fd4e(command_head_006e);
  }else if(poll_event(&c,&b,&a))handle_input_1917(c,b,a);
  else if(current_ticks_9884-last_event_ticks_b07a>=2) {
   d=&event_tick_0072;
   last_event_ticks_b07a=current_ticks_9884;
  }
 }while(!d);
 return d;
}

typedef unsigned char Byte;
typedef struct {char *label;int command;Byte enabled,reserved;} MenuItem;
typedef struct {char *label;MenuItem *items;} Menu;
/* Native command copies use a complete 20-byte record. */

extern unsigned char modal_0054,text_input_active,board_action_active_0056,highlight_flash_0057;
extern int paused,board_input_0ef2,cursor_kind_0ef4,menu_enabled_0ef0;
extern unsigned selected_square_0efa;
extern int pointer_x,pointer_y;
extern int cursor_column_0086,cursor_row_0088,menu_rows;
extern int modes[2];
extern int *command_cursor_0070;
extern Menu *menus;
extern int *cursor_x_b0c6,*cursor_y_b0c8;
extern Event event_tick_0072;
extern int *far write_command_fd4e(int *);
extern int far command_key_fd6a(int);
extern void far special_command_1fc2(void);
extern int input_wait_1da9(char);
extern void input_dialog_260c(int),write_key_command_1cfa(int);
extern void input_control_1c77(char),refresh_panel_1d51(void),input_update_0886(void);
extern void type_chat_14c1(int),position_command_22c5(int,int);
extern int choose_action_2008(int,int,MenuItem *);
int handle_input_1917(char flags,char ascii,char scan)
{
 flags&=0x2f;
 if(flags&4)return 0;
 if(paused)input_wait_1da9(scan);
 else if(highlight_flash_0057)input_dialog_260c(scan);
 else if(modal_0054)write_key_command_1cfa(ascii);
 else if(!(flags&8)) {
  ascii=ascii>='a'&&ascii<='z'?ascii-32:ascii;
  if(text_input_active) {
   *(long *)command_cursor_0070=6L;
   if(command_cursor_0070[2]=ascii)command_cursor_0070=write_command_fd4e(command_cursor_0070);
   return;
  }
  if(board_input_0ef2&&!board_action_active_0056&&cursor_kind_0ef4&&(scan==0x53||scan==0x0e)) {
   selected_square_0efa=255;
   *(long *)command_cursor_0070=4L;command_cursor_0070[2]=1;
   command_cursor_0070=write_command_fd4e(command_cursor_0070);
   return;
  }
  if((ascii>='A'&&ascii<='H')||(ascii>='1'&&ascii<='8')) {
    if(ascii>='A'&&ascii<='H')cursor_column_0086=ascii-'A';
    else cursor_row_0088=-(ascii-'8');
    refresh_panel_1d51();
   }else if(ascii==13||ascii==' ') {
    command_cursor_0070[4]=pointer_x;command_cursor_0070[5]=pointer_y;
    *(long *)command_cursor_0070=4L;command_cursor_0070[2]=1;
    command_cursor_0070=write_command_fd4e(command_cursor_0070);
   }else if(scan==0x3b&&menu_enabled_0ef0) {
    *(long *)command_cursor_0070=4L;command_cursor_0070[2]=3;
    command_cursor_0070=write_command_fd4e(command_cursor_0070);
    *(Event *)command_cursor_0070=event_tick_0072;
    command_cursor_0070=write_command_fd4e(command_cursor_0070);
    position_command_22c5(49,8);
    *(Event *)command_cursor_0070=event_tick_0072;
    command_cursor_0070=write_command_fd4e(command_cursor_0070);
    menu_rows=100;
    position_command_22c5(85,49+8*choose_action_2008(0,1,menus->items));
    *(Event *)command_cursor_0070=event_tick_0072;
    command_cursor_0070=write_command_fd4e(command_cursor_0070);
   }else if(scan==0x3c) {
    if(modes[0]==2||modes[1]==2){input_update_0886();type_chat_14c1(0);}
   }else if(scan==0x3d||scan==0x3e) {
    *(long *)command_cursor_0070=scan;
    command_cursor_0070=write_command_fd4e(command_cursor_0070);
   }else if(board_action_active_0056) {
    *(long *)command_cursor_0070=7L;
    switch(scan) {
    case 0x48:command_cursor_0070[2]=0x80;break;
    case 0x4d:command_cursor_0070[2]=0x83;break;
    case 0x50:command_cursor_0070[2]=0x81;break;
    case 0x4b:command_cursor_0070[2]=0x82;break;
    case 1:command_cursor_0070[2]=27;break;
    default:command_cursor_0070[2]=0;break;
    }
    if(command_cursor_0070[2])command_cursor_0070=write_command_fd4e(command_cursor_0070);
   }else if(command_key_fd6a(scan)&&!board_action_active_0056)refresh_panel_1d51();
 }else input_control_1c77(scan);
}

void input_control_1c77(char scan)
{
 *(long *)command_cursor_0070=6L;
 switch(scan) {
 case 0x21:scan='f';break;
 case 0x14:scan='t';break;
 case 0x13:scan='r';break;
 case 0x32:scan='m';break;
 case 0x1f:scan='s';break;
 case 0x24:special_command_1fc2();return;
 }
 command_cursor_0070[2]=scan+128;
 command_cursor_0070=write_command_fd4e(command_cursor_0070);
}

