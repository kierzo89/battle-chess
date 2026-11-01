extern void write_bytes_dbb5(unsigned char *, int);
extern unsigned char input_reset_state;

void input_reset_e00f(void)
{
    unsigned command[2];
    command[0] = 0x04a5;
    command[1] = 0x34c5;
    write_bytes_dbb5((unsigned char *)command, 4);
    input_reset_state = 0;
}
