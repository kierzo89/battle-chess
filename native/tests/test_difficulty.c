#include "difficulty.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
static uint64_t fake(void *data){uint64_t *time=data;return (*time)++;}
int main(void) {
 BCSearchConfig c;
 for(unsigned level=0;level<=10;level++) {
  assert(bc_difficulty_config(level,2,&c));
  assert(c.time_budget_ms==(level==0?6000:level==10?120000:(5000u<<(level-1))));
  assert(c.max_depth==(level==0?2:23));assert(c.original_level==0);
 }
 BCSearchConfig saved=c;assert(!bc_difficulty_config(11,0,&c));assert(!memcmp(&saved,&c,sizeof c));
 assert(!bc_difficulty_config(10,0,&c));assert(!bc_difficulty_config(10,32768,&c));
 BCPosition p;bc_position_initial(&p);BCSearchResult result;
 assert(bc_difficulty_config(1,0,&c));uint64_t clock=0;c.clock_ms=fake;c.clock_userdata=&clock;c.time_budget_ms=100;
 assert(bc_search(&p,NULL,0,&c,&result));assert(result.interrupted&&result.timed_out&&result.elapsed_ms>=100);
 assert(result.nodes<=100&&result.has_move);assert(bc_play(&p,result.move));
 assert(bc_monotonic_ms()!=UINT64_MAX);
 bc_position_initial(&p);assert(bc_difficulty_config(1,0,&c));c.time_budget_ms=25;
 uint64_t started=bc_monotonic_ms();assert(bc_search(&p,NULL,0,&c,&result));
 assert(result.timed_out&&result.interrupted&&result.has_move);
 assert(result.elapsed_ms>=25&&bc_monotonic_ms()-started<2000);
 assert(bc_play(&p,result.move));
 printf("PASS: all difficulty budgets in seconds, novice depth, fake/real deadlines (real clock: %llu visits).\n",(unsigned long long)result.nodes);
}
