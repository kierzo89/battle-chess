#ifndef BC_CAPTURE_H
#define BC_CAPTURE_H
#include "presentation.h"
typedef struct {unsigned pair,list,step;} BCCaptureFrame;
typedef struct {const uint8_t *control;unsigned length,count;const BCCaptureFrame *frames;} BCCaptureSequence;
/* Engine kinds1..6; side0 is original left (victim), side1 right (attacker). */
const BCCaptureSequence *bc_capture_sequence(unsigned side,unsigned kind,unsigned opponent,unsigned profile);
typedef struct {unsigned pending,animation_counter,registered;bool cleanup;} BCCaptureSync;
typedef struct {
 const BCCaptureSequence *sequence;BCTaskClock clock;
 unsigned cursor,side;bool terminal,done,failed,command_active;
} BCCapture;
bool bc_capture_begin(BCCapture *task,BCCaptureSync *sync,unsigned side,unsigned kind,unsigned opponent,unsigned profile,bool command_active);
/* Eligible native task invocation: -1 invalid,0 waiting,1 new frame,2 done.
 * Both actors share sync. Each must be ticked until done; neither can finish
 * until both report sequence exhaustion. No game-board mutation here. */
int bc_capture_tick(BCCapture *task,BCCaptureSync *sync,unsigned colour,BCSoundEvent sound,void *context,BCCaptureFrame *frame);
#endif
