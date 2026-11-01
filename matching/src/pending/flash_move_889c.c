/* REA889C: flash transformed source/destination squares twenty times. */
extern void highlight_543a(int,int);
extern void wait_941b(long);
void flash_move_889c(int *move)
{
    int to;
    int i;
    int from;
    if ((char)move[3]) {
        to = (((move[1] & 0x70) ^ 0x70) >> 1) | (move[1] & 7);
        from = (((move[0] & 0x70) ^ 0x70) >> 1) | (move[0] & 7);
        i = 0;
        do {
            highlight_543a(to, i % 6 + 2);
            wait_941b(2L);
            highlight_543a(from, i % 6 + 2);
            i++;
        } while (i != 20);
        highlight_543a(to,0);
        highlight_543a(from,0);
    }
}
