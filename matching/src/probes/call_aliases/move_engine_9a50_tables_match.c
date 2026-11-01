/* 0x88 board movement, attack-bit, castling and initial piece tables.
   The mask view starts one word into the pawn/mask union: mask zero shares
   the negative pawn step and is unused by the reconstructed consumers. */
typedef struct { int destination, king_home; } CastleEndpoints;
typedef union {
    struct { int pawn_step[2]; unsigned piece_bits[6]; } initialized;
    struct { int first_pawn_step; unsigned by_kind[7]; } masks;
} PawnAndMasks;
typedef struct {
    int ray_step[8];
    int knight_step[8];
    PawnAndMasks pawn_and_masks;
    CastleEndpoints castle[2][2];
    int back_rank[8];
} MoveLookupTables;

/* Ordinary C reconstruction of the complete2692-byte CODE chunk9A50..A4D3.
 * Original names are unknown; address-compatible global views are explicit. */
typedef struct {unsigned char kind,side; int index;} Cell;
typedef struct {unsigned char square,kind;} Piece;
typedef union {unsigned word;struct{unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
extern Cell board[];
extern Piece pieces[2][16];
/* History views begin at88DC,88E4 and85A4; the last uses a104-record bias. */
extern Move candidate_move, move_list[], history[], history_tail[], history_storage[];
extern MoveLookupTables move_lookup_tables;
extern int current_side, opponent, history_index, castle_owner;
extern int piece_counts[], side_piece_counts[];
extern int move_count, state_index;
extern int pawn_attacks(int,int), piece_attacks(int,int,int,int), abs_i16(int);
extern unsigned lowbit(unsigned);
int original_piece_9b46(int,int);
int legal_move(Move);

int attacked_9a50(int side,int square)
{
    int index;
    register Piece *p;
    int result;
    result=1;
    if (pawn_attacks(side,square)) return result;
    p=&pieces[side][piece_counts[side]];
    index=piece_counts[side];
    for(;index>=0;index--,p--)
        if(p->kind && piece_attacks(p->kind,side,p->square,square)) return result;
    result=0;
    return result;
}

void far castle_flags_9ad5(side,flags) int side; unsigned *flags;
{
    int rank;
    castle_owner=side;
    rank=0;
    if(side==1) rank=0x70;
    *flags=0;
    if(original_piece_9b46(rank+4,1)) {
        if(original_piece_9b46(rank,3)) *flags=1;
        if(original_piece_9b46(rank+7,3)) *(unsigned char *)flags |=2;
    }
}

int original_piece_9b46(int square,int kind)
{
    int found;
    int i;
    register Move *p;
    found=0;
    if(board[square].kind==kind && board[square].side==castle_owner) {
        i=history_index-1;
        p=&history_storage[i+104];
        for(;p->detail.bytes.kind;i--,p--)
            if(history_tail[i].to==square) return found;
        found=1;
    }
    return found;
}

int quiet_9bbc(p) Move *p;
{
    int result;
    result=(p->detail.bytes.kind!=0) & (p->detail.bytes.kind!=6) & (p->detail.bytes.capture==0) & (p->flag==0);
    return result;
}

int count_9bfd()
{
    int n;
    int result;
    n=0;
    while (quiet_9bbc(&history_tail[history_index-n])) n++;
    result=n;
    return result;
}

int repetition_9c34(int required)
{
    /* a=result, b=origin, c=tracked square, d=cursor, e=scan,
       f=bound, g=repetition count, h=end, i=start. */
    int a,b,c,d,e,f,g,h,i;
    a = 1;
    g = 1;
    h = history_index + 1;
    f = h - 4;
    i = h;
    while (quiet_9bbc(&history_tail[i]-1) & ((f < i) | !required)) i--;
    if (f < i) return a;
    d = h;
    for (;;) {
        d--;
        b = history_tail[d].to;
        e = d + 2;
        while (e < h) {
            if (history_tail[e].from == b) goto next;
            e += 2;
        }
        e = d;
        c = history_tail[e].from;
        do {
            if (e - 2 < i) return a;
            e -= 2;
            if (history_tail[e].to == c) c = history_tail[e].from;
        } while (!((c == b) & (f + 1 >= e)));
        if (e < f) {
            f = e;
            if (lowbit(h-f)) {
                if (f == i) return a;
                f--;
            }
            d = h;
        }
next:
        if (d <= f) {
            g++;
            a = g;
            if (f - 2 < i) return a;
            h = f;
            f -= 2;
            d = h;
        }
    }
    return a;
}

int legal_move(move)
Move move;
{
    int middle;
    int valid;
    int saved_kind;
    unsigned flags;
    int shift;
    valid=0;
    if(move.flag & (move.detail.bytes.kind==1)) {
        castle_flags_9ad5(current_side,&flags);
        if(move.to>move.from) shift=1;
        else shift=0;
        if(flags & (1 << shift)) {
            middle=(move.to+move.from)/2;
            if(board[move.to].kind==0 && board[middle].kind==0 &&
               ((move.to>move.from) | (board[move.to-1].kind==0)) &&
               !attacked_9a50(opponent,move.from) && !attacked_9a50(opponent,move.to) &&
               !attacked_9a50(opponent,middle)) valid=1;
        }
    } else if(move.flag & (move.detail.bytes.kind==6)) {
        if(history_tail[history_index-1].detail.bytes.kind==6 && abs_i16(history_tail[history_index-1].to-history_tail[history_index-1].from)>=32 &&
           ((board[move.from].kind==6) & (board[move.from].side==current_side)))
            valid=((history_tail[history_index-1].to+history_tail[history_index-1].from)/2==move.to);
    } else {
        if(move.flag) {
            saved_kind=move.detail.bytes.kind;
            move.detail.bytes.kind=6;
        }
        if(board[move.from].kind==move.detail.bytes.kind && board[move.from].side==current_side &&
           board[move.to].kind==move.detail.bytes.capture && ((board[move.to].side==opponent) | (move.detail.bytes.capture==0))) {
            if(move.detail.bytes.kind==6) {
                if(abs_i16(move.to-move.from)<32) valid=1;
                else valid=(board[(move.to+move.from)/2].kind==0);
            } else valid=piece_attacks(move.detail.bytes.kind,current_side,move.from,move.to);
        }
        if(move.flag) move.detail.bytes.kind=saved_kind;
    }
    return valid;
}

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
    base=candidate_move.to-move_lookup_tables.pawn_and_masks.initialized.pawn_step[current_side];
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
            local_c=move_lookup_tables.ray_step[local_d]+candidate_move.from;
            if(!(local_c&136) && board[local_c].kind==0) {
                candidate_move.to=local_c;
                append_move();
            }
        }
        break;
    case 5:
        for(local_d=7;local_d>=0;local_d--) {
            local_c=move_lookup_tables.knight_step[local_d]+candidate_move.from;
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
            local_e=move_lookup_tables.ray_step[local_d];
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
        candidate_move.to=move_lookup_tables.pawn_and_masks.initialized.pawn_step[current_side]+candidate_move.from;
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
        candidate_move.to = move_lookup_tables.castle[current_side][c].destination;
        candidate_move.from = move_lookup_tables.castle[current_side][c].king_home;
        if (legal_move(candidate_move)) append_move();
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
                if (legal_move(candidate_move)) append_move();
            }
        }
    }
}
