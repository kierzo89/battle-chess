/* A799..A942: two exact functions in one complete426-byte CODE chunk. */
/* REA A7E9. Complete346-byte MSC5 /AS /Zi reconstruction.
 * The222-byte search frame has an observed18-byte prefix and204-byte tail. */
typedef struct {int to,from,flag;unsigned char kind,capture;} Move;
typedef struct {int flag,lower,upper;} SearchOptions;
typedef struct {
    int alpha,beta,depth;
    SearchOptions options;
    Move *line;
    int quiet,best;
    char remaining[204];
} SearchFrame;
typedef struct {unsigned char square,kind;} Piece;
extern SearchFrame *search_frame, search_stack_end[];
extern int history_index, interrupted, current_side, opponent;
extern int check_state[];
extern Piece pieces[2][16];
extern void *memcpy(void *,const void *,unsigned);
extern void fatal_error(int), search_moves(void), store_line(Move);
extern int attacked_9a50(int,int);
extern Move working_move;
extern SearchOptions search_options;
extern int input_state, iteration, best;
int search_node(int,int,int,SearchOptions,Move *);

int search_window(int alpha,int beta)
{
    /* The original frame reserves a second, unread two-byte slot. */
    int value, unused;
    search_options.flag=(working_move.kind!=0);
    input_state=0;
    value=search_node(alpha,beta,iteration,search_options,&working_move);
    if(!input_state) best=value;
    return value;
}

int search_node(int alpha,int beta,int depth,SearchOptions options,Move *line)
{
    int result;
    SearchFrame *frame;
    memcpy(search_frame+1,search_frame,222);
    search_frame++;
    if(search_frame==search_stack_end) fatal_error(10);
    frame=search_frame;
    frame->alpha=alpha;
    frame->beta=beta;
    frame->depth=depth;
    frame->options=options;
    frame->line=line;
    frame->quiet=(check_state[history_index]==0) & (frame->depth<=0);
    if(frame->quiet) {
        frame->best=-frame->options.upper;
        if(frame->alpha<frame->best) {
            frame->alpha=frame->best;
            if(frame->best>=frame->beta) goto finish;
        }
    } else frame->best=-(32000-history_index*128);
    search_moves();
    if(interrupted) goto finish;
    if(frame->best==-(32000-history_index*128) &&
       !attacked_9a50(opponent,pieces[current_side][0].square)) frame->best=0;
    else store_line(frame->line[history_index]);
finish:
    result=frame->best;
    search_frame--;
    return result;
}
