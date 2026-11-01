/* REA3F49: remove an actor's previous drawing, then clear its frame/square. */
typedef unsigned char Byte;
typedef struct {int words[4];} Frame;
typedef struct Actor {
    int x,y;
    Byte prefix[6];
    Byte colour,square;
    Byte middle[8];
    Frame *frame;
    Byte tail[6];
} Actor;
extern void clear_actor_3e81(Actor *);
extern void draw_actor(int,int,int,Frame *,Actor *);
void detach_actor(register Actor *actor)
{
    clear_actor_3e81(actor);
    draw_actor(actor->x,actor->y,actor->colour,actor->frame,actor);
    actor->frame = 0;
    actor->square = 0;
}
