#include "motion.h"
#include "stage.h"
#include "geometry.h"
#include <string.h>
static int x(const BCMotion *m,unsigned square){int x=0,y=0;(void)bc_geometry_anchor(m->perspective,square,&x,&y);return x;}
static int y(const BCMotion *m,unsigned square){int x=0,y=0;(void)bc_geometry_anchor(m->perspective,square,&x,&y);return y;}
static void begin_segment(BCMotion *m){
 BCMove move=m->moves[m->index];m->frame=1;m->x=x(m,move.from);m->y=y(m,move.from);
 m->walking=m->perspective?bc_walk_sequence(move.kind,m->directions[m->index],0):NULL;
 memset(&m->clock,0,sizeof m->clock);
 if(m->walking){m->clock.control=m->walking->control;m->clock.length=m->walking->length;(void)bc_task_ready(&m->clock,false,0,m->sound,m->sound_context);}
}
static uint64_t revision;
static unsigned square(unsigned graphic){return (7-graphic/8)*16+graphic%8;}
static void fail(BCMotion *m){m->failed=true;m->active=false;m->visual_valid=false;}
static void pixel(BCMotion *m,const BCTurnSequence *s,unsigned frame){
 if(frame>=s->count||m->pixel_count>=128){fail(m);return;}
 m->pixels[m->pixel_count++]=(BCPixelEvent){s->pair,s->tokens[frame],frame==0};m->revision=++revision;
}
static bool next_command(BCMotion *m){
 m->walking=NULL;m->face=NULL;m->pixel_count=0;m->revision=++revision;
 while(m->pc<m->plan.count){
  BCStageCommand c=m->plan.commands[m->pc++];unsigned a=square(c.square),b=square(c.argument);
  if(c.operation==8)continue; /* Neighbour reactions remain a separate actor task. */
  if(c.operation==3){
   if(a!=b){m->display.cells[b]=m->display.cells[a];m->display.cells[a].kind=0;m->facing[b]=m->facing[a];}
   continue;
  }
  m->actor=a;m->operation=c.operation;m->frame=1;
  m->from_square=m->positions[a];m->to_square=b;m->x=x(m,m->from_square);m->y=y(m,m->from_square);
  unsigned kind=m->display.cells[a].kind;
  if(c.operation==1){
   m->walking=bc_walk_sequence(kind,m->facing[a],0);if(!m->walking){fail(m);return false;}
   m->clock=(BCTaskClock){.control=m->walking->control,.length=m->walking->length};
   (void)bc_task_ready(&m->clock,false,0,m->sound,m->sound_context);return true;
  }
  if(c.operation==2){
   if(!bc_turn_begin(&m->turn,kind,m->facing[a],c.argument,0)){fail(m);return false;}
   int result=bc_turn_tick(&m->turn,0,m->sound,m->sound_context);m->facing[a]=c.argument;
   if(result==2)continue;
   if(result!=1){fail(m);return false;}
   pixel(m,m->turn.sequence,m->turn.frame);return m->active;
  }
  if(c.operation==6&&kind==3){
   m->face=bc_face_sequence(c.argument);if(!m->face){fail(m);return false;}
   if(c.argument>1)m->facing[a]=m->x>160?7:3;else m->facing[a]=c.argument*4;
   pixel(m,m->face,0);return m->active;
  }
  fail(m);return false;
 }
 m->active=false;return false;
}
static void tick_commands(BCMotion *m){
 if(m->operation==2){
  int result=bc_turn_tick(&m->turn,0,m->sound,m->sound_context);
  if(result<0){fail(m);return;}
  if(result==0)return;
  if(result==1){pixel(m,m->turn.sequence,m->turn.frame);return;}
 }else if(m->operation==6){
  if(m->frame<m->face->count){pixel(m,m->face,m->frame++);return;}
 }else if(m->operation==1){
  if(!bc_task_ready(&m->clock,false,0,m->sound,m->sound_context))return;
  if(m->frame<m->walking->count){
   (void)bc_interpolate(x(m,m->from_square),y(m,m->from_square),x(m,m->to_square),y(m,m->to_square),m->walking->count,m->frame++,&m->x,&m->y);return;
  }
  m->positions[m->actor]=(uint8_t)m->to_square;m->index++;
 }
 (void)next_command(m);
}
bool bc_motion_begin_audio(BCMotion *m,const BCPosition *before,BCMove move,uint64_t tick,bool perspective,const uint8_t *facing,BCSoundEvent sound,void *context){
 uint8_t saved[120]={0};if(facing)memcpy(saved,facing,sizeof saved);
 memset(m,0,sizeof *m);m->perspective=perspective;m->sound=sound;m->sound_context=context;
 if(move.capture||(move.special&&move.kind>=2&&move.kind<=5)){
  if(!perspective)return false;
  m->battle_mode=true;m->last_tick=tick;
  m->active=bc_choreography_begin(&m->battle,before,move,facing?saved:NULL);
  m->battle.sound=sound;m->battle.sound_context=context;
  m->failed=!m->active;return m->active;
 }
 BCPosition verify=*before;if(!bc_play(&verify,move))return false;
 BCStagePlan plan;if(!bc_stage_plan(before,move,&plan))return false;
 if(perspective)for(unsigned i=0;i<plan.count;i++)if(plan.commands[i].operation==8){
  m->battle_mode=true;m->last_tick=tick;
  m->active=bc_choreography_begin(&m->battle,before,move,facing?saved:NULL);
  m->battle.sound=sound;m->battle.sound_context=context;
  m->failed=!m->active;return m->active;
 }
 m->plan=plan;m->display=before->board;m->visual_valid=true;
 for(unsigned sq=0;sq<120;sq++){
  m->positions[sq]=(uint8_t)sq;
  BCCell c=before->board.cells[sq];
  m->facing[sq]=(uint8_t)(facing?saved[sq]:bc_geometry_facing(c.kind,c.side,sq));
 }
 uint8_t position[120],directions[120]={0};
 for(unsigned i=0;i<120;i++)position[i]=(uint8_t)i;
 for(unsigned i=0;i<plan.count;i++){
  BCStageCommand c=plan.commands[i];
  unsigned source=((7-c.square/8)*16)+(c.square%8);
  if(c.operation==2)directions[source]=c.argument;
  if(c.operation!=1)continue;
  unsigned target=((7-c.argument/8)*16)+(c.argument%8);
  if(m->count>=32)return false;
  m->directions[m->count]=directions[source];
  m->origins[m->count]=(uint8_t)source;
  m->moves[m->count++]=(BCMove){position[source],target,0,before->board.cells[source].kind,0};
  position[source]=(uint8_t)target;
 }
 if(!m->count)return false;
 m->last_tick=tick;m->active=true;if(perspective)(void)next_command(m);else begin_segment(m);return !m->failed;
}
bool bc_motion_begin_facing(BCMotion *m,const BCPosition *before,BCMove move,uint64_t tick,bool perspective,const uint8_t *facing){return bc_motion_begin_audio(m,before,move,tick,perspective,facing,NULL,NULL);}
bool bc_motion_begin(BCMotion *m,const BCPosition *before,BCMove move,uint64_t tick,bool perspective){return bc_motion_begin_facing(m,before,move,tick,perspective,NULL);}
void bc_motion_tick(BCMotion *m,uint64_t tick,bool pending){
 if(!m->active||!bc_presentation_tick(tick,&m->last_tick,pending))return;
 if(m->battle_mode){
  int result=bc_choreography_tick(&m->battle);
  if(result!=0){m->active=false;m->failed=result<0;m->visual_valid=false;}
  return;
 }
 if(m->perspective){tick_commands(m);return;}
 BCMove move=m->moves[m->index];
 if(m->walking&&!bc_task_ready(&m->clock,false,0,m->sound,m->sound_context))return;
 unsigned frames=m->walking?m->walking->count:8;
 if(m->frame<frames){(void)bc_interpolate(x(m,move.from),y(m,move.from),x(m,move.to),y(m,move.to),frames,m->frame++,&m->x,&m->y);return;}
 /* Only a completed actor transfers occupancy. Intermediate waypoints can
  * cross occupied squares (knight); never erase an unrelated display piece. */
 unsigned origin=m->origins[m->index];
 if(m->index+1==m->count||m->origins[m->index+1]!=origin){
  m->display.cells[move.to]=m->display.cells[origin];m->display.cells[origin].kind=0;
 }
 if(++m->index==m->count){m->active=false;return;}
 begin_segment(m);
}
int bc_motion_hidden_square(const BCMotion *m){return m->active?(int)(m->perspective?m->actor:m->origins[m->index]):-1;}
BCCell bc_motion_piece(const BCMotion *m){return m->active?m->display.cells[bc_motion_hidden_square(m)]:(BCCell){0};}
