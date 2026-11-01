/* REA A68B/A6D2: timing stop test and search-state initialization. */
typedef unsigned char Byte;
typedef struct {int words[4];} Move;
typedef struct {Byte kind,side;int index;} Cell;
extern int finished, modes[];
extern Byte search_side;
extern long clock_value, limit;
extern void refresh(void);
extern Move search_pair_moves[24][2], initial_move;
extern Cell board[];
extern int check_state[], home_pawn, opponent_pawn, pawn_home[], current_side;

int stop_search(void)
{
    if (finished) {
        refresh();
        return clock_value >= limit || modes[search_side] != 1;
    }
    return 0;
}

void setup_search(void)
{
    int i,side,square,j;
    for (i=0;i<=23;i++)
        for (side=0;side<=1;side++)
            search_pair_moves[i][side] = initial_move;
    check_state[0] = 0;
    home_pawn = -1;
    opponent_pawn = -1;
    for (j=0;j<=1;j++) {
        for (square=pawn_home[j];square<=pawn_home[j]+7;square++) {
            if (board[square].kind==6 && board[square].side==j) {
                if (j==current_side) home_pawn=square;
                else opponent_pawn=square;
            }
        }
    }
}
