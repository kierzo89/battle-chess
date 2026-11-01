#ifndef BC_EVALUATION_H
#define BC_EVALUATION_H
#include "rules.h"
typedef struct {
 int16_t score, phase, endgame, total_material, pawn_material, material_balance;
 int16_t piece_square[2][6][120];
 uint16_t pawn_presence[2],pawn_doubled[2];
} BCEvaluation;
/* Recovered root evaluator, isolated per host thread. 'temporary' is original
 * evaluation-side context; caller must propagate it from the game/search state. */
void bc_evaluate(const BCPosition *position,unsigned temporary,BCEvaluation *out);
/* Search keeps root tables frozen and retains every pawn-mask row, including
 * scratch rows touched before the original evaluator copies parent state. */
typedef struct {
 BCEvaluation root;
 uint16_t pawn_state[26][2][2];
} BCSearchEvaluation;
void bc_search_evaluation_init(BCSearchEvaluation *state,const BCEvaluation *root);
bool bc_evaluate_delta(BCSearchEvaluation *state,BCMove move,unsigned side,
 unsigned ply,int16_t best,unsigned temporary,int16_t *delta);
#endif
