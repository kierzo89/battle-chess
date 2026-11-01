/* REA image 9FDF: append the current eight-byte move when space remains. */
typedef struct { int words[4]; } Move;
extern int move_count;
extern Move move_list[];
extern Move current_move;

void append_move(void)
{
    if (move_count >= 80)
        return;
    move_list[move_count++] = current_move;
}
