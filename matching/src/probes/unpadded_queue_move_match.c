/* REA77AF: queue a move, including castling recursion and pawn capture cleanup. */
typedef unsigned char Byte;
typedef union {unsigned word;struct{Byte low,high;} byte;} Kind;
typedef struct {int from,to,special;Kind kind;} Move;
typedef struct {Byte bytes[28];} Actor;
extern Byte cells[],actor_map[],kind_map[];
extern Actor actors[];
extern void detach_actor(Actor *);
extern void queue_piece(int,int,int,int);
void queue_move(register Move *move)
{
    /* Six original frame bytes have no observed reads/writes. */
    Byte d,e; /* transformed source and destination */
    Move f;
    if (move->special && move->kind.byte.low == 1) {
        f.from = move->from;
        f.to = move->to;
        f.special = 0;
        f.kind.byte.low = move->kind.byte.low;
        f.kind.byte.high = 0;
        queue_move(&f);
        if (((Byte)move->from & 7) == 6) {
            f.from = (move->from & 0xf0) | 5;
            f.to = (move->to & 0xf0) | 7;
        } else {
            f.from = (move->from & 0xf0) | 3;
            f.to = move->to & 0xf0;
        }
        f.kind.byte.low = 3;
        f.kind.byte.high = 0;
        f.special = 0;
        move = &f;
    }
    e = (((move->to >> 1) & 0x38) ^ 0x38) | (move->to & 7);
    d = (((move->from >> 1) & 0x38) ^ 0x38) | (move->from & 7);
    if (cells[d]) detach_actor(&actors[actor_map[d]]);
    detach_actor(&actors[actor_map[e]]);
    queue_piece(kind_map[move->kind.byte.low],cells[e]&64,actor_map[e],d);
    cells[e] = 0;
    if (move->special && move->kind.byte.low == 6) {
        e = (e & 0x38) | (d & 7);
        detach_actor(&actors[actor_map[e]]);
        cells[e] = 0;
    }
}
