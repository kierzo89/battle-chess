/* Inferred storage and callees retain their observed address names. */
extern long ticks_ea5b(void);

void wait_941b(long delay)
{
    long start = ticks_ea5b();
    while (ticks_ea5b() < start + delay) { }
}
