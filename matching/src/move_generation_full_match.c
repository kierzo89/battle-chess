/* Diagnostic candidate:1269 matching procedure bytes, but1270-byte CODE SEGDEF.
 * Its end alignment is not credited; canonical source is move_engine_9a50_full_match.c. */
typedef struct {unsigned char kind,side; int index;} Cell;
typedef struct {unsigned char square,kind;} Piece;
typedef union {unsigned word;struct{unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
extern Move candidate_move;
extern Cell board[];
extern Piece pieces[2][16];
extern int current_side, pawn_step[], piece_counts[];
extern int move_count;
extern Move move_list[];
extern int piece_attacks();
void append_move(void)
{
    if (move_count >= 80)
        return;
    move_list[move_count++] = candidate_move;
}

void append_promotions(void)
{
    int kind;
    candidate_move.flag = 1;
    for (kind = 2; kind <= 5; ++kind) {
        candidate_move.detail.bytes.kind = kind;
        append_move();
    }
    candidate_move.flag = 0;
}

void generate_captures()
{
    int base, square, piece_index;
    candidate_move.flag=0;
    candidate_move.detail.bytes.capture=board[candidate_move.to].kind;
    candidate_move.detail.bytes.kind=6;
    base=candidate_move.to-pawn_step[current_side];
    for(square=base-1;square<=base+1;square++) {
        if(square!=base && !(square&136) &&
           ((board[square].kind==6) & (board[square].side==current_side))) {
            candidate_move.from=square;
            if((candidate_move.to<8) | (candidate_move.to>=112)) append_promotions();
            else append_move();
        }
    }
    for(piece_index=piece_counts[current_side];piece_index>=0;piece_index--) {
        if((pieces[current_side][piece_index].kind!=0) & (pieces[current_side][piece_index].kind!=6)) {
            if(piece_attacks(pieces[current_side][piece_index].kind,current_side,
                             pieces[current_side][piece_index].square,candidate_move.to)) {
                candidate_move.from=pieces[current_side][piece_index].square;
                candidate_move.detail.bytes.kind=pieces[current_side][piece_index].kind;
                append_move();
            }
        }
    }
}


extern int steps[], knight_steps[];
extern int state_index, opponent, side_piece_counts[], history_index;
extern Move history[];
typedef struct {int from,to;} Castle;
extern Castle castle[2][2];
extern int legal_9db3(int,int,int,int),abs_i16(int);

void generate_quiet()
{
    /* Neutral recovered-local names: ray step, first direction, last
     * direction, candidate square, and direction index, respectively. */
    int local_e, local_a, local_b, local_c, local_d;
    candidate_move.flag=0;
    candidate_move.detail.bytes.kind=board[candidate_move.from].kind;
    candidate_move.detail.bytes.capture=0;
    switch(candidate_move.detail.bytes.kind) {
    case 1:
        for(local_d=7;local_d>=0;local_d--) {
            local_c=steps[local_d]+candidate_move.from;
            if(!(local_c&136) && board[local_c].kind==0) {
                candidate_move.to=local_c;
                append_move();
            }
        }
        break;
    case 5:
        for(local_d=7;local_d>=0;local_d--) {
            local_c=knight_steps[local_d]+candidate_move.from;
            if(!(local_c&136) && board[local_c].kind==0) {
                candidate_move.to=local_c;
                append_move();
            }
        }
        break;
    case 2:
    case 3:
    case 4:
        local_b=7;
        local_a=0;
        if(candidate_move.detail.bytes.kind==3) local_b=3;
        if(candidate_move.detail.bytes.kind==4) local_a=4;
        for(local_d=local_b;local_d>=local_a;local_d--) {
            local_e=steps[local_d];
            local_c=local_e+candidate_move.from;
            while(!(local_c&136)) {
                if(board[local_c].kind) break;
                candidate_move.to=local_c;
                append_move();
                local_c=local_e+candidate_move.to;
            }
        }
        break;
    case 6:
        candidate_move.to=pawn_step[current_side]+candidate_move.from;
        if(board[candidate_move.to].kind==0) {
            if((candidate_move.to<8) | (candidate_move.to>=112)) append_promotions();
            else {
                append_move();
                if((candidate_move.from<24) | (candidate_move.from>=96)) {
                    candidate_move.to+=candidate_move.to-candidate_move.from;
                    if(board[candidate_move.to].kind==0) append_move();
                }
            }
        }
        break;
    }
}

void generate_a348(void)
{
    /* a=neighbor square, b=piece index, c=castling-table index. */
    int a,b,c;
    c = 6;
    move_count = 0;
    state_index = 0;
    for (b=1;b<=side_piece_counts[opponent];b++) {
        if (pieces[opponent][b].kind) {
            candidate_move.to = pieces[opponent][b].square;
            generate_captures();
        }
    }
    candidate_move.flag = 1;
    candidate_move.detail.bytes.kind = 1;
    candidate_move.detail.bytes.capture = 0;
    for (c=1;c>=0;c--) {
        candidate_move.to = castle[current_side][c].from;
        candidate_move.from = castle[current_side][c].to;
        if (legal_9db3(candidate_move.to,candidate_move.from,candidate_move.flag,candidate_move.detail.word)) append_move();
    }
    for (b=side_piece_counts[current_side];b>=0;b--) {
        if (pieces[current_side][b].kind) {
            candidate_move.from = pieces[current_side][b].square;
            generate_quiet();
        }
    }
    if (history[history_index].detail.bytes.kind == 6 &&
        abs_i16(history[history_index].to-history[history_index].from) >= 32) {
        candidate_move.flag = 1;
        candidate_move.detail.bytes.kind = 6;
        candidate_move.detail.bytes.capture = 0;
        candidate_move.to = (history[history_index].to+history[history_index].from)/2;
        for(a=history[history_index].to-1;a<=history[history_index].to+1;a++) {
            if (a!=history[history_index].to && !(a&0x88)) {
                candidate_move.from = a;
                if (legal_9db3(candidate_move.to,candidate_move.from,candidate_move.flag,candidate_move.detail.word)) append_move();
            }
        }
    }
}
