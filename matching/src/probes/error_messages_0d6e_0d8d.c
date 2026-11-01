extern int prompt_1296(char *,int,int);
extern void exit_07f3(void);
void show_error_0d6e(register char *message)
{
    prompt_1296(message,12,0);
}
void error_message(register char *message)
{
    prompt_1296(message,12,0);
    exit_07f3();
}
