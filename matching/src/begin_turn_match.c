extern int active, done;
extern long requested_limit, limit;

void begin_turn()
{
    active = 1;
    done = 0;
    limit = requested_limit;
    if (limit < 3L)
        limit = 3L;
}
