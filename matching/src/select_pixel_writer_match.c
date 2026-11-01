/* The selector's DATA word is consumed by indirect near calls in line_pen. */
typedef void (*PixelWriter)(int,int);
extern PixelWriter plot_pixel,pixel_writers[];
void select_pattern_5b00(int index)
{
    plot_pixel=pixel_writers[index];
}
