typedef struct { int mask, step; } Ray;
extern Ray rays[];
extern int steps[], knight_steps[], masks[];
extern void fill_8a96();

void init_rays()
{
    /* The original frame reserves an otherwise unused two-byte slot. */
    int direction_index, j, unused;
    Ray *entry;
    fill_8a96(rays, 956, 0);
    for (direction_index = 7; direction_index >= 0; --direction_index) {
        for (j = 1; j <= 7; ++j) {
            entry = &rays[steps[direction_index] * j + 119];
            if (direction_index < 4)
                entry->mask = masks[2] + masks[3];
            else
                entry->mask = masks[2] + masks[4];
            entry->step = steps[direction_index];
        }
        rays[steps[direction_index] + 119].mask += masks[1];
        rays[knight_steps[direction_index] + 119].mask = masks[5];
        rays[knight_steps[direction_index] + 119].step = knight_steps[direction_index];
    }
}
