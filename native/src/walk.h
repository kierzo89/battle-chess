#ifndef BC_WALK_H
#define BC_WALK_H
#include "presentation.h"
typedef struct {const uint8_t *control;unsigned length,pair,list,count;} BCWalk;
/* Engine kind -> graphics bank, orientation and native control profile. */
const BCWalk *bc_walk_sequence(unsigned kind,unsigned orientation,unsigned profile);
#endif
