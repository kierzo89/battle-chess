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
typedef struct { int mask, step; } Ray;
extern Ray rays[];

extern void fill_8a96();

void init_rays()
{
    int direction_index, j;
    register Ray *entry;
    fill_8a96(rays, 956, 0);
    for (direction_index = 7; direction_index >= 0; --direction_index) {
        for (j = 1; j <= 7; ++j) {
            entry = &rays[move_lookup_tables.ray_step[direction_index] * j + 119];
            if (direction_index < 4)
                entry->mask = move_lookup_tables.pawn_and_masks.masks.by_kind[2] + move_lookup_tables.pawn_and_masks.masks.by_kind[3];
            else
                entry->mask = move_lookup_tables.pawn_and_masks.masks.by_kind[2] + move_lookup_tables.pawn_and_masks.masks.by_kind[4];
            entry->step = move_lookup_tables.ray_step[direction_index];
        }
        rays[move_lookup_tables.ray_step[direction_index] + 119].mask += move_lookup_tables.pawn_and_masks.masks.by_kind[1];
        rays[move_lookup_tables.knight_step[direction_index] + 119].mask = move_lookup_tables.pawn_and_masks.masks.by_kind[5];
        rays[move_lookup_tables.knight_step[direction_index] + 119].step = move_lookup_tables.knight_step[direction_index];
    }
}
