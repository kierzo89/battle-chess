/* REA image A011: enumerate the four promotion piece choices. */
typedef struct {
    int path[2];
    int promotion;
    unsigned char kind, reserved;
} Move;
extern Move current_move;
extern void append_move(void);

void promotion_moves(void)
{
    int kind;
    current_move.promotion = 1;
    for (kind = 2; kind <= 5; ++kind) {
        current_move.kind = kind;
        append_move();
    }
    current_move.promotion = 0;
}
