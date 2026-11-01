typedef union {unsigned word;struct {unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
typedef struct {int from,to;} Castle;
extern Move history_tail[];
extern Castle castle[2][2];
extern int history_index,current_side;
extern int legal_move(Move),try_move_ab58(void),abs_i16(int);

int stage_b860(void)
{
    int result,c;
    result=1;
    history_tail[history_index].flag=1;
    history_tail[history_index].detail.bytes.kind=1;
    history_tail[history_index].detail.bytes.capture=0;
    for(c=1;c>=0;c--) {
        history_tail[history_index].to=castle[current_side][c].from;
        history_tail[history_index].from=castle[current_side][c].to;
        if(legal_move(history_tail[history_index])
           && try_move_ab58()) return result;
    }
    result=0;
    return 0;
}

int stage_b8f4(void)
{
    int result,from;
    result=1;
    if(history_tail[history_index-1].detail.bytes.kind==6 &&
       abs_i16(history_tail[history_index-1].to-history_tail[history_index-1].from)>=32) {
        history_tail[history_index].flag=1;
        history_tail[history_index].detail.bytes.kind=6;
        history_tail[history_index].detail.bytes.capture=0;
        history_tail[history_index].to=
            (history_tail[history_index-1].to+history_tail[history_index-1].from)/2;
        for(from=history_tail[history_index-1].to-1;
            from<=history_tail[history_index-1].to+1;from++) {
            if(from!=history_tail[history_index-1].to && !(from&0x88)) {
                history_tail[history_index].from=from;
                if(legal_move(history_tail[history_index])
                   && try_move_ab58()) return result;
            }
        }
    }
    result=0;
    return 0;
}
