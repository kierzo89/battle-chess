/* REA A799. Complete80-byte MSC5 /AS /Zi reconstruction. */
typedef struct {int to,from,flag;unsigned char kind,capture;} Move;
extern Move working_move;
extern int search_flag, input_state, iteration, lower_bound, upper_bound, best;
extern int search_node(int,int,int,int,int,int,Move *);
int search_window(int alpha,int beta)
{
    /* The original frame reserves a second, unread two-byte slot. */
    int value, unused;
    search_flag=(working_move.kind!=0);
    input_state=0;
    value=search_node(alpha,beta,iteration,search_flag,lower_bound,upper_bound,&working_move);
    if(!input_state) best=value;
    return value;
}
