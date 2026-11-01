/* Native CED4: edit a saved position name, pack the current board and write it. */
typedef unsigned char Byte;
typedef struct {Byte colour,attribute;char *text;} Text;
typedef struct {int kind,status,code,reserved,x,y,word6,word7,word8,word9;} DialogEvent;
extern Text dialog_text;
extern int background,menu_state,pointer_x,pointer_y,saved_name_count_52d4;
typedef struct {char load[5];char save[5];} DialogActions;
extern DialogActions dialog_actions_516c;
extern int read_saved_games(Byte *),write_saved_games_d601(Byte *);
extern void select_mode(int),prepare_dialog_d2cc(void),collect_saved_names_d2dd(char *,char (*)[16]),draw_saved_game_rows_d365(char (*)[16],char *);
extern int prepare_game_name_d8b6(char *,const char *),is_dialog_printable_d8f6(int),dialog_hit_d840(int,int,int),dialog_button_d92e(int,int);
extern DialogEvent *next_dialog_event_d766(void);
extern void draw_dialog_text_d551(char *,int),move_pen_5b3d(int,int),close_dialog_d90e(void),pack_board_8cfa(Byte *),save_ui_931c(Byte *,Byte);
extern char *strcpy(char *,const char *);
extern long ticks_ea5b(void);
extern void far graphics_begin(void);
extern void far graphics_end(void);
extern void far update_pointer_11ef_0030(void);
void save_dialog_ced4(void)
{
 Byte *a;
 unsigned b;
 int c;
 char d[8][16];
 unsigned long e;
 DialogEvent *f;
 char g[15];
 int h,i,j;
 unsigned long k;
 int l;
 Byte m[512];
 i=0;l=1;j=-1;k=0;
 dialog_text.colour=background;dialog_text.attribute=menu_state;
 read_saved_games(m);a=m;
 select_mode(1);graphics_begin();prepare_dialog_d2cc();
 collect_saved_names_d2dd((char *)a,d);draw_saved_game_rows_d365(d,dialog_actions_516c.save);
 c=prepare_game_name_d8b6(g,d[i]);graphics_end();
 for(;;) {
  f=next_dialog_event_d766();
  if(i!=-1)move_pen_5b3d(64,i*10+68);
  switch(f->kind) {
   case 7:
    switch((unsigned)f->code) {case 128:case 129:
     prepare_game_name_d8b6(g,d[i]);draw_dialog_text_d551(g,14);
     if(f->code==128)i--;else i++;
     i=i>7?0:i;i=i<0?7:i;
     c=prepare_game_name_d8b6(g,d[i]);l=1;
    }
    break;
   case 6:
    switch(f->code) {case 27:goto cancel;}
    if(i!=-1) {
     if(f->code==8) {g[c--]=' ';c=c<0?0:c;}
     else if(f->code==13) {
      if(c) {
accept_name:
       g[c]=0;strcpy(d[i],g);
save_position:
       if(c) {
        j=(Byte)d[i][15];if(j==255)j=saved_name_count_52d4;
        strcpy((char *)a+j*48+16,d[i]);pack_board_8cfa(a+j*48+31);
        save_ui_931c(a,j);close_dialog_d90e();write_saved_games_d601(a);return;
       }
       break;
      }
     } else if(is_dialog_printable_d8f6(f->code)) {g[c++]=f->code;if(c>14)c=14;}
     draw_dialog_text_d551(g,14);
    }
    break;
   case 3:
    if(i!=-1 && l && (b&4)) {
     if(g[c]=='_')g[c]=' ';else g[c]='_';
     draw_dialog_text_d551(g,14);
    }
    b++;break;
   case 4:
    if(f->code==1) {
     e=(int)ticks_ea5b();h=dialog_hit_d840(pointer_x,pointer_y,1);
     if(h<=7) {
      prepare_game_name_d8b6(g,d[i]);draw_dialog_text_d551(g,14);
      i=h;c=prepare_game_name_d8b6(g,d[i]);l=1;
     }else if(h==8) {if(dialog_button_d92e(h,1))goto cancel;}
     else if(h==9 && c && dialog_button_d92e(h,1))goto accept_name;
     if(e-k<10 && i==j)goto save_position;
     k=e;j=i;
    }
    break;
   case 5:pointer_x=f->x;pointer_y=f->y;update_pointer_11ef_0030();break;
  }
 }
cancel:close_dialog_d90e();
}
