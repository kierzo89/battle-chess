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
extern unsigned char huge buffer_70000[70000L];
extern unsigned char huge buffer_150000[150000L];
int main(void)
{
    unsigned char huge *p;
    if (move_lookup_tables.knight_step[7] != -33) return 1;
    buffer_70000[65535L] = 18;
    buffer_70000[65536L] = 52;
    buffer_70000[69999L] = 86;
    buffer_150000[65535L] = 120;
    buffer_150000[65536L] = 154;
    buffer_150000[149999L] = 188;
    p = buffer_70000 + 65535L;
    if (*p++ != 18 || *p != 52 || buffer_70000[69999L] != 86) return 2;
    p = buffer_150000 + 65535L;
    if (*p++ != 120 || *p != 154 || buffer_150000[149999L] != 188) return 3;
    return 0;
}
