#include "evaluation.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
int main(void) {
 BCPosition p;bc_position_initial(&p);BCEvaluation root;bc_evaluate(&p,0,&root);
 BCSearchEvaluation state;bc_search_evaluation_init(&state,&root);
 int16_t delta;
 assert(bc_evaluate_delta(&state,(BCMove){20,52,0,6,0},0,0,0,0,&delta));
 assert(delta==root.piece_square[0][5][52]-root.piece_square[0][5][20]);
 assert(state.pawn_state[1][0][0]==255&&state.pawn_state[1][1][0]==255);
 BCSearchEvaluation before=state;
 assert(!bc_evaluate_delta(&state,(BCMove){20,52,0,6,0},0,24,0,0,&delta));
 assert(!memcmp(&before,&state,sizeof state));
 assert(!bc_evaluate_delta(&state,(BCMove){4,0,1,1,0},0,0,0,0,&delta));
 assert(!bc_evaluate_delta(&state,(BCMove){17,0,1,6,0},0,0,0,0,&delta));
 assert(!memcmp(&before,&state,sizeof state));
 /* Raw original routines evaluate move records, not legality. Synthetic capture
  * here checks fixed-root material arithmetic and preserved input state. */
 bc_search_evaluation_init(&state,&root);
 assert(bc_evaluate_delta(&state,(BCMove){6,37,0,5,3},0,0,0,0,&delta));
 assert(delta==1216+root.piece_square[1][2][37]+root.piece_square[0][4][37]-root.piece_square[0][4][6]);
 assert(!memcmp(&root,&state.root,sizeof root));
 puts("PASS: original incremental evaluation adapter, frozen tables and bounded scratch history.");
}
