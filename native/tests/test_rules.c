#include "rules.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
/* Test-only FEN fixture reader. */
static BCPosition position(const char *fen,const char *castle,int ep) {
 uint8_t data[33]={0};unsigned row=7,col=0;
 while(*fen&&*fen!=' ') {
  char c=*fen++;if(c=='/'){row--;col=0;continue;}
  if(c>='1'&&c<='8'){col+=(unsigned)(c-'0');continue;}
  const char *keys="KQRBNPkqrbnp",*at=strchr(keys,c);assert(at);
  unsigned v=(unsigned)(at-keys),nib=v<6?v+1:v-5+8,i=row*8+col++;
  data[1+i/2]|=(uint8_t)(nib<<(i%2?0:4));
 }
 if(*fen==' '&&fen[1]=='b')data[0]=1;
 BCPosition p={0};assert(bc_unpack(&p.board,data));p.ep=(int16_t)ep;p.fullmove=1;
 for(;*castle;castle++)switch(*castle){case 'K':p.castle[0]|=2;break;case 'Q':p.castle[0]|=1;break;case 'k':p.castle[1]|=2;break;case 'q':p.castle[1]|=1;break;}
 return p;
}
static bool contains(BCPosition *p,int from,int to) {
 BCMoveList list;bc_generate_legal(p,&list);
 for(size_t i=0;i<list.count;i++)if(list.moves[i].from==from&&list.moves[i].to==to)return true;
 return false;
}
int main(void) {
 BCPosition p;bc_position_initial(&p);
 const uint64_t expected[]={1,20,400,8902,197281};
 for(unsigned d=0;d<5;d++){uint64_t n=bc_perft(&p,d);printf("start depth %u: %llu\n",d,(unsigned long long)n);assert(n==expected[d]);}
 p=position("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w","KQkq",-1);
 const uint64_t kiwi[]={1,48,2039,97862};
 for(unsigned d=1;d<4;d++){uint64_t n=bc_perft(&p,d);printf("kiwipete depth %u: %llu\n",d,(unsigned long long)n);assert(n==kiwi[d]);}
 p=position("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w","",-1);
 const uint64_t endgame[]={1,14,191,2812,43238};
 for(unsigned d=1;d<5;d++)assert(bc_perft(&p,d)==endgame[d]);
 p=position("k7/8/8/r4pPK/8/8/8/8 w","",0x55);assert(!contains(&p,0x46,0x55));
 p=position("k7/8/8/5pP1/8/8/8/7K w","",0x55);assert(contains(&p,0x46,0x55));
 p=position("k4r2/8/8/8/8/8/8/4K2R w","K",-1);assert(!contains(&p,4,6));
 p=position("k7/8/8/8/8/8/8/4K2R w","K",-1);assert(contains(&p,4,6));
 p=position("7k/6Q1/5K2/8/8/8/8/8 b","",-1);BCMoveList l;bc_generate_legal(&p,&l);assert(l.count==0&&bc_in_check(&p.board,1));
 p=position("7k/5Q2/5K2/8/8/8/8/8 b","",-1);bc_generate_legal(&p,&l);assert(l.count==0&&!bc_in_check(&p.board,1));
 p=position("7k/P7/8/8/8/8/8/7K w","",-1);bc_generate_legal(&p,&l);unsigned promotions=0;
 for(size_t i=0;i<l.count;i++)if(l.moves[i].from==0x60){assert(l.moves[i].special&&l.moves[i].kind>=2&&l.moves[i].kind<=5);promotions++;}
 assert(promotions==4);
 puts("PASS: legal generator, perft, pins, castle-through-check, promotion, mate and stalemate.");
}
