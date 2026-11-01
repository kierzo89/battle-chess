/* REA input flag branch; the meaning of returned code 0xb082 is unresolved. */
extern unsigned char input_flag_0061;
extern void input_reset_e00f();
extern void input_update_0886();
int input_083e()
{
    if (input_flag_0061) {
        input_reset_e00f();
        input_flag_0061 = 0;
        input_update_0886();
        return 0xb082;
    }
    return 0;
}

extern void detach_all(void),display_board_5e18(void),refresh_panel_1d51(void);
extern void far clear_display_fbf6(void);
extern void far draw_fce8(int);
extern unsigned char mode_005a,marked_square_8dd6;
extern unsigned selected_square_0efa,cursor_square_0efc;
extern int current_side;
extern void outline_square_543a(unsigned,unsigned);

void reset_display_0865(void)
{
    detach_all();
    clear_display_fbf6();
    display_board_5e18();
    if(!mode_005a) refresh_panel_1d51();
}

void input_update_0886(void)
{
    if(cursor_square_0efc!=255) {
        outline_square_543a(cursor_square_0efc,0);
        cursor_square_0efc=255;
        draw_fce8(current_side);
    }
    outline_square_543a(selected_square_0efa,0);
    outline_square_543a(marked_square_8dd6,0);
    marked_square_8dd6=selected_square_0efa=255;
}
