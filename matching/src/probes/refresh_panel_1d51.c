extern int *command_cursor_0070;
extern int cursor_column_0086,cursor_row_0088;
extern int *cursor_x_b0c6,*cursor_y_b0c8;
extern int *far write_command_fd4e(int *);
void refresh_panel_1d51(void)
{
    command_cursor_0070[0]=5,command_cursor_0070[1]=0;
    command_cursor_0070[4]=cursor_x_b0c6[cursor_row_0088*8+cursor_column_0086];
    command_cursor_0070[5]=cursor_y_b0c8[cursor_row_0088];
    command_cursor_0070=write_command_fd4e(command_cursor_0070);
}
