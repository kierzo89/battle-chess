/* REA image 7AA7: orient and attach a board piece to its animation actor. */
typedef unsigned char Byte;
typedef struct { Byte prefix[11]; Byte square; Byte rest[16]; } Actor;
typedef struct { int words[4]; } Frame;
extern Actor actors[];
extern Byte cells[], actor_map[];
extern Byte *frame_index;
extern Frame frames[];
extern int *screen_x, *screen_y;
extern void attach_actor(int, int, int, Frame *, Actor *);

void queue_piece(register int kind, register int colour, int actor, int square)
{
    int facing;
    if (kind == 6)
        facing = ((Byte)square & 7) < 4 ? 3 : 7;
    else if (kind == 1) {
        if (((Byte)square & 7) < 4)
            facing = colour ? 1 : 3;
        else
            facing = colour ? 7 : 5;
    } else
        facing = colour ? 0 : 4;
    cells[square] = (facing << 3) | colour | kind;
    actor_map[square] = actor;
    actors[actor].square = square;
    attach_actor(screen_x[square], screen_y[square >> 3], colour,
                 &frames[frame_index[(facing << 3) | kind]], &actors[actor]);
}
