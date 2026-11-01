typedef unsigned char Byte;
typedef struct {Byte colour,attribute;char *text;} Text;
extern Text dialog_text;
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
