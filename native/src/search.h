#ifndef BC_SEARCH_H
#define BC_SEARCH_H
#include "history.h"
typedef bool (*BCCancelSearch)(void *userdata);
typedef struct {
 unsigned max_depth; /* 1..20; original search has 24-ply storage */
 unsigned original_level; /* recovered search mode; 5 is special novice branch */
 unsigned temporary;
 uint32_t seed;
 uint64_t node_limit;
 BCCancelSearch cancel;
 void *userdata;
} BCSearchConfig;
typedef struct {
 BCMove move,pv[24];
 int16_t score;
 unsigned depth;
 uint64_t nodes;
 bool has_move,interrupted;
} BCSearchResult;
/* history is chronological played moves before root; never mutated. */
bool bc_search(const BCPosition *root,const BCMove *history,size_t count,
 const BCSearchConfig *config,BCSearchResult *result);
#endif
