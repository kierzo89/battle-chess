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

typedef struct { unsigned char kind, side; int index; } Cell;
typedef struct { unsigned mask; int step; } Ray;
extern Cell board[];
extern Ray rays[];

extern int abs_i16();

int piece_attacks(kind,side,origin,target)
int kind,side,origin,target;
{
    register Ray *ray;
    int square;
    int result;
    if (kind == 6)
        result = abs_i16(target - move_lookup_tables.pawn_and_masks.initialized.pawn_step[side] - origin) == 1;
    else {
        ray = &rays[target - origin + 119];
        if (ray->mask & move_lookup_tables.pawn_and_masks.masks.by_kind[kind]) {
            if ((kind == 1) | (kind == 5))
                result = 1;
            else {
                square = origin;
                do {
                    square += ray->step;
                } while (square != target && board[square].kind == 0);
                result = square == target;
            }
        } else
            result = 0;
    }
    return result;
}

int pawn_attacks(side,target)
int side,target;
{
    register Cell *node;
    int square;
    square = target - move_lookup_tables.pawn_and_masks.initialized.pawn_step[side] - 1;
    node = board + square;
    if (!(square & 136) && ((node->kind == 6) & (node->side == side)))
        return 1;
    square += 2;
    node += 2;
    if (!(square & 136) && ((node->kind == 6) & (node->side == side)))
        return 1;
    return 0;
}
