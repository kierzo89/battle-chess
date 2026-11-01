/* 0x88 board movement, attack-bit, castling and initial piece tables.
   The mask view starts one word into the pawn/mask union: mask zero shares
   the negative pawn step and is unused by the reconstructed consumers. */
typedef struct { int destination, king_home; } CastleEndpoints;
typedef union {
    struct { int pawn_step[2]; unsigned piece_bits[6]; } initialized;
    struct { int first_pawn_step; unsigned by_kind[7]; } masks;
} PawnAndMasks;
typedef struct {
    int ray_step[8];
    int knight_step[8];
    PawnAndMasks pawn_and_masks;
    CastleEndpoints castle[2][2];
    int back_rank[8];
} MoveLookupTables;
MoveLookupTables move_lookup_tables = {
    { 1, -1, 16, -16, 17, -17, 15, -15 },
    { 14, -14, 18, -18, 31, -31, 33, -33 },
    { { { 16, -16 }, { 1, 2, 4, 8, 16, 32 } } },
    { { { 2, 4 }, { 6, 4 } }, { { 114, 116 }, { 118, 116 } } },
    { 3, 5, 4, 2, 1, 4, 5, 3 }
};
