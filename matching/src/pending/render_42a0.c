typedef unsigned char Byte;
typedef struct {Byte width,height;signed char x,y;char huge *pixels;} Frame;
typedef struct Actor {
    int x,y,old_x,old_y,flag;
    Byte colour,square;
    int left,right,top,bottom;
    Frame *frame;
    Byte rest[4];
    struct Actor *next;
} Actor;
typedef struct {
    int shift,mode,width,height,source_skip,dest_skip,left_mask,right_mask;
    char huge *destination;
    char huge *source;
} Blit;
extern int region_left,region_right,dirty_top,dirty_bottom,stride,height;
extern int left_masks[],right_masks[];
extern Actor *actors_head,*active_actor;
extern Blit blit;
extern char far color_buffer[];
extern char huge region_buffer[];
extern Byte page_mode;
extern void prepare_color_4575(Frame *),blit_e57a(void);
extern void far graphics_begin(void);
extern void far graphics_copy(int,int,int,int,char far *);
extern void far graphics_end(void);
extern void copy_5cb5(int,int,int,int,char far *);
void render_42a0(void)
{
    int p,q,a,r,b;
    int s;
    register Actor *c;
    int t,d,u,e;
    register int v;
    int f;
    int w,g,h,i,j,k,l,m,n;
    unsigned o;
    b = region_left >> 2;
    for (c=actors_head;c;c=c->next) {
        if (c->left<=region_right && c->right>=region_left &&
            c->top<=dirty_bottom && c->bottom>=dirty_top &&
            (!active_actor || active_actor==c)) {
            if (c->colour) prepare_color_4575(c->frame);
            f=c->left-region_left;
            if (f<0) {v=-f;f=0;w=left_masks[v&3];}
            else {v=0;w=-1;}
            k=region_right-c->right;
            if (k<0) {j=-k;k=0;l=right_masks[j&3];}
            else {j=0;l=(k&3)?0:-1;}
            q=((c->frame->width+3)&0xfc)-j-v;
            a=((q+3)>>1)&~1;
            if (c->left&3) {
                if (!j) a+=2;
                else if (v) a+=2;
            }
            p=c->top-dirty_top;
            if (p<0) {
                n=-p;p=0;
                i=(c->bottom>dirty_bottom)?dirty_bottom-dirty_top+1:c->bottom-dirty_top+1;
            } else {
                n=0;
                i=(c->bottom>dirty_bottom)?dirty_bottom-c->top+1:c->bottom-c->top+1;
            }
            o=(((unsigned)c->frame->width+3)>>1)&0xfe;
            g=((unsigned)(i-1)+n)*o+((v>>1)&~1);
            h=(i+p-1)*stride+((f>>1)&~1);
            if (v&3) h-=2;
            r=((((unsigned)c->frame->width+3)>>1)&0xfe)*c->frame->height;
            s=stride*height;
            blit.left_mask=w;
            blit.right_mask=l;
            blit.source_skip=-(((((unsigned)c->frame->width+3)>>1)&0xfe)+a);
            blit.dest_skip=-(a+stride);
            if (c->colour) blit.source=color_buffer+g;
            else blit.source=c->frame->pixels+g;
            blit.destination=region_buffer+h;
            blit.height=i;
            blit.width=a>>1;
            blit.shift=c->left&3;
            blit.mode=1;
            blit_e57a();
        }
    }
    active_actor=0;
    if (!page_mode) {
        graphics_begin();
        graphics_copy(b<<1,dirty_top,stride,height,region_buffer);
        graphics_end();
    } else copy_5cb5(b<<1,dirty_top,stride,height,region_buffer);
}
