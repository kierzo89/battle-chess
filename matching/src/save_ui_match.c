extern int view_mode_053a,modes[],mode_8176,mode_8188,mode_0ef6;
void save_ui_931c(register unsigned char *p,unsigned char index)
{
    unsigned char flags;
    p += index * 2;
    *p++ = view_mode_053a;
    flags = modes[1] & 3;
    flags |= (modes[0] << 2) & 12;
    flags |= (mode_8176 << 6) + (mode_8188 << 5) + (mode_0ef6 << 4);
    *p = flags;
}
