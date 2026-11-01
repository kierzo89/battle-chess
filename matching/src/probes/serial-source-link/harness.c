/* Consumer-only source-link test: no serial I/O, hardware stubs or aliases. */
extern int serial_base,serial_irq;
extern void configure_serial(void);
int main(void)
{
    if (sizeof(serial_base)!=2 || sizeof(serial_irq)!=2)return 1;
    if (serial_base!=0x3f8 || serial_irq!=4)return 2;
    configure_serial();
    if (serial_base!=0x2f8 || serial_irq!=3)return 3;
    configure_serial();
    if (serial_base!=0x2f8 || serial_irq!=3)return 4;
    serial_base=0x3f8;
    serial_irq=4;
    configure_serial();
    if (serial_base!=0x2f8 || serial_irq!=3)return 5;
    return 0;
}
