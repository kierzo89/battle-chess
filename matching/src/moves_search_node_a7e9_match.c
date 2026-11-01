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
extern void copy_bytes(void *,void *,int), fatal_error(int), search_moves(void), store_line(Move);
extern int attacked(int,int);
int search_node(int alpha,int beta,int depth,SearchOptions options,Move *line)
{
    int result;
    SearchFrame *frame;
    copy_bytes(search_frame+1,search_frame,222);
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
       !attacked(opponent,pieces[current_side][0].square)) frame->best=0;
    else store_line(frame->line[history_index]);
finish:
    result=frame->best;
    search_frame--;
    return result;
}
