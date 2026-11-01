/* Genuine initialized serial variables belong only to the real source object. */
extern int serial_irq,serial_base,serial_link_guard;
extern unsigned serial_link_cookie,serial_diagnostic_calls;
extern void configure_serial(void);
unsigned char byte_ring_buffer[128];
unsigned char *byte_read_cursor,*byte_write_cursor;
int main(void)
{
    if(sizeof(serial_irq)!=2||sizeof(serial_base)!=2)return 1;
    if(serial_irq!=4||serial_base!=0x3f8)return 2;
    if(serial_link_guard!=0x1357||serial_link_cookie!=0x2468)return 3;
    if(serial_diagnostic_calls||byte_read_cursor||byte_write_cursor)return 4;
    configure_serial();
    if(serial_irq!=3||serial_base!=0x2f8)return 5;
    configure_serial();
    if(serial_irq!=3||serial_base!=0x2f8)return 6;
    serial_irq=4;serial_base=0x3f8;
    configure_serial();
    if(serial_irq!=3||serial_base!=0x2f8)return 7;
    if(serial_link_guard!=0x1357||serial_link_cookie!=0x2468)return 8;
    if(serial_diagnostic_calls||byte_read_cursor||byte_write_cursor)return 9;
    return 0;
}
