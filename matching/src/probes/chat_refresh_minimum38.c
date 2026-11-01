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

void type_chat_14c1(register int mode)
{
    unsigned char message[38];
    register int length;
    begin_coordinates();
    set_panel_1780(0, 88, 319, 112, menu_state);
    length = text_input_1064(8, 96, message, 37, mode);
    message[length++] = '\r';
    fill_rectangle_58b0(0, 79, 88, 112);
    if (length > 1) {
        if (length == 4 && message[0] == '+' && message[1] == '+' && message[2] == '+')
            write_bytes_dbb5(message, length - 1);
        else
            write_bytes_dbb5(message, length);
    }
    reset_coordinates();
}
