/* Compile the actual recovered attack/table translation units unchanged.
 * The shim supplies globals and scales the original DOS byte fill for host int.
 * This validates C semantics, not 16-bit native machine-code execution. */
#include "rules.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
typedef struct {unsigned char kind,side;int index;} ReferenceCell;
typedef struct {unsigned mask;int step;} ReferenceRay;
ReferenceCell board[120];
ReferenceRay rays[239];
void fill_8a96(void *data,int size,int value) {
 assert(data==(void *)rays&&size==956&&value==0);
 memset(rays,0,sizeof rays);
}
int abs_i16(int value){return abs(value);}
extern void init_rays(void);
extern int piece_attacks(int,int,int,int);
extern int pawn_attacks(int,int);
int main(void) {
 BCPosition p;bc_position_initial(&p);unsigned seed=0x1988;unsigned comparisons=0;
 init_rays();
 for(unsigned sample=0;sample<16;sample++) {
  for(int s=0;s<120;s++)board[s]=(ReferenceCell){p.board.cells[s].kind,p.board.cells[s].side,p.board.cells[s].index};
  for(int side=0;side<2;side++)for(int to=0;to<120;to++)if(!(to&0x88)) {
   bool pawns=false;
   for(int from=0;from<120;from++)if(!(from&0x88)) {
    for(int kind=1;kind<=6;kind++) {
     assert((piece_attacks(kind,side,from,to)!=0)==bc_piece_attacks(&p.board,(unsigned)kind,(unsigned)side,from,to));comparisons++;
    }
    if(board[from].kind==6&&board[from].side==side&&bc_piece_attacks(&p.board,6,(unsigned)side,from,to))pawns=true;
   }
   assert((pawn_attacks(side,to)!=0)==pawns);
  }
  for(unsigned turn=0;turn<6;turn++) {
   BCMoveList list;bc_generate_legal(&p,&list);
   if(!list.count){bc_position_initial(&p);break;}
   seed=1664525u*seed+1013904223u;
   bc_play_unchecked(&p,list.moves[seed%list.count]);
  }
 }
 printf("PASS: %u piece attacks and 2048 pawn-attack queries agree with recovered C.\n",comparisons);
}
