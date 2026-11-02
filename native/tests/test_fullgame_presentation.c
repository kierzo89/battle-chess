#include "board_view.h"
#include "search.h"
#include "book.h"
#include "sound.h"
#include <SDL3/SDL.h>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static BCSoundBank sound_bank;static unsigned sounds;
static void sound(void *ctx,unsigned asset,unsigned colour,int pitch){
 (void)ctx;(void)colour;assert(asset<15&&bc_sound_frames(&sound_bank.slots[asset],pitch,48000)>0);sounds++;
}
int main(int argc,char **argv){
 assert(argc==3&&SDL_Init(SDL_INIT_VIDEO)&&bc_sound_load(&sound_bank,argv[2]));
 SDL_Window *window=SDL_CreateWindow("Full native game",1024,624,SDL_WINDOW_HIDDEN);assert(window);
 SDL_Renderer *renderer=SDL_CreateRenderer(window,NULL);assert(renderer);BCBoardView *view=bc_view_load(renderer,argv[1]);assert(view);
 BCGame *game=bc_game_create(NULL);assert(game);BCMotion *motion=calloc(1,sizeof *motion);assert(motion);
 BCMove history[1024];unsigned plies=0,captures=0,book_moves=0,frames=0;uint64_t tick=0;
 while(bc_game_status(game)==BC_PLAYING||bc_game_status(game)==BC_CHECK){
  assert(plies<1024&&bc_game_copy_moves(game,history,plies));BCPosition before=*bc_game_position(game);BCMove move;
  if(bc_book_move(&before,history,plies,0,&move))book_moves++;
  else {BCSearchConfig cfg={.max_depth=2,.seed=1,.node_limit=100000,.temporary=before.board.side};BCSearchResult r;assert(bc_search(&before,history,plies,&cfg,&r)&&r.has_move&&!r.interrupted);move=r.move;}
  bool retained=motion->visual_valid&&!memcmp(motion->display.cells,before.board.cells,sizeof before.board.cells);
  if(!bc_motion_begin_audio(motion,&before,move,tick,true,retained?motion->facing:NULL,sound,NULL)){
   fprintf(stderr,"Motion begin failed ply%u kind%u %u-%u capture%u special%u\n",plies,move.kind,move.from,move.to,move.capture,move.special);assert(0);
  }
  assert(bc_game_move(game,move));captures+=move.capture|| (move.special&&move.kind==6);plies++;
  unsigned calls=0;
  while(motion->active&&calls++<4000){
   tick+=2;bc_motion_tick(motion,tick,false);
   if(motion->failed){fprintf(stderr,"Motion failed ply%u kind%u %u-%u op%u\n",plies,move.kind,move.from,move.to,motion->operation);assert(0);}
   assert(SDL_SetRenderDrawColor(renderer,0,0,0,255)&&SDL_RenderClear(renderer));
   bc_view_draw(view,renderer,bc_game_position(game),motion,-1,true);assert(SDL_RenderPresent(renderer));frames++;
  }
  assert(!motion->active&&!motion->failed);
  if(bc_game_can_claim_draw(game))assert(bc_game_claim_draw(game));
 }
 assert(plies>12&&captures>0&&book_moves>0&&sounds>0);
 printf("PASS: complete rendered native game: %u plies, status%d, %u book moves, %u captures, %u animation dispatches, %u valid sound callbacks.\n",plies,bc_game_status(game),book_moves,captures,frames,sounds);
 bc_game_destroy(game);free(motion);bc_sound_destroy(&sound_bank);bc_view_destroy(view);SDL_DestroyRenderer(renderer);SDL_DestroyWindow(window);SDL_Quit();
}
