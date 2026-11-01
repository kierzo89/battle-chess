#include "history.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
typedef struct {int from,to,other0,other1;} Pair;
Pair pairs[4097];int counter_9880;
int quiet_9bbc(Pair *p){unsigned kind=(unsigned)p->other1&255;return kind&&kind!=6&&!(p->other1>>8)&&!p->other0;}
int lowbit_a514(int value){return value&1;}
extern int repetition_9c34(int);
static void compare(const BCMove *moves,size_t n) {
 memset(pairs,0,sizeof pairs);counter_9880=(int)n;
 for(size_t i=0;i<n;i++)pairs[i+1]=(Pair){moves[i].to,moves[i].from,moves[i].special,moves[i].kind|(moves[i].capture<<8)};
 for(int required=0;required<2;required++)assert((unsigned)repetition_9c34(required)==bc_original_repetitions(moves,n,required!=0));
}
int main(void) {
 BCMove history[4096];unsigned seed=1988;size_t comparisons=0;
 /* End-to-end legal playouts also include non-quiet history barriers. */
 for(unsigned game=0;game<32;game++) {
  BCPosition p;bc_position_initial(&p);size_t n=0;
  for(;n<160;n++) {
   compare(history,n);comparisons+=2;
   BCMoveList list;bc_generate_legal(&p,&list);if(!list.count)break;
   seed=1664525u*seed+1013904223u;history[n]=list.moves[seed%list.count];bc_play_unchecked(&p,history[n]);
  }
 }
 BCMove cycle[4]={{6,37,0,5,0},{118,85,0,5,0},{37,6,0,5,0},{85,118,0,5,0}};
 for(size_t n=0;n<128;n++){history[n]=cycle[n%4];compare(history,n+1);comparisons+=2;}
 printf("PASS: %zu history scans agree with unchanged recovered repetition C.\n",comparisons);
}
