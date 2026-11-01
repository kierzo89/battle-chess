#define _POSIX_C_SOURCE 200809L
#include "difficulty.h"
#include <time.h>
/* set_limit in hint_limit_turn_context_match.c; novice depth from
 * shared_turn_book_context_match.c::search_turn_8061. clock_history_context
 * refresh uses time(0), i.e. whole elapsed seconds, not BIOS ticks. */
bool bc_difficulty_config(unsigned level,unsigned minutes,BCSearchConfig *config) {
 if(!config||level>10||(level==10&&(!minutes||minutes>32767)))return false;
 BCSearchConfig c={0};
 c.max_depth=level==0?2:23;
 c.original_level=0; /* Internal special search mode is not menu difficulty. */
 c.seed=1;
 uint64_t seconds=level==0?6:level==10?(uint64_t)minutes*60:5u<<(level-1);
 c.time_budget_ms=seconds*1000;
 *config=c;return true;
}
uint64_t bc_monotonic_ms(void) {
 struct timespec t;if(clock_gettime(CLOCK_MONOTONIC,&t))return UINT64_MAX;
 return (uint64_t)t.tv_sec*1000+(uint64_t)t.tv_nsec/1000000;
}
