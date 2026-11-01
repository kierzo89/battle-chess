typedef union {unsigned word;struct{unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
typedef union {long word;struct{unsigned first,second;} bits;} PawnMask;
extern int current_side,opponent,history_index,best,temporary;
extern int evaluation_delta,castle_bonus[],pawn_step[],piece_value[];
extern int piece_square[];
extern unsigned file_mask[],pawn_mask;
extern PawnMask pawn_state[][2];
extern void far castle_95df(int,int *,int *);
extern int far pawn_score(int,int);

int far evaluation_abs(register int value)
{
    if(value<0) value=-value;
    return value;
}

int far evaluation_piece(int kind,int side,int square)
{
    int result;
    return result=piece_square[kind*120+side*720+square]+piece_value[kind];
}

int far evaluation_pawn_remove(int side,int file)
{
    int result;
    pawn_mask=~file_mask[file];
    pawn_state[history_index+1][side].bits.first=
        (pawn_state[history_index+1][side].bits.first & pawn_mask) |
        pawn_state[history_index+1][side].bits.second;
    pawn_state[history_index+1][side].bits.second &= pawn_mask;
    return result=pawn_score(history_index,side)-pawn_score(history_index-1,side);
}

int far evaluation_pawn_move(int side,int to,int from)
{
    int result;
    unsigned mask;
    pawn_mask=file_mask[to];
    mask=~file_mask[from];
    pawn_state[history_index+1][side].bits.second |=
        pawn_state[history_index+1][side].bits.first & pawn_mask;
    pawn_state[history_index+1][side].bits.first=
        (pawn_state[history_index+1][side].bits.first & mask) |
        pawn_state[history_index+1][side].bits.second | pawn_mask;
    pawn_state[history_index+1][side].bits.second &= mask;
    return result=pawn_score(history_index,side)-pawn_score(history_index-1,side);
}

int far evaluate_candidate(Move move)
{
    int a,b,c,d,e;
    a=6;
    evaluation_delta=0;
    if(move.flag) {
        if(move.detail.bytes.kind==1) {
            castle_95df(move.to,&d,&c);
            evaluation_delta=evaluation_piece(3,current_side,d)-evaluation_piece(3,current_side,c);
            if(move.to>move.from) evaluation_delta+=castle_bonus[1];
            else evaluation_delta+=castle_bonus[0];
        } else if(move.detail.bytes.kind==6) {
            b=move.to-pawn_step[current_side];
            evaluation_delta=evaluation_piece(6,opponent,b);
        } else {
            evaluation_delta=evaluation_piece(move.detail.bytes.kind,current_side,move.from)-
                evaluation_piece(6,current_side,move.from)+
                evaluation_pawn_remove(current_side,move.from&7);
        }
    }
    if(move.detail.bytes.capture) {
        evaluation_delta+=evaluation_piece(move.detail.bytes.capture,opponent,move.to);
        if(evaluation_abs(best)>=256 && move.detail.bytes.capture!=6 &&
           ((temporary==opponent)==(best>=0))) evaluation_delta-=16;
    }
    pawn_state[history_index+1][0].word=pawn_state[history_index][0].word;
    pawn_state[history_index+1][1].word=pawn_state[history_index][1].word;
    if((move.detail.bytes.kind==6) & ((move.detail.bytes.capture!=0) | move.flag))
        evaluation_delta+=evaluation_pawn_move(current_side,move.to&7,move.from&7);
    if(((move.detail.bytes.kind==6) & move.flag) | (move.detail.bytes.capture==6))
        evaluation_delta-=evaluation_pawn_remove(opponent,move.to&7);
    return a=evaluation_delta+evaluation_piece(move.detail.bytes.kind,current_side,move.to)-
        evaluation_piece(move.detail.bytes.kind,current_side,move.from);
}
