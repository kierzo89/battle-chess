/* Load the selected archive bank into the 70,000-byte huge byte buffer. */
extern unsigned char mode_11aa;
extern unsigned long far *asset_lengths, far *asset_offsets;
extern unsigned char huge asset_buffer[];
extern char asset_overflow[];
extern void select_asset_file(int), seek_asset(unsigned long);
extern void read_asset(unsigned char huge *, unsigned long);
extern int prompt_1296(char *, int, int);
extern void exit_07f3(void);

void load_asset_bank(void)
{
    unsigned long a;
    int b, c;
    select_asset_file(0);
    if (mode_11aa) { b=15; c=31; }
    else { b=0; c=15; }
    a=0;
    for (;b!=c;b++) {
        if (a+asset_lengths[b]>70000UL) {
            prompt_1296(asset_overflow,12,0);
            exit_07f3();
        }
        seek_asset(asset_offsets[b]);
        read_asset(asset_buffer+a,asset_lengths[b]);
        a+=asset_lengths[b];
    }
}
