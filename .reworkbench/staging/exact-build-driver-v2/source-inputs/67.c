typedef struct {
 char load[5];
 char separator[10];
 char done[5];
 char cancel[7];
 char filename[10];
 char active_cancel[7];
 char active_done[5];
 char inactive_cancel[7];
 char inactive_done[5];
} DialogStrings;
extern DialogStrings dialog_strings;
typedef unsigned char Byte;
typedef struct {Byte colour,attribute;char *text;} Text;
extern Text dialog_text;
extern int dialog_button_state_2b2c,background,menu_state,foreground;
extern void select_pen_5b18(int),move_pen_5b3d(int,int);
extern void offset_dialog_rect_d528(int,int,int,int);
extern void draw_dialog_text_d551(char *,int);
extern void rect_2079(int,int,int,int);
extern void far graphics_begin(void);
extern void far graphics_end(void);
void paint_dialog_button_d9c6(int button,int active)
{
 if(active) {
  if(button!=dialog_button_state_2b2c) {
   select_pen_5b18(background);
   dialog_text.colour=menu_state;dialog_text.attribute=background;
   graphics_begin();
   if(button==8) {
    offset_dialog_rect_d528(145,74,198,86);
    move_pen_5b3d(204,138);draw_dialog_text_d551(dialog_strings.active_cancel,6);
   } else {
    offset_dialog_rect_d528(145,54,198,66);
    move_pen_5b3d(211,118);draw_dialog_text_d551(dialog_strings.active_done,4);
   }
   dialog_button_state_2b2c=button;
   graphics_end();
   dialog_text.colour=background;dialog_text.attribute=menu_state;
  }
 } else {
  if(dialog_button_state_2b2c!=-1) {
   select_pen_5b18(menu_state);graphics_begin();
   if(button==8) {
    offset_dialog_rect_d528(145,74,198,86);
    move_pen_5b3d(204,138);draw_dialog_text_d551(dialog_strings.inactive_cancel,6);
    select_pen_5b18(foreground);rect_2079(200,129,253,141);
   } else {
    offset_dialog_rect_d528(145,54,198,66);
    move_pen_5b3d(211,118);draw_dialog_text_d551(dialog_strings.inactive_done,4);
    select_pen_5b18(foreground);rect_2079(200,109,253,121);
   }
   graphics_end();dialog_button_state_2b2c=-1;
  }
 }
}

int next_dialog_row_db3d(char rows[8][16],int row)
{
 do {
  ++row;
  if(row>=8)row=0;
 }while(rows[row][15]==-1);
 return row;
}
int previous_dialog_row_db65(char rows[8][16],int row)
{
 do {
  --row;
  if(row<0)row=7;
 }while(rows[row][15]==-1);
 return row;
}
