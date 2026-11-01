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
typedef struct Actor {
 int x,y,old_x,old_y,flag;
 Byte colour,square;
 int left,right,top,bottom;
 Frame *frame;
 Byte rest[4];
 struct Actor *next;
} Actor;
extern Actor *actors_head;
extern void draw_actor(int,int,int,Frame *,Actor *);
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

/* 3E4F: present the complete 160 by200 screen through the existing graphics ABI. */
extern char huge *screen;
extern void far graphics_begin(void);
extern void far graphics_copy(int,int,int,int,char far *);
extern void far graphics_end(void);
void reset_graphics_3e4f(void)
{
 graphics_begin();
 graphics_copy(0,0,160,200,screen);
 graphics_end();
}

void clear_actor_3e81(register Actor *actor)
{
    register Actor **link;
    link = &actors_head;
    while (*link) {
        if (*link == actor) *link = actor->next;
        else link = &(*link)->next;
    }
}

void insert_actor(register int y, register Actor *actor)
{
    Actor **link;
    link = &actors_head;
    while (*link != actor) {
        if (!*link) {
            actor->next = 0;
            *link = actor;
        } else if ((*link)->y >= y) {
            actor->next = *link;
            *link = actor;
        } else
            link = &(*link)->next;
    }
}

void attach_actor(register int x, register int y, int colour, Frame *frame, Actor *actor)
{
    clear_actor_3e81(actor);
    insert_actor(y,actor);
    draw_actor(x,y,colour,frame,actor);
}

void detach_actor(register Actor *actor)
{
    clear_actor_3e81(actor);
    draw_actor(actor->x,actor->y,actor->colour,actor->frame,actor);
    actor->frame = 0;
    actor->square = 0;
}

void detach_all(void)
{
    while (actors_head)
        detach_actor(actors_head);
}
