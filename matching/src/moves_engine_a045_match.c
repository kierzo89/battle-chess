/* REA A045. Complete316-byte MSC5 /AS /Zi reconstruction. */
typedef struct {unsigned char kind,side; int index;} Cell;
typedef struct {unsigned char square,kind;} Piece;
typedef struct {int to,from,flag;unsigned char kind,capture;} Move;
extern Move candidate_move;
extern Cell board[];
extern Piece pieces[2][16];
extern int current_side, pawn_step[], piece_counts[];
extern void append_move(), append_promotions();
extern int piece_attacks();
void generate_captures()
{
    int base, square, piece_index;
    candidate_move.flag=0;
    candidate_move.capture=board[candidate_move.to].kind;
    candidate_move.kind=6;
    base=candidate_move.to-pawn_step[current_side];
    for(square=base-1;square<=base+1;square++) {
        if(square!=base && !(square&136) &&
           ((board[square].kind==6) & (board[square].side==current_side))) {
            candidate_move.from=square;
            if((candidate_move.to<8) | (candidate_move.to>=112)) append_promotions();
            else append_move();
        }
    }
    for(piece_index=piece_counts[current_side];piece_index>=0;piece_index--) {
        if((pieces[current_side][piece_index].kind!=0) & (pieces[current_side][piece_index].kind!=6)) {
            if(piece_attacks(pieces[current_side][piece_index].kind,current_side,
                             pieces[current_side][piece_index].square,candidate_move.to)) {
                candidate_move.from=pieces[current_side][piece_index].square;
                candidate_move.kind=pieces[current_side][piece_index].kind;
                append_move();
            }
        }
    }
}
