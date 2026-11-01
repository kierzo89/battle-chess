/* Semantic reconstructions of CHESS.EXE image offsets 8f95, 8fa5, 8fb5.
 * These portable C functions are not claims of matching compiler output.
 */
#include <stdint.h>

int16_t min_i16(int16_t a, int16_t b)
{
    return a <= b ? a : b;
}

int16_t max_i16(int16_t a, int16_t b)
{
    return a >= b ? a : b;
}

int16_t abs_i16(int16_t value)
{
    /* The 8086 NEG instruction preserves 8000h for the minimum integer.
     * Handle that case explicitly so signed overflow and out-of-range
     * signed conversions are unnecessary on any conforming C host.
     */
    if (value == INT16_MIN)
        return INT16_MIN;
    return value > 0 ? value : (int16_t)-value;
}
