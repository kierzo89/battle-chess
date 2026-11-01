/* Diagnostic storage mechanism only, not a reconstructed game helper. */
static unsigned selection_xor_52cc;
static unsigned selection_colour_52ce;
unsigned storage_access(unsigned slot, unsigned value, unsigned write)
{
    if (write) {
        if (slot) selection_colour_52ce = value;
        else selection_xor_52cc = value;
    }
    return slot ? selection_colour_52ce : selection_xor_52cc;
}
unsigned storage_toggle(void)
{
    selection_colour_52ce ^= selection_xor_52cc;
    return selection_colour_52ce;
}
