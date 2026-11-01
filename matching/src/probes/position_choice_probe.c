typedef unsigned char Byte;
typedef struct {char *label;int command;Byte enabled,reserved;} MenuItem;
extern int menu_rows;
int choose_action_2008(int index,int step,MenuItem *items)
{
 int count;
 if(!step)step=-1;
 for(count=0;count!=menu_rows;count++) {
  if(items[index].enabled)return index;
  index+=step;
  index=index>=menu_rows?0:index;
  index=index<0?menu_rows-1:index;
 }
 return 255;
}
extern int *command_cursor_0070;
extern int *far write_command_fd4e(int *);
void position_command_22c5(int x,int y)
{
 *(long *)command_cursor_0070=5L;
 command_cursor_0070[4]=x;
 command_cursor_0070[5]=y;
 command_cursor_0070=write_command_fd4e(command_cursor_0070);
}
