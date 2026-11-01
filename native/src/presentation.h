#ifndef BC_PRESENTATION_H
#define BC_PRESENTATION_H
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
typedef void (*BCSoundEvent)(void *context,unsigned asset,unsigned colour,int pitch);
typedef struct {
 const uint8_t *control;size_t length,cursor;
 uint8_t wait;bool failed;
} BCTaskClock;
/* One eligible task dispatch, not one wall-clock frame. FF remains ready. */
bool bc_task_ready(BCTaskClock *clock,bool tilted,unsigned colour,BCSoundEvent event,void *context);
/* Recovered signed rounding, for coordinates in [-1024,1024] and 1..128 steps. */
bool bc_interpolate(int x,int y,int to_x,int to_y,unsigned steps,unsigned step,int *out_x,int *out_y);
/* Original two-BIOS-tick fallback: queued input suppresses fallback; late polls
 * set last=now, never issue catch-up frames. Caller supplies unwrapped ticks. */
bool bc_presentation_tick(uint64_t now,uint64_t *last,bool input_pending);
#endif
