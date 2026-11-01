/* B44A: test pawn and non-pawn captures onto a candidate destination. */
typedef union {unsigned word;struct {unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
typedef struct {unsigned char kind,side;int index;} Cell;
typedef struct {unsigned char square,kind;} Piece;
extern Move history_storage[];
extern Move history_tail[];
extern Cell board[];
extern Piece pieces[2][16];
extern int history_index,current_side,pawn_step[],piece_counts[];
extern int promote_search_b3e6(void),try_move_ab58(void),piece_attacks(int,int,int,int);
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
