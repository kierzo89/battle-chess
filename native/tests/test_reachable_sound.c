#include "sound.h"
#include "capture.h"
#include "walk.h"
#include "turn_animation.h"
#include <assert.h>
#include <stdio.h>
static BCSoundBank bank;static unsigned events;static bool pairs[15][128];
static void sound(void *ctx,unsigned asset,unsigned colour,int pitch){
 (void)ctx;(void)colour;assert(asset<15&&pitch>=-64&&pitch<=63);
 size_t frames=bc_sound_frames(&bank.slots[asset],pitch,48000);
 if(!frames)fprintf(stderr,"Unrenderable active sound: %u/%d\n",asset,pitch);
 assert(frames>0&&frames<=480000);events++;pairs[asset][pitch+64]=true;
}
int main(int argc,char **argv){
 assert(argc==2&&bc_sound_load(&bank,argv[1]));unsigned battles=0,walks=0,turns=0;
 /* Left actor is the victim. Legal chess never captures engine kind1 (king).
  * Live choreography uses profile0 for both actors, including en passant. */
 for(unsigned attacker=1;attacker<=6;attacker++)for(unsigned victim=2;victim<=6;victim++){
  BCCaptureSync sync={0};BCCapture a,b;assert(bc_capture_begin(&a,&sync,0,victim,attacker,0,false));assert(bc_capture_begin(&b,&sync,1,attacker,victim,0,false));
  unsigned tick=0;while((!a.done||!b.done)&&tick++<3000){BCCaptureFrame f;assert(bc_capture_tick(&a,&sync,0,sound,NULL,&f)>=0);assert(bc_capture_tick(&b,&sync,64,sound,NULL,&f)>=0);}
  assert(a.done&&b.done);battles++;
 }
 for(unsigned kind=1;kind<=6;kind++)for(unsigned from=0;from<8;from++){
  const BCWalk *w=bc_walk_sequence(kind,from,0);assert(w);BCTaskClock c={.control=w->control,.length=w->length};
  unsigned ready=0,ticks=0;while(ready<=w->count&&ticks++<3000){ready+=bc_task_ready(&c,false,0,sound,NULL);assert(!c.failed);}assert(ready>w->count);walks++;
  for(unsigned to=0;to<8;to++){BCTurnAnimation t;if(!bc_turn_begin(&t,kind,from,to,0))continue;
   unsigned ticks=0;while(!t.done&&ticks++<3000)assert(bc_turn_tick(&t,0,sound,NULL)>=0);assert(t.done);turns++;
  }
 }
 unsigned distinct=0;for(unsigned a=0;a<15;a++)for(unsigned p=0;p<128;p++)distinct+=pairs[a][p];
 bc_sound_destroy(&bank);printf("PASS: %u legal capture pairings, %u walking orientations, %u valid turns: %u callbacks / %u distinct active sound pairs, all bounded and renderable.\n",battles,walks,turns,events,distinct);
}
