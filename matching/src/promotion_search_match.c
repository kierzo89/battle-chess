/* B3E6: try each promotion kind through the ordinary search validator. */
typedef union {unsigned word;struct {unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
extern Move history_tail[];
extern int history_index;
extern int try_move_ab58(void);

int promote_search_b3e6(void)
{
    int result,kind;
    result=1;
    history_tail[history_index].flag=1;
    for(kind=2;kind<=5;kind++) {
        history_tail[history_index].detail.bytes.kind=kind;
        if(try_move_ab58()) return result;
    }
    history_tail[history_index].flag=0;
    result=0;
    return 0;
}
