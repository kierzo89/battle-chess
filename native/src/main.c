#include <SDL3/SDL.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "board.h"
typedef struct { unsigned pair,list,step,w,h; int ax,ay; uint8_t *pixels; } Frame;
static unsigned word(FILE *f) {
 int a=fgetc(f),b=fgetc(f);
 if(a<0 || b<0){fprintf(stderr,"Truncated frame file\n");exit(1);}
 return (unsigned)a|((unsigned)b<<8);
}
static void fatal(const char *msg){fprintf(stderr,"%s: %s\n",msg,SDL_GetError());exit(1);}
static SDL_Texture *texture(SDL_Renderer *renderer,const Frame *f,const uint8_t *palette,bool red){
 uint8_t *rgba=malloc(f->w*f->h*4);
 if(!rgba)fatal("Allocation");
 for(unsigned i=0;i<f->w*f->h;i++) {
  unsigned p=f->pixels[i];if(red && (p==1||p==9))p+=3;
  memcpy(rgba+i*4,palette+p*3,3);rgba[i*4+3]=p?255:0;
 }
 SDL_Surface *s=SDL_CreateSurfaceFrom((int)f->w,(int)f->h,SDL_PIXELFORMAT_RGBA32,rgba,(int)f->w*4);
 if(!s)fatal("Surface");
 SDL_Texture *t=SDL_CreateTextureFromSurface(renderer,s);
 SDL_DestroySurface(s);free(rgba);
 if(!t)fatal("Texture");
 SDL_SetTextureScaleMode(t,SDL_SCALEMODE_NEAREST);SDL_SetTextureBlendMode(t,SDL_BLENDMODE_BLEND);
 return t;
}
int main(int argc,char **argv) {
 if(argc<2 || argc>3){fprintf(stderr,"Usage: %s assets.bcframes [--smoke]\n",argv[0]);return 2;}
 bool smoke=argc==3 && !strcmp(argv[2],"--smoke");
 if(argc==3&&!smoke)return 2;
 FILE *fp=fopen(argv[1],"rb");if(!fp){perror(argv[1]);return 1;}
 char magic[4];if(fread(magic,1,4,fp)!=4 || memcmp(magic,"BCF1",4))return 1;
 unsigned n=word(fp); n|=word(fp)<<16;
 if(!n||n>10000)return 1;
 uint8_t palette[768];if(fread(palette,1,sizeof palette,fp)!=sizeof palette)return 1;
 Frame *frames=calloc(n,sizeof *frames);if(!frames)return 1;
 for(unsigned i=0;i<n;i++) {
  Frame *f=&frames[i];f->pair=word(fp);f->list=word(fp);f->step=word(fp);
  f->w=word(fp);f->h=word(fp);f->ax=(int16_t)word(fp);f->ay=(int16_t)word(fp);
  if(!f->w||!f->h||f->w>640||f->h>400)return 1;
  size_t size=f->w*f->h;f->pixels=malloc(size);
  if(!f->pixels||fread(f->pixels,1,size,fp)!=size)return 1;
  for(size_t p=0;p<size;p++)if(f->pixels[p]>15)return 1;
 }
 if(fgetc(fp)!=EOF)return 1;
 fclose(fp);
 if(!SDL_Init(SDL_INIT_VIDEO))fatal("SDL initialization");
 SDL_Window *window;SDL_Renderer *renderer;
 if(!SDL_CreateWindowAndRenderer("Battle Chess - native Linux port laboratory",960,600,
       smoke?SDL_WINDOW_HIDDEN:SDL_WINDOW_RESIZABLE,&window,&renderer))fatal("Window");
 SDL_SetRenderLogicalPresentation(renderer,640,400,SDL_LOGICAL_PRESENTATION_LETTERBOX);
 unsigned index=0;bool running=true,playing=false,red=false;uint64_t last=SDL_GetTicks();
 unsigned rendered=0;
 while(running) {
  SDL_Event e;
  while(SDL_PollEvent(&e)) {
   if(e.type==SDL_EVENT_QUIT)running=false;
   if(e.type==SDL_EVENT_KEY_DOWN) {
    switch(e.key.key) {
     case SDLK_ESCAPE:running=false;break;
     case SDLK_SPACE:playing=!playing;break;
     case SDLK_C:red=!red;break;
     case SDLK_RIGHT:index=(index+1)%n;playing=false;break;
     case SDLK_LEFT:index=(index+n-1)%n;playing=false;break;
     case SDLK_DOWN:
      do{index=(index+1)%n;}while(frames[index].step!=0);break;
     case SDLK_UP:
      do{index=(index+n-1)%n;}while(frames[index].step!=0);break;
     default:break;
    }
   }
  }
  if(playing && SDL_GetTicks()-last>=100) {
   unsigned next=(index+1)%n;
   if(frames[next].step==0) {while(index && frames[index].step)index--;}
   else index=next;
   last=SDL_GetTicks();
  }
  Frame *f=&frames[index];
  SDL_SetRenderDrawColor(renderer,24,27,34,255);SDL_RenderClear(renderer);
  SDL_SetRenderDrawColor(renderer,225,229,238,255);
  SDL_RenderDebugText(renderer,12,12,"NATIVE LINUX PORT - ASSET / PLATFORM MILESTONE");
  SDL_RenderDebugText(renderer,12,28,"Not yet the playable game. No DOSBox or CPU emulator.");
  char label[160];snprintf(label,sizeof label,"Pair %02u / list %02u / frame %u | %ux%u | anchor %d,%d",
   f->pair,f->list,f->step,f->w,f->h,f->ax,f->ay);
  SDL_RenderDebugText(renderer,12,52,label);
  SDL_RenderDebugText(renderer,12,360,"Left/right: frame  Up/down: sequence  C: colour  Esc: quit");
  SDL_RenderDebugText(renderer,12,380,"Space: preview at 10 fps (not original game timing)");
  SDL_SetRenderDrawColor(renderer,50,55,65,255);
  SDL_RenderLine(renderer,320,80,320,330);SDL_RenderLine(renderer,80,290,560,290);
  SDL_Texture *t=texture(renderer,f,palette,red);
  SDL_FRect rect={320-f->ax*2.0f,290-f->ay*2.0f,f->w*2.0f,f->h*2.0f};
  if(!SDL_RenderTexture(renderer,t,NULL,&rect)||!SDL_RenderPresent(renderer))fatal("Render");
  SDL_DestroyTexture(t);rendered++;
  if(smoke) {red=!red;if(red==false)index++;if(index==n)running=false;}
  else SDL_Delay(16);
 }
 printf("Native SDL: %u frames loaded; %u render passes completed.\n",n,rendered);
 SDL_DestroyRenderer(renderer);SDL_DestroyWindow(window);SDL_Quit();
 for(unsigned i=0;i<n;i++)free(frames[i].pixels);
 free(frames);return 0;
}
