typedef unsigned char Byte;
typedef struct {int kind,code,status,reserved,x,y,data[4];} Event;
extern int *command_cursor_0070;
extern Event event_tick_0072;
extern Byte flash_rank_b0a3;
extern int *far write_command_fd4e(int *);
extern void refresh_panel_1d51(void),select_pen_5b18(int),position_command_22c5(int,int);
extern void far graphics_rect_110d_0003(int,int,int,int);
void input_dialog_260c(int scan)
{
 int a;
 a=flash_rank_b0a3;
 switch(scan) {
 case 77:a++;break;
 case 75:a--;break;
 case 28:
  *(long *)command_cursor_0070=4L;
  command_cursor_0070[2]=1;
  command_cursor_0070=write_command_fd4e(command_cursor_0070);
  *(Event *)command_cursor_0070=event_tick_0072;
  command_cursor_0070=write_command_fd4e(command_cursor_0070);
  refresh_panel_1d51();
  return;
 }
 a=a<0?3:a;
 a=a>3?0:a;
 if(a!=flash_rank_b0a3) {
  select_pen_5b18(0);
  graphics_rect_110d_0003(flash_rank_b0a3*32+96,121,flash_rank_b0a3*32+128,123);
  position_command_22c5(a*32+97,100);
  flash_rank_b0a3=a;
 }
}
