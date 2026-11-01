extern void far write_byte_far(unsigned);
void write_bytes_dbb5(register unsigned char *source,register int count)
{
    while(count--) write_byte_far(*source++);
}
