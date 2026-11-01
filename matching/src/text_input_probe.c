typedef unsigned char Byte;
typedef struct {Byte colour,attribute;char *text;} Text;
extern Byte text_input_active;
extern int menu_state;
extern Text menu_text;
extern int read_event_0254(void);
extern void draw_text_e915(Text *,int,int);
int text_input_1064(register int x,register int y,char *buffer,int limit,int key)
{
 int length;
 text_input_active=1;
 if(key) {buffer[0]=key;buffer[1]='_';buffer[2]=0;length=1;}
 else {buffer[0]='_';buffer[1]=0;length=0;}
 menu_text.text=buffer;menu_text.colour=15;menu_text.attribute=menu_state;
 do {
  draw_text_e915(&menu_text,x,y);
  read_again:
  key=read_event_0254();if((key&0xf000)!=0x2000)goto read_again;
  key&=0xfff;
  if(key>=32 && length<limit && key<128) {
   buffer[length++]=key;buffer[length]='_';buffer[length+1]=0;
  }
  if(key==8 && length>0) {
   buffer[--length]='_';buffer[length+1]=' ';buffer[length+2]=0;
  }
 }while(key!=13);
 buffer[length]=0;text_input_active=0;
 return length;
}
