#include "board_view.h"
#include "geometry.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef struct {SDL_Texture *texture[2];int w,h,x,y;} Sprite;
struct BCBoardView {SDL_Texture *background[2];Sprite sprites[2][64],walk[6][8][64];};
static int word(FILE *f){int a=fgetc(f),b=fgetc(f);return a<0||b<0?-1:a+(b<<8);}
static SDL_Texture *texture(SDL_Renderer *r,const uint8_t *data,const uint8_t *pal,int w,int h,int side,bool transparent){
 uint8_t *rgba=malloc((size_t)w*h*4);if(!rgba)return NULL;
 for(int i=0;i<w*h;i++){unsigned v=data[i];if(v>15){free(rgba);return NULL;}if(!side&&(v==1||v==9))v+=3;memcpy(rgba+4*i,pal+3*v,3);rgba[4*i+3]=transparent&&!v?0:255;}
 SDL_Surface *s=SDL_CreateSurfaceFrom(w,h,SDL_PIXELFORMAT_RGBA32,rgba,w*4);
 SDL_Texture *t=s?SDL_CreateTextureFromSurface(r,s):NULL;SDL_DestroySurface(s);free(rgba);
 if(t){SDL_SetTextureScaleMode(t,SDL_SCALEMODE_NEAREST);SDL_SetTextureBlendMode(t,transparent?SDL_BLENDMODE_BLEND:SDL_BLENDMODE_NONE);}return t;
}
void bc_view_destroy(BCBoardView *v){if(!v)return;for(int m=0;m<2;m++){SDL_DestroyTexture(v->background[m]);for(int i=0;i<64;i++)for(int s=0;s<2;s++)SDL_DestroyTexture(v->sprites[m][i].texture[s]);}for(int p=0;p<6;p++)for(int l=0;l<8;l++)for(int f=0;f<64;f++)for(int s=0;s<2;s++)SDL_DestroyTexture(v->walk[p][l][f].texture[s]);free(v);}
BCBoardView *bc_view_load(SDL_Renderer *r,const char *path){
 FILE *f=fopen(path,"rb");if(!f)return NULL;
 BCBoardView *v=calloc(1,sizeof *v);uint8_t *data=malloc(64000),pal[768];char magic[4];
 if(!v||!data)goto bad;
 if(fread(magic,1,4,f)!=4||memcmp(magic,"BCP3",4)||fread(pal,1,768,f)!=768)goto bad;
 for(int m=0;m<2;m++){
  if(fread(data,1,64000,f)!=64000)goto bad;
  v->background[m]=texture(r,data,pal,320,200,1,false);if(!v->background[m])goto bad;
  int count=word(f);if(count!=(m?6:47))goto bad;
  for(int i=0;i<count;i++){
   int id=word(f),w=word(f),h=word(f),x=word(f),y=word(f);
   if(id<17||id>=(m?23:64)||w<1||w>320||h<1||h>200||x<0||y<0||v->sprites[m][id].texture[0])goto bad;
   Sprite *s=&v->sprites[m][id];s->w=w;s->h=h;s->x=(int16_t)x;s->y=(int16_t)y;
   if(fread(data,1,(size_t)w*h,f)!=(size_t)w*h)goto bad;
   for(int side=0;side<2;side++){s->texture[side]=texture(r,data,pal,w,h,side,true);if(!s->texture[side])goto bad;}
  }
 }
 int total=word(f);if(total<1||total>3072)goto bad;
 for(int i=0;i<total;i++){
  int pair=word(f),list=word(f),step=word(f),w=word(f),h=word(f),x=word(f),y=word(f);
  if(pair<0||pair>=6||list<0||list>=8||step<0||step>=64||w<1||w>320||h<1||h>200||x<0||y<0)goto bad;
  Sprite *s=&v->walk[pair][list][step];if(s->texture[0])goto bad;
  s->w=w;s->h=h;s->x=(int16_t)x;s->y=(int16_t)y;
  if(fread(data,1,(size_t)w*h,f)!=(size_t)w*h)goto bad;
  for(int side=0;side<2;side++){s->texture[side]=texture(r,data,pal,w,h,side,true);if(!s->texture[side])goto bad;}
 }
 for(unsigned kind=1;kind<=6;kind++)for(unsigned o=0;o<8;o++){
  const BCWalk *w=bc_walk_sequence(kind,o,0);for(unsigned i=0;i<w->count;i++)if(!v->walk[w->pair][w->list][i].texture[0])goto bad;
 }
 if(fgetc(f)!=EOF||ferror(f))goto bad;
 free(data);fclose(f);return v;
bad:free(data);fclose(f);bc_view_destroy(v);return NULL;
}
int bc_view_hit(bool perspective,float x,float y){if(x<24||y<100||x>=664||y>=500)return -1;return bc_geometry_hit(perspective,(int)((x-24)/2),(int)((y-100)/2));}
void bc_view_square_point(bool perspective,unsigned square,float *x,float *y){int px=0,py=0;(void)bc_geometry_anchor(perspective,square,&px,&py);*x=24+px*2.0f;*y=100+py*2.0f;}
typedef struct {BCCell piece;unsigned square;int x,y;bool moving;} Draw;
static int depth(const void *a,const void *b){const Draw *x=a,*y=b;if(x->y!=y->y)return x->y-y->y;return (int)y->square-(int)x->square;}
void bc_view_draw(BCBoardView *v,SDL_Renderer *r,const BCPosition *p,const BCMotion *motion,int selected,bool perspective){
 int mode=perspective?0:1;SDL_FRect bg={24,100,640,400};SDL_RenderTexture(r,v->background[mode],NULL,&bg);
 SDL_Rect clip={24,100,640,400};SDL_SetRenderClipRect(r,&clip);
 Draw items[33]={0};unsigned count=0;const BCBoard *b=motion->active?&motion->display:&p->board;
 for(unsigned square=0;square<120;square++)if(!(square&0x88)&&b->cells[square].kind&&(int)square!=bc_motion_hidden_square(motion)){
  Draw *d=&items[count++];d->piece=b->cells[square];d->square=square;(void)bc_geometry_anchor(perspective,square,&d->x,&d->y);
 }
 if(motion->active){Draw *d=&items[count++];d->piece=bc_motion_piece(motion);d->square=(unsigned)bc_motion_hidden_square(motion);d->x=motion->x;d->y=motion->y;d->moving=true;}
 qsort(items,count,sizeof *items,depth);
 for(unsigned i=0;i<count;i++){
  Draw d=items[i];static const unsigned icons[7]={0,18,21,22,17,19,20};
  unsigned frame=perspective?bc_geometry_frame(d.piece.kind,d.piece.side,d.square):icons[d.piece.kind];
  Sprite *s=&v->sprites[mode][frame];
  if(d.moving&&motion->walking){const BCWalk *w=motion->walking;s=&v->walk[w->pair][w->list][motion->frame-1];}
  SDL_FRect dest={24+2.0f*(d.x-s->x),100+2.0f*(d.y-s->y),2.0f*s->w,2.0f*s->h};SDL_RenderTexture(r,s->texture[d.piece.side],NULL,&dest);
 }
 if(selected>=0){BCMoveList moves;bc_generate_legal(p,&moves);for(size_t i=0;i<=moves.count;i++){
  if(i<moves.count&&moves.moves[i].from!=selected)continue;
  unsigned square=i==moves.count?(unsigned)selected:moves.moves[i].to;float x,y;bc_view_square_point(perspective,square,&x,&y);
  SDL_SetRenderDrawColor(r,i==moves.count?250:45,i==moves.count?210:220,70,255);SDL_FRect mark={x-5,y-3,10,6};SDL_RenderRect(r,&mark);
 }}
 SDL_SetRenderClipRect(r,NULL);
}
