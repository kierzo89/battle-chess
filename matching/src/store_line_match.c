/* REA AE11: maintain two distinct candidate moves for each search level. */
typedef struct {int to,from,flag;unsigned char kind,capture;} Move;
extern Move history[], search_pair_moves[24][2];
extern int history_index;
extern int equal_state(Move *,Move *);
void store_line(Move move)
{
    if (move.kind && (!history[history_index].kind ||
                     history[history_index].to != move.to)) {
        if (!search_pair_moves[history_index][0].kind ||
            equal_state(&move,&search_pair_moves[history_index][1])) {
            search_pair_moves[history_index][1] = search_pair_moves[history_index][0];
            search_pair_moves[history_index][0] = move;
        } else if (!equal_state(&move,&search_pair_moves[history_index][0]))
            search_pair_moves[history_index][1] = move;
    }
}
