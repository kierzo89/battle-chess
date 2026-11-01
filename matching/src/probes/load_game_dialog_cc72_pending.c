typedef unsigned char Byte;
typedef struct {int kind,status,code,reserved,x,y;} DialogEvent;
typedef struct {Byte colour,attribute;char *text;} Text;
extern Text dialog_text;
extern int background,menu_state,pointer_x,pointer_y,command_active;
extern char no_saved_games[],saved_games_title[];
extern int read_saved_games(Byte *),prompt_1296(char *,int,int);
extern void select_wait_mode_17f9(int),initialize_dialog_d2cc(void);
extern void make_game_rows_d2dd(Byte *,Byte (*)[16]);
extern void title_game_rows_d365(Byte (*)[16],char *);
extern void highlight_game_d66c(int,Byte (*)[16]);
extern DialogEvent *next_dialog_event_d766(void);
extern int previous_game_db65(Byte (*)[16],int),next_game_db3d(Byte (*)[16],int);
extern int dialog_hit_d840(int,int,int),dialog_button_d92e(int,int);
extern void close_dialog_d90e(void),dispatch_8d73(Byte *),flush_df71(void);
extern void restore_ui_92ab(Byte *,Byte),init_surface(void),reset_graphics_3e4f(void),setup_assets_0865(void);
extern long ticks_ea5b(void);
extern void far graphics_begin(void);
extern void far graphics_end(void);
extern void far update_pointer_11ef_0030(void);
void load_game_dialog_cc72(void)
{
 Byte *a;
 Byte b[8][16];
 unsigned long c;
 DialogEvent *d;
 int e,f;
 unsigned long g;
 Byte h[512];
 int i;
 f=0;i=-1;g=0;
 dialog_text.colour=background;dialog_text.attribute=menu_state;
 if(!read_saved_games(h))prompt_1296(no_saved_games,12,0);
 else {
  a=h;
  select_wait_mode_17f9(1);graphics_begin();initialize_dialog_d2cc();
  make_game_rows_d2dd(a,b);title_game_rows_d365(b,saved_games_title);
  highlight_game_d66c(f,b);graphics_end();
  for(;;) {
   d=next_dialog_event_d766();
   if(d->kind==7 && d->status==0) {
    switch(d->code) {
     case 129:f=next_game_db3d(b,f);break;
     case 128:f=previous_game_db65(b,f);break;
     default:continue;
    }
    highlight_game_d66c(f,b);
   } else if(d->kind==6 && d->status==0) {
    switch(d->code) {
     case 13:case 32:
choose_game:
   graphics_begin();close_dialog_d90e();
   f=b[f][15];dispatch_8d73(a+f*48+31);flush_df71();
   e=command_active;restore_ui_92ab(a,f);
   if(e!=command_active) {init_surface();reset_graphics_3e4f();setup_assets_0865();}
   goto finished;
     case 27:goto cancel;
     default:continue;
    }
   } else
   switch(d->kind) {
    case 4:
     if(d->code==1) {
      c=(int)ticks_ea5b();
      e=dialog_hit_d840(pointer_x,pointer_y,0);
      if(e<=7) {if(b[e][15]!=255) {f=e;highlight_game_d66c(f,b);}}
      else if(e==8 && dialog_button_d92e(e,0))goto cancel;
      if(e==f) {
       if(c-g<10 && i==f)goto choose_game;
       g=c;i=f;
      }
     }
     break;
    case 5:
     pointer_x=d->x;pointer_y=d->y;update_pointer_11ef_0030();break;
   }
   continue;
  }
cancel:
  graphics_begin();close_dialog_d90e();
finished:
  graphics_end();
 }
}
