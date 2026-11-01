typedef union {unsigned word;struct {unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
extern long time(long *);
extern long clock_epoch,clock_sample,clock_value,timer_b[];
extern void notify_866d(Move);
extern void apply_9749(Move,int);
extern Move history[],current,selected_move;
extern int history_index,history_move_counter,temporary,opponent,current_side;

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
    history[history_index+2]=current;
    selected_move=current;
    notify_wrapper_861b(history[history_index+2]);
}

void notify_866d(Move move)
{
    history_index++;
    history_move_counter++;
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
    history_move_counter--;
    history_index--;
}

typedef struct {
    unsigned char square;
    char remaining[31];
} SideInfo;

extern void apply_9749(Move,int);
extern int attacked_9a50(int, int);
extern int current_side;
extern int opponent;
extern SideInfo side_info_9604[];

int probe_move_86d6(Move move)
{
    int result;
    apply_9749(move,0);
    result = attacked_9a50(opponent, side_info_9604[current_side].square);
    apply_9749(move,1);
    return result;
}

extern int ready_9856,command_active,mode_8176,modes[],current_side;
extern void prompt_8835(void),set_limit(void),init_surface(void),reset_graphics_3e4f(void),reset_display_0865(void),write_banner_157c(void),write_control_1562(void),poll_input(void);
void step_872a(void)
{
    if(ready_9856&0xf000) {ready_9856=0;return;}
    switch((unsigned char)ready_9856) {
    case 7: prompt_8835(); ready_9856=0;break;
    case 3: set_limit(); ready_9856=0;break;
    case 16:
        if(!command_active) {
            command_active=1;
            init_surface();reset_graphics_3e4f();reset_display_0865();
        }
        ready_9856=0;break;
    case 17:
        if(command_active) {
            command_active=0;
            init_surface();reset_graphics_3e4f();reset_display_0865();
        }
        ready_9856=0;break;
    case 8:mode_8176=1;ready_9856=0;break;
    case 9:mode_8176=0;ready_9856=0;break;
    case 10:mode_8176^=1;ready_9856=0;break;
    case 12:
        if(modes[0]==2 && ready_9856==0x20c)write_banner_157c();
        if((modes[0]=ready_9856>>8)==2)write_control_1562();
        if(current_side==0 && modes[0]==1) ready_9856=2;
        else ready_9856=0;
        break;
    case 13:
        if(modes[1]==2 && ready_9856==0x20d)write_banner_157c();
        if((modes[1]=ready_9856>>8)==2)write_control_1562();
        if(current_side==1 && modes[1]==1) ready_9856=2;
        else ready_9856=0;
        break;
    default:goto finish;
    }
finish:
    poll_input();
}

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
