#ifndef BC_TURN_ANIMATION_H
#define BC_TURN_ANIMATION_H
#include "presentation.h"
typedef struct {
 const uint8_t *control; unsigned length,pair,list,count;
 const unsigned *tokens;
} BCTurnSequence;
const BCTurnSequence *bc_turn_sequence(unsigned kind,unsigned orientation,int direction,unsigned profile);
typedef struct {
 BCTaskClock clock;
 const BCTurnSequence *sequence;
 unsigned kind,from,to,profile,step,frame;
 int direction;
 bool failed,done;
} BCTurnAnimation;
bool bc_turn_begin(BCTurnAnimation *turn,unsigned kind,unsigned from,unsigned to,unsigned profile);
/* One eligible original task dispatch: -1 malformed, 0 waiting, 1 frame,
 * 2 complete. pair/list/frame identify an authenticated composed frame.
 * The caller retains the previous rendered frame on waiting/completion. */
int bc_turn_tick(BCTurnAnimation *turn,unsigned colour,BCSoundEvent sound,void *context);
#endif
