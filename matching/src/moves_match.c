/* Pending semantic reconstruction from REA. No byte match is claimed.
 * Original 9749 also requires same-segment far-call relaxation. */
typedef union { unsigned word; struct { unsigned char lo, hi; } byte; } MoveKind;
extern void move_961c(int,int);
extern void remove_967c(int);
extern void add_96af(int,int,int);
extern void change_96f9(int,int);
extern void far castle_95df(int,int *,int *);
extern int side_a836;
void apply_9749(int a,int b,int c,MoveKind d,int undo)
{
    int square;
    int unused;
    int dest;
    int src;
    if (undo) {
        move_961c(b,a);
        if (d.byte.hi) add_96af(d.byte.hi,side_a836,a);
    } else {
        if (d.byte.hi) remove_967c(a);
        move_961c(a,b);
    }
    if (c) {
        if (d.byte.lo==1) {
            castle_95df(a,&src,&dest);
            if (undo) move_961c(dest,src);
            else move_961c(src,dest);
        } else if (d.byte.lo==6) {
            square=(a&7)+(b&0x70);
            if (undo) add_96af(6,side_a836,square);
            else remove_967c(square);
        } else {
            if (undo) change_96f9(6,b);
            else change_96f9(d.byte.lo,a);
        }
    }
}

typedef struct { unsigned char square,kind; } Piece;
extern Piece pieces_9604[][16];
extern int count_b0a6[];
extern int pawn_99be(int,int);
extern int piece_98f9(int,int,int,int);
int attacked_9a50(int side,int square)
{
    int result=1;
    int count;
    int index;
    register int n;
    register Piece *p;
    if (pawn_99be(side,square)) return result;
    n=count_b0a6[side];
    p=&pieces_9604[side][n];
    for(index=n;index>=0;index--,p--)
        if(p->kind && piece_98f9(p->kind,side,p->square,square)) return result;
    result=0;
    return result;
}

typedef struct {int from,to,flag; unsigned char kind,capture;} Move;
int quiet_9bbc(Move *p)
{
    int result;
    result=(p->kind!=6) & (p->kind!=0) & (p->capture==0) & (p->flag==0);
    return result;
}
extern Move moves_88e4[];
extern int counter_9880;
int count_9bfd(void)
{
    int result;
    int n=0;
    while (quiet_9bbc(&moves_88e4[counter_9880-n])) n++;
    return n;
}
extern int castle_side_52d0;
extern int original_piece_9b46(int,int);
void far castle_flags_9ad5(int side,unsigned *flags)
{
    int rank=0;
    castle_side_52d0=side;
    if(side==1) rank=0x70;
    *flags=0;
    if(original_piece_9b46(rank+4,1)) {
        if(original_piece_9b46(rank,3)) *flags=1;
        if(original_piece_9b46(rank+7,3)) *(unsigned char *)flags |=2;
    }
}
typedef struct {unsigned char kind,side,a,b;} BoardSquare;
extern BoardSquare board_a8ba[];
typedef struct {char prefix[0x340]; Move moves[1];} GameHistory;
extern GameHistory history_85a4;
int original_piece_9b46(int square,int kind)
{
    int result=0;
    int index;
    int unused;
    register Move *p;
    register int board_index;
    board_index=square;
    if(board_a8ba[board_index].kind==kind && board_a8ba[board_index].side==castle_side_52d0) {
        index=counter_9880-1;
        p=&history_85a4.moves[index];
        for(;p->kind;index--,p--)
            if(moves_88e4[index].from==square) return result;
        result=1;
    }
    return result;
}
