typedef union {unsigned word;struct{unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
extern int menu_enabled_0ef0,waiting_0eee,view_mode_053a,history_index,book_choice_offset;
extern int state_cbd2,state_934c,hint_score_964c,best;
extern Move hint_line[],working_move,initial_move;
extern void trim_history(void),prepare_hint_8384(void),accept_hint_82db(void),run_search(int),flash_move_889c(int *);
void prompt_893c(void)
{
    struct {int waiting,help;} saved;
    saved.help=menu_enabled_0ef0;
    saved.waiting=waiting_0eee;
    menu_enabled_0ef0=waiting_0eee=0;
    trim_history();
    if(view_mode_053a) {
        prepare_hint_8384();
        history_index=0;
        if(book_choice_offset>0) {
            accept_hint_82db();
            goto display;
        }
    }
    state_cbd2=1;
    state_934c=0;
    history_index=0;
    run_search(2);
display:
    history_index=-1;
    hint_line[0]=working_move;
    hint_line[1]=initial_move;
    hint_score_964c=-best;
    flash_move_889c((int *)hint_line);
    hint_line[0]=initial_move;
    menu_enabled_0ef0=saved.help;
    waiting_0eee=saved.waiting;
}

extern int view_mode_053a, ready_9856;
extern long requested_limit, limit;
extern long timer_b[];
extern long get_number();

void set_limit()
{
    int previous;
    previous = view_mode_053a;
    view_mode_053a = ready_9856 >> 8;
    if (view_mode_053a == 0)
        requested_limit = 6L;
    else if (view_mode_053a == 10) {
        if (limit = get_number() * 60L)
            requested_limit = limit;
        else
            view_mode_053a = previous;
    } else {
        requested_limit = 5 << (view_mode_053a - 1);
        timer_b[0] = timer_b[1] = 0L;
    }
}

extern int state_cbd2, state_934c;
extern long requested_limit, limit;

void begin_turn()
{
    state_cbd2 = 1;
    state_934c = 0;
    limit = requested_limit;
    if (limit < 3L)
        limit = 3L;
}
