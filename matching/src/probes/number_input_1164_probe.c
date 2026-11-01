typedef unsigned char Byte;
typedef struct {Byte colour,attribute;char *text;} Text;
extern int menu_state;
extern Byte foreground;
extern Text menu_text;
extern char number_label_4c28[];
extern void begin_input_0fb0(void),end_input_102d(void);
extern void fill_region_1780(int,int,int,int,int);
extern void restore_region_58b0(int,int,int,int);
extern void draw_text_e915(Text *,int,int);
extern int text_input_1064(int,int,char *,int,int);
long get_number(void)
{
 long value;
 int initial_key=0;
 char buffer[16];
 register int i,length;
 begin_input_0fb0();
 do {
  fill_region_1780(0,88,319,111,menu_state);
  menu_text.text=number_label_4c28;menu_text.colour=foreground;menu_text.attribute=menu_state;
  draw_text_e915(&menu_text,8,96);
  length=text_input_1064(232,96,buffer,5,initial_key);
  value=0;
  if(length) {
   for(i=0;i<length;i++) {
    value=value*10+(buffer[i]-'0');
    if(buffer[i]<'0'||buffer[i]>'9') {value=0;i=length;}
   }
  }else value=-1;
 }while(value==0||value>10000L);
 restore_region_58b0(0,79,88,111);
 end_input_102d();
 if(value<0)value=0;
 return value;
}
