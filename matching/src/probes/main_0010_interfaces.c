/* Uncredited interface proposal; native boundary proof remains separate.
 * a=scanword compared59, b=argv index, c=ASCII-output word, d=shiftflags-output word.
 * BIOS polling writes one byte per output: preserve the original word locals
 * and comparison, without invented upper-byte clearing. Unmatched callees
 * remain provisional. main_menus_114a is an actual typed reference; DATA ownership remains unresolved. */
extern unsigned char palette_mode, mode_11aa, mode_005a, flag_005b;
extern int init_stage;
extern int foreground, menu_state, background, border;
extern int menu_phase, paused;
typedef unsigned char Byte;
typedef struct {char *label;int command;Byte enabled,reserved;} MenuItem;
typedef struct {char *label;MenuItem *items;} Menu;
extern Menu *menus;
extern Menu main_menus_114a[];
extern unsigned long arena_capacity;
extern unsigned long far *startup_offsets_9648, far *startup_lengths_a8b6;
extern void far graphics_copy(int,int,int,int,char far *);
extern unsigned char huge splash_buffer[];
extern char arg_comp[], arg_keyb[], arg_com2[], joystick_question[];
extern int compare_argument(char *, char *);
extern void configure_serial(void), setup_assets(void);
extern void far initialize_video(int);
extern void load_asset_tables(int), load_asset_index(void);
extern void select_asset_file(int), seek_asset(long);
extern void read_asset(unsigned char huge *, long);
extern void initialize_io(void), load_asset_bank(void), initialize_asset_storage(void);
extern void far initialize_renderer(void);
extern void configure_game(int), reset_graphics_3e4f(void);
extern int poll_event(Byte *,Byte *,Byte *);
extern long ticks_ea5b(void);
extern void srand(unsigned), prepare_asset_decode(void);
extern long huff_frame_decode(unsigned char huge *,long);
extern void show_splash(void);
extern void save_active_arena(void), reset_display(void), refresh_panel_1d51(void);
extern unsigned char far input_probe_11ef_004e(void);
extern int prompt_1296(char *, int, int);
extern void far input_select_11ef_001e(void), far input_init_11ef_0000(void);
extern void select_display(void);

void main(int argc, char **argv)
{
    int a, b, c, d;
    palette_mode = 0;
    for (b = 1; b != argc; ++b) {
        if (compare_argument(argv[b], arg_comp) == 0)
            palette_mode = 3;
        if (compare_argument(argv[b], arg_keyb) == 0)
            mode_005a = 255;
        if (compare_argument(argv[b], arg_com2) == 0)
            configure_serial();
    }
    ++init_stage;
    setup_assets();
    initialize_video(palette_mode);
    if (palette_mode == 0 || palette_mode == 3) {
        foreground = 15; menu_state = 0; background = 15; border = 1;
    } else {
        foreground = 14; menu_state = 1; background = 15; border = 9;
    }
    load_asset_tables(mode_11aa);
    load_asset_index();
    select_asset_file(0);
    seek_asset(startup_offsets_9648[8 + palette_mode]);
    read_asset((unsigned char huge *)graphics_copy, startup_lengths_a8b6[8 + palette_mode]);
    ++init_stage;
    arena_capacity = 150000L;
    ++init_stage;
    initialize_io();
    ++init_stage;
    initialize_renderer();
    load_asset_bank();
    ++init_stage;
    initialize_asset_storage();
    configure_game(3);
    reset_graphics_3e4f();
    while (poll_event((Byte *)&d, (Byte *)&c, (Byte *)&a))
        ;
    while (!poll_event((Byte *)&d, (Byte *)&c, (Byte *)&a))
        srand((unsigned)ticks_ea5b());
    if (a == 59) {
        select_asset_file(0);
        seek_asset(startup_offsets_9648[4]);
        prepare_asset_decode();
        huff_frame_decode(splash_buffer, 32000L);
        show_splash();
    }
    save_active_arena();
    if (!mode_005a) {
        mode_005a = input_probe_11ef_004e();
        if (flag_005b) {
            if (prompt_1296(joystick_question, 12, 3) != 4099)
                mode_005a = 0;
        }
    } else
        mode_005a = 0;
    reset_display();
    menu_phase = 0;
    paused = 0;
    menus = main_menus_114a;
    if (!mode_005a)
        input_select_11ef_001e();
    refresh_panel_1d51();
    input_init_11ef_0000();
    for (;;)
        select_display();
}
