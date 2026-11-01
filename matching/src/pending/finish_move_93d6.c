typedef union {unsigned word;struct{unsigned char low,high;} byte;} Kind;
typedef struct{int from,to,special;Kind kind;} Move;
extern int side,modes[];
extern Move history;
extern void record_dfac(Move *), record_kind_dfe3(int);
extern void animate_7a61(int,int), change_96f9(int,int);
void finish_move_93d6(void)
{
    if (modes[side] == 2) {
        record_dfac(&history);
        record_kind_dfe3(history.kind.byte.low);
    }
    animate_7a61(history.from,history.kind.byte.low);
    change_96f9(history.kind.byte.low,history.from);
}
