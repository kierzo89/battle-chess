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
