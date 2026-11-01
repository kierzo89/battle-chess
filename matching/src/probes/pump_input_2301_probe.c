typedef unsigned char Byte;
typedef struct {int kind,code,status,reserved,x,y;} Event;
typedef struct {int words[10];} EventImage20;
extern void far input_poll_11ef_00b9(void);
extern int input_x_005c,input_y_005e,pointer_x,pointer_y,buttons_8d04,previous_buttons_9888;
extern int *command_cursor_0070;
extern unsigned long current_ticks_9884,last_event_ticks_b07a;
extern Event event_tick_0072;
extern Byte modal_0054;
extern void position_command_22c5(int,int),input_control_1c77(int);
extern int *far write_command_fd4e(int *);
extern long ticks_ea5b(void);
extern int poll_event(Byte *,Byte *,Byte *);
void pump_input_2301(void)
{
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
 if(current_ticks_9884-last_event_ticks_b07a>=2) {
  *(EventImage20 *)command_cursor_0070=*(EventImage20 *)&event_tick_0072;
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
      *(EventImage20 *)command_cursor_0070=*(EventImage20 *)&event_tick_0072;
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
      command_cursor_0070[2]=(c>='a'&&c<='z')?c-32:c;
      if(command_cursor_0070[2])command_cursor_0070=write_command_fd4e(command_cursor_0070);
     }
    }
   }else input_control_1c77(a);
  }
 }
}
