extern int serial_base,serial_irq;
void configure_serial(void)
{
 serial_base=0x2f8;
 serial_irq=3;
}
