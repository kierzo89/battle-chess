typedef union {unsigned word;struct {unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
extern long time(long *);
extern long clock_epoch,clock_sample,clock_value,timer_b[];
extern void notify_866d(Move);

void prepare_85c4(void) {}

void prepare_85c5(void)
{
    clock_sample=clock_epoch=time(0);
}

void refresh(void)
{
    clock_sample=time(0);
    clock_value=clock_sample-clock_epoch;
}

void charge_clock_85fd(int side)
{
    refresh();
    timer_b[side]+=clock_value;
}

void notify_wrapper_861b(Move move)
{
    notify_866d(move);
}
