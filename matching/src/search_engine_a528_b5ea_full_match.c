/* Fifteen contiguous reconstructed search functions, A528..B5E9.
 * Shared types describe the observed ABI; historical TU attribution is unknown. */
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
extern void fatal_error(int);
void store_line(Move);
extern int attacked_9a50(int,int);
int try_move_ab58(void);
extern int capture_moves_b44a(int),quiet_moves_b5ea(int);
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

extern int paused;
extern int preferred_move(void),prepare_af87(void),prune_b2ae(void);
extern void apply_9749(Move,int),update_b383(void);
extern int max_i16(int,int),min_i16(int,int),equal_state(Move *,Move *);

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

void store_line(Move move)
{
    if (move.detail.bytes.kind && (!history[history_index].detail.bytes.kind ||
                     history[history_index].to != move.to)) {
        if (!search_pair_moves[history_index][0].detail.bytes.kind ||
            equal_state(&move,&search_pair_moves[history_index][1])) {
            search_pair_moves[history_index][1] = search_pair_moves[history_index][0];
            search_pair_moves[history_index][0] = move;
        } else if (!equal_state(&move,&search_pair_moves[history_index][0]))
            search_pair_moves[history_index][1] = move;
    }
}

int update_best(int);
extern int piece_attacks(int,int,int,int);
extern int far evaluate_candidate(Move);
extern int rand(void),count_9bfd(void),repetition_9c34(int);

int preferred_move(void)
{
    int result,index;
    result=1;
    if (search_frame->phase) {
        if (equal_state(&history_tail[history_index],&search_frame->line[history_index]))
            return result;
        if (!search_frame->quiet && search_frame->phase!=2) {
            for (index=0;index<=1;index++)
                if (equal_state(&history_tail[history_index],&search_pair_moves[history_index][index]))
                    return result;
        }
    }
    result=0;
    return result;
}

int update_best(int score)
{
    int accepted;
    accepted=0;
    if (score<=search_frame->alpha) {
        accepted=1;
        if (search_frame->best<score) search_frame->best=score;
    }
    return accepted;
}

int prepare_af87(void)
{
 int a; /* returned status; retained stack local */
 register SearchFrame *b; /* current frame */
 int c; /* shallow candidate eligible for the bound test */
 b=search_frame;
 b->child_depth=b->depth-1;
 if(search_level==5) {
  apply_9749(history_tail[history_index],0);
  if(attacked_9a50(opponent,pieces[current_side][0].square)) goto undo;
   if(!history_index) input_state++;
   check_state[history_index+1]=0;
   home_pawn[history_index+2]=-1;
   b->child_options.lower=0;
   b->child_options.upper=0;
   if(b->child_depth<=0) {
    if(b->child_depth==0)
     check_state[history_index+1]=attacked_9a50(current_side,pieces[opponent][0].square);
    if(!check_state[history_index+1] && update_best(b->child_options.lower)) goto undo;
   }
  goto accepted;
 }
 {
  { /* Candidate score and shallow-bound phase. */
  if(iteration<=1 && (b->quiet & (history_index>=2)) &&
     !((history[history_index-1].to==history_tail[history_index].from) |
       (history_tail[history_index].detail.bytes.capture<history_tail[history_index].detail.bytes.kind) |
       (b->phase==1))) goto rejected;
  b->child_options.lower=-b->options.lower+evaluate_candidate(history_tail[history_index]);
  check_state[history_index+1]=piece_attacks(history_tail[history_index].detail.bytes.kind,current_side,
                                         history_tail[history_index].to,pieces[opponent][0].square);
  if(check_state[history_index+1]) b->child_depth=b->depth;
  home_pawn[history_index+2]=home_pawn[history_index];
  if(history_tail[history_index].detail.bytes.kind==6 &&
     ((history_tail[history_index].to<24)|(history_tail[history_index].to>=96))) {
   home_pawn[history_index+2]=history_tail[history_index].to;
   b->child_depth=b->depth;
  }
  c=(!check_state[history_index+1]) & (b->child_depth<=0) & (history_index>0);
  if(c && update_best(b->child_options.lower)) goto rejected;
  }
  apply_9749(history_tail[history_index],0);
  if(attacked_9a50(opponent,pieces[current_side][0].square)) goto undo;
  { /* Validate the inherited home-pawn square after applying the move. */
   if(home_pawn[history_index+2]>=0 &&
      ((board[home_pawn[history_index+2]].side!=current_side)|
       (board[home_pawn[history_index+2]].kind!=6))) home_pawn[history_index+2]=-1;
   if(!history_index) input_state++;
   if(!history_index) b->child_options.lower+=rand()&7;
   b->child_options.upper=b->child_options.lower;
  }
 }
accepted:
 a=0;return 0;
undo:
 apply_9749(history_tail[history_index],1);
rejected:
 a=1;return 1;
}

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

extern Move history_storage[];
extern int pawn_step[],piece_counts[];
int promote_search_b3e6(void);

int promote_search_b3e6(void)
{
    int result,kind;
    result=1;
    history_tail[history_index].flag=1;
    for(kind=2;kind<=5;kind++) {
        history_tail[history_index].detail.bytes.kind=kind;
        if(try_move_ab58()) return result;
    }
    history_tail[history_index].flag=0;
    result=0;
    return 0;
}

int capture_moves_b44a(int square)
{
    int result,base,from,piece_index;
    register Move *record;
    result=1;
    record=&history_storage[history_index+104];
    record->detail.bytes.capture=board[square].kind;
    record->flag=0;
    record->to=square;
    record->detail.bytes.kind=6;
    base=record->to-pawn_step[current_side];
    for(from=base-1;from<=base+1;from++) {
        if(from!=base && !(from&0x88) &&
           ((board[from].kind==6) & (board[from].side==current_side))) {
            history_tail[history_index].from=from;
            if((history_tail[history_index].to<8) | (history_tail[history_index].to>=0x70)) {
                if(promote_search_b3e6()) return result;
            } else if(try_move_ab58()) return result;
        }
    }
    for(piece_index=piece_counts[current_side];piece_index>=0;piece_index--) {
        if((pieces[current_side][piece_index].kind!=0) & (pieces[current_side][piece_index].kind!=6)) {
            if(piece_attacks(pieces[current_side][piece_index].kind,current_side,
                             pieces[current_side][piece_index].square,square)) {
                history_tail[history_index].from=pieces[current_side][piece_index].square;
                history_tail[history_index].detail.bytes.kind=pieces[current_side][piece_index].kind;
                if(try_move_ab58()) return result;
            }
        }
    }
    result=0;
    return 0;
}
