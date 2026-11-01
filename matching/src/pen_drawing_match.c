/* Complete pen movement and integer Bresenham routine. */
extern int pen_x,pen_y;
extern void (*plot_pixel)(int,int);
extern int abs_i16(int),sign_5c8b(int);
void move_pen_5b3d(int x,int y)
{
 pen_x=x;pen_y=y;
}
void line_pen_5b55(int x,int y)
{
 int a,b,c,d,e,f,g;
 e=abs_i16(x-pen_x);
 g=abs_i16(y-pen_y);
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
