/* Native event waits and recursive decimal conversion, image5D48 onward. */
/* These are observed near record prefixes; enclosing allocation sizes remain unknown. */
typedef struct {int kind,code,status,reserved,x,y;} Event;
typedef struct {int words[5];int queue;} EventContext;
extern EventContext *event_context;
extern Event *current_event;
/* Legacy callers retain one ignored word; the callee reads no arguments. */
extern Event *next_event_184d();
extern void exit_07f3();
extern int pointer_x,pointer_y;
void wait_exit_event_5d48(void)
{
 int done;
 done=0;
 do {current_event=next_event_184d(event_context->queue);if(current_event->status==1)done=1;}while(!done);
}
void wait_pointer_event_5d7a(void)
{
 int done;
 done=0;
 do {
  current_event=next_event_184d(event_context->queue);
  if(current_event->status==1)exit_07f3();
  if(current_event->kind==5&&current_event->code==0){pointer_x=current_event->x;pointer_y=current_event->y;done=1;}
 }while(!done);
}
char *decimal_digits_5dca(long value,char *destination)
{
 if(value==0)*destination='0';
 else {destination=decimal_digits_5dca(value/10L,destination);*destination++=value%10L+'0';}
 return destination;
}
