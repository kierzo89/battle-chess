#ifndef BC_CHOREOGRAPHY_H
#define BC_CHOREOGRAPHY_H
#include "commands.h"
#include "capture.h"
#include "placement.h"
#include "turn_animation.h"
#include "sidestep.h"
typedef struct {unsigned pair,token;bool initial;} BCActorPixel;
typedef enum {BC_ACTOR_STANDING,BC_ACTOR_WALK,BC_ACTOR_COMPOSED,BC_ACTOR_CAPTURE} BCActorImage;
typedef struct {
 BCCell piece;unsigned square,facing;int x,y,old_x,old_y;bool visible;
 BCActorImage image;unsigned pair,list,frame;
 BCActorPixel pixels[128];unsigned pixel_count;uint64_t revision;
} BCVisualActor;
typedef struct {
 unsigned actor,operation,frame;int remove_actor,from_x,from_y,to_x,to_y;
 const BCWalk *walk;const BCTurnSequence *face;BCTaskClock clock;
 BCSidestep sidestep;BCTurnAnimation turn;BCPlacement placement;BCCapture capture;
} BCActorTask;
typedef struct {
 BCCommands commands;BCVisualActor actors[32];unsigned count;
 int actor_map[120];BCActorTask tasks[4];BCCaptureSync capture;
 unsigned attacker_kind,victim_kind,promotion_kind,promotion_square;bool done,failed;
 uint64_t revision;BCSoundEvent sound;void *sound_context;
} BCChoreography;
/* Native task composition. Does not mutate authoritative chess state.
 * Neighbour op8 retains its actor frame while changing position. */
bool bc_choreography_begin(BCChoreography *,const BCPosition *,BCMove,const uint8_t *facing);
/* One eligible original dispatch. -1 failure,0 running,1 complete. */
int bc_choreography_tick(BCChoreography *);
#endif
