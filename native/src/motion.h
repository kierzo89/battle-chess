#ifndef BC_MOTION_H
#define BC_MOTION_H
#include "presentation.h"
#include "rules.h"
typedef struct {
 BCBoard display;BCMove moves[32];uint8_t origins[32];unsigned count,index,frame;
 bool active,perspective;int x,y;uint64_t last_tick;
} BCMotion;
/* Original command-active (static-sprite) move task: eight emitted positions,
 * then completion. Captures stay outside this adapter until the battle task
 * executor is connected. Authoritative chess state is never modified here. */
bool bc_motion_begin(BCMotion *motion,const BCPosition *before,BCMove move,uint64_t tick,bool perspective);
void bc_motion_tick(BCMotion *motion,uint64_t tick,bool input_pending);
int bc_motion_hidden_square(const BCMotion *motion);
BCCell bc_motion_piece(const BCMotion *motion);
#endif
