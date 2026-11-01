/* A distinct medium-model CODE contribution, using the shared DGROUP. */
extern int shared_state;
int far medium_b(int value)
{
    return (value ^ 0x1357) + shared_state;
}
