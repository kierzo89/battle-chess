/* REA3F9E: update actor geometry and the clipped redraw rectangle. */
typedef unsigned char Byte;
typedef struct {Byte width,height;signed char x,y;Byte rest[4];} Frame;
typedef struct Actor {
    int x,y,old_x,old_y,flag;
    Byte colour,square;
    int left,right,top,bottom;
    Frame *frame;
    Byte rest[4];
    struct Actor *next;
} Actor;
extern int dirty_left,dirty_right,dirty_top,dirty_bottom;
extern Actor *active_actor;
extern void release_frame_3a99(Frame *),mark_region_41a8(int),render_42a0(void);
void draw_actor(register int x,register int y,int colour,Frame *frame,Actor *actor)
{
    int a; /* original frame word has no observed reads/writes */
    Frame *b;
    int c;
    while (y>=200) y-=200;
    dirty_left = -(frame->x-x)>>2;
    dirty_right = (((frame->width+(unsigned)3)&0xfc)-frame->x+x-1)>>2;
    dirty_top = -(frame->y-y);
    dirty_bottom = -(frame->y-frame->height)+y-1;
    actor->left = -(frame->x-x);
    actor->right = ((frame->width+3)&0xfc)+actor->left-1;
    actor->top = dirty_top;
    actor->bottom = dirty_bottom;
    if (b=actor->frame) {
        if (actor->flag) release_frame_3a99(actor->frame);
        c = (actor->x-b->x)>>2;
        if (c<dirty_left) dirty_left=c;
        c = (((b->width+(unsigned)3)&0xfc)-b->x+actor->x-1)>>2;
        if (c>dirty_right) dirty_right=c;
        c = actor->y-b->y;
        if (c<dirty_top) dirty_top=c;
        c = actor->y-b->y+b->height-1;
        if (c>dirty_bottom) dirty_bottom=c;
    } else actor->flag=0;
    if (dirty_left<0) dirty_left=0;
    if (dirty_right>79) dirty_right=79;
    if (dirty_top<0) dirty_top=0;
    if (dirty_bottom>199) dirty_bottom=199;
    actor->x=x;
    actor->y=y;
    actor->old_x=x;
    actor->old_y=y;
    actor->colour=colour!=0;
    actor->frame=frame;
    if (dirty_right>=0 && dirty_left<=79 && dirty_top<=199 && dirty_bottom>=0) {
        if (actor->square==254) {
            mark_region_41a8(1);
            active_actor=actor;
        } else mark_region_41a8(0);
        render_42a0();
    }
}
