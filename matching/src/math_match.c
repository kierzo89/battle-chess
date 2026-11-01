/* Reconstructed 16-bit target C, compiled by Microsoft C 5.00.
 * sizeof(int)==2; the target compiler's NEG wraps INT_MIN to INT_MIN.
 * Unlike portable math16.c, this is the source actually byte-checked.
 */
int min_i16(int a, int b)
{
    return a <= b ? a : b;
}

int max_i16(int a, int b)
{
    return a >= b ? a : b;
}

int abs_i16(int a)
{
    if (a > 0)
        return a;
    return -a;
}
