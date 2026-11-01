/* REA A943. Complete533-byte MSC5 /AS /Zi reconstruction.
 * home_pawn is the indexed view of the canonical8DEA search-state base. */
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
extern SearchFrame *search_frame;
extern int history_index,current_side,opponent,side_piece_counts[],home_pawn[];
extern Move history[],history_tail[],search_pair_moves[][2];
extern Piece pieces[2][16];
extern Cell board[];
extern int try_move_ab58(void),capture_moves_b44a(int),quiet_moves_b5ea(int);
extern int stage_b860(void),stage_b8f4(void),legal_move(Move);
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
               legal_move(history_tail[history_index]) &&
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
