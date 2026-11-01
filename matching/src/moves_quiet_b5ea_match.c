/* B5EA: non-capturing moves, including the complete compiler switch table. */
typedef union {unsigned word;struct{unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
typedef struct {unsigned char kind,side;int index;} Cell;
extern Move history_tail[];
extern Cell board[];
extern int history_index,current_side,pawn_step[],steps[],knight_steps[];
extern int try_move_ab58(void),promote_search_b3e6(void);
int quiet_moves_b5ea(int from)
{
 /* Neutral recovered locals: result, ray step, first direction, last
  * direction, candidate square, and direction index; slots -2 through -12. */
 int a,b,c,d,e,f;
 a=1;
 history_tail[history_index].flag=0;
 history_tail[history_index].from=from;
 history_tail[history_index].detail.bytes.kind=board[from].kind;
 history_tail[history_index].detail.bytes.capture=0;
 switch(history_tail[history_index].detail.bytes.kind) {
 case 1:
  for(f=7;f>=0;f--) {
   e=steps[f]+history_tail[history_index].from;
   if(!(e&0x88)&&board[e].kind==0) {
    history_tail[history_index].to=e;
    if(try_move_ab58())return a;
   }
  }
  break;
 case 5:
  for(f=7;f>=0;f--) {
   e=knight_steps[f]+history_tail[history_index].from;
   if(!(e&0x88)&&board[e].kind==0) {
    history_tail[history_index].to=e;
    if(try_move_ab58())return a;
   }
  }
  break;
 case 2:case 3:case 4:
  d=7;c=0;
  if(history_tail[history_index].detail.bytes.kind==3)d=3;
  if(history_tail[history_index].detail.bytes.kind==4)c=4;
  for(f=d;f>=c;f--) {
   b=steps[f];
   e=history_tail[history_index].from+b;
   while(!(e&0x88)) {
    if(board[e].kind)break;
    history_tail[history_index].to=e;
    if(try_move_ab58())return a;
    e=history_tail[history_index].to+b;
   }
  }
  break;
 case 6:
  history_tail[history_index].to=pawn_step[current_side]+history_tail[history_index].from;
  if(board[history_tail[history_index].to].kind==0) {
   if((history_tail[history_index].to<8)|(history_tail[history_index].to>=112)) {
    if(promote_search_b3e6())return a;
   }else {
    if(try_move_ab58())return a;
    if((history_tail[history_index].from<24)|(history_tail[history_index].from>=96)) {
     history_tail[history_index].to+=history_tail[history_index].to-history_tail[history_index].from;
     if(board[history_tail[history_index].to].kind==0&&try_move_ab58())return a;
    }
   }
  }
  break;
 }
 a=0;
 return 0;
}
