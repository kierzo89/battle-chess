typedef unsigned char Byte;
typedef struct {Byte colour,attribute;char *text;} Text;
extern Text dialog_text;
extern int pen_x,pen_y;
extern void draw_text_e915(Text *,int,int);
extern void far graphics_rect_110d_0003(int,int,int,int);
extern void make_save_name_d65a(char *),set_flag_11b8(void),select_asset_file(int);
extern int open(char *,int,...),close(int),read(int,void *,unsigned),write(int,const void *,unsigned);
extern char *strcpy(char *,const char *);
extern char save_game_filename[];
void offset_dialog_rect_d528(int x1,int y1,int x2,int y2)
{
 graphics_rect_110d_0003(x1+55,y1+55,x2+55,y2+55);
}
extern void fill_8a96(char *,int,int);
void draw_dialog_text_d551(char *text,int limit)
{
 char a;
 if(limit) {a=text[limit];text[limit]=0;}
 dialog_text.text=text;
 draw_text_e915(&dialog_text,pen_x,pen_y-6);
 if(limit)text[limit]=a;
}

int read_saved_games(Byte *buffer)
{
 char a[32];
 int b;
 make_save_name_d65a(a);set_flag_11b8();select_asset_file(1);
 if((b=open(a,0))==-1) {fill_8a96((char *)buffer,512,0);return 0;}
 read(b,buffer,512);close(b);return 1;
}
int write_saved_games_d601(Byte *buffer)
{
 char a[32];
 int b;
 make_save_name_d65a(a);set_flag_11b8();select_asset_file(1);
 if((b=open(a,0x101,0x180))==-1)return 0;
 write(b,buffer,512);close(b);return 1;
}
void make_save_name_d65a(char *buffer)
{
 strcpy(buffer,save_game_filename);
}
extern int dialog_selected,menu_state,border;
extern void fill_8a96(char *,int,int),move_pen_5b3d(int,int);
extern void draw_dialog_text_d551(char *,int);
void highlight_game_d66c(int selected,Byte rows[8][16])
{
 char *a,*b;
 char c[16];
 if(selected!=dialog_selected) {
  if(dialog_selected!=-1) {
   fill_8a96(c,15,32);
   a=(char *)rows[dialog_selected];b=c;
   while(*a)*b++=*a++;
   dialog_text.attribute=menu_state;
   move_pen_5b3d(64,dialog_selected*10+68);
   draw_dialog_text_d551(c,15);
  }
  fill_8a96(c,15,32);
  a=(char *)rows[selected];b=c;
  while(*a)*b++=*a++;
  dialog_text.attribute=border;
  move_pen_5b3d(64,selected*10+68);
  draw_dialog_text_d551(c,15);
  dialog_text.attribute=menu_state;
  dialog_selected=selected;
 }
}
