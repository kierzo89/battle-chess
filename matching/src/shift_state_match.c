typedef union {unsigned word;struct{unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
extern int history_index;
extern Move history_tail[], initial_move, saved_state;

void shift_state(void)
{
    int i;
    --history_index;
    for (i = -104; i <= history_index; ++i)
        history_tail[i] = history_tail[i + 1];
    saved_state = initial_move;
}
