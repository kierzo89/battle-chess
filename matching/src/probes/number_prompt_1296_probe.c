typedef unsigned char Byte;
typedef struct {Byte colour,attribute;char *text;} Text;
extern Byte modal_0054,foreground,background;
extern int menu_state;
extern Text menu_text;
extern char prompt_accept_4c44[],prompt_choice_4c68[],prompt_save_4c8e[];
extern char prompt_help_4cae[],prompt_choice_help_4cce[],prompt_save_help_4cf0[];
extern void begin_input_0fb0(void),end_input_102d(void);
extern void fill_region_1780(int,int,int,int,int),restore_region_58b0(int,int,int,int);
extern void draw_text_e915(Text *,int,int);
extern int obtain_input(void);
int prompt_1296(register char *message,int unused,register int type)
{
 char *p;
 int extra;
 long left,right;
 int length;
 extra=type?12:0;
 modal_0054=1;begin_input_0fb0();
 p=message;length=0;
 while(*p++)length++;
 if(length<36)length=36;
 length++;
 left=(20-(length>>1))*8-8;
 right=(length>>1)*8+167;
 fill_region_1780(left,80,right,120+extra,menu_state);
 menu_text.text=message;menu_text.colour=background;menu_text.attribute=menu_state;
 draw_text_e915(&menu_text,left+8,88);
 menu_text.colour=foreground;
 switch(type) {
 case 0:case 1:menu_text.text=prompt_accept_4c44;break;
 case 2:menu_text.text=prompt_choice_4c68;break;
 case 3:menu_text.text=prompt_save_4c8e;break;
 }
 draw_text_e915(&menu_text,left+8,104);
 if(extra) {
  switch(type) {
  case 1:menu_text.text=prompt_help_4cae;break;
  case 2:menu_text.text=prompt_choice_help_4cce;break;
  case 3:menu_text.text=prompt_save_help_4cf0;break;
  }
  draw_text_e915(&menu_text,left+8,115);
 }
 do {length=obtain_input();}while(length!=0x1003&&(length!=0x1004||!extra));
 restore_region_58b0(left>>2,right>>2,80,120+extra);
 end_input_102d();modal_0054=0;
 return length;
}
