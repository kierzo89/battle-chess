typedef unsigned char Byte;
typedef struct {int kind,status,code,reserved,x,y,word6,word7,word8,word9;} DialogEvent;
extern void fill_8a96(char *,int,int);
extern char *strcpy(char *,const char *);
extern unsigned strlen(const char *);
extern void select_pattern_5b00(int),restore_region_58b0(int,int,int,int);
extern void paint_dialog_button_d9c6(int,int);
extern DialogEvent *next_dialog_event_d766(void);
extern int dialog_hit_d840(int,int,int),pointer_x,pointer_y;
extern void far update_pointer_11ef_0030(void);
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
int dialog_button_d92e(int button,int extra)
{
 DialogEvent *a;
 int b=1;
 for(;;) {
  paint_dialog_button_d9c6(button,b);
  for(;;) {
   a=next_dialog_event_d766();
   if(a->kind==4 && a->status==0 && a->code==0) {
    paint_dialog_button_d9c6(button,0);
    return dialog_hit_d840(pointer_x,pointer_y,extra)==button;
   }
   if(a->kind==5 && a->status==0) {
    pointer_x=a->x;pointer_y=a->y;update_pointer_11ef_0030();
    b=dialog_hit_d840(pointer_x,pointer_y,extra)==button;
    break;
   }
  }
 }
}
