/* Faithful checked BP-frame helpers, also exact under MSC5.00 /AS /Zi. */
void empty_argument(unused) int unused; {}
unsigned lowbit(value) unsigned value; { return value & 1; }
extern char board[];
extern void fill_8a96();
void clear_board() { fill_8a96(board,480,0); }
