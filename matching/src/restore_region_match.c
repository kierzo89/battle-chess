extern int dirty_left,dirty_right,dirty_top,dirty_bottom;
extern void mark_region_41a8(int),render_42a0(void);
void restore_region_58b0(register int left,register int right,int top,int bottom)
{
 /* a=packed row bytes, b=rows per rendering chunk, c=remaining byte area.
    All three words are assigned and consumed by the native loop. */
 int a,b,c;
 dirty_left=left;dirty_right=right;
 a=(right-left)*2+2;
 c=(bottom-top+1)*a;
 while(c) {
  b=812/a;
  dirty_top=top;
  dirty_bottom=top+b-1;
  if(bottom<dirty_bottom)dirty_bottom=bottom;
  mark_region_41a8(0);
  render_42a0();
  top=dirty_bottom+1;
  c=(bottom-top+1)*a;
 }
}
