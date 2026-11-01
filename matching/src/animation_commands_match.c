/* Animation command queue. BB0E's omitted trailing caller arguments remain
 * unresolved; these definitions expose every field actually read here. */
typedef unsigned char Byte;
typedef struct {
 Byte operation,state,child,next,square,argument,extra,reserved;
} Command;
extern Command commands[32];
extern Byte command_cursor,command_root,cells[],piece_flags[],capture_first,capture_second;
extern int command_active;
extern void start_3713(void),run_command_6167(Byte);
void advance_60bb(void);
int append_command_5fbd(Byte parent,Byte operation,Byte square,Byte argument,Byte extra)
{
 register Command *record;
 Byte next;
 if(operation==5) {
  if(argument)capture_second=cells[square]&7;
  else capture_first=cells[square]&7;
 }else if(operation!=8)piece_flags[cells[square]&7]=1;
 command_cursor=(command_cursor+1)&31;
 next=commands[parent].child;
 if(next==255)commands[parent].child=command_cursor;
 else {
  while(next!=255) {
   parent=next;
   next=commands[parent].next;
  }
  commands[parent].next=command_cursor;
 }
 record=&commands[command_cursor];
 record->operation=operation;
 record->square=square;
 record->argument=argument;
 record->extra=extra;
 record->state=2;
 record->child=255;
 record->next=255;
 if(operation==3&&square!=argument) {
  if(!command_active)start_3713();
  advance_60bb();
 }
 return command_cursor;
}
void advance_60bb(void)
{
 run_command_6167(command_root);
}
int begin_command_60d3(Byte operation,Byte square,Byte argument,Byte extra)
{
 register Command *record;
 command_cursor=(command_cursor+1)&31;
 record=&commands[command_cursor];
 record->operation=operation;
 record->square=square;
 record->argument=argument;
 record->extra=extra;
 record->child=255;
 record->next=255;
 command_root=command_cursor;
 if(operation==5) {
  if(argument)capture_second=cells[square]&7;
  else capture_first=cells[square]&7;
 }else if(operation!=8)piece_flags[cells[square]&7]=1;
 return command_root;
}
