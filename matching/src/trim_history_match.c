typedef struct { int word[4]; } Move;
extern int counter;
extern Move history_tail[], initial, saved;

void trim_history()
{
    int i;
    for (i = counter; i >= -104; --i)
        history_tail[i - counter - 1] = history_tail[i];
    counter = -1;
    saved = initial;
    history_tail[0] = initial;
}
