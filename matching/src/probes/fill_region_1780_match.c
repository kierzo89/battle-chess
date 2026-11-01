/* Fill a modal region, then draw its three inset border rectangles. */
extern void far input_select_11ef_001e(void),far input_init_11ef_0000(void);
extern void far graphics_rect_110d_0003(int,int,int,int);
extern void select_pen_5b18(int),rect_2079(int,int,int,int);
void fill_region_1780(register int left,register int top,int right,int bottom,int colour)
{
 input_select_11ef_001e();
 select_pen_5b18(colour);
 graphics_rect_110d_0003(left,top,right,bottom);
 rect_2079(left,top,right,bottom);
 select_pen_5b18(14);
 for(colour=0;colour<3;colour++)rect_2079(++left,++top,--right,--bottom);
 input_init_11ef_0000();
}
