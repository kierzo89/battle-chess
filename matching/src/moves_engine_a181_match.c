/* REA A181: complete455-byte MSC5 /AS /Zi compiler extent matches,
 * including the six-word switch table and redundant unreachable branch.
 * Production boundary/linker policy review is still required. */
typedef struct {unsigned char kind,side; int index;} Cell;
typedef struct {int to,from,flag;unsigned char kind,capture;} Move;
extern Move candidate_move;
extern Cell board[];
extern int current_side, pawn_step[], steps[], knight_steps[];
extern void append_move(), append_promotions();
void generate_quiet()
{
    /* Neutral recovered-local names: ray step, first direction, last
     * direction, candidate square, and direction index, respectively. */
    int local_e, local_a, local_b, local_c, local_d;
    candidate_move.flag=0;
    candidate_move.kind=board[candidate_move.from].kind;
    candidate_move.capture=0;
    switch(candidate_move.kind) {
    case 1:
        for(local_d=7;local_d>=0;local_d--) {
            local_c=steps[local_d]+candidate_move.from;
            if(!(local_c&136) && board[local_c].kind==0) {
                candidate_move.to=local_c;
                append_move();
            }
        }
        break;
    case 5:
        for(local_d=7;local_d>=0;local_d--) {
            local_c=knight_steps[local_d]+candidate_move.from;
            if(!(local_c&136) && board[local_c].kind==0) {
                candidate_move.to=local_c;
                append_move();
            }
        }
        break;
    case 2:
    case 3:
    case 4:
        local_b=7;
        local_a=0;
        if(candidate_move.kind==3) local_b=3;
        if(candidate_move.kind==4) local_a=4;
        for(local_d=local_b;local_d>=local_a;local_d--) {
            local_e=steps[local_d];
            local_c=local_e+candidate_move.from;
            while(!(local_c&136)) {
                if(board[local_c].kind) break;
                candidate_move.to=local_c;
                append_move();
                local_c=local_e+candidate_move.to;
            }
        }
        break;
    case 6:
        candidate_move.to=pawn_step[current_side]+candidate_move.from;
        if(board[candidate_move.to].kind==0) {
            if((candidate_move.to<8) | (candidate_move.to>=112)) append_promotions();
            else {
                append_move();
                if((candidate_move.from<24) | (candidate_move.from>=96)) {
                    candidate_move.to+=candidate_move.to-candidate_move.from;
                    if(board[candidate_move.to].kind==0) append_move();
                }
            }
        }
        break;
    }
}
