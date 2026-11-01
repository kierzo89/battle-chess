typedef unsigned char Byte;
typedef struct { int from,to,flag; Byte kind,capture; } Move;
typedef struct { char prefix[20]; int busy; char tail[6]; } Actor;
extern Actor actors[];
extern Byte actor_map[], cells[], capture_types[];
extern void release_actor(Actor *);
extern void queue_piece(Byte,Byte,Byte,Byte);
extern void queue_move(Move *);

void animate_move(register Move *move)
{
    Byte captured, colour, destination, origin, unused_a, unused_b;
    Move rook;
    captured = 0;
    destination = (((move->to >> 1) & 56) ^ 56) | (move->to & 7);
    origin = (((move->from >> 1) & 56) ^ 56) | (move->from & 7);
    release_actor(&actors[actor_map[origin]]);
    if (move->flag && move->kind != 6 && move->kind != 1)
        cells[origin] = (cells[origin] & 120) | 4;
    colour = cells[origin] & 64;
    queue_piece(cells[origin] & 7, colour, actor_map[origin], destination);
    cells[origin] = 0;
    if (move->flag && move->kind == 6) {
        captured = 4;
        origin = (origin & 7) | (destination & 56);
    }
    if (move->capture)
        captured = capture_types[move->capture];
    if (captured) {
        for (destination = 0; destination < 32 && actors[destination].busy; ++destination)
            ;
        queue_piece(captured, colour ^ 64, destination, origin);
    }
    if (move->flag && move->kind == 1) {
        rook.kind = 3;
        rook.flag = 0;
        if (((Byte)move->from & 7) == 6) {
            rook.from = (move->from & 240) | 7;
            rook.to = (move->from & 240) | 5;
        } else {
            rook.from = move->from & 240;
            rook.to = (move->from & 240) | 3;
        }
        queue_move(&rook);
    }
}
