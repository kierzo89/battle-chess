/* REA 948C reconstruction candidate. */
typedef struct { unsigned char kind, side; int index; } Cell;
typedef struct { unsigned char square, kind; } Piece;
extern Cell board[];
extern Piece pieces[2][16];
extern int counts[], piece_counts[];
extern void copy_bytes();
void reset_pieces()
{
    int square, colour, entry;
    for(square=0;square<=119;square++) board[square].index=16;
    for(colour=0;colour<=1;colour++)
        for(entry=0;entry<=15;entry++) pieces[colour][entry].kind=0;
    counts[0]=-1;
    counts[1]=-1;
    copy_bytes(piece_counts,counts,4);
}
