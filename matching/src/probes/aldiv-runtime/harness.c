/* Target-free arithmetic control. Real C5 compound assignment selects ALDIV. */
extern int puts(char *);
long dividend=-1001L;
void divide(long divisor) { dividend/=divisor; }
int main(void)
{
 divide(10L); if(dividend!=-100L)return 1;
 divide(-3L); if(dividend!=33L)return 2;
 dividend=2147483647L;divide(65536L);if(dividend!=32767L)return 3;
 dividend=-2147483647L;divide(65536L);if(dividend!=-32767L)return 4;
 dividend=7L;divide(99L);if(dividend!=0L)return 5;
 puts("ALDIV_OK");return 0;
}
