#include "compositor.h"
#include <string.h>
static bool valid(const BCImage *f){
 if(!f||f->width>255||f->height>255||f->x< -128||f->x>127||f->y< -128||f->y>127)return false;
 size_t n=((f->width+3)&~3u)*f->height;
 return f->length==n&&(!n||f->pixels);
}
bool bc_compose(const BCImage *a,const BCImage *b,uint8_t *pixels,size_t capacity,BCImage *out){
 if(!valid(a)||!valid(b)||!a->width||!a->height||!pixels||!out)return false;
 BCImage result=*a;
 if(b->width&&b->height){
  result.x=a->x>b->x?a->x:b->x;result.y=a->y>b->y?a->y:b->y;
  unsigned aw=result.x-a->x+a->width,bw=result.x-b->x+b->width;
  unsigned ah=result.y-a->y+a->height,bh=result.y-b->y+b->height;
  result.width=aw>bw?aw:bw;result.height=ah>bh?ah:bh;
 }
 if(result.width>255||result.height>255)return false;
 unsigned stride=(result.width+3)&~3u;size_t n=(size_t)stride*result.height;
 if(n>capacity)return false;
 memset(pixels,0,n);
 for(unsigned layer=0;layer<2;layer++){
  const BCImage *f=layer?b:a;if(!f->width||!f->height)continue;
  unsigned fs=(f->width+3)&~3u;
  for(unsigned row=0;row<f->height;row++)for(unsigned col=0;col<fs;col++){
   unsigned value=f->pixels[row*fs+col];if(value>15)return false;
   size_t at=(size_t)(result.y-f->y+row)*stride+(result.x-f->x)+col;
   if(at>=n){if(value)return false;continue;}
   if(layer)pixels[at]^=value;else pixels[at]=value;
  }
 }
 result.pixels=pixels;result.length=n;*out=result;return true;
}
