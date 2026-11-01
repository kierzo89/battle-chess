/* REA3F7F: detach actors until the active chain is empty. */
typedef struct Actor Actor;
extern Actor *actors_head;
extern void detach_actor(Actor *);
void detach_all(void)
{
    while (actors_head)
        detach_actor(actors_head);
}
