/* REA AEBA: recognize the line move or one of two stored search candidates. */
typedef struct {int to,from,flag;unsigned char kind,capture;} Move;
typedef struct {int flag,lower,upper;} SearchOptions;
typedef struct {
    int alpha,beta,depth;
    SearchOptions options;
    Move *line;
    int quiet,best;
    char middle[10];
    int phase;
    char remaining[192];
} SearchFrame;
extern SearchFrame *search_frame;
extern Move history_tail[], search_pair_moves[24][2];
extern int history_index;
extern int equal_state(Move *,Move *);
int preferred_move(void)
{
    int result,index;
    result=1;
    if (search_frame->phase) {
        if (equal_state(&history_tail[history_index],&search_frame->line[history_index]))
            return result;
        if (!search_frame->quiet && search_frame->phase!=2) {
            for (index=0;index<=1;index++)
                if (equal_state(&history_tail[history_index],&search_pair_moves[history_index][index]))
                    return result;
        }
    }
    result=0;
    return result;
}
