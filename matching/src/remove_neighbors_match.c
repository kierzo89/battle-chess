void empty_argument(unused) int unused; {}

void empty_5a37() {}
void empty_5a43() {}

/* REA5A4F: fill bytes through a huge pointer, preserving segment carry. */
void fill_5a4f(char huge *destination,int count,char value)
{
    for (;count;count--) *destination++=value;
}

/* REA5A7C: replace one packed pixel nibble in the huge region buffer. */
typedef unsigned char Byte;
extern int stride;
extern Byte packed_pen;
extern Byte huge region_buffer[];
void plot_region_5a7c(int x,int y)
{
    Byte mask;
    y = y*stride+x/2;
    if (y>3248) return;
    mask = (x&1)?15:240;
    region_buffer[y]=(region_buffer[y]&~mask)|(mask&packed_pen);
}
