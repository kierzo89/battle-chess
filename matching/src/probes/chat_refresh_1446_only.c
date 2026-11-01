/* Cooperatively poll the remote side and compose one line of chat text. */
extern int modes[2], waiting_0eee, refresh_active_0548, ready_9856;
extern unsigned char refresh_stop_11a6;
extern int menu_state;
extern void write_bytes_dbb5(unsigned char *, int);
extern void poll_8aaa(void);
extern int obtain_input(void);
extern void step_872a(void);
extern void begin_coordinates(void), reset_coordinates(void);
extern void set_panel_1780(int,int,int,int,int);
extern int text_input_1064(int,int,unsigned char *,int,int);
extern void fill_rectangle_58b0(int,int,int,int);

void refresh_1446(void)
{
    unsigned command[2];
    if (modes[0] == 2 || modes[1] == 2) {
        waiting_0eee = 0;
        command[0] = 0x04aa;
        command[1] = 0x34ca;
        write_bytes_dbb5((unsigned char *)command, 4);
        refresh_active_0548 = 1;
        poll_8aaa();
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

