#include "audio_output.h"
#include "motion.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
static BCMove pick(BCPosition *p,unsigned from,unsigned to){BCMoveList l;bc_generate_legal(p,&l);for(size_t i=0;i<l.count;i++)if(l.moves[i].from==from&&l.moves[i].to==to)return l.moves[i];assert(0);return (BCMove){0};}
int main(int argc,char **argv){
 assert(argc==2);BCAudio a;assert(bc_audio_open(&a,argv[1]));bc_audio_pause(&a,true);
 bc_audio_event(&a,0,64,0);assert(a.accepted==1&&bc_audio_busy(&a));
 bc_audio_event(&a,15,0,-18);bc_audio_event(&a,11,0,-64);assert(a.rejected==2);
 bc_audio_mute(&a,true);assert(!bc_audio_busy(&a)&&SDL_GetAudioStreamQueued(a.stream)==0);
 bc_audio_event(&a,0,0,0);assert(a.accepted==1);bc_audio_mute(&a,false);
 BCPosition p;bc_position_initial(&p);assert(bc_play(&p,pick(&p,20,52)));assert(bc_play(&p,pick(&p,99,67)));
 BCMotion *m=calloc(1,sizeof *m);assert(m&&bc_motion_begin_audio(m,&p,pick(&p,52,67),0,true,NULL,bc_audio_event,&a));
 for(unsigned tick=2;m->active&&tick<2000&&a.accepted==1;tick+=2)bc_motion_tick(m,tick,false);
 assert(a.accepted>1&&bc_audio_busy(&a)&&!m->failed);free(m);bc_audio_clear(&a);
 bc_audio_event(&a,0,0,0);bc_audio_pause(&a,false);uint64_t start=SDL_GetTicks();
 while(bc_audio_busy(&a)&&SDL_GetTicks()-start<3000)SDL_Delay(10);
 assert(!bc_audio_busy(&a));bc_audio_close(&a);assert(!a.stream&&!a.initialized);
 puts("PASS: SDL stream output/drain, real capture-event connection, mute/clear/pause/close and explicit unsupported-event rejection.");
}
