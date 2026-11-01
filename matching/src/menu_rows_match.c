/* Complete menu row and animation routines reconstructed from original code. */
typedef unsigned char Byte;
typedef struct {Byte width,height;signed char x,y;char huge *pixels;} Frame;
typedef struct Actor {int x,y,old_x,old_y,flag;Byte colour,square;int left,right,top,bottom;Frame *frame;void far *resource;struct Actor *next;} Actor;
typedef struct {char *label;int command;Byte enabled,reserved;} MenuItem;
typedef struct {char *label;MenuItem *items;} Menu;
typedef struct {Byte colour,attribute;char *text;} Text;
extern Menu *menus;
extern Text menu_text;
extern int menu_columns,menu_x,menu_state,selected_menu,menu_phase;
extern Byte menu_blink;
extern Frame frames[];
extern Actor actors[];
extern void far *frame_resources[];
extern void draw_text_e915(Text *,int,int),attach_actor(int,int,int,Frame *,Actor *);
void draw_menu_row_527e(register int row,register int selected)
{
 char *a,*b,*c;
 char line[20];
 c=line+(menu_columns<<1)+3;
 a=line;
 b=menus[selected_menu].items[row].label;
 while(*b)*a++=*b++;
 while(a!=c)*a++=' ';
 *a=0;
 menu_text.text=line;
 if(menus[selected_menu].items[row].enabled) {
  if(!menu_state) {
   menu_text.attribute=selected?0:9;
   menu_text.colour=15;
  }else {
   menu_text.attribute=selected?1:9;
   menu_text.colour=14;
  }
 }else {
  menu_text.attribute=9;
  if(!menu_state)menu_text.colour=0;
  else menu_text.colour=8;
 }
 draw_text_e915(&menu_text,menu_x+36,(row<<3)+48);
}
void advance_menu_5381(void)
{
 Actor *a;
 if(selected_menu!=255) {
  a=&actors[68];
  menu_phase=!menu_phase;
  a->resource=frame_resources[menu_phase];
  attach_actor(a->x,a->y+200,a->colour,&frames[menu_phase],a);
  a++;
  a->resource=frame_resources[menu_phase+2];
  attach_actor(a->x,a->y+200,a->colour,&frames[menu_phase+2],a);
  if(menu_blink++)menu_blink=0;
 }
}
