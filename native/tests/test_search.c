#include "search.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
static BCPosition terminal(bool mate) {
 uint8_t data[33]={1}; /* black king h8; white king f6; white queen g7/f7 */
 data[32]=9;data[23]=1; /* f6 = index45 => low nibble byte23 */
 if(mate)data[28]=0x20;else data[27]=2;
 BCPosition p={0};assert(bc_unpack(&p.board,data));p.ep=-1;p.fullmove=1;return p;
}
static bool cancel(void *p){(*(unsigned *)p)++;return true;}
int main(void) {
 BCPosition p;bc_position_initial(&p);BCPosition saved=p;
 BCSearchConfig config={.max_depth=2,.original_level=1,.temporary=0,.seed=1,.node_limit=100000};
 BCSearchResult result,again;assert(bc_search(&p,NULL,0,&config,&result));
 printf("depth=%u nodes=%llu score=%d move=%u-%u cancelled=%d\n",result.depth,(unsigned long long)result.nodes,result.score,result.move.from,result.move.to,result.interrupted);
 assert(result.has_move&&!result.interrupted);assert(bc_play(&p,result.move));
 assert(bc_search(&saved,NULL,0,&config,&again));assert(!memcmp(&result,&again,sizeof result));
 unsigned calls=0;config.cancel=cancel;config.userdata=&calls;
 assert(bc_search(&saved,NULL,0,&config,&result));assert(result.interrupted&&calls);
 config.cancel=NULL;config.node_limit=1;
 assert(bc_search(&saved,NULL,0,&config,&result));assert(result.interrupted&&result.nodes<=2);
 config.node_limit=100000;config.max_depth=1;
 BCMove played[20];size_t n=0;p=saved;
 for(unsigned i=0;i<12;i++) {
  assert(bc_search(&p,played,n,&config,&result));assert(result.has_move&&!result.interrupted);
  played[n++]=result.move;assert(bc_play(&p,result.move));
 }
 config.max_depth=4;config.node_limit=100000;assert(bc_search(&saved,NULL,0,&config,&result));
 assert(result.has_move);BCPosition deep=saved;assert(bc_play(&deep,result.move));
 printf("deeper search: depth=%u nodes=%llu cancelled=%d\n",result.depth,(unsigned long long)result.nodes,result.interrupted);
 config.max_depth=2;
 BCPosition mate=terminal(true);assert(bc_search(&mate,NULL,0,&config,&result));assert(!result.has_move&&result.score<0);
 BCPosition stale=terminal(false);assert(bc_search(&stale,NULL,0,&config,&result));assert(!result.has_move&&result.score==0);
 assert(!memcmp(&saved,&(BCPosition){.board=saved.board,.castle={3,3},.ep=-1,.halfmove=0,.fullmove=1},sizeof saved));
 puts("PASS: recovered phased search produces legal repeatable moves, responds to cancellation and plays 12 plies.");
}
