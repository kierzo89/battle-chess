#include "choreography.h"
#include "geometry.h"
#include <string.h>
static unsigned square(unsigned s){return (7-s/8)*16+s%8;}
static bool pixel(BCChoreography *g,BCVisualActor *a,const BCTurnSequence *s,unsigned frame){
 if(frame>=s->count||a->pixel_count>=128)return false;
 a->pixels[a->pixel_count++]=(BCActorPixel){s->pair,s->tokens[frame],frame==0};
 a->image=BC_ACTOR_COMPOSED;a->revision=++g->revision;return true;
}
static void walking(BCChoreography *g,BCVisualActor *a,const BCWalk *w,unsigned frame){
 a->image=BC_ACTOR_WALK;a->pair=w->pair;a->list=w->list;a->frame=frame;a->revision=++g->revision;
}
static bool start(void *ctx,unsigned slot,unsigned command,const BCStageCommand *c){
 BCChoreography *g=ctx;(void)command;unsigned source=square(c->square),target=square(c->argument);
 int id=g->actor_map[source];if(id<0||id>=(int)g->count)return false;
 BCVisualActor *a=&g->actors[id];BCActorTask *t=&g->tasks[slot];memset(t,0,sizeof *t);
 t->actor=(unsigned)id;t->operation=c->operation;t->remove_actor=-1;
 switch(c->operation){
 case 1:
  t->walk=bc_walk_sequence(a->piece.kind,a->facing,0);if(!t->walk)return false;
  if(!bc_geometry_anchor(true,a->square,&t->from_x,&t->from_y)||!bc_geometry_anchor(true,target,&t->to_x,&t->to_y))return false;
  a->square=target;t->clock=(BCTaskClock){.control=t->walk->control,.length=t->walk->length};return true;
 case 2:
  if(!bc_turn_begin(&t->turn,a->piece.kind,a->facing,c->argument,0))return false;
  a->facing=c->argument;return true;
 case 3:
  if(source!=target){
   if(g->capture.pending){t->remove_actor=g->actor_map[target];g->capture.pending=0;}
   g->actor_map[target]=id;g->actor_map[source]=-1;
  }
  return true;
 case 4: {
  static const int dx[]={0,19,19,19,0,-19,-19,-19},dy[]={-9,-9,0,9,9,9,0,-9};
  if(c->argument>7)return false;
  return bc_placement_begin(&t->placement,BC_EFFECT,a->piece.kind,a->facing,0,a->old_x,a->old_y,a->old_x+dx[c->argument],a->old_y+dy[c->argument],false);
 }
 case 5: {
  if(c->argument>1)return false;
  unsigned opponent=c->argument?g->victim_kind:g->attacker_kind;
  return bc_capture_begin(&t->capture,&g->capture,c->argument,a->piece.kind,opponent,0,false);
 }
 case 6:
  if(a->piece.kind!=3)return false;
  t->face=bc_face_sequence(c->argument);if(!t->face)return false;
  a->facing=c->argument>1?(a->x>160?7:3):c->argument*4;return true;
 case 7: {
  if(!c->extra_known||c->extra>2||!bc_geometry_anchor(true,target,&t->to_x,&t->to_y))return false;
  a->square=target;bool full=false;
  if(c->extra==1){t->to_x+=9;t->to_y-=5;full=a->facing>=4&&a->facing<=6;}
  else if(c->extra==0){t->to_x-=9;t->to_y+=5;}
  return bc_placement_begin(&t->placement,full?BC_OFFSET_FULL:BC_OFFSET_HALF,a->piece.kind,a->facing,0,a->old_x,a->old_y,t->to_x,t->to_y,false);
 }
 default:return false;
 }
}
static int step(void *ctx,unsigned slot,unsigned command,const BCStageCommand *c){
 BCChoreography *g=ctx;(void)command;(void)c;BCActorTask *t=&g->tasks[slot];BCVisualActor *a=&g->actors[t->actor];unsigned colour=a->piece.side?64:0;
 switch(t->operation){
 case 1:
  if(!bc_task_ready(&t->clock,false,colour,g->sound,g->sound_context))return t->clock.failed?-1:0;
  if(t->frame==t->walk->count){a->old_x=t->to_x;a->old_y=t->to_y;return 1;}
  if(!bc_interpolate(t->from_x,t->from_y,t->to_x,t->to_y,t->walk->count,t->frame,&a->x,&a->y))return -1;
  walking(g,a,t->walk,t->frame++);return 0;
 case 2: {
  int r=bc_turn_tick(&t->turn,colour,g->sound,g->sound_context);
  if(r<0)return -1;
  if(r==2)return 1;
  if(r==1){if(!t->frame++)a->pixel_count=0;if(!pixel(g,a,t->turn.sequence,t->turn.frame))return -1;a->x=a->old_x;a->y=a->old_y;}
  return 0;
 }
 case 3:
  a->x=a->old_x;a->y=a->old_y;a->image=BC_ACTOR_STANDING;a->revision=++g->revision;
  if(t->remove_actor>=0)g->actors[t->remove_actor].visible=false;
  return 1;
 case 4:case 7: {
  int r=bc_placement_tick(&t->placement,colour,g->sound,g->sound_context);if(r<0)return -1;
  if(r==1){walking(g,a,t->placement.sequence,t->placement.frame);a->x=t->placement.x;a->y=t->placement.y;a->old_x=t->placement.anchor_x;a->old_y=t->placement.anchor_y;}
  return t->placement.done?1:0;
 }
 case 5: {
  BCCaptureFrame f;int r=bc_capture_tick(&t->capture,&g->capture,colour,g->sound,g->sound_context,&f);
  if(r<0)return -1;
  if(r==2)return 1;
  if(r==1){a->image=BC_ACTOR_CAPTURE;a->pair=f.pair;a->list=f.list;a->frame=f.step;a->revision=++g->revision;}
  return 0;
 }
 case 6:
  if(!t->frame)a->pixel_count=0;
  if(!pixel(g,a,t->face,t->frame++))return -1;
  a->x=a->old_x;a->y=a->old_y;return t->frame==t->face->count;
 default:return -1;
 }
}
bool bc_choreography_begin(BCChoreography *g,const BCPosition *p,BCMove move,const uint8_t *facing){
 if(!g||!p)return false;
 memset(g,0,sizeof *g);for(unsigned s=0;s<120;s++)g->actor_map[s]=-1;
 BCStagePlan plan;if(!bc_stage_plan(p,move,&plan)){g->failed=true;return false;}
 /* Fail before any actor work if the remaining neighbour handler is required. */
 for(unsigned i=0;i<plan.count;i++)if(plan.commands[i].operation==8){g->failed=true;return false;}
 for(unsigned s=0;s<120;s++)if(!(s&0x88)&&p->board.cells[s].kind){
  if(g->count==32){g->failed=true;return false;}
  BCVisualActor *a=&g->actors[g->count];a->piece=p->board.cells[s];a->square=s;a->visible=true;
  a->facing=facing?facing[s]:bc_geometry_facing(a->piece.kind,a->piece.side,s);
  (void)bc_geometry_anchor(true,s,&a->x,&a->y);a->old_x=a->x;a->old_y=a->y;g->actor_map[s]=(int)g->count++;
 }
 g->attacker_kind=move.kind;g->victim_kind=move.capture;
 if(!bc_commands_begin(&g->commands,&plan,start,g)){g->failed=true;return false;}return true;
}
int bc_choreography_tick(BCChoreography *g){
 if(!g||g->failed)return -1;
 int r=bc_commands_tick(&g->commands,start,step,g);
 if(r<0)g->failed=true;else if(r==1)g->done=true;return r;
}
