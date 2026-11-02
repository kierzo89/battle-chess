#include "controls.h"
#include <stdio.h>
static const SDL_Keycode actions[]={SDLK_N,SDLK_U,SDLK_H,SDLK_SPACE,SDLK_S,SDLK_L,SDLK_V,SDLK_M,SDLK_D,SDLK_ESCAPE};
static bool inside(float x,float y,SDL_FRect r){return x>=r.x&&y>=r.y&&x<r.x+r.w&&y<r.y+r.h;}
static SDL_FRect level_rect(unsigned i){return (SDL_FRect){700+(i%5)*58,204+(i/5)*28,52,24};}
static SDL_FRect action_rect(unsigned i){return (SDL_FRect){700+(i%2)*148,270+(i/2)*36,140,30};}
SDL_Keycode bc_controls_hit(float x,float y){
 for(unsigned i=0;i<10;i++)if(inside(x,y,level_rect(i)))return SDLK_0+i;
 for(unsigned i=0;i<10;i++)if(inside(x,y,action_rect(i)))return actions[i];
 if(inside(x,y,(SDL_FRect){700,550,288,30}))return SDLK_C;
 for(unsigned i=0;i<2;i++)if(inside(x,y,(SDL_FRect){700,458+i*28,288,24}))return i?SDLK_F2:SDLK_F1;
 if(inside(x,y,(SDL_FRect){700,582,140,24}))return SDLK_F3;
 if(inside(x,y,(SDL_FRect){848,582,140,24}))return SDLK_F4;
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
 button(r,(SDL_FRect){700,550,288,30},"C Custom minutes",level==10);
}

void bc_controls_engines(SDL_Renderer *r,const unsigned engines[2],unsigned depth){
 char label[40];snprintf(label,sizeof label,"F3 Depth - (%u)",depth);
 button(r,(SDL_FRect){700,582,140,24},label,false);
 button(r,(SDL_FRect){848,582,140,24},"F4 Depth +",false);
 const char *names[]={"Human","Original","Stockfish"};
 for(unsigned i=0;i<2;i++){char label[64];snprintf(label,sizeof label,"F%u %s: %s",i+1,i?"Blue":"Red",names[engines[i]%3]);button(r,(SDL_FRect){700,458+i*28,288,24},label,false);}
}
