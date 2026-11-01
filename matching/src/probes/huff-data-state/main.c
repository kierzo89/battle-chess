typedef unsigned char Byte;
extern Byte huff_long_masks[9],huff_prefix_byte,huff_memory_mode,huff_checksum;
extern unsigned huff_pending_count,huff_saved_extent;
extern Byte far *huff_memory_cursor;
extern Byte huff_input_buffer[512];
int main(void){int i;
 if(huff_long_masks[0]!=0||huff_long_masks[8]!=255||huff_prefix_byte||huff_memory_mode||huff_checksum||huff_pending_count||huff_saved_extent||huff_memory_cursor)return 1;
 for(i=0;i<512;i++)if(huff_input_buffer[i])return 2;
 for(i=0;i<512;i++)huff_input_buffer[i]=(Byte)(i*37+11);
 for(i=0;i<512;i++)if(huff_input_buffer[i]!=(Byte)(i*37+11))return 3;
 return 0;}
