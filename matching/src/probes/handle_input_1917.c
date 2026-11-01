/* Native command copies use a complete 20-byte record. */
typedef struct {long kind;int status,reserved,x,y,data[4];} InputEvent;
extern unsigned char modal_0054,key_mode_0055,command_mode_0056,input_mode_0057;
extern int pending_input_988e,board_ready_0ef2,player_ready_0ef4,help_ready_0ef0;
extern int input_action_0efa,pointer_x_933a,pointer_y_935e;
extern int cursor_column_0086,cursor_row_0088,position_hint_0484,side_053c,side_053e;
extern int *command_cursor_0070,*position_8dda;
extern InputEvent event_tick_0072;
extern int *far write_command_fd4e(int *);
extern int far command_key_fd6a(int);
extern void input_wait_1da9(int),input_dialog_260c(int),write_key_command_1cfa(int);
extern void input_control_1c77(int),refresh_panel_1d51(void),reset_command_0886(void);
extern void type_chat_14c1(int),position_command_22c5(int,int);
extern int choose_action_2008(int,int,int);
int handle_input_1917(char flags,char ascii,char scan)
{
 flags&=0x2f;
 if(flags&4)return 0;
 if(pending_input_988e)input_wait_1da9(scan);
 else if(input_mode_0057)input_dialog_260c(scan);
 else if(modal_0054)write_key_command_1cfa(ascii);
 else if(!(flags&8)) {
  ascii=ascii>='a'&&ascii<='z'?ascii-32:ascii;
  if(key_mode_0055) {
   *(long *)command_cursor_0070=6L;
   if(command_cursor_0070[2]=ascii)command_cursor_0070=write_command_fd4e(command_cursor_0070);
   return;
  }
  if(board_ready_0ef2&&!command_mode_0056&&player_ready_0ef4&&(scan==0x53||scan==0x0e)) {
   input_action_0efa=255;
   *(long *)command_cursor_0070=4L;command_cursor_0070[2]=1;
   command_cursor_0070=write_command_fd4e(command_cursor_0070);
   return;
  }
  if((ascii>='A'&&ascii<='H')||(ascii>='1'&&ascii<='8')) {
    if(ascii>='A'&&ascii<='H')cursor_column_0086=ascii-'A';
    else cursor_row_0088=-(ascii-'8');
    refresh_panel_1d51();
   }else if(ascii==13||ascii==' ') {
    command_cursor_0070[4]=pointer_x_933a;command_cursor_0070[5]=pointer_y_935e;
    *(long *)command_cursor_0070=4L;command_cursor_0070[2]=1;
    command_cursor_0070=write_command_fd4e(command_cursor_0070);
   }else if(scan==0x3b&&help_ready_0ef0) {
    *(long *)command_cursor_0070=4L;command_cursor_0070[2]=3;
    command_cursor_0070=write_command_fd4e(command_cursor_0070);
    *(InputEvent *)command_cursor_0070=event_tick_0072;
    command_cursor_0070=write_command_fd4e(command_cursor_0070);
    position_command_22c5(49,8);
    *(InputEvent *)command_cursor_0070=event_tick_0072;
    command_cursor_0070=write_command_fd4e(command_cursor_0070);
    position_hint_0484=100;
    position_command_22c5(85,49+8*choose_action_2008(0,1,position_8dda[1]));
    *(InputEvent *)command_cursor_0070=event_tick_0072;
    command_cursor_0070=write_command_fd4e(command_cursor_0070);
   }else if(scan==0x3c) {
    if(side_053c==2||side_053e==2){reset_command_0886();type_chat_14c1(0);}
   }else if(scan==0x3d||scan==0x3e) {
    *(long *)command_cursor_0070=scan;
    command_cursor_0070=write_command_fd4e(command_cursor_0070);
   }else if(command_mode_0056) {
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
   }else if(command_key_fd6a(scan)&&!command_mode_0056)refresh_panel_1d51();
 }else input_control_1c77(scan);
}
