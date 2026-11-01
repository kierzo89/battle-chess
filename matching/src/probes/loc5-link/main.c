extern int far loc5_target(int);
int shared_state=3;
int main(void)
{
    int (far *selected)(int);
    selected=loc5_target;
    return selected(7)!=24;
}
