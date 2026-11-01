/* 4575/45A2: prepare packed frame colours and attach a configured actor. */
typedef unsigned char Byte;
typedef struct {Byte width,height;signed char x,y;char huge *pixels;} Frame;
typedef struct Actor {
 int x,y,old_x,old_y,flag;
 Byte colour,square;
 int left,right,top,bottom;
 Frame *frame;
 void far *resource;
 struct Actor *next;
} Actor;
extern Frame frames[];
extern Actor actors[];
extern void far *frame_resources[];
extern void prepare_pixels_e8cb(char huge *,int,int),insert_actor(int,Actor *);
void prepare_color_4575(register Frame *frame)
{
 prepare_pixels_e8cb(frame->pixels,(((unsigned)frame->width+3)>>1)&0xfffe,frame->height);
}
void configure_actor_45a2(register int x,register int y,int frame_index,int actor_index)
{
 Frame *a;
 Actor *b;
 a=&frames[frame_index];
 b=&actors[actor_index];
 b->colour=0;
 b->x=x;b->y=y;
 b->left=-(a->x-x);
 b->right=((a->width+3)&252)+b->left-1;
 b->top=-(a->y-y);
 b->bottom=-(a->y-a->height)+y-1;
 b->resource=frame_resources[frame_index];
 b->square=255;
 b->frame=a;
 insert_actor(y+200,b);
}
