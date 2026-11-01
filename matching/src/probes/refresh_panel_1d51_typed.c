typedef struct {int operation,state,unclassified4,unclassified6,x,y;} PositionCommandPrefix;
extern PositionCommandPrefix *command_cursor_0070;
extern int cursor_column_0086,cursor_row_0088;
extern int *cursor_x_b0c6,*cursor_y_b0c8;
extern PositionCommandPrefix *far write_command_fd4e(PositionCommandPrefix *);
void refresh_panel_1d51(void)
{
    command_cursor_0070->operation=5,command_cursor_0070->state=0;
    command_cursor_0070->x=cursor_x_b0c6[cursor_row_0088*8+cursor_column_0086];
    command_cursor_0070->y=cursor_y_b0c8[cursor_row_0088];
    command_cursor_0070=write_command_fd4e(command_cursor_0070);
}
