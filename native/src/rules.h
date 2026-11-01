#ifndef BC_RULES_H
#define BC_RULES_H
#include "board.h"
#include <stddef.h>
/* Host-side turn/history context; board remains original 0x88 representation. */
typedef struct {
 BCBoard board;
 uint8_t castle[2]; /* original bits: queen-side=1, king-side=2 */
 int16_t ep; /* -1 or a valid empty en-passant destination */
 unsigned halfmove,fullmove;
} BCPosition;
typedef struct { BCMove moves[256]; size_t count; } BCMoveList;
void bc_position_initial(BCPosition *p);
bool bc_piece_attacks(const BCBoard *b,unsigned kind,unsigned side,int from,int to);
bool bc_attacked(const BCBoard *b,unsigned side,int target);
bool bc_in_check(const BCBoard *b,unsigned side);
void bc_generate_legal(const BCPosition *p,BCMoveList *moves);
/* Moves from bc_generate_legal only. Whole-position copies provide lossless undo. */
void bc_play_unchecked(BCPosition *p,BCMove move);
bool bc_play(BCPosition *p,BCMove move);
uint64_t bc_perft(const BCPosition *p,unsigned depth);
#endif
