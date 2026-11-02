#include "board_view.h"
#include <SDL3/SDL.h>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static void put(uint8_t data[33],unsigned s,unsigned k){unsigned i=(s>>4)*8+(s&7);if(i&1)data[1+i/2]|=k;else data[1+i/2]|=k<<4;}
static BCMove pick(BCPosition *p,unsigned from,unsigned to){BCMoveList l;bc_generate_legal(p,&l);for(size_t i=0;i<l.count;i++)if(l.moves[i].from==from&&l.moves[i].to==to)return l.moves[i];assert(0);return (BCMove){0};}
static unsigned run(BCPosition before,BCMove move,SDL_Renderer *r,BCBoardView *v){
 BCPosition saved=before,after=before;assert(bc_play(&after,move));
 BCMotion *m=calloc(1,sizeof *m);assert(m&&bc_motion_begin(m,&before,move,0,true));
 unsigned ticks=0,battle_frames=0;
 while(m->active&&ticks<6000){
  ticks+=2;bc_motion_tick(m,ticks,false);assert(!m->failed);
  if(m->battle_mode)for(unsigned i=0;i<m->battle.count;i++)battle_frames+=m->battle.actors[i].visible&&m->battle.actors[i].image==BC_ACTOR_CAPTURE;
  assert(SDL_SetRenderDrawColor(r,0,0,0,255)&&SDL_RenderClear(r));
  bc_view_draw(v,r,&after,m,-1,true);assert(SDL_RenderPresent(r));
 }
 assert(!m->active&&!m->failed&&!memcmp(&before,&saved,sizeof before));
 unsigned visible=0,expected=0;
 for(unsigned s=0;s<120;s++)if(!(s&0x88)){
  BCCell cell=m->display.cells[s];
  if(m->battle_mode){int id=m->battle.actor_map[s];cell=id<0?(BCCell){0}:m->battle.actors[id].piece;if(id>=0)assert(m->battle.actors[id].visible);}
  assert(cell.kind==after.board.cells[s].kind);if(cell.kind){assert(cell.side==after.board.cells[s].side);expected++;}
 }
 if(move.kind==6){
  assert(m->visual_valid&&!memcmp(m->display.cells,after.board.cells,sizeof m->display.cells));
  for(unsigned s=0;s<120;s++){int id=m->battle.actor_map[s];if(id>=0)assert(m->facing[s]==m->battle.actors[id].facing);}
  assert(m->battle_mode&&m->battle.done&&m->battle.capture.animation_counter==4&&battle_frames>0);
  for(unsigned i=0;i<m->battle.count;i++)visible+=m->battle.actors[i].visible;
  assert(visible==expected); /* No ghost victim at its original square. */
 }
 free(m);return battle_frames;
}
int main(int argc,char **argv){
 assert(argc==2&&SDL_Init(SDL_INIT_VIDEO));SDL_Window *w=SDL_CreateWindow("Special move validation",1024,624,SDL_WINDOW_HIDDEN);assert(w);
 SDL_Renderer *r=SDL_CreateRenderer(w,NULL);assert(r);BCBoardView *v=bc_view_load(r,argv[1]);assert(v);
 unsigned ep=0,castles=0,frames=0;
 for(unsigned side=0;side<2;side++){
  for(unsigned file=0;file<8;file++)for(int direction=-1;direction<=1;direction+=2){
   int neighbour=(int)file+direction;if(neighbour<0||neighbour>7)continue;
   unsigned rank=side?3:4,from=rank*16+file,victim=rank*16+neighbour,to=(side?rank-1:rank+1)*16+neighbour;
   uint8_t packed[33]={0};put(packed,4,1);put(packed,116,9);put(packed,from,6+side*8);put(packed,victim,6+(side^1)*8);
   BCPosition p={0};assert(bc_unpack(&p.board,packed));p.board.side=side;p.ep=to;p.fullmove=2;
   BCMove move=pick(&p,from,to);assert(move.special&&move.kind==6&&!move.capture);
   frames+=run(p,move,r,v);ep++;
  }
  uint8_t packed[33]={0};put(packed,4,1);put(packed,116,9);put(packed,side*112,3+side*8);put(packed,side*112+7,3+side*8);
  BCPosition p={0};assert(bc_unpack(&p.board,packed));p.board.side=side;p.ep=-1;p.fullmove=1;p.castle[side]=3;
  for(unsigned file=2;file<=6;file+=4){BCMove move=pick(&p,side*112+4,side*112+file);assert(move.special&&move.kind==1);run(p,move,r,v);castles++;}
 }
 bc_view_destroy(v);SDL_DestroyRenderer(r);SDL_DestroyWindow(w);SDL_Quit();
 printf("PASS: %u en-passant directions/files/colours and %u castles rendered to exact final occupancy (%u battle actor frames), no mutation or ghost victims.\n",ep,castles,frames);
}
