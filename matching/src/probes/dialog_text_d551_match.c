typedef unsigned char Byte;
typedef struct {Byte colour,attribute;char *text;} Text;
extern Text dialog_text;
extern int pen_x,pen_y;
extern void draw_text_e915(Text *,int,int);
void draw_dialog_text_d551(char *text,int limit)
{
 char a;
 if(limit) {a=text[limit];text[limit]=0;}
 dialog_text.text=text;
 draw_text_e915(&dialog_text,pen_x,pen_y-6);
 if(limit)text[limit]=a;
}
