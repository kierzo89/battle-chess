/* Return the low bit; far entry in the evaluation code segment. */
unsigned far evaluation_parity(unsigned value)
{
    return value & 1;
}
