/* Six contiguous reconstructed search functions, A528..AB57.
 * Shared types describe the observed ABI; historical TU attribution is unknown. */
typedef union {unsigned word;struct{unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
typedef struct {int flag,lower,upper;} SearchOptions;
typedef struct {
    int alpha,beta,depth;
    SearchOptions options;
    Move *line;
    int quiet,best;
    char middle[10];
    int phase;
    char remaining[192];
} SearchFrame;
typedef struct {unsigned char square,kind;} Piece;
typedef struct {unsigned char kind,side;int index;} Cell;
extern void far begin_wait();
extern void far draw_progress();
extern void far end_wait();
extern unsigned char search_side,search_active;
extern int current_side,interrupted,finished,ready,input_state,search_level;
extern int position_score,iteration,best,window_limit,first_score;
extern long clock_value,limit;
extern int modes[],check_state[],home_pawn[],pawn_home[];
extern Move initial_move,working_move,search_pair_moves[24][2];
extern void select_mode(int),prepare_85c4(void),prepare_85c5(void),refresh(void);
extern int clamp(int,int),abs_i16(int),obtain_input(void);
extern void poll_input(void),accept_input(void);
extern SearchFrame *search_frame,search_stack_end[];
extern int history_index,opponent,side_piece_counts[];
extern Piece pieces[2][16];
extern Cell board[];
extern Move history[],history_tail[];
extern SearchOptions search_options;
extern void *memcpy(void *,const void *,unsigned);
extern void fatal_error(int),store_line(Move);
extern int attacked_9a50(int,int);
extern int try_move_ab58(void),capture_moves_b44a(int),quiet_moves_b5ea(int);
extern int stage_b860(void),stage_b8f4(void),legal_move(int,int,int,MoveKind);
void setup_search(void),search_moves(void);
int stop_search(void),search_window(int,int),search_node(int,int,int,SearchOptions,Move *);

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
    search_options.upper=search_options.lower=-position_score;
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

int stop_search(void)
{
    if (finished) {
        refresh();
        return clock_value >= limit || modes[search_side] != 1;
    }
    return 0;
}

void setup_search(void)
{
    int i,side,square,j;
    for (i=0;i<=23;i++)
        for (side=0;side<=1;side++)
            search_pair_moves[i][side] = initial_move;
    check_state[0] = 0;
    home_pawn[0] = -1;
    home_pawn[1] = -1;
    for (j=0;j<=1;j++) {
        for (square=pawn_home[j];square<=pawn_home[j]+7;square++) {
            if (board[square].kind==6 && board[square].side==j) {
                if (j==current_side) home_pawn[0]=square;
                else home_pawn[1]=square;
            }
        }
    }
}

int search_window(int alpha,int beta)
{
    /* The original frame reserves a second, unread two-byte slot. */
    int value, unused;
    search_options.flag=(working_move.detail.bytes.kind!=0);
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

void search_moves(void)
{
    Move *previous_move;
    int index,killer_index;
    if(search_frame->line[history_index].detail.bytes.kind) {
        history_tail[history_index]=search_frame->line[history_index];
        search_frame->phase=0;
        if(try_move_ab58()) return;
    }
    previous_move=&history[history_index];
    if(previous_move->detail.bytes.kind && previous_move->detail.bytes.kind!=1) {
        search_frame->phase=1;
        if(capture_moves_b44a(previous_move->to)) return;
    }
    search_frame->phase=2;
    if(!search_frame->quiet) {
        for(killer_index=0;killer_index<=1;killer_index++) {
            history_tail[history_index]=search_pair_moves[history_index][killer_index];
            if(history_tail[history_index].detail.bytes.kind &&
               legal_move(history_tail[history_index].to,history_tail[history_index].from,
                          history_tail[history_index].flag,history_tail[history_index].detail) &&
               try_move_ab58()) return;
        }
    }
    search_frame->phase=3;
    for(index=1;index<=side_piece_counts[opponent];index++) {
        if(pieces[opponent][index].kind &&
           ((previous_move->to!=pieces[opponent][index].square) | (previous_move->detail.bytes.kind==0)) &&
           capture_moves_b44a(pieces[opponent][index].square)) return;
    }
    if(search_frame->quiet && home_pawn[history_index]>=0 &&
       ((board[home_pawn[history_index]].kind==6) &
        (board[home_pawn[history_index]].side==current_side)) &&
       quiet_moves_b5ea(home_pawn[history_index])) return;
    if(!search_frame->quiet) {
        if(stage_b860()) return;
        for(index=side_piece_counts[current_side];index>=0;index--) {
            if(pieces[current_side][index].kind &&
               quiet_moves_b5ea(pieces[current_side][index].square)) return;
        }
    }
    if(stage_b8f4()) return;
}
