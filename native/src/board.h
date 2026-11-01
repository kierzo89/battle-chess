#ifndef BC_BOARD_H
#define BC_BOARD_H
#include <stdbool.h>
#include <stdint.h>
/* Original DOS cell layout: two bytes followed by a signed 16-bit index. */
typedef struct { uint8_t kind, side; int16_t index; } BCCell;
typedef struct { uint8_t square, kind; } BCPiece;
typedef struct {
 BCCell cells[120];
 BCPiece pieces[2][16];
 int16_t last_piece[2], last_nonpawn[2];
 uint8_t side;
} BCBoard;
typedef struct { uint8_t from, to, special, kind, capture; } BCMove;
bool bc_unpack(BCBoard *board, const uint8_t data[33]);
void bc_pack(const BCBoard *board, uint8_t data[33]);
void bc_initial(BCBoard *board);
/* Caller must supply a legal move. This is original state mutation, not legality. */
void bc_apply(BCBoard *board, BCMove move, bool undo);
#endif
