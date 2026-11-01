/* REA 78F6. Complete363-byte MSC5 /AS /Zi reconstruction. */
typedef unsigned char Byte;
typedef struct { int from,to,flag; Byte kind,capture; } Move;
typedef struct { char prefix[20]; int busy; char tail[6]; } Actor;
extern Actor actors[];
extern Byte actor_map[], cells[], kind_map[];
extern void release_actor(Actor *);
extern void queue_piece(Byte,Byte,Byte,Byte);
extern void queue_move(Move *);

void animate_move(register Move *move)
{
    Byte taken, colour, target, screen_origin, unused_a, unused_b;
    Move rook;
    taken = 0;
    target = (((move->to >> 1) & 56) ^ 56) | (move->to & 7);
    screen_origin = (((move->from >> 1) & 56) ^ 56) | (move->from & 7);
    release_actor(&actors[actor_map[screen_origin]]);
    if (move->flag && move->kind != 6 && move->kind != 1)
        cells[screen_origin] = (cells[screen_origin] & 120) | 4;
    colour = cells[screen_origin] & 64;
    queue_piece(cells[screen_origin] & 7, colour, actor_map[screen_origin], target);
    cells[screen_origin] = 0;
    if (move->flag && move->kind == 6) {
        taken = 4;
        screen_origin = (screen_origin & 7) | (target & 56);
    }
    if (move->capture)
        taken = kind_map[move->capture];
    if (taken) {
        for (target = 0; target < 32 && actors[target].busy; ++target)
            ;
        queue_piece(taken, colour ^ 64, target, screen_origin);
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
