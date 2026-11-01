/* One compatible initialized context; historical translation-unit identity unknown. */
typedef unsigned char Byte;
Byte huff_long_masks[9]={0,128,192,224,240,248,252,254,255};
unsigned huff_prefix_byte=0;
unsigned huff_pending_count=0;
unsigned huff_saved_extent=0;
Byte far *huff_memory_cursor=0;
Byte huff_memory_mode=0;
Byte huff_checksum=0;
