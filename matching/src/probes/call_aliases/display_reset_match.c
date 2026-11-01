/* REA image 7B86..7BF8: reset and select board display state. */
extern unsigned char saved_state[];
extern int current_square, display_mode;
extern int rays_ready, actors_ready, silent;
extern void fill_8a96(char *, int, int);
extern void init_display(void), setup_state(void);
extern void turn_7ddb(void), alternate_view(void), flat_view(void);
extern void init_rays(void), init_surface(void), reset_graphics_3e4f(void);
extern void init_animation(void), redraw_frame(void), play_effect(int);

void reset_display(void)
{
    fill_8a96((char *)saved_state, 1024, 0);
    init_display();
    setup_state();
    current_square = 0;
}

void select_display(void)
{
    switch (display_mode) {
    case 0: turn_7ddb(); break;
    case 1: alternate_view(); break;
    case 2: flat_view(); break;
    }
}

void init_display(void)
{
    init_rays();
    rays_ready = 1;
    actors_ready = 1;
    init_surface();
    reset_graphics_3e4f();
    init_animation();
    redraw_frame();
    if (!silent) {
        play_effect(3);
        play_effect(2);
    }
}
