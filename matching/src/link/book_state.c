/* Minimal consumed storage views; historical owner, order and COMMON choice unknown. */
typedef union { unsigned word; struct { unsigned char kind,capture; } bytes; } MoveKind;
typedef struct { int to,from,flag; MoveKind detail; } Move;
int book_choice_offset,book_saved_index,book_matches,hint_score_964c,book_state_index,best,iteration;
Move working_follow_8bb6;
