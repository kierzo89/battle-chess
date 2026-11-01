/* REA889C: flash transformed source/destination squares twenty times. */
extern void outline_square_543a(unsigned,unsigned);
extern void wait_941b(long);
void flash_move_889c(int *move)
{
    int c; /* transformed destination */
    int b; /* flash iteration */
    int a; /* transformed source */
    if ((char)move[3]) {
        c = (((move[1] & 0x70) ^ 0x70) >> 1) | (move[1] & 7);
        a = (((move[0] & 0x70) ^ 0x70) >> 1) | (move[0] & 7);
        b = 0;
        do {
            outline_square_543a(c, b % 6 + 2);
            wait_941b(2L);
            outline_square_543a(a, b % 6 + 2);
            b++;
        } while (b != 20);
        outline_square_543a(c,0);
        outline_square_543a(a,0);
    }
}
