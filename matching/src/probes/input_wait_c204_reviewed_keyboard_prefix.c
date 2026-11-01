typedef unsigned char Byte;
typedef struct {char *label;int command;Byte enabled,reserved;} MenuItem;
typedef struct {char *label;MenuItem *items;} Menu;
/* Native command copies use a complete 20-byte record. */
typedef struct {int kind,code,status,reserved,x,y,data[4];} Event;
extern unsigned char modal_0054,text_input_active,board_action_active_0056,highlight_flash_0057;
extern int pending_input_988e,board_ready_0ef2,cursor_kind_0ef4,help_ready_0ef0;
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
 if(pending_input_988e)input_wait_1da9(scan);
 else if(highlight_flash_0057)input_dialog_260c(scan);
 else if(modal_0054)write_key_command_1cfa(ascii);
 else if(!(flags&8)) {
  ascii=ascii>='a'&&ascii<='z'?ascii-32:ascii;
  if(text_input_active) {
   *(long *)command_cursor_0070=6L;
   if(command_cursor_0070[2]=ascii)command_cursor_0070=write_command_fd4e(command_cursor_0070);
   return;
  }
  if(board_ready_0ef2&&!board_action_active_0056&&cursor_kind_0ef4&&(scan==0x53||scan==0x0e)) {
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
   }else if(scan==0x3b&&help_ready_0ef0) {
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

