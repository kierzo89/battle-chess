#ifndef BC_GEOMETRY_H
#define BC_GEOMETRY_H
#include <stdbool.h>
/* Original 320x200 coordinates. The recovered name 'flat' is perspective;
 * 'tilted' is the rectangular static-piece board. */
int bc_geometry_hit(bool perspective,int x,int y); /* engine 0x88 or -1 */
bool bc_geometry_anchor(bool perspective,unsigned square,int *x,int *y);
unsigned bc_geometry_frame(unsigned kind,unsigned side,unsigned square);
unsigned bc_geometry_facing(unsigned kind,unsigned side,unsigned square);
unsigned bc_geometry_faced_frame(unsigned kind,unsigned facing);
#endif
