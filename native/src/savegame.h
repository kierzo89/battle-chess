#ifndef BC_SAVEGAME_H
#define BC_SAVEGAME_H
#include "history.h"
/* Native BCS1 format: standard starting position and complete legal move log.
 * Not binary-compatible with original DOS saved games. Atomic replacement. */
bool bc_game_save(const BCGame *game,const char *path);
/* Failure returns NULL; callers retain their current game. */
BCGame *bc_game_load(const char *path);
#endif
