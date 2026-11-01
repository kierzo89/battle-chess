/* REA 9DB3. Complete556-byte MSC5 /AS /Zi reconstruction.
 * The actual9AD5 body is included so MSC emits its same-segment far call. */
extern int castle_side_52d0;
extern int original_piece_9b46();
void far castle_flags_9ad5(side,flags) int side; unsigned *flags;
{
    int rank;
    castle_side_52d0=side;
    rank=0;
    if(side==1) rank=0x70;
    *flags=0;
    if(original_piece_9b46(rank+4,1)) {
        if(original_piece_9b46(rank,3)) *flags=1;
        if(original_piece_9b46(rank+7,3)) *(unsigned char *)flags |=2;
    }
}
typedef struct { unsigned char kind,side; int index; } Cell;
typedef struct { int a,b,special; unsigned char kind,capture; } Move;
typedef union { unsigned word; struct {unsigned char lo,hi;} byte; } Code;
extern Cell board[];
extern Move history_tail[];
extern int counter, current_side, other_side;
extern int attacked(), piece_attacks(), abs_i16();
int legal_move(a,b,special,code)
int a,b,special;
Code code;
{
    int middle;
    int valid;
    int saved_kind;
    unsigned flags;
    int shift;
    valid=0;
    if(special & (code.byte.lo==1)) {
        castle_flags_9ad5(current_side,&flags);
        if(a>b) shift=1;
        else shift=0;
        if(flags & (1 << shift)) {
            middle=(a+b)/2;
            if(board[a].kind==0 && board[middle].kind==0 &&
               ((a>b) | (board[a-1].kind==0)) &&
               !attacked(other_side,b) && !attacked(other_side,a) &&
               !attacked(other_side,middle)) valid=1;
        }
    } else if(special & (code.byte.lo==6)) {
        if(history_tail[counter-1].kind==6 && abs_i16(history_tail[counter-1].a-history_tail[counter-1].b)>=32 &&
           ((board[b].kind==6) & (board[b].side==current_side)))
            valid=((history_tail[counter-1].a+history_tail[counter-1].b)/2==a);
    } else {
        if(special) {
            saved_kind=code.byte.lo;
            code.byte.lo=6;
        }
        if(board[b].kind==code.byte.lo && board[b].side==current_side &&
           board[a].kind==code.byte.hi && ((board[a].side==other_side) | (code.byte.hi==0))) {
            if(code.byte.lo==6) {
                if(abs_i16(a-b)<32) valid=1;
                else valid=(board[(a+b)/2].kind==0);
            } else valid=piece_attacks(code.byte.lo,current_side,b,a);
        }
        if(special) code.byte.lo=saved_kind;
    }
    return valid;
}
