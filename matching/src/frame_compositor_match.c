/* 3B3A: union the current/cached frame bounds and composite both pixel planes.
 * Complete789-byte MSC5 /AS /Zi function reconstruction. */
typedef unsigned char Byte;
typedef struct {Byte width,height;signed char x,y;char huge *pixels;} Frame;
typedef struct {
 int shift,mode,width,height,source_skip,dest_skip,left_mask,right_mask;
 char huge *destination;
 char huge *source;
 int reserved[3],saved_word;
} Blit;
extern Frame cached_frames[];
extern Blit blit;
extern void fill_5a4f(char huge *,int,int),blit_e57a(void);
void compose_frame_3b3a(register Frame *source,int index,Frame *destination)
{
 /* a: destination pointer; b: unsigned bound; c/d: coordinate deltas;
  * e: cached frame; f: signed pixel offset; g: observed unwritten word;
  * h: cached width. Neutral locals retain the recovered stack slots. */
 char huge *a;
 register unsigned b;
 int c,d;
 Frame *e;
 int f,g;
 Byte h;
 e=&cached_frames[index];
 h=e->width;
 if(h&&e->height) {
  if(e->x<source->x) {
   b=source->x-e->x+h;
   destination->width=source->width>b?source->width:b;
   destination->x=source->x;
  }else {
   b=e->x-source->x+source->width;
   destination->width=e->width>b?e->width:b;
   destination->x=e->x;
  }
  if(e->y<source->y) {
   b=source->y-e->y+e->height;
   destination->height=source->height>b?source->height:b;
   destination->y=source->y;
  }else {
   b=e->y-source->y+source->height;
   destination->height=e->height>b?e->height:b;
   destination->y=e->y;
  }
 }else {
  destination->width=source->width;
  destination->height=source->height;
  destination->x=source->x;
  destination->y=source->y;
 }
 fill_5a4f(destination->pixels,(((unsigned)destination->width+3)>>1)*destination->height,0);
 c=destination->x-source->x;
 d=destination->y-source->y;
 f=((((unsigned)destination->width+3)>>1)&0xfe)*d;
 f+=(c>>1)&0xfffe;
 a=destination->pixels+f;
 blit.height=source->height;
 blit.width=((((((unsigned)source->width+3)>>1)&0xfe)+2)>>1);
 blit.shift=c&3;
 blit.left_mask=-1;blit.right_mask=0;blit.source_skip=-2;
 blit.dest_skip=(((((unsigned)destination->width+3)>>1)&0xfe)-((((unsigned)source->width+3)>>1)&0xfe))-2;
 blit.source=source->pixels;blit.destination=a;
 blit.mode=0;
 blit_e57a();
 if(e->width&&e->height) {
  c=destination->x-e->x;
  d=destination->y-e->y;
  a=destination->pixels+((((unsigned)destination->width+3)>>1)&0xfe)*d+((c>>1)&0xfffe);
  blit.height=e->height;
  blit.width=((((((unsigned)e->width+3)>>1)&0xfe)+2)>>1);
  blit.shift=c&3;
  blit.mode=2;
  blit.left_mask=-1;blit.right_mask=0;blit.source_skip=-2;
  blit.dest_skip=(((((unsigned)destination->width+3)>>1)&0xfe)-((((unsigned)e->width+3)>>1)&0xfe))-2;
  blit.source=e->pixels;blit.destination=a;
  /* The original reads this frame word without an observed assignment. */
  blit.saved_word=g;
  blit_e57a();
 }
}
