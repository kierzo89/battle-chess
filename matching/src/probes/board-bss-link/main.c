typedef struct { unsigned char kind,side; int index; } Cell;
extern Cell board[120];
extern void clear_board(void);
extern int printf(char *,...);
int main(void)
{
 int i;
 if(sizeof(Cell)!=4 || sizeof(board)!=480)return 1;
 if((char *)&board[0].side-(char *)&board[0]!=1)return 2;
 if((char *)&board[0].index-(char *)&board[0]!=2)return 3;
 for(i=0;i<120;i++)
  if(board[i].kind || board[i].side || board[i].index)return 4;
 for(i=0;i<120;i++) {
  board[i].kind=255;board[i].side=7;board[i].index=0x1234;
 }
 clear_board();
 for(i=0;i<120;i++)
  if(board[i].kind || board[i].side || board[i].index)return 5;
 printf("board:120 cells,480B; CRT zero and genuine clear passed\n");
 return 0;
}
