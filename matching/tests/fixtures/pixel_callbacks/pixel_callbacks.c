/* Near CODE callbacks used by the pen renderer, selected with modes 0 and 1. */
typedef void (*PixelWriter)(int,int);
extern void plot_region_5a7c(int,int);
extern void bios_plot_pixel_ea64(int,int);
PixelWriter plot_pixel = plot_region_5a7c;
PixelWriter pixel_writers[] = {plot_region_5a7c,bios_plot_pixel_ea64};
