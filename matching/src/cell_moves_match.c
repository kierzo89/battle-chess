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
