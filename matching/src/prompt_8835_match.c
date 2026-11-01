extern int prompt_1296();
extern void exit_07f3();
extern char prompt_text[];
void prompt_8835()
{
    if (prompt_1296(prompt_text, 12, 1) == 4099)
        exit_07f3(0);
}
