typedef unsigned char Byte;
typedef struct {Byte colour,attribute;char *text;} Text;
extern Text menu_text;
extern int foreground;
extern int menu_state;
extern Byte huge splash_buffer[];
extern void fill_region_1780(int,int,int,int,int),draw_text_e915(Text *,int,int);
extern int poll_event(Byte *,Byte *,Byte *);
extern void reset_graphics_3e4f(void);
void show_splash(void)
{
 char huge *a;
 char *b;
 int c;
 register int d,e;
 int f;
 char g[40];
 int h;
 menu_text.colour=foreground;
 menu_text.attribute=menu_state;
 menu_text.text=g;
 fill_region_1780(0,0,319,199,menu_state);
 a=(char huge *)splash_buffer;
 while(*a) {
  d=*a++<<3;e=*a++<<3;
  b=g;while(*b++=*a++);
  draw_text_e915(&menu_text,d,e);
 }
 while(!poll_event((Byte *)&h,(Byte *)&f,(Byte *)&c));
 fill_region_1780(0,0,319,199,menu_state);
 a++;
 while(*a) {
  d=*a++<<3;e=*a++<<3;
  b=g;while(*b++=*a++);
  draw_text_e915(&menu_text,d,e);
 }
 while(!poll_event((Byte *)&h,(Byte *)&f,(Byte *)&c));
 reset_graphics_3e4f();
}
