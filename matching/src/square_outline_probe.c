/* Original board-square outline routine. */
extern int (*square_x)[9];
extern int *square_y;
extern int clip_left,clip_right,clip_top,clip_bottom,draw_origin_x,draw_width;
extern unsigned adjacent_square;
extern void graphics_region_41a8(int),graphics_restore_42a0(void),select_pen_5b18(unsigned),move_pen_5b3d(int,int),line_pen_5b55(int,int);
void outline_square_543a(unsigned square,unsigned pen)
{
 register int *p;
 register int a;
 int b,c,d,e,f,g,h,i,j,k,l,m,n,o;
 if(square<=63) {
  h=square>>3;
  l=square&7;
  p=square_x[h];
  a=p[l]-1;
  j=p[l+1];
  p+=9;
  n=p[l]-1;
  o=p[l+1];
  i=square_y[h];
  m=square_y[h+1]+1;
  clip_left=(a<n?a:n)>>2;
  clip_right=(j>o?j:o)>>2;
  clip_top=i;clip_bottom=m;
  if(clip_left<0)clip_left=0;
  if(clip_right>79)clip_right=79;
  if(clip_top<0)clip_top=0;
  if(clip_bottom>199)clip_bottom=199;
  graphics_region_41a8(0);
  if(pen) {
   select_pen_5b18(pen);
   a-=draw_origin_x;
   j-=draw_origin_x;
   n-=draw_origin_x;
   o-=draw_origin_x;
   move_pen_5b3d(a,0);
   line_pen_5b55(j,0);
   line_pen_5b55(o,m-i);
   line_pen_5b55(n,m-i);
   line_pen_5b55(a,0);
   move_pen_5b3d(a+1,1);
   line_pen_5b55(j-1,1);
   line_pen_5b55(j-1,0);
   line_pen_5b55(o-1,m-i);
   line_pen_5b55(o-1,m-i-1);
   line_pen_5b55(n+1,m-i-1);
   line_pen_5b55(n+1,m-i);
   line_pen_5b55(a+1,0);
   if(pen&&pen<28&&adjacent_square!=255) {
    select_pen_5b18(28);
    square=((square<<1)&0x70)|(square&7);
    e=((adjacent_square<<1)&0x70)|(adjacent_square&7);
    if(square-1==e||square-17==e) {
     move_pen_5b3d(0,0);line_pen_5b55(a,0);
     move_pen_5b3d(0,1);line_pen_5b55(a,1);
    }
    if(square-1==e||square+15==e) {
     move_pen_5b3d(0,m-i-1);line_pen_5b55(n,m-i-1);
     move_pen_5b3d(0,m-i);line_pen_5b55(n,m-i);
    }
    if(square+1==e||square-15==e) {
     move_pen_5b3d(draw_width-1,0);line_pen_5b55(j,0);
     move_pen_5b3d(draw_width-1,1);line_pen_5b55(j,1);
    }
    if(square+1==e||square+17==e) {
     move_pen_5b3d(draw_width-1,m-i-1);line_pen_5b55(o,m-i-1);
     move_pen_5b3d(draw_width-1,m-i);line_pen_5b55(o,m-i);
    }
   }
  }
  graphics_restore_42a0();
 }
}
