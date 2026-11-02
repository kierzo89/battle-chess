#ifndef BC_SIDESTEP_H
#define BC_SIDESTEP_H
#include <stdbool.h>
typedef struct {int from_x,from_y,to_x,to_y,x,y,anchor_x,anchor_y;unsigned step;bool done,failed;} BCSidestep;
bool bc_sidestep_begin(BCSidestep *,int x,int y,unsigned direction);
/* Original6BF9 seven eligible calls: steps0..6, static actor frame, no
 * readiness stream. Completion updates anchor after the final visible step. */
int bc_sidestep_tick(BCSidestep *);
bool bc_direction_step(unsigned direction,int *x,int *y);
#endif
