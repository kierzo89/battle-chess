/* Pending:207 emitted bytes versus210 original bytes; no matching credit. */
typedef struct { unsigned char kind, side; int index; } Cell;
typedef struct { unsigned char square, kind; } Piece;
typedef union { int word; struct { unsigned char lo, hi; } byte; } Square;
extern Cell board[];
extern Piece pieces[2][16];
extern int counts[], piece_counts[];
extern void reset_pieces(), copy_bytes();

void init_pieces()
{
    int *count;
    int kind;
    Square square;
    Piece *piece;
    reset_pieces();
    for (kind = 1; kind <= 6; ++kind) {
        if (kind == 6)
            copy_bytes(piece_counts, counts, 4);
        square.word = 0;
        do {
            if (board[square.word].kind == kind) {
                count = &counts[board[square.word].side];
                piece = pieces[board[square.word].side] + ++*count;
                piece->kind = kind;
                piece->square = square.word;
                board[square.word].index = counts[board[square.word].side];
            }
            square.byte.lo ^= 119;
            if (!(square.byte.lo & 4)) {
                if (square.word >= 112)
                    square.word = (square.word + 17) & 115;
                else
                    square.word += 16;
            }
        } while (square.word != 0);
    }
}
