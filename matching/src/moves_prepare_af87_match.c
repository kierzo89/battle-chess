/* AF87: prepare one search candidate.
 * The far evaluator is the original 0FDF:0D25 alias, image10B15. */
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
typedef struct {unsigned char square,kind;} Piece;
typedef struct {unsigned char kind,side;int index;} Cell;
extern SearchFrame *search_frame;
extern Move history[],history_tail[];
extern Piece pieces[2][16];
extern Cell board[];
extern int search_level,history_index,current_side,opponent,input_state,iteration;
extern int check_state[],home_pawn[];
extern void apply_9749(Move,int);
extern int attacked_9a50(int,int),piece_attacks(int,int,int,int),update_best(int);
extern int far evaluate_candidate(Move);
extern int rand(void);
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
