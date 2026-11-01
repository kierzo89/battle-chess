typedef union {unsigned word;struct{unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
typedef union {long word;struct{unsigned first,second;} bits;} PawnMask;
extern int current_side,opponent,history_index,best,temporary;
extern int evaluation_delta,castle_bonus[],pawn_step[],piece_value[];
extern int piece_square[2][6][120];
extern unsigned file_mask[],pawn_mask;
extern PawnMask pawn_state[][2];
extern void far castle_95df(int,int *,int *);
extern int far pawn_score(int,int);
extern int far pawn_bit_count(int);

/* Complete evaluation contribution reconstructed as ordinary C. */
typedef unsigned char Byte;
typedef struct { Byte kind,side; int index; } Cell;
typedef struct { Byte square,kind; } Piece;
typedef union { unsigned word; Byte bytes[2]; } FlagWord;
extern Cell board[];
extern Piece pieces[2][16];
extern int endgame,total_material,pawn_material,material_balance,phase,position_score;
extern int pawn_bonus_side;
extern int center_distance055a[],pawn_rank_bonus056a[],passed_rank_bonus057a[];
extern int pawn_file_weight058a[],rank_weight059e[],steps[],knight_steps[];
extern void far castle_flags_9ad5(int,unsigned *);
int far evaluation_abs(int);
int far evaluation_max(int,int);
int far evaluation_min(int,int);
int far evaluation_piece(int,int,int);
unsigned far evaluation_parity(unsigned);

int far evaluation_abs(register int value)
{
    if(value<0) value=-value;
    return value;
}

int far evaluation_max(register int left,register int right)
{
 if(left>=right)return left;
 else return right;
}
int far evaluation_min(register int left,register int right)
{
 if(left<=right)return left;
 else return right;
}

unsigned far evaluation_parity(unsigned value)
{
    return value&1;
}

void far evaluate_full(void)
{
 /* C5 allocates autos by 16 identifier buckets; reverse each bucket here.
    Role order: kind,side,square,passed,left,square,center,sum,value,score,right;
    weight[2][120]; prevleft,diagonal,rank,file; mobility[2][2][120];
    masks/flags/ray/rank/bonuses; pawn ranks[2][8]; direction,enemy,bit,mask,kind. */
 int P,p;
 int Q,q,A,a;
 int R,r,B,b;
 int S,s,C[2][120],c;
 int T,t[2][2][120],D,d;
 Byte U;
 int u;
 FlagWord E;
 int e;
 int V,v,F,f;
 int W,w,G,g;
 int X,x,H,h[2][8];
 Byte I;
 int i;
 endgame=0;
 total_material=0;
 pawn_material=0;
 material_balance=0;
 for(a=0;a<=119;a++) {
  if(!(a&0x88) && (I=board[a].kind) && I!=1) {
   r=piece_value[I];
   total_material+=r;
   if(I==6)pawn_material+=piece_value[6];
   if(board[a].side==0)r=-r;
   material_balance-=r;
  }
 }
 phase=evaluation_max(0,total_material-8192)/256;
 if(material_balance<0)g=0;else g=1;
 endgame=(evaluation_abs(material_balance)>=piece_value[3]-piece_value[4]) &
         ((total_material-evaluation_abs(material_balance))/2<=piece_value[4]*2);
 for(f=0;f<=7;f++) {
  for(D=0;D<=7;D++) {
   a=f*16+D;
   V=evaluation_max(0,8-3*(center_distance055a[f]+center_distance055a[D]));
   for(P=0;P<=1;P++) {
    C[P][a]=((rank_weight059e[f]*(phase+8)*3)>>5)+V;
    a^=0x70;
   }
  }
 }
 for(P=0;P<=1;P++) {
  x=P^1;
  castle_flags_9ad5(x,&E.word);
  if((phase>0)&(!(E.bytes[0]&2))) {
   for(H=0;H<=7;H++) {
    Q=pieces[x][0].square+steps[H];
    if(!(Q&0x88))C[P][Q]+=(phase*12+96)>>5;
   }
  }
 }
 for(a=119;a>=0;a--) {
  if(!(a&0x88)) {
   for(P=0;P<=1;P++) {
    for(p=3;p<=4;p++)t[P][p-3][a]=0;
   }
  }
 }
 for(a=119;a>=0;a--) {
  if(!(a&0x88)) {
   for(P=0;P<=1;P++) {
    for(H=7;H>=0;H--) {
     if(H<4)p=3;else p=4;
     B=0;
     Q=a;
     U=1;
     do {
      Q+=steps[H];
      if(Q&0x88)break;
      r=C[P][Q];
      if(U)B+=r;else B+=r>>1;
      if((I=board[Q].kind) && ((I!=2)&(I!=p)))U=0;
     }while(board[Q].kind!=6);
     t[P][p-3][a]+=B>>2;
    }
   }
  }
 }
 for(a=119;a>=0;a--) {
  if(!(a&0x88)) {
   for(P=0;P<=1;P++) {
    x=P^1;
    D=a&7;
    d=a>>4;
    f=d;
    if(P==1)f=7-f;
    b=center_distance055a[f]+center_distance055a[D];
    w=(evaluation_abs((a>>4)-(pieces[x][0].square>>4))-pieces[x][0].square+a)&7;
    for(p=1;p<=6;p++) {
     R=0;
     if(endgame&(p!=6)) {
      if(p==1) {
       if(P==g) {
        R=128-16*center_distance055a[f]-12*center_distance055a[D];
        if(center_distance055a[f]==3)R-=16;
       }else {
        R=128-4*w;
        if((center_distance055a[f]>=2)|(center_distance055a[D]==3))R-=16;
       }
      }
     }else {
      r=t[P][0][a];
      S=t[P][1][a];
      switch(p) {
       case 1:if(phase<=0)R=-2*b;break;
       case 2:R=(r+S)>>2;break;
       case 3:R=r;break;
       case 4:R=S;break;
       case 5:
        B=0;
        for(H=0;H<=7;H++) {
         Q=knight_steps[H]+a;
         if(!(Q&0x88))B+=C[P][Q];
        }
        R=(B>>1)-3*b;
        break;
       case 6:
        if((f!=0)&(f!=7))R=pawn_file_weight058a[D]*(f+2)+pawn_rank_bonus056a[f]-12;
        break;
      }
     }
     piece_square[P][p-1][a]=R;
    }
   }
  }
 }
 for(P=0;P<=1;P++)for(f=0;f<=7;f++)h[P][f]=0;
 for(a=119;a>=0;a--) {
  if(!(a&0x88) && board[a].kind==6) {
   f=a>>4;
   if(board[a].side==1)f=7-(a>>4);
   h[board[a].side][f]|=file_mask[a&7];
  }
 }
 for(P=0;P<=1;P++) {
  pawn_state[0][P].bits.first=0;
  pawn_state[0][P].bits.second=0;
  for(f=1;f<=6;f++) {
   r=h[P][f];
   pawn_state[0][P].bits.second=((int)pawn_state[0][P].bits.first&r)|pawn_state[0][P].bits.second;
   pawn_state[0][P].bits.first|=r;
  }
 }
 position_score=pawn_score(-1,current_side)-pawn_score(-1,opponent);
 for(P=0;P<=1;P++) {
  x=P^1;
  i=0;
  T=0;
  F=0;
  W=255;
  A=0;
  for(f=1;f<=6;f++) {
   W&=~(i|T|F);
   A|=h[x][7-f]&W;
   s=T;
   e=F;
   i=h[P][f];
   T=(Byte)(i<<1);
   F=(i>>1)&255;
   G=T|F;
   u=s|e;
   r=h[P][f+1];
   q=(Byte)(r<<1);
   c=(r>>1)&255;
   Q=f<<4;
   if(P==1)Q^=0x70;
   X=1;
   while(X) {
    v=0;
    if(X&G)v=6;else if(X&u)v=3;
    if(X&q)v+=3;
    if(X&c)v+=3;
    if(X&i)v+=3;
    piece_square[P][5][Q]+=v;
    if((x!=temporary)|(phase<=0)) {
     if(X&W)piece_square[x][5][Q]+=passed_rank_bonus057a[7-f];
     if(X&A) {
      r=Q^0x10;
      for(pawn_bonus_side=1;pawn_bonus_side<=0;pawn_bonus_side++) {
       piece_square[pawn_bonus_side][2][Q]+=16;
       if(f==6)piece_square[pawn_bonus_side][2][r]+=16;
      }
     }
    }
    Q++;
    X=(Byte)(X<<1);
   }
  }
 }
 for(Q=3;Q<=4;Q++) {
  if((board[Q+16].kind==6)&(board[Q+16].side==0))piece_square[0][3][0x20+Q]-=20;
  if((board[Q+96].kind==6)&(board[Q+96].side==1))piece_square[1][3][0x50+Q]-=20;
 }
 for(a=119;a>=0;a--) {
  if(!(a&0x88) && board[a].kind) {
   if(board[a].side==current_side)position_score+=evaluation_piece(board[a].kind,current_side,a);
   else position_score-=evaluation_piece(board[a].kind,opponent,a);
  }
 }
}


int far pawn_bit_count(int value)
{
    int b;
    b=0;
    while(value) {
        b+=evaluation_parity(value)?1:0;
        value>>=1;
    }
    return b;
}

int far pawn_score(int index,int side)
{
    PawnMask *a;
    int b,c;
    a=&pawn_state[index+1][side];
    c=~(((int)a->bits.first<<1)|((int)a->bits.first>>1)) & a->bits.first;
    return b=-(40*pawn_bit_count(a->bits.second & c)+
               20*pawn_bit_count(c)+8*pawn_bit_count(a->bits.second));
}


int far evaluation_piece(int kind,int side,int square)
{
    int result;
    return result=*(int *)((char *)piece_square+(kind-1)*240+side*1440+square*2)+piece_value[kind];
}

int far evaluation_pawn_remove(int side,int file)
{
    int result;
    {
    pawn_mask=~file_mask[file];
    pawn_state[history_index+1][side].bits.first=
        (pawn_state[history_index+1][side].bits.first & pawn_mask) |
        pawn_state[history_index+1][side].bits.second;
    pawn_state[history_index+1][side].bits.second &= pawn_mask;
    }
    return result=pawn_score(history_index,side)-pawn_score(history_index-1,side);
}

int far evaluation_pawn_move(int side,int to,int from)
{
    int result;
    unsigned mask;
    {
    pawn_mask=file_mask[to];
    mask=~file_mask[from];
    pawn_state[history_index+1][side].bits.second |=
        pawn_state[history_index+1][side].bits.first & pawn_mask;
    pawn_state[history_index+1][side].bits.first=
        (pawn_state[history_index+1][side].bits.first & mask) |
        pawn_state[history_index+1][side].bits.second | pawn_mask;
    pawn_state[history_index+1][side].bits.second &= mask;
    }
    return result=pawn_score(history_index,side)-pawn_score(history_index-1,side);
}

int far evaluate_candidate(Move move)
{
    int a,b,c,d;
    a=6;
    evaluation_delta=0;
    if(move.flag) {
        if(move.detail.bytes.kind==1) {
            castle_95df(move.to,&d,&c);
            evaluation_delta=evaluation_piece(3,current_side,d)-evaluation_piece(3,current_side,c);
            if(move.to>move.from) evaluation_delta+=castle_bonus[1];
            else evaluation_delta+=castle_bonus[0];
        } else if(move.detail.bytes.kind==6) {
            b=move.to-pawn_step[current_side];
            evaluation_delta=evaluation_piece(6,opponent,b);
        } else {
            evaluation_delta=evaluation_piece(move.detail.bytes.kind,current_side,move.from)-
                evaluation_piece(6,current_side,move.from)+
                evaluation_pawn_remove(current_side,move.from&7);
        }
    }
    if(move.detail.bytes.capture) {
        evaluation_delta+=evaluation_piece(move.detail.bytes.capture,opponent,move.to);
        if(evaluation_abs(best)>=256 && move.detail.bytes.capture!=6 &&
           ((temporary==opponent)==(best>=0))) evaluation_delta-=16;
    }
    pawn_state[history_index+1][0].word=pawn_state[history_index][0].word;
    pawn_state[history_index+1][1].word=pawn_state[history_index][1].word;
    if((move.detail.bytes.kind==6) & ((move.detail.bytes.capture!=0) | move.flag))
        evaluation_delta+=evaluation_pawn_move(current_side,move.to&7,move.from&7);
    if(((move.detail.bytes.kind==6) & move.flag) | (move.detail.bytes.capture==6))
        evaluation_delta-=evaluation_pawn_remove(opponent,move.to&7);
    return a=evaluation_delta+evaluation_piece(move.detail.bytes.kind,current_side,move.to)-
        evaluation_piece(move.detail.bytes.kind,current_side,move.from);
}
