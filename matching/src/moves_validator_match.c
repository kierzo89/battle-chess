/* REAAB58: validate and search one candidate using the222-byte frame. */
typedef union {unsigned word;struct{unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
typedef struct {int flag,lower,upper;} SearchOptions;
typedef struct SearchFrame {
    int alpha,beta,depth;
    SearchOptions options;
    Move *line;
    int quiet,best,child_depth;
    SearchOptions child_options;
    int research,phase;
    Move pv[24];
} SearchFrame;
extern SearchFrame *search_frame;
extern Move initial_move,history_tail[];
extern int history_index,current_side,opponent,search_level,check_state[];
extern int interrupted,finished,ready,paused,best,window_limit,iteration;
extern int preferred_move(void),prepare_af87(void),prune_b2ae(void);
extern int search_node(int,int,int,SearchOptions,Move *);
extern void *memcpy(void *,const void *,unsigned);
extern void apply_9749(Move,int);
extern void poll_input(void),accept_input(void),refresh(void),update_b383(void);
extern int obtain_input(void),stop_search(void),max_i16(int,int),min_i16(int,int),equal_state(Move *,Move *);
int try_move_ab58(void)
{
    int a; /* returned status */
    register SearchFrame *b;
    int c,d,e; /* input snapshot, side swap, polled key */
    b=search_frame;
    a=0;
    if(preferred_move()) return a;
    if(history_index<23) {
        b->pv[history_index+1]=initial_move;
        if(!b->phase) memcpy(b->pv,b->line,192);
    }
    b->child_options.flag=0;
    b->research=0;
    if(b->options.flag) {
        if(!b->phase) b->child_options.flag=(b->line[history_index+1].detail.bytes.kind!=0);
        else b->research=(b->best>=b->alpha);
    }
retry:
    if(prepare_af87()) return a;
    if(search_level==5 && ((b->child_depth<=0)&!check_state[history_index+1])) goto restore;
    if(prune_b2ae()) goto restore;
    if(history_index>=23) goto restore;
    d=current_side;current_side=opponent;opponent=d;
    history_index++;
    if(b->research)
        b->child_options.upper=-search_node(-b->alpha-1,-b->alpha,b->child_depth,b->child_options,b->pv);
    else
        b->child_options.upper=-search_node(-b->beta,-b->alpha,b->child_depth,b->child_options,b->pv);
    history_index--;
    d=opponent;opponent=current_side;current_side=d;
restore:
    apply_9749(history_tail[history_index],1);
    if(interrupted) {a=1;return 1;}
    c=finished;
    poll_input();
    if(!ready) ready=obtain_input();
    if(paused) {
        while(paused) {
            if(e=obtain_input()) ready=e;
        }
    }
    if(!ready) ready=obtain_input();
    if(ready) accept_input();
    if(!interrupted && finished && (!history_index || !c)) {
        refresh();
        if(best>window_limit) interrupted=stop_search();
    }
    if(finished && iteration<=1) interrupted=0;
    b->best=max_i16(b->best,b->child_options.upper);
    if(equal_state(b->line+history_index,&history_tail[history_index])) update_b383();
    if(b->best>b->alpha) {
        update_b383();
        if(b->best>=b->beta) {a=1;return 1;}
        if(b->depth>=2 && b->options.flag && !b->research)
            b->best=min_i16(b->best+4,b->beta-1);
        b->alpha=b->best;
        if(b->research & !interrupted) {
            b->research=0;
            goto retry;
        }
    }
    return(a=interrupted);
}
