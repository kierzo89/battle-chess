typedef union {unsigned word;struct{unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
extern int counter;
extern Move history_tail[], initial_move, saved_state;

void shift_state(void)
{
    int i;
    --counter;
    for (i = -104; i <= counter; ++i)
        history_tail[i] = history_tail[i + 1];
    saved_state = initial_move;
}
