extern unsigned char control_bytes_0064[],banner_bytes_4d0e[];
extern void write_bytes_dbb5(unsigned char *,int);
void write_control_1562(void)
{
    write_bytes_dbb5(control_bytes_0064,4);
}
void write_banner_157c(void)
{
    write_bytes_dbb5(banner_bytes_4d0e,24);
}
