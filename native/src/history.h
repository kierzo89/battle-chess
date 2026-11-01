#ifndef BC_HISTORY_H
#define BC_HISTORY_H
#include "rules.h"
/* Original search predicates. moves[0] is earliest, no caller sentinel needed. */
unsigned bc_original_quiet_count(const BCMove *moves,size_t count);
unsigned bc_original_repetitions(const BCMove *moves,size_t count,bool required);
typedef struct BCGame BCGame;
typedef enum {BC_PLAYING,BC_CHECK,BC_CHECKMATE,BC_STALEMATE,BC_DEAD_MATERIAL,
 BC_DRAW_CLAIMED,BC_DRAW_FIVEFOLD,BC_DRAW_SEVENTYFIVE} BCGameStatus;
BCGame *bc_game_create(const BCPosition *start);
void bc_game_destroy(BCGame *game);
const BCPosition *bc_game_position(const BCGame *game);
const BCPosition *bc_game_initial_position(const BCGame *game);
size_t bc_game_plies(const BCGame *game);
bool bc_game_copy_moves(const BCGame *game,BCMove *out,size_t capacity);
bool bc_game_move(BCGame *game,BCMove move);
bool bc_game_undo(BCGame *game);
unsigned bc_game_repetitions(const BCGame *game);
BCGameStatus bc_game_status(const BCGame *game);
bool bc_game_can_claim_draw(const BCGame *game);
bool bc_game_claim_draw(BCGame *game);
#endif
