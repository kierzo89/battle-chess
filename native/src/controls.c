#include "controls.h"
#include <stdio.h>
static const SDL_Keycode actions[]={SDLK_N,SDLK_U,SDLK_H,SDLK_SPACE,SDLK_S,SDLK_L,SDLK_V,SDLK_M,SDLK_D,SDLK_ESCAPE};
static bool inside(float x,float y,SDL_FRect r){return x>=r.x&&y>=r.y&&x<r.x+r.w&&y<r.y+r.h;}
static SDL_FRect level_rect(unsigned i){return (SDL_FRect){700+(i%5)*58,204+(i/5)*28,52,24};}
static SDL_FRect action_rect(unsigned i){return (SDL_FRect){700+(i%2)*148,270+(i/2)*36,140,30};}
SDL_Keycode bc_controls_hit(float x,float y){
 for(unsigned i=0;i<10;i++)if(inside(x,y,level_rect(i)))return SDLK_0+i;
 for(unsigned i=0;i<10;i++)if(inside(x,y,action_rect(i)))return actions[i];
 return 0;
}
static void button(SDL_Renderer *r,SDL_FRect rect,const char *label,bool selected){
 SDL_SetRenderDrawColor(r,selected?77:45,selected?99:55,selected?132:73,255);SDL_RenderFillRect(r,&rect);
 SDL_SetRenderDrawColor(r,235,235,240,255);SDL_RenderDebugText(r,rect.x+8,rect.y+(rect.h-8)/2,label);
}
void bc_controls_draw(SDL_Renderer *r,unsigned level,bool computer,bool paused,bool perspective,bool muted){
 for(unsigned i=0;i<10;i++){char label[16];snprintf(label,sizeof label,"%u",i);button(r,level_rect(i),label,i==level);}
 const char *labels[]={"N New game","U Undo turn",computer?"H Two players":"H Vs computer",paused?"Space Resume":"Space Pause","S Save game","L Load game",perspective?"V Flat board":"V Perspective",muted?"M Sound on":"M Sound off","D Claim draw","Esc Quit"};
 for(unsigned i=0;i<10;i++)button(r,action_rect(i),labels[i],false);
}
