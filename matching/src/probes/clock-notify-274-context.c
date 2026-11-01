typedef union {unsigned word;struct {unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
extern long time(long *);
extern long clock_epoch,clock_sample,clock_value,timer_b[];
extern void notify_866d(Move);
extern void apply_9749(Move,int);
extern Move history[],current,selected_move;
extern int history_index,move_count,temporary,opponent,current_side;

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

void commit_move_8632(void)
{
    register Move *move;
    move=history+2+history_index;
    selected_move=*move=current;
    notify_wrapper_861b(*move);
}

void notify_866d(Move move)
{
    history_index++;
    move_count++;
    apply_9749(move,0);
    temporary=opponent;
    opponent=current_side;
    current_side=temporary;
}

void notify_86a1(Move move)
{
    temporary=opponent;
    opponent=current_side;
    current_side=temporary;
    apply_9749(move,1);
    move_count--;
    history_index--;
}
