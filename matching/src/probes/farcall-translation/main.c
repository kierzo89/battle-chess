extern int far translation_caller(int);
extern int far translation_target(int);
int main(void)
{
    if(translation_target(7)!=48)return 1;
    if(translation_caller(7)!=51)return 2;
    if(translation_caller(0)!=40)return 3;
    if(translation_caller(-4)!=-44)return 4;
    return 0;
}
