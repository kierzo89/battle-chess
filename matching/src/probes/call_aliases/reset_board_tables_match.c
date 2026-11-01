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

extern MoveLookupTables move_lookup_tables;
extern void clear_board(), set_cell_bytes(), init_pieces();
extern int side, opposite_side;

void reset_board()
{
    int i;
    clear_board();
    i = 0;
    do {
        set_cell_bytes(move_lookup_tables.back_rank[i], 0, i);
        set_cell_bytes(6, 0, i + 16);
        set_cell_bytes(6, 1, i + 96);
        set_cell_bytes(move_lookup_tables.back_rank[i], 1, i + 112);
        ++i;
    } while (i <= 7);
    init_pieces();
    side = 0;
    opposite_side = 1;
}
