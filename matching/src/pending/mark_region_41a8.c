typedef struct {
    int shift,mode,width,height,source_skip,dest_skip,left_mask,right_mask;
    char huge *destination; char huge *source;
} Blit;
extern int dirty_left,dirty_right,dirty_top,dirty_bottom;
extern int region_left,region_right,region_width,stride,height;
extern char huge *screen;
extern char huge region_buffer[];
extern Blit blit;
extern char overflow_message[];
extern void error_0d8d(char *),blit_e57a(void),fill_5a4f(char far *,int,int);
void mark_region_41a8(register int special)
{
    char huge *a;
    int b;
    region_left = dirty_left << 2;
    region_right = (dirty_right << 2) + 3;
    region_width = region_right - region_left + 1;
    stride = ((dirty_right-dirty_left)<<1)+2;
    height = dirty_bottom-dirty_top+1;
    if (stride*height>3248) {
        error_0d8d(overflow_message);
        return;
    }
    a = screen + (160*dirty_top + (dirty_left<<1));
    blit.left_mask=-1;
    blit.right_mask=-1;
    blit.source_skip=160-stride;
    blit.dest_skip=0;
    blit.source=a;
    blit.destination=region_buffer;
    blit.height=height;
    blit.width=stride>>1;
    blit.shift=0;
    blit.mode=0;
    if (!special) blit_e57a();
    else fill_5a4f(region_buffer,height*stride,0);
}
