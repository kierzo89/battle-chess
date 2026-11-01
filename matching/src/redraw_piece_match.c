extern unsigned char actor_map[], cells[], kind_map[];
extern void queue_piece(int,int,int,int);

void redraw_piece(register int square, register int kind)
{
    square = (((square >> 1) & 56) ^ 56) | (square & 7);
    queue_piece(kind_map[kind], cells[square] & 64,
        actor_map[square], square);
}
