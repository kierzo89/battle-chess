/* Native adaptation of recovered init_rays, piece_attacks, pawn_attacks,
 * generate_quiet (A181), generate_captures (A045), promotion_moves (A011),
 * legal_move (9DB3), and post-apply king-safety test in prepare_af87.
 * See rules-provenance.json for host adaptations and ordering limitations. */
#include "rules.h"
#include <assert.h>
#include <stdlib.h>
static const int steps[8]={1,-1,16,-16,17,-17,15,-15};
static const int knights[8]={14,-14,18,-18,31,-31,33,-33};
static const int pawn[2]={16,-16};
static bool on_board(int s){return s>=0&&s<120&&!(s&0x88);}
bool bc_piece_attacks(const BCBoard *b,unsigned kind,unsigned side,int from,int to) {
 if(!on_board(from)||!on_board(to)||from==to||side>1)return false;
 if(kind==6)return abs(to-pawn[side]-from)==1;
 if(kind==5){for(int i=7;i>=0;i--)if(to-from==knights[i])return true;return false;}
 if(kind<1||kind>4)return false;
 int first=kind==4?4:0,last=kind==3?3:7;
 for(int i=last;i>=first;i--) {
  int s=from+steps[i];
  while(on_board(s)) {
   if(s==to)return true;
   if(kind==1||b->cells[s].kind)break;
   s+=steps[i];
  }
 }
 return false;
}
bool bc_attacked(const BCBoard *b,unsigned side,int target) {
 if(side>1||!on_board(target))return false;
 for(int d=-1;d<=1;d+=2) {
  int s=target-pawn[side]+d;
  if(on_board(s)&&b->cells[s].kind==6&&b->cells[s].side==side)return true;
 }
 for(int i=b->last_nonpawn[side];i>=0;i--) {
  BCPiece p=b->pieces[side][i];
  if(p.kind&&bc_piece_attacks(b,p.kind,side,p.square,target))return true;
 }
 return false;
}
bool bc_in_check(const BCBoard *b,unsigned side) {
 if(side>1||b->pieces[side][0].kind!=1)return true;
 return bc_attacked(b,side^1,b->pieces[side][0].square);
}
void bc_position_initial(BCPosition *p) {
 *p=(BCPosition){0};bc_initial(&p->board);p->castle[0]=p->castle[1]=3;
 p->ep=-1;p->fullmove=1;
}
static void revoke(BCPosition *p,unsigned s) {
 if(s==0)p->castle[0]&=2;
 if(s==7)p->castle[0]&=1;
 if(s==112)p->castle[1]&=2;
 if(s==119)p->castle[1]&=1;
}
void bc_play_unchecked(BCPosition *p,BCMove m) {
 unsigned side=p->board.side,kind=p->board.cells[m.from].kind;
 if(kind==1)p->castle[side]=0;
 revoke(p,m.from);revoke(p,m.to);
 p->ep=kind==6&&abs(m.to-m.from)==32 ? (m.to+m.from)/2:-1;
 p->halfmove=(kind==6||m.capture)?0:p->halfmove+1;
 bc_apply(&p->board,m,false);
 p->board.side^=1;p->fullmove+=side;
}
static void emit(const BCPosition *p,BCMoveList *list,BCMove move) {
 BCPosition next=*p;
 bc_play_unchecked(&next,move);
 if(bc_in_check(&next.board,p->board.side))return;
 assert(list->count<256);
 list->moves[list->count++]=move;
}
static void pawn_emit(const BCPosition *p,BCMoveList *list,BCMove m) {
 if(m.to<8||m.to>=112) {
  m.special=1;
  for(m.kind=2;m.kind<=5;m.kind++)emit(p,list,m);
 } else emit(p,list,m);
}
void bc_generate_legal(const BCPosition *p,BCMoveList *list) {
 list->count=0;unsigned side=p->board.side;
 const BCBoard *b=&p->board;
 /* A045 capture enumeration onto each opponent destination. King captures
  * are excluded: the host game ends at checkmate, not capture of a king. */
 for(int to=0;to<120;to++) {
  if(!on_board(to)||!b->cells[to].kind||b->cells[to].side==side||b->cells[to].kind==1)continue;
  int base=to-pawn[side];
  for(int from=base-1;from<=base+1;from+=2) {
   if(on_board(from)&&b->cells[from].kind==6&&b->cells[from].side==side)
    pawn_emit(p,list,(BCMove){(uint8_t)from,(uint8_t)to,0,6,b->cells[to].kind});
  }
  for(int i=b->last_nonpawn[side];i>=0;i--) {
   BCPiece pc=b->pieces[side][i];
   if(pc.kind&&pc.kind!=6&&bc_piece_attacks(b,pc.kind,side,pc.square,to))
    emit(p,list,(BCMove){pc.square,(uint8_t)to,0,pc.kind,b->cells[to].kind});
  }
 }
 /* A181 quiet enumeration for each active piece, retaining direction order. */
 for(int i=b->last_piece[side];i>=0;i--) {
  BCPiece pc=b->pieces[side][i];if(!pc.kind)continue;
  int from=pc.square;
  if(pc.kind==6) {
   int to=from+pawn[side];
   if(on_board(to)&&!b->cells[to].kind) {
    pawn_emit(p,list,(BCMove){pc.square,(uint8_t)to,0,6,0});
    if((side==0&&(from&0x70)==16)||(side==1&&(from&0x70)==96)) {
     to+=pawn[side];if(!b->cells[to].kind)emit(p,list,(BCMove){pc.square,(uint8_t)to,0,6,0});
    }
   }
   if(on_board(p->ep)&&!b->cells[p->ep].kind&&abs(p->ep-pawn[side]-from)==1) {
    int captured=(p->ep&7)+(from&0x70);
    if(b->cells[captured].kind==6&&b->cells[captured].side!=side)
     emit(p,list,(BCMove){pc.square,(uint8_t)p->ep,1,6,0});
   }
  } else {
   int first=pc.kind==4?4:0,last=pc.kind==3?3:7;
   for(int d=last;d>=first;d--) {
    int step=pc.kind==5?knights[d]:steps[d],to=from+step;
    while(on_board(to)&&!b->cells[to].kind) {
     emit(p,list,(BCMove){pc.square,(uint8_t)to,0,pc.kind,0});
     if(pc.kind==1||pc.kind==5)break;
     to+=step;
    }
   }
  }
 }
 /* 9DB3: original king/rook, empty path and safe king path. Historical
  * original-piece scan is represented by irreversible host castling rights. */
 int home=side?116:4;
 if(b->cells[home].kind==1&&b->cells[home].side==side&&!bc_in_check(b,side)) {
  for(int k=0;k<2;k++) {
   int dir=k?1:-1,rook=home+(k?3:-4),to=home+dir*2;
   if(!(p->castle[side]&(1<<k))||b->cells[rook].kind!=3||b->cells[rook].side!=side)continue;
   if(b->cells[home+dir].kind||b->cells[to].kind||(!k&&b->cells[to-1].kind))continue;
   BCBoard crossing=*b;
   bc_apply(&crossing,(BCMove){(uint8_t)home,(uint8_t)(home+dir),0,1,0},false);
   if(!bc_in_check(&crossing,side))emit(p,list,(BCMove){(uint8_t)home,(uint8_t)to,1,1,0});
  }
 }
}
bool bc_play(BCPosition *p,BCMove move) {
 BCMoveList list;bc_generate_legal(p,&list);
 for(size_t i=0;i<list.count;i++) {
  BCMove m=list.moves[i];
  if(m.from==move.from&&m.to==move.to&&m.kind==move.kind&&m.special==move.special&&m.capture==move.capture) {
   bc_play_unchecked(p,m);return true;
  }
 }
 return false;
}
uint64_t bc_perft(const BCPosition *p,unsigned depth) {
 if(!depth)return 1;
 BCMoveList list;bc_generate_legal(p,&list);if(depth==1)return list.count;
 uint64_t n=0;
 for(size_t i=0;i<list.count;i++) {BCPosition next=*p;bc_play_unchecked(&next,list.moves[i]);n+=bc_perft(&next,depth-1);}
 return n;
}

bool bc_finale_attack(const BCPosition *p,int preferred,BCMove *out){
 if(!p||!out||!bc_in_check(&p->board,p->board.side))return false;
 BCMoveList legal;bc_generate_legal(p,&legal);if(legal.count)return false;
 int king=-1;for(int s=0;s<120;s++)if(!(s&0x88)&&p->board.cells[s].kind==1&&p->board.cells[s].side==p->board.side){king=s;break;}
 if(king<0)return false;
 for(int i=-1;i<120;i++){int s=i<0?preferred:i;if(s<0||s>=120||(s&0x88))continue;BCCell c=p->board.cells[s];
  if(c.kind&&c.side!=p->board.side&&bc_piece_attacks(&p->board,c.kind,c.side,s,king)){*out=(BCMove){s,king,0,c.kind,1};return true;}}
 return false;
}
