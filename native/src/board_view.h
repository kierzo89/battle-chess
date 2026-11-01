#ifndef BC_BOARD_VIEW_H
#define BC_BOARD_VIEW_H
#include <SDL3/SDL.h>
#include "motion.h"
typedef struct BCBoardView BCBoardView;
BCBoardView *bc_view_load(SDL_Renderer *renderer,const char *path);
void bc_view_destroy(BCBoardView *view);
void bc_view_draw(BCBoardView *view,SDL_Renderer *renderer,const BCPosition *position,const BCMotion *motion,int selected,bool perspective);
int bc_view_hit(bool perspective,float x,float y);
void bc_view_square_point(bool perspective,unsigned square,float *x,float *y);
#endif
