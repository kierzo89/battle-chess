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
