/* REA 86D6: apply a candidate, inspect an attacked square, then undo.
 * Names retain addresses where original semantics/names remain uncertain.
 */
typedef union {unsigned word;struct{unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;

typedef struct {
    unsigned char square;
    char remaining[31];
} SideInfo;

extern void apply_9749(Move,int);
extern int attacked_9a50(int, int);
extern int side_9846;
extern int side_a836;
extern SideInfo side_info_9604[];

int probe_move_86d6(Move move)
{
    int result;
    apply_9749(move,0);
    result = attacked_9a50(side_a836, side_info_9604[side_9846].square);
    apply_9749(move,1);
    return result;
}
