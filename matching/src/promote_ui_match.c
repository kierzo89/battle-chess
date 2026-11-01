typedef union {unsigned word; struct{unsigned char low,high;} byte;} Kind;
typedef struct{int from,to,special;Kind kind;} Move;
extern Move current,history;
extern int ready;
extern int apply_bb0e(Move,int);
int promote_ui_9371(void)
{
    int result;
    current = history;
    if (current.special && current.kind.byte.low != 1 && current.kind.byte.low != 6) {
        current.kind.byte.low = 6;
        current.special = 0;
        result = apply_bb0e(current,1);
        if (result) ready = result;
        return 1;
    }
    return 0;
}
