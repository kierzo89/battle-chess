typedef unsigned char Byte;
extern Byte *byte_read_cursor,*byte_write_cursor,byte_ring_buffer[128];
extern void far restore_mode_10e0d(void);
extern void far set_serial_format_10d3_0000(unsigned);
extern void far enable_serial_irq_10d3_0023(void);
void initialize_io(void)
{
 byte_read_cursor=byte_write_cursor=byte_ring_buffer;
 restore_mode_10e0d();
 set_serial_format_10d3_0000(0x43);
 enable_serial_irq_10d3_0023();
}

extern void far write_byte_far(unsigned);
extern long time(long *);
extern Byte *byte_read_cursor,*byte_write_cursor,byte_ring_buffer[128];

void write_bytes_dbb5(register Byte *source,register int count)
{
    while(count--) write_byte_far(*source++);
}

int read_bytes_dbe3(register Byte *destination,register int count)
{
    unsigned long a,b;
    while(count--) {
        b=a=time(0);
        a+=8;
        while(byte_read_cursor==byte_write_cursor&&(b=time(0))<a) ;
        if(b<a) {
            *destination++=*byte_read_cursor++;
            if(byte_read_cursor==byte_ring_buffer+128) byte_read_cursor=byte_ring_buffer;
        } else return -1;
    }
    return 0;
}

void discard_bytes_dc7f(void)
{
    byte_read_cursor=byte_write_cursor;
}

int available_bytes_dc91(void)
{
    Byte *a;
    int b;
    a=byte_write_cursor;
    if(a>=byte_read_cursor) b=a-byte_read_cursor;
    else b=a-byte_read_cursor+128;
    return b;
}

int serial_irq=4;
int serial_base=0x3f8;
void configure_serial(void)
{
 serial_base=0x2f8;
 serial_irq=3;
}
