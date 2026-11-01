/* Scan at most the actual menu-item count, wrapping in the requested direction. */
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
