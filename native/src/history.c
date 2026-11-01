#include "history.h"
#include <stdlib.h>
#include <string.h>
static bool quiet(BCMove m){return m.kind&&m.kind!=6&&!m.capture&&!m.special;}
unsigned bc_original_quiet_count(const BCMove *moves,size_t count) {
 unsigned n=0;while(count&&quiet(moves[--count]))n++;return n;
}
/* 9C34 recovered reverse-link repetition scan; first DOS word is destination,
 * despite the retained Pair source naming it 'from'. Bounds replace the DOS
 * sentinel before the accessible move history, not the scan algorithm. */
unsigned bc_original_repetitions(const BCMove *moves,size_t count,bool required) {
 if(count<4)return 1;
 size_t h=count,f=h-4,i=h,d;
 while(i&&quiet(moves[i-1])&&((f<i)||!required))i--;
 if(f<i)return 1;
 unsigned result=1;d=h;
 for(;;) {
  d--;unsigned b=moves[d].to;size_t e=d+2;
  while(e<h){if(moves[e].from==b)goto next;e+=2;}
  e=d;unsigned c=moves[e].from;
  do {
   if(e<i+2)return result;
   e-=2;if(moves[e].to==c)c=moves[e].from;
  }while(!(c==b&&f+1>=e));
  if(e<f) {
   f=e;if((h-f)&1){if(f==i)return result;f--;}
   d=h;
  }
next:
  if(d<=f) {
   result++;if(f<i+2)return result;
   h=f;f-=2;d=h;
  }
 }
}
typedef struct {BCPosition position;uint8_t key[36];BCMove move;} Step;
struct BCGame {Step *steps;size_t count,capacity;bool claimed;};
static void key(const BCPosition *p,uint8_t out[36]) {
 bc_pack(&p->board,out);
 /* Empty-cell side/index are bookkeeping, not chess position identity. */
 for(unsigned i=1;i<33;i++) {
  if(!(out[i]&0x70))out[i]&=15;
  if(!(out[i]&7))out[i]&=240;
 }
 out[33]=p->castle[0];out[34]=p->castle[1];out[35]=255;
 if(p->ep>=0) {
  BCMoveList l;bc_generate_legal(p,&l);
  for(size_t i=0;i<l.count;i++)if(l.moves[i].special&&l.moves[i].kind==6){out[35]=(uint8_t)p->ep;break;}
 }
}
BCGame *bc_game_create(const BCPosition *start) {
 BCGame *g=calloc(1,sizeof *g);if(!g)return NULL;
 g->capacity=32;g->steps=calloc(g->capacity,sizeof *g->steps);
 if(!g->steps){free(g);return NULL;}
 if(start)g->steps[0].position=*start;else bc_position_initial(&g->steps[0].position);
 key(&g->steps[0].position,g->steps[0].key);return g;
}
void bc_game_destroy(BCGame *g){if(g){free(g->steps);free(g);}}
const BCPosition *bc_game_position(const BCGame *g){return &g->steps[g->count].position;}
size_t bc_game_plies(const BCGame *g){return g->count;}
unsigned bc_game_repetitions(const BCGame *g) {
 unsigned n=1;const Step *now=&g->steps[g->count];
 size_t earliest=g->count>now->position.halfmove?g->count-now->position.halfmove:0;
 for(size_t i=g->count;i>=earliest+2;) {
  i-=2;if(!memcmp(now->key,g->steps[i].key,36))n++;
 }
 return n;
}
static bool dead_material(const BCBoard *b) {
 unsigned minor=0,knights=0;int bishop_colour=-1;
 for(int s=0;s<120;s++)if(!(s&0x88)) {
  unsigned k=b->cells[s].kind;if(!k||k==1)continue;
  if(k!=4&&k!=5)return false;
  minor++;if(k==5)knights++;
  else {int c=((s&7)+(s>>4))&1;if(bishop_colour==-1)bishop_colour=c;else if(bishop_colour!=c)bishop_colour=2;}
 }
 return minor<=1||(!knights&&bishop_colour!=2);
}
BCGameStatus bc_game_status(const BCGame *g) {
 const BCPosition *p=bc_game_position(g);BCMoveList moves;bc_generate_legal(p,&moves);
 bool check=bc_in_check(&p->board,p->board.side);
 if(!moves.count)return check?BC_CHECKMATE:BC_STALEMATE;
 if(g->claimed)return BC_DRAW_CLAIMED;
 if(dead_material(&p->board))return BC_DEAD_MATERIAL;
 if(p->halfmove>=150)return BC_DRAW_SEVENTYFIVE;
 if(bc_game_repetitions(g)>=5)return BC_DRAW_FIVEFOLD;
 return check?BC_CHECK:BC_PLAYING;
}
bool bc_game_can_claim_draw(const BCGame *g) {
 BCGameStatus state=bc_game_status(g);if(state!=BC_PLAYING&&state!=BC_CHECK)return false;
 return bc_game_position(g)->halfmove>=100||bc_game_repetitions(g)>=3;
}
bool bc_game_claim_draw(BCGame *g) {
 if(!bc_game_can_claim_draw(g))return false;
 g->claimed=true;return true;
}
bool bc_game_move(BCGame *g,BCMove move) {
 BCGameStatus state=bc_game_status(g);if(state!=BC_PLAYING&&state!=BC_CHECK)return false;
 Step next={0};next.position=*bc_game_position(g);
 if(!bc_play(&next.position,move))return false;
 if(g->count+1>=g->capacity) {
  if(g->capacity>SIZE_MAX/(2*sizeof *g->steps))return false;
  size_t capacity=g->capacity*2;Step *steps=realloc(g->steps,capacity*sizeof *steps);
  if(!steps)return false;
  g->steps=steps;g->capacity=capacity;
 }
 next.move=move;key(&next.position,next.key);g->steps[++g->count]=next;return true;
}
bool bc_game_undo(BCGame *g) {
 if(g->claimed){g->claimed=false;return true;}
 if(!g->count)return false;
 g->count--;return true;
}

bool bc_game_copy_moves(const BCGame *g,BCMove *out,size_t capacity) {
 if(capacity<g->count||(!out&&g->count))return false;
 for(size_t i=0;i<g->count;i++)out[i]=g->steps[i+1].move;
 return true;
}

const BCPosition *bc_game_initial_position(const BCGame *g){return &g->steps[0].position;}
