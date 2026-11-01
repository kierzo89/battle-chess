#include "evaluation.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
int main(void) {
 BCPosition p;bc_position_initial(&p);BCEvaluation a,b;
 bc_evaluate(&p,0,&a);
 printf("Initial: score=%d material=%d pawn=%d phase=%d\n",a.score,a.total_material,a.pawn_material,a.phase);
 assert(a.total_material==2*(2304+2*1216+4*768+8*256));
 assert(a.pawn_material==4096&&a.material_balance==0);
 assert(a.pawn_presence[0]==255&&a.pawn_presence[1]==255);
 assert(!a.pawn_doubled[0]&&!a.pawn_doubled[1]);
 assert(a.score==0);
 unsigned seed=1988;
 for(unsigned i=0;i<100;i++) {
  bc_evaluate(&p,0,&a);
  BCPosition opposite=p;opposite.board.side^=1;bc_evaluate(&opposite,0,&b);
  assert(a.score==-b.score);
  assert(!memcmp(a.piece_square,b.piece_square,sizeof a.piece_square));
  BCEvaluation repeat;bc_evaluate(&p,0,&repeat);assert(repeat.score==a.score);
  BCMoveList list;bc_generate_legal(&p,&list);if(!list.count)break;
  seed=1664525u*seed+1013904223u;bc_play_unchecked(&p,list.moves[seed%list.count]);
 }
 puts("PASS: recovered evaluation tables, material, perspective and deterministic replay.");
}
