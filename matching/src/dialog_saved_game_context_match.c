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
/* Actual native dialog setup, compact saved-name rows and rendering. */
extern int dialog_selected,saved_name_count_52d4,background;
extern void select_pattern_5b00(int),fill_8a96(char *,int,int);
extern char *strcpy(char *,const char *);
extern int strcmp(const char *,const char *);
extern unsigned strlen(const char *);
extern void fill_dialog_background_d440(void),outline_dialog_d474(int),label_dialog_buttons_d4db(int);
extern void select_pen_5b18(int),move_pen_5b3d(int,int),draw_dialog_text_d551(char *,int);
void prepare_dialog_d2cc(void)
{
 select_pattern_5b00(1);
 dialog_selected=-1;
}
void collect_saved_names_d2dd(char *records,char rows[8][16])
{
 register int i,j;
 char *p;
 fill_8a96((char *)rows,128,0);
 p=(char *)rows;
 for(i=0;i!=8;i++,p+=16) {
  *p=0;
  p[15]=-1;
 }
 for(i=j=0;i!=8;i++) {
  if(*(records+i*48+16)) {
   strcpy(rows[j],records+i*48+16);
   rows[j++][15]=i;
  }
 }
 saved_name_count_52d4=j;
}
void draw_saved_game_rows_d365(char rows[8][16],char *action)
{
 int v;
 v=strcmp(action,dialog_strings.load);
 fill_dialog_background_d440();
 outline_dialog_d474(v);
 label_dialog_buttons_d4db(v);
 select_pen_5b18(background);
 for(v=0;v!=8;v++) {
  move_pen_5b3d(64,v*10+68);
  draw_dialog_text_d551(rows[v],strlen(rows[v]));
 }
 v=strlen(action);
 if(v>9)v=9;
 move_pen_5b3d(-(v*4-226),84);
 draw_dialog_text_d551(dialog_strings.separator,v);
 move_pen_5b3d(-(v*4-226),78);
 draw_dialog_text_d551(action,v);
}

/* Native dialog backdrop, outlines and labels; no automatic padding/storage. */
extern int menu_state,foreground,background;
extern void select_pen_5b18(int),offset_dialog_rect_d528(int,int,int,int);
extern void fill_region_1780(int,int,int,int,int),rect_2079(int,int,int,int);
extern void move_pen_5b3d(int,int),draw_dialog_text_d551(char *,int);
void fill_dialog_background_d440(void)
{
 select_pen_5b18(menu_state);
 offset_dialog_rect_d528(0,0,208,89);
 fill_region_1780(51,51,267,148,menu_state);
}
void outline_dialog_d474(int allow_extra)
{
 select_pen_5b18(foreground);
 rect_2079(58,58,189,141);
 rect_2079(59,59,188,140);
 rect_2079(200,129,253,141);
 if(allow_extra)rect_2079(200,109,253,121);
}
void label_dialog_buttons_d4db(int allow_extra)
{
 select_pen_5b18(background);
 move_pen_5b3d(211,118);
 if(allow_extra)draw_dialog_text_d551(dialog_strings.done,4);
 move_pen_5b3d(204,138);
 draw_dialog_text_d551(dialog_strings.cancel,6);
}

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
 strcpy(buffer,dialog_strings.filename);
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
