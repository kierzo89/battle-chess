/* REA91DC constructs a representative move attacking the current king. */
typedef union { unsigned word; struct {unsigned char square,piece;} byte; } Piece;
typedef struct {int from,to,special; Piece kind;} Move;
typedef struct {Piece piece[16];} SideInfo;
extern Move current,history,initial;
extern SideInfo side_info[];
extern int side,opponent,counts[];
extern int can_move(int,int,int,int);
void present_check_91dc(void)
{
    {
        register int square;
        current = history;
        current.to = current.from;
        current.from = square = side_info[side].piece[0].byte.square;
        current.special = 0;
        current.kind.byte.piece = 1;
        if (!history.kind.byte.square) goto none;
        if (can_move(history.kind.byte.square,opponent,history.from,square)) return;
    }
    {
        Piece a;
        int b,c;
        for (b=1,c=counts[opponent];b<=c;b++) {
            a = side_info[opponent].piece[b];
            if (a.byte.piece && can_move(a.byte.piece,opponent,a.byte.square,current.from)) {
                current.kind.byte.square = a.byte.piece;
                current.to = a.byte.square;
                return;
            }
        }
    }
none:
    current = initial;
}
