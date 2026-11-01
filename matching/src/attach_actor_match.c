/* REA3F0F: unlink, insert at the requested depth, and draw an actor. */
typedef struct Actor Actor;
typedef struct {int words[4];} Frame;
extern void clear_actor_3e81(Actor *);
extern void insert_actor(int, Actor *);
extern void draw_actor(int,int,int,Frame *,Actor *);
void attach_actor(register int x, register int y, int colour, Frame *frame, Actor *actor)
{
    clear_actor_3e81(actor);
    insert_actor(y,actor);
    draw_actor(x,y,colour,frame,actor);
}
