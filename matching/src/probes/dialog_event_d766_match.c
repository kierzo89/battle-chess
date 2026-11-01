typedef unsigned char Byte;
typedef struct {int kind,status,code,reserved,x,y,word6,word7,word8,word9;} DialogEvent;
extern Byte mode_005a;
extern int *command_head_006e,*command_cursor_0070;
extern DialogEvent dialog_event;
extern unsigned long current_ticks_9884,last_event_ticks_b07a;
extern void pump_input_2301(void);
extern int * far write_command_fd4e(int *);
extern int poll_event(Byte *,Byte *,Byte *);
extern long ticks_ea5b(void);
DialogEvent *next_dialog_event_d766(void)
{
 Byte a,b,c;
 if(mode_005a) {
  while(command_head_006e==command_cursor_0070)pump_input_2301();
  dialog_event=*(DialogEvent *)command_head_006e;
  command_head_006e=write_command_fd4e(command_head_006e);
  return &dialog_event;
 }
 for(;;) {
  current_ticks_9884=(int)ticks_ea5b();
  if(current_ticks_9884-last_event_ticks_b07a>=2) {
   dialog_event.kind=3;dialog_event.status=0;
   last_event_ticks_b07a=current_ticks_9884;
   return &dialog_event;
  }
  if(poll_event(&c,&b,&a)) {
   dialog_event.kind=7;dialog_event.status=0;
   switch(a) {
    case 72:dialog_event.code=128;return &dialog_event;
    case 80:dialog_event.code=129;return &dialog_event;
   }
   if(b) {
    dialog_event.kind=6;dialog_event.status=0;dialog_event.code=b;
    return &dialog_event;
   }
  }
 }
}
