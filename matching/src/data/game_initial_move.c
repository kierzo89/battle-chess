/* Canonical empty move copied into both search slots at all 24 depths.
   Square 8 is outside the playable 0x88 board; kind/capture are empty. */
typedef union { unsigned word; struct { unsigned char kind, capture; } bytes; } MoveKind;
typedef struct { int to, from, flag; MoveKind detail; } Move;
Move initial_move = { 8, 8, 0, { 0 } };
