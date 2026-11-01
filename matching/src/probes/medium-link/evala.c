/* A real cross-source far dependency with shared small-model DATA. */
extern int shared_state;
extern int far medium_b(int);
int far medium_a(int value)
{
    return medium_b(value) + shared_state;
}
