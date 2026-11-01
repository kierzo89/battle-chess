/* REA A348: generate candidate states from piece, castling and pawn history. */
typedef union {unsigned word;struct{unsigned char low,high;} byte;} Kind;
typedef struct{int from,to,special;Kind kind;} Move;
typedef union {unsigned word;struct{unsigned char square,piece;} byte;} Piece;
typedef struct{Piece piece[16];} SideInfo;
typedef struct{int from,to;} Castle;
extern int state_count,state_index,side,opponent,side_piece_counts[],history_index;
extern Move candidate_move,history[];
extern SideInfo side_info[];
extern Castle castle[2][2];
extern void collect_a045(void),collect_a181(void),append_9fdf(void);
extern int legal_9db3(int,int,int,int),abs_i16(int);
void generate_a348(void)
{
    /* a=neighbor square, b=piece index, c=castling-table index. */
    int a,b,c;
    c = 6;
    state_count = 0;
    state_index = 0;
    for (b=1;b<=side_piece_counts[opponent];b++) {
        if (side_info[opponent].piece[b].byte.piece) {
            candidate_move.from = side_info[opponent].piece[b].byte.square;
            collect_a045();
        }
    }
    candidate_move.special = 1;
    candidate_move.kind.byte.low = 1;
    candidate_move.kind.byte.high = 0;
    for (c=1;c>=0;c--) {
        candidate_move.from = castle[side][c].from;
        candidate_move.to = castle[side][c].to;
        if (legal_9db3(candidate_move.from,candidate_move.to,candidate_move.special,candidate_move.kind.word)) append_9fdf();
    }
    for (b=side_piece_counts[side];b>=0;b--) {
        if (side_info[side].piece[b].byte.piece) {
            candidate_move.to = side_info[side].piece[b].byte.square;
            collect_a181();
        }
    }
    if (history[history_index].kind.byte.low == 6 &&
        abs_i16(history[history_index].from-history[history_index].to) >= 32) {
        candidate_move.special = 1;
        candidate_move.kind.byte.low = 6;
        candidate_move.kind.byte.high = 0;
        candidate_move.from = (history[history_index].from+history[history_index].to)/2;
        for(a=history[history_index].from-1;a<=history[history_index].from+1;a++) {
            if (a!=history[history_index].from && !(a&0x88)) {
                candidate_move.to = a;
                if (legal_9db3(candidate_move.from,candidate_move.to,candidate_move.special,candidate_move.kind.word)) append_9fdf();
            }
        }
    }
}
