extern int level, input;
extern long requested_limit, limit;
extern long timer_b[];
extern long get_number();

void set_limit()
{
    int previous;
    previous = level;
    level = input >> 8;
    if (level == 0)
        requested_limit = 6L;
    else if (level == 10) {
        if (limit = get_number() * 60L)
            requested_limit = limit;
        else
            level = previous;
    } else {
        requested_limit = 5 << (level - 1);
        timer_b[0] = timer_b[1] = 0L;
    }
}
