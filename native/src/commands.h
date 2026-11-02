#ifndef BC_COMMANDS_H
#define BC_COMMANDS_H
#include "stage.h"
typedef struct {int command,next;} BCCommandSlot;
typedef struct {
 BCStagePlan plan;
 int child[BC_STAGE_MAX],sibling[BC_STAGE_MAX];
 unsigned char state[BC_STAGE_MAX];
 BCCommandSlot slots[4];int pool[4],used,head,root,next_root;
 bool failed,done;
} BCCommands;
/* Setup a task in slot before scheduling. Return false for unsupported or
 * malformed commands. The callback owns per-slot animation state. */
typedef bool (*BCCommandStart)(void *,unsigned slot,unsigned command,const BCStageCommand *);
/* One task invocation: -1 failure,0 waiting,1 completed. */
typedef int (*BCCommandStep)(void *,unsigned slot,unsigned command,const BCStageCommand *);
bool bc_commands_begin(BCCommands *,const BCStagePlan *,BCCommandStart,void *);
/* One original-style queue dispatch: -1 failed,0 dispatched,1 all roots idle.
 * Retains four-slot reuse and post-completion next-pointer traversal. Separate
 * recorded roots (castle/EP recursion) run serially, like original wait loops. */
int bc_commands_tick(BCCommands *,BCCommandStart,BCCommandStep,void *);
#endif
