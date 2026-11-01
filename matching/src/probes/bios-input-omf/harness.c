/* Consumer-only real DOSBox BIOS control. No keyboard/clock stubs and no
 * assertion about running original main or its surrounding game state. */
typedef unsigned char Byte;
typedef struct {unsigned before,value,after;} GuardedWord;
extern int poll_event(Byte *shiftflags,Byte *ascii,Byte *scancode);
extern long ticks_ea5b(void);
int main(void)
{
    GuardedWord shift,ascii,scan;
    unsigned long first,now,attempts;
    int i;
    shift.before=0x1234;shift.value=0xa1b2;shift.after=0x5678;
    ascii.before=0x1357;ascii.value=0xc3d4;ascii.after=0x2468;
    scan.before=0x9876;scan.value=0xe5f6;scan.after=0x5432;
    for (i=0;i<16;++i) {
        if (poll_event((Byte *)&shift.value,(Byte *)&ascii.value,(Byte *)&scan.value)!=0)return 1;
        if (shift.before!=0x1234 || shift.value!=0xa1b2 || shift.after!=0x5678)return 2;
        if (ascii.before!=0x1357 || ascii.value!=0xc3d4 || ascii.after!=0x2468)return 3;
        if (scan.before!=0x9876 || scan.value!=0xe5f6 || scan.after!=0x5432)return 4;
    }
    first=(unsigned long)ticks_ea5b();
    attempts=0;
    do {
        now=(unsigned long)ticks_ea5b();
        if (++attempts==5000000UL)return 5;
    } while (now==first);
    if (now<first || now-first>36UL)return 6;
    if (poll_event((Byte *)&shift.value,(Byte *)&ascii.value,(Byte *)&scan.value)!=0)return 7;
    if (shift.value!=0xa1b2 || ascii.value!=0xc3d4 || scan.value!=0xe5f6)return 8;
    return 0;
}
