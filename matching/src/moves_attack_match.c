/* REA 9A50. Complete133-byte MSC5.00 /AS /Zi match. */
typedef struct { unsigned char square,kind; } Piece;
extern Piece pieces_9604[][16];
extern int count_b0a6[];
extern int pawn_99be(int,int);
extern int piece_98f9(int,int,int,int);
int attacked_9a50(int side,int square)
{
    int index;
    register Piece *p;
    int result;
    result=1;
    if (pawn_99be(side,square)) return result;
    p=&pieces_9604[side][count_b0a6[side]];
    index=count_b0a6[side];
    for(;index>=0;index--,p--)
        if(p->kind && piece_98f9(p->kind,side,p->square,square)) return result;
    result=0;
    return result;
}

