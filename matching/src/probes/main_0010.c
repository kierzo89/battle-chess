/* Uncredited reconstruction from the full expanded REA main body.
 * All four frame words have genuine uses: key, argv index, x and y.
 * Names and types for unmatched callees remain provisional. */
extern unsigned char display_mode, asset_mode, demo_mode, demo_prompt;
extern unsigned init_stage;
extern int foreground, menu_state, background, border;
extern int game_state, history_count;
extern unsigned menu_address;
extern unsigned long memory_limit;
extern unsigned long far *asset_offsets, far *asset_lengths;
extern unsigned char far graphics_code[], far splash_buffer[];
extern char arg_display[], arg_demo[], arg_serial[], demo_message[];
extern int compare_argument(char *, char *);
extern void configure_serial(void), setup_assets(void);
extern void far initialize_video(int);
extern void load_asset_tables(int), load_asset_index(void);
extern void select_asset_file(int), seek_asset(long);
extern void read_asset(unsigned char far *, long);
extern void initialize_io(void), initialize_game(void), load_board(void);
extern void far initialize_renderer(void);
extern void configure_game(int), reset_graphics_3e4f(void);
extern int poll_event(int *, int *, int *), idle_delay(void);
extern void sleep_ticks(int), huff_initialize(void);
extern void huff_decode(unsigned char far *, long), show_splash(void);
extern void prepare_board(void), turn_7b86(void), refresh_panel_1d51(void);
extern unsigned char far initialize_demo(void);
extern int prompt_1296(char *, int, int);
extern void far start_game(void), far finish_game_setup(void);
extern void dispatch_game(void);

void main(int argc, char **argv)
{
    int a, b, c, d;
    display_mode = 0;
    for (b = 1; b != argc; ++b) {
        if (compare_argument(argv[b], arg_display) == 0)
            display_mode = 3;
        if (compare_argument(argv[b], arg_demo) == 0)
            demo_mode = 255;
        if (compare_argument(argv[b], arg_serial) == 0)
            configure_serial();
    }
    ++init_stage;
    setup_assets();
    initialize_video(display_mode);
    if (display_mode == 0 || display_mode == 3) {
        foreground = 15; menu_state = 0; background = 15; border = 1;
    } else {
        foreground = 14; menu_state = 1; background = 15; border = 9;
    }
    load_asset_tables(asset_mode);
    load_asset_index();
    select_asset_file(0);
    seek_asset(asset_offsets[8 + display_mode]);
    read_asset(graphics_code, asset_lengths[8 + display_mode]);
    ++init_stage;
    memory_limit = 150000L;
    ++init_stage;
    initialize_io();
    ++init_stage;
    initialize_renderer();
    initialize_game();
    ++init_stage;
    load_board();
    configure_game(3);
    reset_graphics_3e4f();
    while (poll_event(&d, &c, &a))
        ;
    while (!poll_event(&d, &c, &a))
        sleep_ticks(idle_delay());
    if (a == 59) {
        select_asset_file(0);
        seek_asset(asset_offsets[4]);
        huff_initialize();
        huff_decode(splash_buffer, 32000L);
        show_splash();
    }
    prepare_board();
    if (!demo_mode) {
        demo_mode = initialize_demo();
        if (demo_prompt) {
            if (prompt_1296(demo_message, 12, 3) != 4099)
                demo_mode = 0;
        }
    } else
        demo_mode = 0;
    turn_7b86();
    game_state = 0;
    history_count = 0;
    menu_address = 0x114a;
    if (!demo_mode)
        start_game();
    refresh_panel_1d51();
    finish_game_setup();
    for (;;)
        dispatch_game();
}
