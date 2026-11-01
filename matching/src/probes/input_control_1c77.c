extern int *command_cursor_0070;
extern int *far write_command_fd4e(int *);
extern void far special_command_1fc2(void);
void input_control_1c77(char scan)
{
 *(long *)command_cursor_0070=6L;
 switch(scan) {
 case 0x21:scan='f';break;
 case 0x14:scan='t';break;
 case 0x13:scan='r';break;
 case 0x32:scan='m';break;
 case 0x1f:scan='s';break;
 case 0x24:special_command_1fc2();return;
 }
 command_cursor_0070[2]=scan+128;
 command_cursor_0070=write_command_fd4e(command_cursor_0070);
}
