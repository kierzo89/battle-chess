/* Genuine adjacent source: dialog_file_flow_match.c */
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

/* Genuine adjacent source: dialog_event_hit_flow_match.c */
typedef struct {int kind,status,code,reserved,x,y,word6,word7,word8,word9;} DialogEvent;
extern Byte mode_005a;
extern int *command_head_006e,*command_cursor_0070;
extern DialogEvent dialog_event;
extern unsigned long current_ticks_9884,last_event_ticks_b07a;
extern void pump_input_2301(void);
extern int * far write_command_fd4e(int *);
extern int poll_event(Byte *,Byte *,Byte *);
extern long ticks_ea5b(void);
DialogEvent *next_dialog_event_d766(void)
{
 Byte a,b,c;
 if(mode_005a) {
  while(command_head_006e==command_cursor_0070)pump_input_2301();
  dialog_event=*(DialogEvent *)command_head_006e;
  command_head_006e=write_command_fd4e(command_head_006e);
  return &dialog_event;
 }
 for(;;) {
  current_ticks_9884=(int)ticks_ea5b();
  if(current_ticks_9884-last_event_ticks_b07a>=2) {
   dialog_event.kind=3;dialog_event.status=0;
   last_event_ticks_b07a=current_ticks_9884;
   return &dialog_event;
  }
  if(poll_event(&c,&b,&a)) {
   dialog_event.kind=7;dialog_event.status=0;
   switch(a) {
    case 72:dialog_event.code=128;return &dialog_event;
    case 80:dialog_event.code=129;return &dialog_event;
   }
   if(b) {
    dialog_event.kind=6;dialog_event.status=0;dialog_event.code=b;
    return &dialog_event;
   }
  }
 }
}

/* Signed screen-coordinate hit test: eight rows, cancel, optional action. */
int dialog_hit_d840(int x,int y,int allow_extra)
{
 if(x>60 && x<187 && y>60 && y<139)return (y-60)/10;
 if(x>200 && x<253 && y>129 && y<141)return 8;
 if(allow_extra && x>200 && x<253 && y>109 && y<121)return 9;
 return 255;
}

/* Genuine adjacent source: dialog_followons_match.c */
extern void fill_8a96(char *,int,int);
extern char *strcpy(char *,const char *);
extern unsigned strlen(const char *);
extern void select_pattern_5b00(int),restore_region_58b0(int,int,int,int);
int prepare_game_name_d8b6(char *destination,const char *source)
{
 int a;
 fill_8a96(destination,15,32);
 strcpy(destination,source);
 a=strlen(destination);
 destination[a]=' ';
 return a;
}
int is_dialog_printable_d8f6(int key)
{
 if(key>=32 && key<=126)return 1;
 return 0;
}
void close_dialog_d90e(void)
{
 select_pattern_5b00(0);
 restore_region_58b0(12,66,51,148);
}
