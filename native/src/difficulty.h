#ifndef BC_DIFFICULTY_H
#define BC_DIFFICULTY_H
#include "search.h"
/* Recovered menu levels: 0 novice, 1..9 timed levels, 10 custom minutes. */
bool bc_difficulty_config(unsigned level,unsigned minutes,BCSearchConfig *config);
uint64_t bc_monotonic_ms(void);
#endif
