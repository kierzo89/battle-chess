/* Reconstructed consumed scalar views; original COMMON choice/order unknown. */
typedef union { unsigned word; struct { unsigned char kind,capture; } bytes; } MoveKind;
typedef struct { int to,from,flag; MoveKind detail; } Move;
int temporary,current_side,history_move_counter,history_index,opponent;
Move selected_move;
