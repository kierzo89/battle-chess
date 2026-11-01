typedef struct { unsigned char kind,side; int index; } Cell;
extern Cell board[120];
extern void fill_8a96(char *,int,int);
void clear_board(void) { fill_8a96((char *)board,480,0); }
