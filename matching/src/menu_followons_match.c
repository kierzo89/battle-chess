/* Complete menu follow-ons, original image4C74..527D. */
typedef unsigned char Byte;
typedef struct {Byte width,height;signed char x,y;char huge *pixels;} Frame;
typedef struct Actor {int x,y,old_x,old_y,flag;Byte colour,square;int left,right,top,bottom;Frame *frame;void far *resource;struct Actor *next;} Actor;
typedef struct {char *label;int command;Byte enabled,reserved;} MenuItem;
typedef struct {char *label;MenuItem *items;} Menu;
typedef struct {Byte colour,attribute;char *text;} Text;
extern Menu *menus;
extern Frame frames[];
extern Actor actors[];
extern void far *frame_resources[];
extern int menu_positions[],menu_x,menu_y,menu_columns,menu_rows,menu_state,speed_2eb3;
extern int menu_selected,menu_row_selected,menu_last;
extern Byte palette_mode;
extern Text menu_title_text;
extern void far graphics_begin(void);
extern void far graphics_end(void);
extern void configure_actor_45a2(int,int,int,int),attach_actor(int,int,int,Frame *,Actor *);
extern void clear_actor_3e81(Actor *),detach_actor(Actor *),advance_menu_5381(void),draw_menu_row_527e(int,int),draw_text_e915(Text *,int,int);
extern void restore_region_58b0(int,int,int,int),build_menu_466b(int);
void title_menu_50af(int,int);
void close_menu_4c74(void)
{
 register int a,b;Actor *c;int d,e,f,g;
 graphics_begin();a=32;
 if(speed_2eb3<=3000) {
  while(menu_y>25) {
   advance_menu_5381();menu_y-=8;
   configure_actor_45a2(menu_x+16,menu_y+23,5,56);
   for(b=0;b<menu_columns;b++)configure_actor_45a2((b<<4)+menu_x+48,menu_y+23,6,b+58);
   attach_actor((menu_columns<<4)+menu_x+48,menu_y+223,0,&frames[7],&actors[57]);
   configure_actor_45a2(menu_x+16,menu_y+23,7,57);
  }
  configure_actor_45a2(menu_x,menu_y,16,33);
 }
 c=&actors[56];
 for(b=0;b<menu_columns+2;b++){clear_actor_3e81(c);(c++)->frame=0;}
 c=&actors[32];
 for(b=0;b<menu_columns+2;b++){clear_actor_3e81(c);(c++)->frame=0;}
 detach_actor(&actors[68]);detach_actor(&actors[69]);
 if(speed_2eb3>3000)restore_region_58b0(actors[68].left>>2,actors[69].right>>2,actors[69].bottom,actors[57].bottom);
 else {
  actors[33].frame=&frames[16];actors[57].frame=&frames[7];
  attach_actor((menu_columns<<4)+menu_x+32,menu_y+200,0,&frames[16],&actors[33]);
  attach_actor((menu_columns<<4)+menu_x+48,menu_y+223,0,&frames[7],&actors[57]);
  detach_actor(&actors[33]);detach_actor(&actors[57]);
 }
 menu_row_selected=255;graphics_end();
}
void initialize_menu_bar_4e5d(void)
{
 char *a;register Menu *b;Actor *c;register int d;int e,f,g,h;
 graphics_begin();b=menus;d=f=0;h=32;c=&actors[h];
 c->square=255;c->resource=frame_resources[11];c->frame=0;
 attach_actor(d,200,0,&frames[11],c);clear_actor_3e81(c);c->frame=0;(c++)->square=0;d+=48;
 while(a=(b++)->label) {
  e=0;while(*a++)e++;e=(e+1)>>1;menu_positions[f++]=d;
  for(g=0;g<e;g++) {
   c->square=255;c->resource=frame_resources[13];
   attach_actor(d,200,0,&frames[13],c);clear_actor_3e81(c);c->frame=0;(c++)->square=0;d+=16;
  }
  title_menu_50af(f-1,0);
  if(b->label) {
   c->square=255;c->resource=frame_resources[12];
   attach_actor(d,200,0,&frames[12],c);clear_actor_3e81(c);c->frame=0;(c++)->square=0;d+=16;
  }else {
   menu_positions[f++]=d;c->square=255;c->resource=frame_resources[14];
   attach_actor(d,200,0,&frames[14],c);clear_actor_3e81(c);c->frame=0;(c++)->square=0;d+=24;
  }
 }
 menu_last=f-1;graphics_end();
}
int finish_menu_5035(void)
{
 register MenuItem *a;int b,c,d,e,f,g;
 graphics_begin();f=0;
 if(menu_selected!=255) {
  if(menu_row_selected!=255) {
   a=&menus[menu_selected].items[menu_row_selected];
   if(a->enabled)f=a->command;
  }
  close_menu_4c74();
 }
 menu_selected=255;restore_region_58b0(0,79,0,23);graphics_end();return f;
}
void title_menu_50af(register int menu,register int active)
{
 graphics_begin();menu_title_text.text=menus[menu].label;
 if(menu_state)menu_title_text.colour=active?9:0;
 else if(palette_mode==3)menu_title_text.colour=active?15:0;
 else menu_title_text.colour=active?12:0;
 draw_text_e915(&menu_title_text,menu_positions[menu],8);graphics_end();
}
void track_menu_512d(register int x,int y)
{
 int a;register int b;int c;
 graphics_begin();
 if(y<16) {
  for(a=0;a<5&&menu_positions[a]<x;a++);
  if(a>0&&a<=menu_last) {
   a--;
   if(a!=menu_selected) {
    if(menu_selected!=255){close_menu_4c74();title_menu_50af(menu_selected,0);menu_selected=255;}
    title_menu_50af(a,1);menu_selected=a;build_menu_466b(a);
   }
  }
 }
 if(menu_selected!=255) {
  if(x>=menu_x+36&&x<(menu_columns<<4)+menu_x+52&&y>=48) {
   b=48;a=0;c=menu_y+31;while(b<c&&b<=y){b+=8;a++;}
   if(b<c) {
    a--;
    if(a!=menu_row_selected) {
     if(menu_row_selected!=255)draw_menu_row_527e(menu_row_selected,0);
     draw_menu_row_527e(a,1);menu_row_selected=a;
    }
   }else if(menu_row_selected!=255){draw_menu_row_527e(menu_row_selected,0);menu_row_selected=255;}
  }else if(menu_row_selected!=255){draw_menu_row_527e(menu_row_selected,0);menu_row_selected=255;}
 }
 graphics_end();
}
