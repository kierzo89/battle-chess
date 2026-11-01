/* Isolated executable harness: maintain actual board/piece state, no stubs. */
typedef struct { unsigned char kind, side; int index; } Cell;
typedef struct { unsigned char square, kind; } Piece;
typedef union { int word; struct { unsigned char lo, hi; } byte; } Square;
Cell board[120];
Piece pieces[2][16];
int counts[2], piece_counts[2];
int side, opposite_side;
void clear_board(void)
{
    int i;
    for (i=0;i<120;i++) { board[i].kind=0; board[i].side=0; board[i].index=0; }
}
void set_cell_bytes(first, second, square)
char first, second;
int square;
{
    board[square].kind=first;
    board[square].side=second;
}
void update_950d(void)
{
    int kind, colour, slot;
    Square s;
    Piece *entry;
    for(slot=0;slot<120;slot++) board[slot].index=16;
    for(colour=0;colour<2;colour++)
        for(slot=0;slot<16;slot++) pieces[colour][slot].kind=0;
    counts[0]=counts[1]=-1;
    for(kind=1;kind<=6;kind++) {
        if(kind==6) { piece_counts[0]=counts[0];piece_counts[1]=counts[1]; }
        s.word=0;
        do {
            if(board[s.word].kind==kind) {
                ++counts[board[s.word].side];
                entry=pieces[board[s.word].side]+counts[board[s.word].side];
                entry->kind=kind;
                entry->square=s.word;
                board[s.word].index=counts[board[s.word].side];
            }
            s.byte.lo^=119;
            if(!(s.byte.lo&4)) {
                if(s.word>=112)s.word=(s.word+17)&115;
                else s.word+=16;
            }
        } while(s.word!=0);
    }
}
int main(void) { reset_board(); return 0; }
