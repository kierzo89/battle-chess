/* Pen setup and ordinary integer Bresenham drawing. */
typedef unsigned char Byte;
typedef struct {Byte unread[12];Byte colour;} PenState;
extern unsigned pen_segment;
extern Byte packed_pen;
extern int pen_x,pen_y;
extern void (*plot_pixel)(int,int);
extern int abs_8fb5(int),sign_5c8b(int);
void select_pen_5b18(Byte colour)
{
 ((PenState far *)((unsigned long)pen_segment<<16))->colour=colour&15;
 packed_pen=(((PenState far *)((unsigned long)pen_segment<<16))->colour<<4)|((PenState far *)((unsigned long)pen_segment<<16))->colour;
}
