#ifndef BC_STAGE_H
#define BC_STAGE_H
#include "rules.h"
#define BC_STAGE_MAX 192
/* Graphics squares use top-left=0, bottom-right=63, unlike engine 0x88. */
typedef struct {uint8_t parent,operation,square,argument,extra;bool extra_known;} BCStageCommand;
typedef struct {BCStageCommand commands[BC_STAGE_MAX];unsigned count;bool failed;} BCStagePlan;
/* Recovered BB0E command construction. Host record/input waits are excluded.
 * Unknown omitted caller arguments remain explicitly unknown. Promotions
 * use the recovered9371 pawn-kind/cleared-flag normalization. */
bool bc_stage_plan(const BCPosition *before,BCMove move,BCStagePlan *out);
bool bc_stage_finale(const BCPosition *,BCMove,BCStagePlan *);
#endif
