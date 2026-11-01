/* REA 9B46 reconstruction candidate. */
typedef struct {int from,to,flag; unsigned char kind,capture;} Move;
typedef struct {unsigned char kind,side,a,b;} BoardSquare;
typedef struct {char prefix[0x340]; Move moves[1];} GameHistory;
extern BoardSquare board_a8ba[];
extern Move history_85a4[];
extern Move moves_88e4[];
extern int counter_9880;
extern int castle_side_52d0;
int original_piece_9b46(int square,int kind)
{
    int found;
    int i;
    register Move *p;
    found=0;
    if(board_a8ba[square].kind==kind && board_a8ba[square].side==castle_side_52d0) {
        i=counter_9880-1;
        p=&history_85a4[i+104];
        for(;p->kind;i--,p--)
            if(moves_88e4[i].from==square) return found;
        found=1;
    }
    return found;
}
