/* Actual adjacent display and history operations; no added declarations or bodies. */
/* REA image 7B86..7BF8: reset and select board display state. */
extern unsigned char saved_state[];
extern int ready_9856, state_57cc;
extern int modes[2], mode_8176, command_active;
extern void fill_8a96(char *, int, int);
extern void init_display(void), setup_state(void);
extern void turn_7ddb(void), alternate_view(void), computer_cycle_801a(void);
extern void init_rays(void), init_surface(void), reset_graphics_3e4f(void);
extern void init_animation(void), load_book_82a5(void), load_asset_group(int);

void reset_display(void)
{
    fill_8a96((char *)saved_state, 1024, 0);
    init_display();
    setup_state();
    ready_9856 = 0;
}

void select_display(void)
{
    switch (state_57cc) {
    case 0: turn_7ddb(); break;
    case 1: alternate_view(); break;
    case 2: computer_cycle_801a(); break;
    }
}

void init_display(void)
{
    init_rays();
    modes[1] = 1;
    mode_8176 = 1;
    init_surface();
    reset_graphics_3e4f();
    init_animation();
    load_book_82a5();
    if (!command_active) {
        load_asset_group(3);
        load_asset_group(2);
    }
}

typedef union {unsigned word;struct{unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
extern int history_index;
extern Move history_tail[], initial_move, saved;

void trim_history()
{
    int i;
    for (i = history_index; i >= -104; --i)
        history_tail[i - history_index - 1] = history_tail[i];
    history_index = -1;
    saved = initial_move;
    history_tail[0] = initial_move;
}
