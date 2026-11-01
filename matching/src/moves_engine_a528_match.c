/* REA A528. Complete355-byte MSC5 /AS /Zi reconstruction. */
typedef struct {int a,b,c,d;} FourWords;
extern void far begin_wait();
extern void far draw_progress();
extern void far end_wait();
extern int current_side;
extern unsigned char search_side, search_active;
extern void select_mode(), prepare_85c4(), prepare_85c5(), setup_search(), refresh();
extern int interrupted, finished, ready, input_state, search_level;
extern long clock_value;
extern int position_score, lower_bound, upper_bound, iteration, best, window_limit, first_score;
extern FourWords initial_move, working_move;
extern int clamp(), search_window(), abs_i16(), stop_search(), obtain_input();
extern void poll_input(), accept_input();
void run_search(int depth)
{
    int score;
    /* The original stores this clock snapshot in its frame. */
    long started;
    begin_wait();
    search_side=current_side;
    search_active=1;
    select_mode(3);
    prepare_85c4();
    prepare_85c5();
    interrupted=0;
    setup_search();
    draw_progress();
    refresh();
    started=clock_value;
    upper_bound=lower_bound=-position_score;
    iteration=0;
    working_move=initial_move;
    best=position_score;
    window_limit=32767;
    do {
        if(iteration<=1) first_score=best;
        window_limit=clamp(window_limit,best-128);
        if(search_level==5) {
            window_limit=24576;
            if(iteration>0) iteration++;
        }
        iteration++;
        score=search_window(window_limit,32512);
        if(score<=window_limit && !interrupted && search_level!=5 && input_state>0) {
            best=window_limit;
            score=search_window(-32512,window_limit-8);
            input_state=2;
        }
    } while(!interrupted && iteration<depth && input_state>1 && abs_i16(best)<28800 && !stop_search());
    poll_input();
    while(!finished && !interrupted) {
        if(!ready) ready=obtain_input();
        if(ready) accept_input();
    }
    refresh();
    search_active=0;
    end_wait();
}
