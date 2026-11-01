typedef union {unsigned word;struct{unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
typedef struct {int flag,lower,upper;} SearchOptions;
typedef struct {
    int alpha,beta,depth;
    SearchOptions options;
    Move *line;
    int quiet,best,child_depth;
    SearchOptions child_options;
    int research,phase;
    Move pv[24];
} SearchFrame;
extern SearchFrame *search_frame;
extern int history_index,first_score,best,search_level,window_limit;
extern Move history_tail[];
extern int count_9bfd(void),repetition_9c34(int);
extern void *memcpy(void *,const void *,unsigned);

int prune_b2ae(void)
{
    int a,b,c,d;
    a=0;
    if(history_index==1) {
        d=count_9bfd();
        c=repetition_9c34(0);
        if(c>=3) {
            a=1;
            search_frame->child_options.upper=0;
            return a;
        }
        b=0;
        if(d>=96) b=3;
        else if(c>=2) b=2;
        else if(d>=20) b=1;
        search_frame->child_options.lower+=(first_score/4)*b;
        search_frame->child_options.upper+=(first_score/4)*b;
    }
    if(history_index>=3) {
        c=repetition_9c34(1);
        if(c>=2) {
            a=1;
            search_frame->child_options.upper=0;
            return a;
        }
    }
    return a;
}

void update_b383(void)
{
    memcpy(search_frame->line,search_frame->pv,192);
    search_frame->line[history_index]=history_tail[history_index];
    if(history_index==0) {
        best=search_frame->best;
        if(search_level==5) search_frame->best=window_limit;
    }
}
