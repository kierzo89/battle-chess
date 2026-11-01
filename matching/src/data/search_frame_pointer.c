typedef union {unsigned word;struct{unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
typedef struct {int flag,lower,upper;} SearchOptions;
typedef struct {
    int alpha,beta,depth;
    SearchOptions options;
    Move *line;
    int quiet,best,child_depth;
    SearchOptions child_options;
    int research,phase;
    Move pv[24];
} SearchFrame;

/* Consumed external view only; no backing capacity or definition. */
extern SearchFrame search_frames[];
SearchFrame *search_frame=search_frames;
