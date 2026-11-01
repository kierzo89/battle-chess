/* Copy a packed rectangle to the huge screen pointer, preserving carries. */
extern char huge *screen;
void copy_5cb5(int x,int y,int width,int height,char huge *source)
{
 int a,b;
 char huge *c;
 c=screen;
 c+=160*y+x;
 a=160-width;
 while(height--) {
  b=width;
  while(b--)*c++=*source++;
  c+=a;
 }
}
