extern int ready,modes[],mode_8176,mode_8188,mode_0ef6;
extern void ui_89df(void);
void restore_ui_92ab(register unsigned char *p,unsigned char index)
{
    unsigned char flags;
    p += index * 2;
    ready = (unsigned)*p++ << 8;
    ui_89df();
    ready = 0;
    flags = *p;
    modes[1] = flags & 3;
    modes[0] = (flags >> 2) & 3;
    mode_8176 = (flags & 64) != 0;
    mode_8188 = (flags & 32) != 0;
    mode_0ef6 = (flags & 16) != 0;
}
