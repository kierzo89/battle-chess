/* Original board-square outline routine. */
extern int (*square_x)[9];
extern int *square_y;
extern int dirty_left,dirty_right,dirty_top,dirty_bottom,region_left,region_width;
extern unsigned adjacent_square;
extern void mark_region_41a8(int),render_42a0(void),select_pen_5b18(unsigned),move_pen_5b3d(int,int),line_pen_5b55(int,int);
void outline_square_543a(unsigned square,unsigned pen)
{
 register int *p;
 register int a;
 /* p=near x-row pointer inSI; a=left top inDI. Compiler reserves their
  * frame slots too. Unread original words b/c/d/f/g/k retain unknown purpose.
  * e=converted adjacent square; h=row; i=top; j=right top; l=column;
  * m=bottom; n=left bottom; o=right bottom. Two CSE words are compiler-made. */
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
  dirty_left=(a<n?a:n)>>2;
  dirty_right=(j>o?j:o)>>2;
  dirty_top=i;dirty_bottom=m;
  if(dirty_left<0)dirty_left=0;
  if(dirty_right>79)dirty_right=79;
  if(dirty_top<0)dirty_top=0;
  if(dirty_bottom>199)dirty_bottom=199;
  mark_region_41a8(0);
  if(pen) {
   select_pen_5b18(pen);
   a-=region_left;
   j-=region_left;
   n-=region_left;
   o-=region_left;
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
     move_pen_5b3d(region_width-1,0);line_pen_5b55(j,0);
     move_pen_5b3d(region_width-1,1);line_pen_5b55(j,1);
    }
    if(square+1==e||square+17==e) {
     move_pen_5b3d(region_width-1,m-i-1);line_pen_5b55(o,m-i-1);
     move_pen_5b3d(region_width-1,m-i);line_pen_5b55(o,m-i);
    }
   }
  }
  render_42a0();
 }
}
