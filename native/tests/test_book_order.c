#include "book_order.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
static unsigned char data[32000];
static unsigned offset=1,nodes,sentinels,max_depth,roots;
static void walk(BCPosition position,BCMove previous,unsigned depth){
 assert(depth<64&&offset<sizeof data);if(depth>max_depth)max_depth=depth;
 BCMoveList list;assert(bc_book_order(&position,depth?&previous:NULL,&list));
 for(;;){
  assert(offset<sizeof data);unsigned byte=data[offset++],index=byte&63;
  BCPosition next=position;BCMove move={0};
  if(index==63){sentinels++;assert(!(byte&64));}
  else {
   assert(index<list.count);move=list.moves[index];nodes++;
   if(!depth){
    static const unsigned from[]={20,19,6,18,21,17,22,17,22};
    static const unsigned to[]={52,51,37,50,53,33,38,49,54};
    assert(roots<9&&move.from==from[roots]&&move.to==to[roots]);roots++;
   }
   /* Independent host legal generator checks every original book edge. */
   assert(bc_play(&next,move));
  }
  if(byte&64)walk(next,move,depth+1);
  if(byte&128)return;
 }
}
int main(int argc,char **argv){
 assert(argc==2);FILE *f=fopen(argv[1],"rb");assert(f);
 assert(fread(data,1,sizeof data,f)==sizeof data&&fgetc(f)==EOF);fclose(f);
 assert(data[0]==255);BCPosition initial;bc_position_initial(&initial);BCPosition saved=initial;
 walk(initial,(BCMove){0},0);
 assert(nodes==28636&&sentinels==1191&&offset==29828&&max_depth==41&&roots==9);
 assert(!memcmp(&initial,&saved,sizeof initial));
 BCMoveList list;assert(!bc_book_order(NULL,NULL,&list));
 /* Preserve input on invalid unpromoted final-rank pawn rather than access OOB. */
 initial.board.cells[0].kind=6;assert(!bc_book_order(&initial,NULL,&list));
 printf("PASS: %u legal book edges, %u list sentinels, %u root choices, %u plies; recovered pseudo-legal ordering.\n",nodes,sentinels,roots,max_depth+1);
}
