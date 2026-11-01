extern long clock_epoch,clock_sample,clock_value;
extern long time(long *);
long diagnostic_marker=0x12345678L;
int main(void)
{
    long now;
    if(clock_epoch!=0L||clock_sample!=0L||clock_value!=0L)return 1;
    if(diagnostic_marker!=0x12345678L)return 2;
    clock_epoch=0x12345678L;
    clock_sample=-123456789L;
    if(clock_epoch!=0x12345678L||clock_sample!=-123456789L)return 3;
    clock_epoch=-2147483647L;
    clock_sample=2147483647L;
    if(clock_epoch!=-2147483647L||clock_sample!=2147483647L)return 4;
    now=time((long *)0);
    if(now==-1L)return 5;
    clock_epoch=now;
    clock_sample=now+7L;
    clock_value=clock_sample-clock_epoch;
    if(clock_value!=7L)return 6;
    return 0;
}
