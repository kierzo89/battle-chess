/* Reconstructed move module. MSC5.00 emits a near call preceded by PUSH CS
 * for the far helper defined in this translation unit. */
typedef union { unsigned word; struct { unsigned char lo, hi; } byte; } MoveKind;
void far castle_95df(a,s,d) int a,*s,*d;
{
 if (((unsigned char)a & 7) >= 4) { *s=a-1; *d=a+1; }
 else { *s=a+1; *d=a-2; }
}


typedef struct { unsigned char kind, side; int index; } Cell;
typedef struct { unsigned char square, kind; } Piece;
extern Cell board[];
extern Piece pieces[2][16];
extern int piece_counts[];

void swap_cells(a,b)
int a,b;
{
    Cell temporary;
    temporary = board[a];
    board[a] = board[b];
    board[b] = temporary;
    pieces[board[a].side][board[a].index].square = a;
}

void remove_piece(square)
int square;
{
    board[square].kind = 0;
    pieces[board[square].side][board[square].index].kind = 0;
}

void add_piece(kind,side,square)
int kind,side,square;
{
    Piece *piece;
    piece = &pieces[side][board[square].index];
    board[square].kind = kind;
    board[square].side = side;
    piece->kind = kind;
    piece->square = square;
}

void change_piece(kind,square)
int kind,square;
{
    int *count;
    board[square].kind = kind;
    pieces[board[square].side][board[square].index].kind = kind;
    count = &piece_counts[board[square].side];
    if (*count < board[square].index)
        *count = board[square].index;
}

extern int side_a836;
void apply_9749(a,b,c,d,undo) int a,b,c,undo; MoveKind d;
{
    int u; /* castling rook source */
    int t; /* castling rook destination */
    int s; /* unused local retained in the original stack frame */
    int q; /* en-passant capture square */
    if (undo) {
        swap_cells(b,a);
        if (d.byte.hi) add_piece(d.byte.hi,side_a836,a);
    } else {
        if (d.byte.hi) remove_piece(a);
        swap_cells(a,b);
    }
    if (c) {
        if (d.byte.lo==1) {
            castle_95df(a,&u,&t);
            if (undo) swap_cells(t,u);
            else swap_cells(u,t);
        } else if (d.byte.lo==6) {
            q=(a&7)+(b&0x70);
            if (undo) add_piece(6,side_a836,q);
            else remove_piece(q);
        } else {
            if (undo) change_piece(6,b);
            else change_piece(d.byte.lo,a);
        }
    }
}

