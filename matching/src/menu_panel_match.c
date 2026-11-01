/* 466B: complete1545-byte menu-panel reconstruction, MSC5 /AS /Zi. */
typedef unsigned char Byte;
typedef struct {Byte width,height;signed char x,y;char huge *pixels;} Frame;
typedef struct Actor {
 int x,y,old_x,old_y,flag;
 Byte colour,square;
 int left,right,top,bottom;
 Frame *frame;void far *resource;struct Actor *next;
} Actor;
typedef struct {char *label;int word;Byte enabled,reserved;} MenuItem;
typedef struct {int word;MenuItem *items;} Menu;
typedef struct {Byte colour,attribute;char *text;} Text;
extern Menu *menus;
extern Frame frames[];
extern Actor actors[];
extern int menu_positions[],menu_x,menu_y,menu_columns,menu_rows,menu_state,speed_2eb3;
extern Text menu_text;
extern void far graphics_begin(void);
extern void far graphics_end(void);
extern void configure_actor_45a2(int,int,int,int),attach_actor(int,int,int,Frame *,Actor *);
extern void clear_actor_3e81(Actor *),advance_menu_5381(void),draw_menu_row_527e(int,int),draw_text_e915(Text *,int,int);
void build_menu_466b(register int which)
{
 /* a: register loop index; b: label cursor; c: frame; e/g: menu entries;
  * f: actor cursor; k: length/row index; d/h/i/j: unread original words. */
 register int a;
 char *b;
 Frame *c;
 int d;
 MenuItem *e;
 Actor *f;
 MenuItem *g;
 int h,i,j,k;
 graphics_begin();
 menu_text.attribute=9;
 menu_y=25;
 g=e=menus[which].items;
 menu_x=menu_positions[which]-32;
 menu_columns=0;
 while(b=(g++)->label) {
  k=0;
  while(*b++)k++;
  if(k>menu_columns)menu_columns=k;
 }
 menu_columns=(menu_columns>>1)-1;
 if((menu_columns<<4)+menu_x>224)menu_x=224-(menu_columns<<4);
 configure_actor_45a2(menu_x,menu_y,15,32);
 configure_actor_45a2(menu_x,menu_y,16,33);
 for(a=0;a<menu_columns;a++)configure_actor_45a2((a<<4)+menu_x+48,menu_y,4,a+34);
 if(speed_2eb3<=3000) {
  configure_actor_45a2(menu_x+32,menu_y+23,8,44);
  configure_actor_45a2((menu_columns<<4)+menu_x+48,menu_y+23,10,45);
  configure_actor_45a2(menu_x+16,menu_y+23,7,57);
  for(a=0;a<menu_columns;a++)configure_actor_45a2((a<<4)+menu_x+48,menu_y+23,9,a+46);
  configure_actor_45a2(menu_x+16,menu_y+23,5,56);
  for(a=0;a<menu_columns;a++)configure_actor_45a2((a<<4)+menu_x+48,menu_y+23,6,a+58);
 }
 configure_actor_45a2(menu_x,menu_y,0,68);
 configure_actor_45a2((menu_columns<<4)+menu_x+32,menu_y,2,69);
 attach_actor(menu_x,menu_y+200,0,&frames[0],&actors[68]);
 attach_actor((menu_columns<<4)+menu_x+32,menu_y+200,0,&frames[2],&actors[69]);
 attach_actor((menu_columns<<4)+menu_x+32,menu_y+200,0,&frames[16],&actors[33]);
 if(speed_2eb3<=3000) {
  attach_actor((menu_columns<<4)+menu_x+48,menu_y+223,0,&frames[7],&actors[57]);
  configure_actor_45a2(menu_x+16,menu_y+23,7,57);
 }
 g=e;
 menu_rows=0;k=0;
 while(b=g->label) {
  advance_menu_5381();
  menu_y+=8;menu_rows++;
  if(speed_2eb3>3000) {
   configure_actor_45a2((menu_columns<<4)+menu_x+48,menu_y+15,10,45);
   configure_actor_45a2(menu_x+32,menu_y+15,8,44);
   attach_actor(menu_x+32,menu_y+215,0,&frames[8],&actors[44]);
   attach_actor((menu_columns<<4)+menu_x+48,menu_y+215,0,&frames[10],&actors[45]);
   draw_menu_row_527e(k++,0);
  }else {
   configure_actor_45a2(menu_x+16,menu_y+23,5,56);
   for(a=0;a<menu_columns;a++) {
    c=&frames[6];f=&actors[a+58];
    f->y=menu_y+23;
    f->top=menu_y-c->y+23;
    f->bottom=menu_y-c->y+c->height+22;
   }
   attach_actor((menu_columns<<4)+menu_x+48,menu_y+223,0,&frames[7],&actors[57]);
   menu_text.text=b;
   if(menu_state)menu_text.colour=g->enabled?14:8;
   else menu_text.colour=g->enabled?15:0;
   draw_text_e915(&menu_text,menu_x+36,menu_y+15);
   for(a=0;a<menu_columns;a++) {
    c=&frames[9];f=&actors[a+46];
    f->y=menu_y+23;
    f->top=menu_y-c->y+23;
    f->bottom=menu_y-c->y+c->height+22;
   }
   configure_actor_45a2((menu_columns<<4)+menu_x+48,menu_y+23,10,45);
   configure_actor_45a2(menu_x+32,menu_y+23,8,44);
   configure_actor_45a2(menu_x+16,menu_y+23,7,57);
  }
  g++;
 }
 if(speed_2eb3>3000) {
  configure_actor_45a2(menu_x+16,menu_y+23,5,56);
  configure_actor_45a2(menu_x+16,menu_y+23,7,57);
  for(a=0;a<menu_columns;a++)configure_actor_45a2((a<<4)+menu_x+48,menu_y+23,6,a+58);
  attach_actor((menu_columns<<4)+menu_x+48,menu_y+223,0,&frames[7],&actors[57]);
 }
 f=&actors[44];
 for(a=0;a<menu_columns+2;a++) {
  clear_actor_3e81(f);
  (f++)->frame=0;
 }
 graphics_end();
}
