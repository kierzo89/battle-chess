/* REA3EB1: insert an actor in the depth-ordered chain. */
typedef struct Actor {int x,y;unsigned char rest[22];struct Actor *next;} Actor;
extern Actor *actors_head;
void insert_actor(register int y, register Actor *actor)
{
    Actor **link;
    link = &actors_head;
    while (*link != actor) {
        if (!*link) {
            actor->next = 0;
            *link = actor;
        } else if ((*link)->y >= y) {
            actor->next = *link;
            *link = actor;
        } else
            link = &(*link)->next;
    }
}
