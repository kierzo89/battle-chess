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
 /* a=message cursor; b=extra height; c/d=left/right pixels; e=length, then input code. */
 char *a;
 int b;
 long c,d;
 int e;
 b=type?12:0;
 modal_0054=1;begin_input_0fb0();
 a=message;e=0;
 while(*a++)e++;
 if(e<36)e=36;
 e++;
 c=(20-(e>>1))*8-8;
 d=(e>>1)*8+167;
 fill_region_1780(c,80,d,120+b,menu_state);
 menu_text.text=message;menu_text.colour=background;menu_text.attribute=menu_state;
 draw_text_e915(&menu_text,c+8,88);
 menu_text.colour=foreground;
 switch(type) {
 case 0:case 1:menu_text.text=prompt_accept_4c44;break;
 case 2:menu_text.text=prompt_choice_4c68;break;
 case 3:menu_text.text=prompt_save_4c8e;break;
 }
 draw_text_e915(&menu_text,c+8,104);
 if(b) {
  switch(type) {
  case 1:menu_text.text=prompt_help_4cae;break;
  case 2:menu_text.text=prompt_choice_help_4cce;break;
  case 3:menu_text.text=prompt_save_help_4cf0;break;
  }
  draw_text_e915(&menu_text,c+8,115);
 }
 do {e=obtain_input();}while(e!=0x1003&&(e!=0x1004||!b));
 restore_region_58b0(c>>2,d>>2,80,120+b);
 end_input_102d();modal_0054=0;
 return e;
}
