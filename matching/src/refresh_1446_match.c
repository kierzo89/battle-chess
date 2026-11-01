/* Cooperatively poll the remote side while accepting input. */
extern int modes[2], waiting_0eee, refresh_active_0548, ready_9856;
extern unsigned char refresh_stop_11a6;
extern void write_bytes_dbb5(unsigned char *, int);
extern void poll_input(void);
extern int obtain_input(void);
extern void step_872a(void);

void refresh_1446(void)
{
    unsigned command[2];
    if (modes[0] == 2 || modes[1] == 2) {
        waiting_0eee = 0;
        command[0] = 0x04aa;
        command[1] = 0x34ca;
        write_bytes_dbb5((unsigned char *)command, 4);
        refresh_active_0548 = 1;
        poll_input();
        while ((modes[0] == 2 || modes[1] == 2) && !refresh_stop_11a6) {
            if (!ready_9856)
                ready_9856 = obtain_input();
            if (ready_9856)
                step_872a();
        }
        refresh_active_0548 = 0;
        refresh_stop_11a6 = 0;
    }
}

