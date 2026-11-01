extern void clear_board(), set_cell_bytes(), update_950d();
extern int back_rank[], side, opposite_side;

void reset_board()
{
    int i;
    clear_board();
    i = 0;
    do {
        set_cell_bytes(back_rank[i], 0, i);
        set_cell_bytes(6, 0, i + 16);
        set_cell_bytes(6, 1, i + 96);
        set_cell_bytes(back_rank[i], 1, i + 112);
        ++i;
    } while (i <= 7);
    update_950d();
    side = 0;
    opposite_side = 1;
}
