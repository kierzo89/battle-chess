#ifndef BC_CONTROLS_H
#define BC_CONTROLS_H
#include <SDL3/SDL.h>
/* Native menu actions share the keyboard dispatch path. Zero means no action. */
SDL_Keycode bc_controls_hit(float x,float y);
void bc_controls_draw(SDL_Renderer *r,unsigned level,bool computer,bool paused,bool perspective,bool muted);
#endif
