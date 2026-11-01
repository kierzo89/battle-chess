#include "search.h"
#include <assert.h>
#include <stdio.h>
int main(void){
 for(unsigned seed=1;seed<=3;seed++){
  BCGame *game=bc_game_create(NULL);assert(game);BCMove history[2048];size_t n=0;uint64_t nodes=0;
  BCSearchConfig c={.max_depth=2,.original_level=0,.seed=seed,.node_limit=100000};
  while(bc_game_status(game)==BC_PLAYING||bc_game_status(game)==BC_CHECK){
   assert(n<2048);assert(bc_game_copy_moves(game,history,n));c.temporary=bc_game_position(game)->board.side;
   BCSearchResult r;assert(bc_search(bc_game_position(game),history,n,&c,&r));
   assert(r.has_move&&!r.interrupted);assert(bc_game_move(game,r.move));nodes+=r.nodes;n++;
   if(bc_game_can_claim_draw(game))assert(bc_game_claim_draw(game));
  }
  printf("Full native selfplay seed %u: %zu plies, terminal status %d, %llu candidates\n",seed,n,bc_game_status(game),(unsigned long long)nodes);
  assert(n>12);bc_game_destroy(game);
 }
 return 0;
}
