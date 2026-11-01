extern int prompt_1296(char *, int, int);
extern char prompt_text[];
extern void exit_07f3();

void empty_8834(void)
{
}

void prompt_8835(void)
{
    if (prompt_1296(prompt_text, 12, 1) == 0x1003)
        exit_07f3(0);
}
