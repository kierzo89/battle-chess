#define _POSIX_C_SOURCE 200809L
#include "stockfish.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static unsigned checks;
static bool cancel(void *ctx){(void)ctx;return ++checks>15;}
int main(int argc,char **argv){
 if(getenv("BC_TEST_UCI_DEPTH")){char line[1024];while(fgets(line,sizeof line,stdin)){
  if(!strcmp(line,"uci\n"))puts("uciok");else if(!strcmp(line,"isready\n"))puts("readyok");
  else if(!strncmp(line,"go ",3)){puts(!strcmp(line,"go depth 4\n")?"bestmove e2e4":"bestmove invalid");fflush(stdout);return 0;}
  fflush(stdout);
 }return 0;}
 BCPosition initial,p;bc_position_initial(&initial);p=initial;char fen[160],v[6],error[160];BCMove move,history[12];
 assert(bc_uci_fen(&p,fen,sizeof fen));assert(!strcmp(fen,"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"));
 assert(!bc_uci_fen(&p,fen,2));assert(!bc_uci_parse(&p,"e2e5",&move));assert(!bc_uci_parse(&p,"e2e4q",&move));
 assert(bc_uci_parse(&p,"e2e4",&move));history[0]=move;assert(bc_play(&p,move));assert(bc_uci_fen(&p,fen,sizeof fen));assert(strstr(fen," b KQkq e3 0 1"));
 BCMove castle={.from=4,.to=6,.kind=1,.special=1};bc_uci_move(castle,v);assert(!strcmp(v,"e1g1"));
 for(unsigned k=2;k<=5;k++){BCMove promo={.from=96,.to=112,.kind=k,.special=1};bc_uci_move(promo,v);assert(v[4]=="  qrbn"[k]);}
 /* Build a legal promotion fixture; all four suffixes must map to native moves. */
 BCPosition promotion={0};promotion.ep=-1;promotion.fullmove=1;
 uint8_t packed[33]={0};packed[1+4/2]=0x10;packed[1+60/2]=0x90;packed[1+48/2]=0x60;
 assert(bc_unpack(&promotion.board,packed));
 for(unsigned k=2;k<=5;k++){snprintf(v,sizeof v,"a7a8%c","  qrbn"[k]);assert(bc_uci_parse(&promotion,v,&move));assert(move.kind==k&&move.special);}
 if(argc>1){assert(setenv("BC_STOCKFISH",argv[1],1)==0);
  for(size_t n=1;n<8;n++){assert(bc_stockfish(&initial,&p,history,n,4,NULL,NULL,&move,error,sizeof error));history[n]=move;assert(bc_play(&p,move));}
  assert(!bc_stockfish(&initial,&p,history,8,128,cancel,NULL,&move,error,sizeof error));
 }
 /* Verify the actual command uses depth only, rather than a time cutoff. */
 assert(setenv("BC_STOCKFISH",argv[0],1)==0);assert(setenv("BC_TEST_UCI_DEPTH","1",1)==0);
 assert(bc_stockfish(&initial,&initial,NULL,0,4,NULL,NULL,&move,error,sizeof error));
 assert(move.from==20&&move.to==52);assert(unsetenv("BC_TEST_UCI_DEPTH")==0);
 assert(!bc_stockfish(&initial,&initial,NULL,0,0,NULL,NULL,&move,error,sizeof error));
 assert(strstr(error,"depth"));
 assert(setenv("BC_STOCKFISH","/nonexistent/bc-stockfish",1)==0);
 assert(!bc_stockfish(&initial,&p,history,0,4,NULL,NULL,&move,error,sizeof error));assert(strstr(error,"unavailable"));
 puts("PASS: FEN, legal move filtering, promotion/castling notation, engine history, cancellation and missing executable.");
}
