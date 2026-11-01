extern int state_9844, state_8fde, state_9646;
extern void reset_7d26(void), init_state(void), finish_0865(void);
extern unsigned display_segment;
extern long state_8fda, state_8fd6;
extern char state_88e3;
extern int state_57c8, state_984c, side, modes[], state_57cc, state_934a;
extern char workspace[];
extern void fill(char *, int, int);

void setup_state(void)
{
    state_9844 = 0;
    state_8fde = 0;
    state_9646 = 23;
    reset_7d26();
    init_state();
    if (*(char far *)((unsigned long)display_segment << 16) == 0) state_8fde = 0;
    else state_8fde = 200;
    state_8fd6 = state_8fda = 0L;
    state_88e3 = 1;
    state_984c = state_57c8 = 0;
    fill(workspace, 2880, 0);
    switch (modes[side]) {
    case 0: case 2: state_57cc = 0; break;
    case 1: state_57cc = 2; break;
    }
    state_934a = 0;
    finish_0865();
}
