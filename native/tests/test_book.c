#include "book.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
static unsigned char data[32000];
static unsigned next[32000],end=1,checks,leaves;
static BCMove history[44];
static bool same(BCMove a,BCMove b){return a.from==b.from&&a.to==b.to&&a.special==b.special&&a.kind==b.kind&&a.capture==b.capture;}
static void index_list(unsigned depth){
 assert(depth<64);
 for(;;){assert(end<32000);unsigned at=end++,v=data[at];if(v&64)index_list(depth+1);next[at]=end;if(v&128)return;}
}
static void verify(BCPosition p,unsigned list,unsigned depth){
 BCMoveList order;assert(bc_book_order(&p,depth?&history[depth-1]:NULL,&order));
 unsigned siblings[64],n=0,weighted=0;
 for(unsigned at=list;;at=next[at]){assert(at<29828&&n<64);if((data[at]&63)!=63)siblings[n++]=at;else if(!weighted)weighted=n;if(data[at]&128)break;}
 assert(n);if(!weighted)weighted=n;
 /* Independent tree child/sibling interpretation vs original scan and rotation. */
 if(depth<2||list%251==0){
  const unsigned weights[]={7,10,12,13,14,15,16};
  for(unsigned draw=0;draw<16;draw++){
   unsigned k=0;while(weights[k]<=draw)k++;
   BCMove out={0};assert(bc_book_move(&p,history,depth,draw,&out));
   if(!same(out,order.moves[data[siblings[k%weighted]]&63])){fprintf(stderr,"Mismatch list %u depth %u draw %u n %u k %u actual %u-%u expected %u-%u\n",list,depth,draw,n,k,out.from,out.to,order.moves[data[siblings[k%weighted]]&63].from,order.moves[data[siblings[k%weighted]]&63].to);for(unsigned z=0;z<n;z++)fprintf(stderr,"%u:%02x ",siblings[z],data[siblings[z]]);fputc(10,stderr);assert(0);}checks++;
  }
 }
 for(unsigned i=0;i<n;i++){
  unsigned at=siblings[i];BCPosition child=p;history[depth]=order.moves[data[at]&63];assert(bc_play(&child,history[depth]));
  if(data[at]&64)verify(child,at+1,depth+1);
  else if(at%101==0){BCMove out={99,99,99,99,99};assert(!bc_book_move(&child,history,depth+1,0,&out));assert(out.from==99);leaves++;}
 }
}
int main(int argc,char **argv){
 assert(argc==2);FILE *f=fopen(argv[1],"rb");assert(f);assert(fread(data,1,32000,f)==32000&&fgetc(f)==EOF);fclose(f);
 index_list(0);assert(end==29828);BCPosition p;bc_position_initial(&p);verify(p,1,0);
 BCMove out={99,99,99,99,99};assert(!bc_book_move(&p,NULL,1,0,&out));assert(!bc_book_move(&p,NULL,0,16,&out));
 p.halfmove=1;assert(!bc_book_move(&p,NULL,0,0,&out));assert(out.from==99);
 printf("PASS: %u weighted history lookups and %u exhausted leaf fallbacks; independent tree oracle and unchanged failure output.\n",checks,leaves);
}
