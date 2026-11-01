/* Rebuild visible board actors and interpolate a screen-space position. */
typedef unsigned char Byte;
typedef struct {Byte width,height;signed char x,y;char huge *pixels;} Frame;
typedef struct Actor {int x,y,old_x,old_y,flag;Byte colour,square;int left,right,top,bottom;Frame *frame;void far *resource;struct Actor *next;} Actor;
extern Actor actors[];
extern Frame frames[];
extern Byte cells[],actor_map[],*frame_index;
extern int *screen_x,*screen_y;
extern void attach_actor(int,int,int,Frame *,Actor *);
extern int motion_x,motion_y;
void display_board_5e18(void)
{
 /* a: board cursor; b: actor index; c: square; d/e: coordinate cursors. */
 Byte *a;register int b,c;int *d,*e;
 b=0;d=screen_x;e=screen_y;a=cells;
 for(c=0;c<=63;c++) {
  if(*a) {
   actors[b].square=c;actor_map[c]=b;
   attach_actor(*d,*e,*a&64,&frames[frame_index[*a&63]],&actors[b++]);
  }
  d++;a++;if((c&7)==7)e++;
 }
}
void interpolate_position_5ebc(register int x,register int y,int to_x,int to_y,int steps,int step)
{
 /* a/b: remainders; c/d: whole steps; e/f: signed displacement. */
 int a,b,c,d,e,f;
 e=to_x-x;f=to_y-y;
 c=e/steps;d=f/steps;a=e%steps;b=f%steps;
 if(e>=0)motion_x=c*step+(a*step+steps/2)/steps+x;
 else motion_x=c*step+(a*step-steps/2)/steps+x;
 if(f>=0)motion_y=d*step+(b*step+steps/2)/steps+y;
 else motion_y=d*step+(b*step-steps/2)/steps+y;
}
