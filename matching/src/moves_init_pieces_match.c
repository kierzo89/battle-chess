/* REA 950D. Complete210-byte MSC5 /AS /Zi reconstruction. */
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
    Square s;
    Piece *entry;
    reset_pieces();
    for (kind = 1; kind <= 6; ++kind) {
        if (kind == 6)
            copy_bytes(piece_counts, counts, 4);
        s.word = 0;
        do {
            if (board[s.word].kind == kind) {
                count = &counts[board[s.word].side];
                ++counts[board[s.word].side];
                entry = pieces[board[s.word].side] + *count;
                entry->kind = kind;
                entry->square = s.word;
                board[s.word].index = counts[board[s.word].side];
            }
            s.byte.lo ^= 119;
            if (!(s.byte.lo & 4)) {
                if (s.word >= 112)
                    s.word = (s.word + 17) & 115;
                else
                    s.word += 16;
            }
        } while (s.word != 0);
    }
}
