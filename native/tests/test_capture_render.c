#include "board_view.h"
#include <SDL3/SDL.h>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
static BCMove pick(BCPosition *p,unsigned from,unsigned to){BCMoveList l;bc_generate_legal(p,&l);for(size_t i=0;i<l.count;i++)if(l.moves[i].from==from&&l.moves[i].to==to)return l.moves[i];assert(0);return (BCMove){0};}
int main(int argc,char **argv){
 assert(argc==2&&SDL_Init(SDL_INIT_VIDEO));SDL_Window *w=SDL_CreateWindow("Capture proof",1024,624,SDL_WINDOW_HIDDEN);assert(w);
 SDL_Renderer *r=SDL_CreateRenderer(w,NULL);assert(r);BCBoardView *v=bc_view_load(r,argv[1]);assert(v);
 BCPosition p;bc_position_initial(&p);assert(bc_play(&p,pick(&p,20,52)));assert(bc_play(&p,pick(&p,99,67)));BCMove move=pick(&p,52,67);
 BCMotion *m=calloc(1,sizeof *m);assert(m&&bc_motion_begin(m,&p,move,0,true)&&m->battle_mode);assert(bc_play(&p,move));
 unsigned ticks=0,battle_frames=0;
 while(m->active&&ticks<4000){
  ticks+=2;bc_motion_tick(m,ticks,false);assert(!m->failed);
  SDL_SetRenderDrawColor(r,22,26,32,255);assert(SDL_RenderClear(r));bc_view_draw(v,r,&p,m,-1,true);
  unsigned count=0;for(unsigned i=0;i<m->battle.count;i++)count+=m->battle.actors[i].visible&&m->battle.actors[i].image==BC_ACTOR_CAPTURE;
  if(count==2&&++battle_frames==10&&getenv("BC_CAPTURE_SCREENSHOT")){
   SDL_Surface *s=SDL_RenderReadPixels(r,NULL);assert(s&&SDL_SaveBMP(s,getenv("BC_CAPTURE_SCREENSHOT")));SDL_DestroySurface(s);
  }
  assert(SDL_RenderPresent(r));
 }
 assert(!m->active&&m->battle.done&&battle_frames>10);
 free(m);bc_view_destroy(v);SDL_DestroyRenderer(r);SDL_DestroyWindow(w);SDL_Quit();
 printf("PASS: visible two-actor capture rendered across %u dispatches (%u battle frames), clean completion.\n",ticks/2,battle_frames);
}
