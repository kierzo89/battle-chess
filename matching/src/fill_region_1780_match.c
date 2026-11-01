/* Fill a modal region, then draw its three inset border rectangles. */
extern void far graphics_begin(void),far graphics_end(void);
extern void far graphics_rect_110d_0003(int,int,int,int);
extern void select_pen_5b18(int),rect_2079(int,int,int,int);
void fill_region_1780(register int left,register int top,int right,int bottom,int colour)
{
 graphics_begin();
 select_pen_5b18(colour);
 graphics_rect_110d_0003(left,top,right,bottom);
 rect_2079(left,top,right,bottom);
 select_pen_5b18(14);
 for(colour=0;colour<3;colour++)rect_2079(++left,++top,--right,--bottom);
 graphics_end();
}
