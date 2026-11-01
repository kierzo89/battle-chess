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
#endif
