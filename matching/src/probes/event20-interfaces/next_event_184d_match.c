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
