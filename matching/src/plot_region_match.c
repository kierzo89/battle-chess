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
