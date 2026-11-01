extern int prompt_1296(char *,int,int);
extern void exit_07f3(void);
void show_error_0d6e(register char *message)
{
    prompt_1296(message,12,0);
}
/* Normal execution terminates through exit_07f3 and the runtime exit. */
int error_message(register char *message)
{
    prompt_1296(message,12,0);
    exit_07f3();
}
