/* Allocation/CRT control only; this does not execute the game consumer. */
extern unsigned selection_xor_52cc, selection_colour_52ce;
extern unsigned char row_mask_9230[8];
extern unsigned storage_guard;
int main(void)
{
    int i;
    if (sizeof(selection_xor_52cc) != 2 ||
        sizeof(selection_colour_52ce) != 2 || sizeof(row_mask_9230) != 8)
        return 1;
    if (selection_xor_52cc || selection_colour_52ce || storage_guard != 0x1379)
        return 2;
    for (i = 0; i < 8; ++i)
        if (row_mask_9230[i]) return 3;
    selection_xor_52cc = 0xA35C;
    selection_colour_52ce = 0x17E9;
    for (i = 0; i < 8; ++i) row_mask_9230[i] = (unsigned char)(0x31 + 7*i);
    if (selection_xor_52cc != 0xA35C || selection_colour_52ce != 0x17E9)
        return 4;
    for (i = 0; i < 8; ++i)
        if (row_mask_9230[i] != 0x31 + 7*i) return 5;
    selection_xor_52cc ^= selection_colour_52ce;
    if (selection_xor_52cc != 0xB4B5 || selection_colour_52ce != 0x17E9 ||
        storage_guard != 0x1379) return 6;
    return 0;
}
