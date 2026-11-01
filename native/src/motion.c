#include "motion.h"
#include <string.h>
static int x(unsigned square){return 24+(square&7)*64+32;}
static int y(unsigned square){return 48+(7-(square>>4))*64+60;}
bool bc_motion_begin(BCMotion *m,const BCPosition *before,BCMove move,uint64_t tick){
 memset(m,0,sizeof *m);
 if(move.capture)return false;
 BCPosition verify=*before;if(!bc_play(&verify,move))return false;
 m->display=before->board;m->moves[0]=move;m->count=1;
 if(move.special&&move.kind==1){
  m->moves[0].special=0;unsigned rank=move.from&112;
  m->moves[1]=(BCMove){(uint8_t)(rank+((move.to&7)==6?7:0)),(uint8_t)(rank+((move.to&7)==6?5:3)),0,3,0};m->count=2;
 }
 m->last_tick=tick;m->active=true;m->x=x(move.from);m->y=y(move.from);
 /* Initial attach is visible immediately; the next ready call emits step1. */
 m->frame=1;return true;
}
void bc_motion_tick(BCMotion *m,uint64_t tick,bool pending){
 if(!m->active||!bc_presentation_tick(tick,&m->last_tick,pending))return;
 BCMove move=m->moves[m->index];
 if(m->frame<8){(void)bc_interpolate(x(move.from),y(move.from),x(move.to),y(move.to),8,m->frame++,&m->x,&m->y);return;}
 /* Complete this actor before a possible rook task. Display copy deliberately
  * uses cells only; piece-list bookkeeping remains in authoritative BCGame. */
 m->display.cells[move.to]=m->display.cells[move.from];m->display.cells[move.from].kind=0;
 if(++m->index==m->count){m->active=false;return;}
 move=m->moves[m->index];m->frame=1;m->x=x(move.from);m->y=y(move.from);
}
int bc_motion_hidden_square(const BCMotion *m){return m->active?m->moves[m->index].from:-1;}
BCCell bc_motion_piece(const BCMotion *m){return m->active?m->display.cells[m->moves[m->index].from]:(BCCell){0};}
