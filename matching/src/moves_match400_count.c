/* Pending; not an exact byte match. */
typedef struct {int from,to,flag; unsigned char kind,capture;} Move;
extern int quiet_9bbc();
extern Move moves_88e4[];
extern int counter_9880;
int count_9bfd()
{
    int n;
    int result;
    n=0;
    while (quiet_9bbc(&moves_88e4[counter_9880-n])) n++;
    result=n;
    return result;
}
