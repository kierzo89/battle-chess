#ifndef BC_PLACEMENT_H
#define BC_PLACEMENT_H
#include "walk.h"
typedef enum {BC_EFFECT,BC_OFFSET_HALF,BC_OFFSET_FULL} BCPlacementKind;
typedef struct {
 const BCWalk *sequence;BCTaskClock clock;
 unsigned frame,emitted,total,steps;
 int from_x,from_y,to_x,to_y,x,y,anchor_x,anchor_y;
 bool done,failed,command_active;
 BCPlacementKind mode;
} BCPlacement;
/* from is actor.old_x/y, not necessarily its currently drawn position.
 * Target is absolute: command4 supplies old+signed step table; command7 supplies
 * the capture square offsets. Preserve the original last-frame/anchor split. */
bool bc_placement_begin(BCPlacement *task,BCPlacementKind mode,unsigned engine_kind,unsigned orientation,unsigned profile,int from_x,int from_y,int to_x,int to_y,bool command_active);
/* -1 invalid,0 waiting,1 emitted frame (possibly final),2 already complete.
 * On final emission done becomes true and anchor becomes the exact target.
 * sequence+frame identify the original composed walking frame to draw at x/y. */
int bc_placement_tick(BCPlacement *task,unsigned colour,BCSoundEvent sound,void *context);
#endif
