/* Inferred scalar storage used by the native Huff decoder.  These initialized
   objects describe observed widths; original C declarations remain unknown. */
unsigned int huff_shift_word = 0;
unsigned int huff_bits_left = 0;
unsigned char near *huff_input_cursor = 0;
unsigned long huff_remaining = 0;
