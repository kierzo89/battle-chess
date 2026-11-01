/* REA3E81: unlink every occurrence of an actor from the actor chain. */
typedef struct Actor {unsigned char prefix[26];struct Actor *next;} Actor;
extern Actor *actors_head;
void clear_actor_3e81(register Actor *actor)
{
    register Actor **link;
    link = &actors_head;
    while (*link) {
        if (*link == actor) *link = actor->next;
        else link = &(*link)->next;
    }
}
