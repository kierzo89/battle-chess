typedef struct { int word[4]; } State;
extern int state_index, state_count;
extern State candidate_move, initial, move_list[];

void advance()
{
    if (state_index >= state_count)
        candidate_move = initial;
    else
        candidate_move = move_list[state_index++];
}
