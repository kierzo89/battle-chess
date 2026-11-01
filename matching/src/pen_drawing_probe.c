/* Pen setup and ordinary integer Bresenham drawing. */
typedef unsigned char Byte;
typedef struct {Byte unread[12];Byte colour;} PenState;
extern unsigned pen_segment;
extern Byte packed_pen;
extern int pen_x,pen_y;
extern void (*plot_pixel)(int,int);
extern int abs_8fb5(int),sign_5c8b(int);
void select_pen_5b18(Byte colour)
{
 ((PenState far *)((unsigned long)pen_segment<<16))->colour=colour&15;
 packed_pen=(((PenState far *)((unsigned long)pen_segment<<16))->colour<<4)|((PenState far *)((unsigned long)pen_segment<<16))->colour;
}
void move_pen_5b3d(int x,int y)
{
 pen_x=x;pen_y=y;
}
void line_pen_5b55(int x,int y)
{
 int a,b,c,d,e,f,g;
 e=abs_8fb5(x-pen_x);
 g=abs_8fb5(y-pen_y);
 d=sign_5c8b(x-pen_x);
 f=sign_5c8b(y-pen_y);
 if(e>g) {
  a=(g<<1)-e;b=g<<1;c=(g-e)<<1;
  (*plot_pixel)(pen_x,pen_y);
  while(e--) {
   pen_x+=d;
   if(a<0)a+=b;
   else {pen_y+=f;a+=c;}
   (*plot_pixel)(pen_x,pen_y);
  }
 }else {
  a=(e<<1)-g;b=e<<1;c=(e-g)<<1;
  (*plot_pixel)(pen_x,pen_y);
  while(g--) {
   pen_y+=f;
   if(a<0)a+=b;
   else {pen_x+=d;a+=c;}
   (*plot_pixel)(pen_x,pen_y);
  }
 }
 pen_x=x;pen_y=y;
}
