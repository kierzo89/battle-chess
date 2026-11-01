/* REA AF55: accept a bounded score and update the current frame maximum. */
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
int update_best(int score)
{
    int accepted;
    accepted=0;
    if (score<=search_frame->alpha) {
        accepted=1;
        if (search_frame->best<score) search_frame->best=score;
    }
    return accepted;
}
