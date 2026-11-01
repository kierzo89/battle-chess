/* Decode frame data and undo XOR rows in the huge arena, image2D13. */
typedef unsigned char Byte;
typedef struct {Byte width,height;signed char x,y;Byte huge *pixels;} Frame;
extern Frame frames[];
extern unsigned count_0096;
extern Byte huge *arena_cursor;
extern void decode_asset_bytes_e282(Byte huge *,unsigned long,unsigned);
void decode_frame_directory(Byte *source)
{
 register int i,j;
 int n;
 Byte huge *a,huge *b;
 unsigned long *directory;
 a=arena_cursor;
 directory=(unsigned long *)&frames[count_0096];
 for(i=count_0096;*(unsigned long *)source;i++) {
  *directory++=*(unsigned long *)source;source+=4;
  *(Byte huge **)directory=a;directory++;
  decode_asset_bytes_e282(a,(unsigned)(frames[i].height*((unsigned)(frames[i].width+1)>>1)),(frames[i].width+1)>>1);
  n=(frames[i].height-1)*(((frames[i].width+3)>>1)&254);
  b=a+(((frames[i].width+3)>>1)&254);
  for(j=n;j;j--){*b^=*a;b++;a++;}
  a=b;
 }
 arena_cursor=a;
 count_0096=i;
}
