typedef union {unsigned word;struct{unsigned char low,high;} byte;} Kind;
typedef struct{int from,to,special;Kind kind;} Move;
typedef union {unsigned word;struct{unsigned char square,piece;} byte;} Piece;
typedef struct{Piece piece[16];} SideInfo;
typedef struct{int from,to;} Castle;
extern int state_count,state_index,side,opponent,piece_counts[],history_index;
extern Move current,history[];
extern SideInfo side_info[];
extern Castle castle[2][2];
extern void collect_a045(void),collect_a181(void),append_9fdf(void);
extern int legal_9db3(int,int,int,int),abs_i16(int);
void generate_a348(void)
{
    int a,b,c;
    c = 6;
    state_count = 0;
    state_index = 0;
    for (b=1;b<=piece_counts[opponent];b++) {
        if (side_info[opponent].piece[b].byte.piece) {
            current.from = side_info[opponent].piece[b].byte.square;
            collect_a045();
        }
    }
    current.special = 1;
    current.kind.byte.low = 1;
    current.kind.byte.high = 0;
    for (c=1;c>=0;c--) {
        current.from = castle[side][c].from;
        current.to = castle[side][c].to;
        if (legal_9db3(current.from,current.to,current.special,current.kind.word)) append_9fdf();
    }
    for (b=piece_counts[side];b>=0;b--) {
        if (side_info[side].piece[b].byte.piece) {
            current.to = side_info[side].piece[b].byte.square;
            collect_a181();
        }
    }
    if (history[history_index].kind.byte.low == 6 &&
        abs_i16(history[history_index].from-history[history_index].to) >= 32) {
        current.special = 1;
        current.kind.byte.low = 6;
        current.kind.byte.high = 0;
        current.from = (history[history_index].from+history[history_index].to)/2;
        for(a=history[history_index].from-1;a<=history[history_index].from+1;a++) {
            if (a!=history[history_index].from && !(a&0x88)) {
                current.to = a;
                if (legal_9db3(current.from,current.to,current.special,current.kind.word)) append_9fdf();
            }
        }
    }
}
