/* Pending; not an exact byte match. */
typedef struct { unsigned char square,kind; } Piece;
extern Piece pieces_9604[][16];
extern int count_b0a6[];
extern int pawn_99be();
extern int piece_98f9();
int attacked_9a50(side,square) int side,square;
{
    register int index;
    int result;
    register Piece *p;
    result=1;
    if (pawn_99be(side,square)) return result;
    index=count_b0a6[side];
    p=&pieces_9604[side][index];
    goto test;
again:
    index--; p--;
test:
    if(index>=0) {
        if(p->kind && piece_98f9(p->kind,side,p->square,square)) return result;
        goto again;
    }
    result=0;
    return result;
}

