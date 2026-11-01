/* Compatible logical Move8 owner; historical name, class, TU and capacity unknown. */
typedef union { unsigned word; struct { unsigned char kind,capture; } bytes; } MoveKind;
typedef struct { int to,from,flag; MoveKind detail; } Move;
Move state_8d12;
