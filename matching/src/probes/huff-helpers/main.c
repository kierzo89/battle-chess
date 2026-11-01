/* Diagnostic storage only: one refill consumes exactly512 bytes.
   These capacities and ordering are not proposed historical game storage. */
typedef unsigned char Byte;
Byte huff_memory_mode=1;
Byte huge *huff_memory_cursor;
Byte huff_input_buffer[512],helper_test_source[512];
int asset_file;
extern unsigned invoke_huff_refill(void);
int main(void)
{
    huff_memory_cursor=helper_test_source;
    return invoke_huff_refill()==(unsigned)huff_input_buffer ? 0 : 1;
}
