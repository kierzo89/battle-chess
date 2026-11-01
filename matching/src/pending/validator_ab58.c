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
extern Move initial,history_tail[];
extern int history_index,current_side,opponent,search_mode,check_state[];
extern int interrupted,input_state,ready,paused,timer_value,timer_limit,iteration;
extern int abort_aeba(void),prepare_af87(void),prune_b2ae(void);
extern int search_node(int,int,int,SearchOptions,Move *);
extern void copy_bytes(void *,void *,int),apply_move(Move,int);
extern void poll_8aaa(void),dispatch_baaf(void),tick_85dd(void),update_b383(void);
extern int obtain_0254(void),limit_a68b(void),max_i16(int,int),min_i16(int,int),equal_state(Move *,Move *);
int try_move_ab58(void)
{
    int a;
    register SearchFrame *b;
    int c,d,e;
    b=search_frame;
    a=0;
    if(abort_aeba()) return a;
    if(history_index<23) {
        b->pv[history_index+1]=initial;
        if(!b->phase) copy_bytes(b->pv,b->line,192);
    }
    b->child_options.flag=0;
    b->research=0;
    if(b->options.flag) {
        if(!b->phase) b->child_options.flag=(b->line[history_index+1].detail.bytes.kind!=0);
        else b->research=(b->best>=b->alpha);
    }
retry:
    if(prepare_af87()) return a;
    if(search_mode==5 && ((b->child_depth<=0)&!check_state[history_index])) goto restore;
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
    apply_move(history_tail[history_index],1);
    if(interrupted) {a=1;return 1;}
    c=input_state;
    poll_8aaa();
    if(!ready) ready=obtain_0254();
    if(paused) {
        while(paused) {
            if(e=obtain_0254()) ready=e;
        }
    }
    if(!ready) ready=obtain_0254();
    if(ready) dispatch_baaf();
    if(!interrupted && input_state && (!history_index || !c)) {
        tick_85dd();
        if(timer_value>timer_limit) interrupted=limit_a68b();
    }
    if(input_state && iteration<=1) interrupted=0;
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
