/* Queue one position event and advance the real command ring cursor. */
extern int *command_cursor_0070;
extern int *far write_command_fd4e(int *);
void position_command_22c5(int x,int y)
{
 *(long *)command_cursor_0070=5L;
 command_cursor_0070[4]=x;
 command_cursor_0070[5]=y;
 command_cursor_0070=write_command_fd4e(command_cursor_0070);
}
