typedef union {unsigned word;struct{unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
typedef struct {int flag,lower,upper;} SearchOptions;
extern Move working_move;
extern SearchOptions search_options;
extern int input_state,best,iteration;
extern int search_node(int,int,int,SearchOptions,Move *);
int search_window(int alpha,int beta)
{
    int value;
    int flag;
    flag=(working_move.detail.bytes.kind!=0);
    search_options.flag=flag;
    input_state=0;
    value=search_node(alpha,beta,iteration,search_options,&working_move);
    if(!input_state) best=value;
    return value;
}
