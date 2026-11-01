extern char *select_alpha(int), *select_beta(int);
extern int puts(char *);
int text_equal(char *left,char *right)
{
    while(*left && *left==*right){++left;++right;}
    return *left==*right;
}
int main(void)
{
    if(!text_equal(select_alpha(1),"alpha ready"))return 1;
    if(!text_equal(select_alpha(0),"alpha idle"))return 2;
    if(!text_equal(select_beta(1),"beta ready"))return 3;
    if(!text_equal(select_beta(0),"beta idle"))return 4;
    if(select_alpha(1)==select_beta(1))return 5;
    puts("OWNED_CONST_OK");
    return 0;
}
