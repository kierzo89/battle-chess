typedef unsigned char Byte;
typedef struct {char *label;int command;Byte enabled,reserved;} MenuItem;
typedef struct {char *label;MenuItem *items;} Menu;
typedef struct {int kind,code,status,reserved,x,y,data[4];} Event;
extern Menu *menus;
extern int selected_menu,menu_row_selected,menu_rows,menu_last,menu_positions[];
extern int *command_cursor_0070;
extern Event event_tick_0072;
extern int *far write_command_fd4e(int *);
extern void position_command_22c5(int,int),refresh_panel_1d51(void);
extern int choose_action_2008(int,int,MenuItem *);
int input_wait_1da9(char scan)
{
 /* a=menu index; b=row. The confirmation exit leaves AX unspecified. */
 int a,b;
 if(scan==1) {
  position_command_22c5(0,0);
  *(Event *)command_cursor_0070=event_tick_0072;
  command_cursor_0070=write_command_fd4e(command_cursor_0070);
  *(long *)command_cursor_0070=4L;
  command_cursor_0070[2]=2;
  command_cursor_0070=write_command_fd4e(command_cursor_0070);
  *(Event *)command_cursor_0070=event_tick_0072;
  command_cursor_0070=write_command_fd4e(command_cursor_0070);
  refresh_panel_1d51();
  *(Event *)command_cursor_0070=event_tick_0072;
  command_cursor_0070=write_command_fd4e(command_cursor_0070);
 }else if(selected_menu!=255) {
  b=menu_row_selected;a=selected_menu;
  switch(scan) {
  case 72:b--;break;
  case 77:a++;break;
  case 80:b++;break;
  case 75:a--;break;
  case 28:case 57:
   *(long *)command_cursor_0070=4L;
   command_cursor_0070[2]=2;
   command_cursor_0070=write_command_fd4e(command_cursor_0070);
   *(Event *)command_cursor_0070=event_tick_0072;
   command_cursor_0070=write_command_fd4e(command_cursor_0070);
   refresh_panel_1d51();
   goto done;
  }
  b=b>=menu_rows?0:b;
  b=b<0?menu_rows-1:b;
  a=a<0?menu_last-1:a;
  a=a>menu_last-1?0:a;
  if(a==selected_menu) {
   b=choose_action_2008(b,scan==80,menus[a].items);
   if(b!=255)position_command_22c5(menu_positions[a]+37,b*8+49);
  }else {
   position_command_22c5(menu_positions[a]+1,8);
   *(long *)command_cursor_0070=4L;
   command_cursor_0070[2]=3;
   command_cursor_0070=write_command_fd4e(command_cursor_0070);
   *(Event *)command_cursor_0070=event_tick_0072;
   command_cursor_0070=write_command_fd4e(command_cursor_0070);
   position_command_22c5(menu_positions[a]+37,choose_action_2008(0,1,menus[a].items)*8+49);
  }
 }
 return 0;
 done:;
}
