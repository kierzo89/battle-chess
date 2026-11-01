/* Consumed-compatible COMMON views, not proof of historical capacity/order. */
typedef unsigned char Byte;
Byte byte_ring_buffer[128];
Byte *byte_read_cursor,*byte_write_cursor;
Byte serial_irq_flags_b0d4;
