#include "history.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
static BCMove select_move(const BCPosition *p,unsigned from,unsigned to) {
 BCMoveList list;bc_generate_legal(p,&list);
 for(size_t i=0;i<list.count;i++)if(list.moves[i].from==from&&list.moves[i].to==to)return list.moves[i];
 assert(!"missing move");return (BCMove){0};
}
int main(void) {
 BCGame *g=bc_game_create(NULL);assert(g);
 BCPosition initial=*bc_game_position(g);
 BCMove moves[20];unsigned n=0;
 unsigned from[]={6,118,37,85},to[]={37,85,6,118};
 for(unsigned cycle=0;cycle<4;cycle++) {
  for(unsigned i=0;i<4;i++) {
   BCMove m=select_move(bc_game_position(g),from[i],to[i]);moves[n++]=m;
   assert(bc_game_move(g,m));
  }
  assert(bc_game_repetitions(g)==cycle+2);
  assert(bc_original_repetitions(moves,n,false)==cycle+2);
  assert(bc_original_repetitions(moves,n,true)==2);
  if(cycle==0)assert(!bc_game_can_claim_draw(g));
  if(cycle==1) {
   assert(bc_game_can_claim_draw(g));assert(bc_game_claim_draw(g));assert(bc_game_status(g)==BC_DRAW_CLAIMED);
   assert(!bc_game_move(g,moves[0]));assert(bc_game_undo(g));assert(bc_game_plies(g)==8);
  }
 }
 assert(bc_game_status(g)==BC_DRAW_FIVEFOLD);assert(bc_original_quiet_count(moves,n)==16);
 for(unsigned i=0;i<16;i++)assert(bc_game_undo(g));
 assert(!memcmp(&initial,bc_game_position(g),sizeof initial));assert(!bc_game_undo(g));
 BCMove illegal={0,0,0,3,0};assert(!bc_game_move(g,illegal));assert(!bc_game_plies(g));
 BCMove pawn=select_move(bc_game_position(g),20,52);assert(bc_game_move(g,pawn));assert(bc_game_position(g)->halfmove==0);
 moves[n++]=pawn;assert(bc_original_quiet_count(moves,n)==0);assert(bc_original_repetitions(moves,n,false)==1);
 bc_game_destroy(g);
 initial.halfmove=99;g=bc_game_create(&initial);assert(g);
 assert(bc_game_move(g,select_move(bc_game_position(g),6,37)));assert(bc_game_can_claim_draw(g));bc_game_destroy(g);
 initial.halfmove=149;g=bc_game_create(&initial);assert(g);
 assert(bc_game_move(g,select_move(bc_game_position(g),6,37)));assert(bc_game_status(g)==BC_DRAW_SEVENTYFIVE);bc_game_destroy(g);
 g=bc_game_create(NULL);assert(g);initial=*bc_game_position(g);unsigned seed=2026;
 for(unsigned i=0;i<100;i++) {
  BCGameStatus status=bc_game_status(g);if(status!=BC_PLAYING&&status!=BC_CHECK)break;
  BCMoveList list;bc_generate_legal(bc_game_position(g),&list);assert(list.count);
  seed=1664525u*seed+1013904223u;assert(bc_game_move(g,list.moves[seed%list.count]));
 }
 assert(bc_game_plies(g)>32);while(bc_game_undo(g)){}
 assert(!memcmp(&initial,bc_game_position(g),sizeof initial));bc_game_destroy(g);
 puts("PASS: original repetition/quiet scan, complete undo, draw claims and automatic limits.");
}
