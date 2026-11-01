#define _POSIX_C_SOURCE 200809L
#include "savegame.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
static void move(BCGame *g,unsigned from,unsigned to){BCMoveList l;bc_generate_legal(bc_game_position(g),&l);for(size_t i=0;i<l.count;i++)if(l.moves[i].from==from&&l.moves[i].to==to){assert(bc_game_move(g,l.moves[i]));return;}assert(0);}
static void same(BCGame *a,BCGame *b){assert(b);assert(bc_game_plies(a)==bc_game_plies(b));assert(bc_game_status(a)==bc_game_status(b));assert(bc_game_repetitions(a)==bc_game_repetitions(b));assert(!memcmp(bc_game_position(a),bc_game_position(b),sizeof(BCPosition)));}
static uint32_t crc(uint8_t *p,size_t n){uint32_t v=UINT32_MAX;while(n--){v^=*p++;for(int i=0;i<8;i++)v=v&1?(v>>1)^0xedb88320u:v>>1;}return ~v;}
static void write_data(const char *path,uint8_t *data,size_t n){FILE *f=fopen(path,"wb");assert(f);assert(fwrite(data,1,n,f)==n);assert(!fclose(f));}
int main(void){
 char dir[]="/tmp/bc-save-test-XXXXXX";assert(mkdtemp(dir));char path[128];snprintf(path,sizeof path,"%s/game.bcs",dir);
 BCGame *g=bc_game_create(NULL);assert(bc_game_save(g,path));BCGame *loaded=bc_game_load(path);same(g,loaded);bc_game_destroy(loaded);
 unsigned from[]={6,118,37,85},to[]={37,85,6,118};
 for(unsigned i=0;i<8;i++)move(g,from[i%4],to[i%4]);
 assert(bc_game_can_claim_draw(g));assert(bc_game_claim_draw(g));assert(bc_game_save(g,path));loaded=bc_game_load(path);same(g,loaded);
 for(unsigned i=0;i<9;i++){assert(bc_game_undo(g));assert(bc_game_undo(loaded));same(g,loaded);}bc_game_destroy(loaded);
 unsigned seed=39;for(unsigned i=0;i<120;i++){BCGameStatus s=bc_game_status(g);if(s!=BC_PLAYING&&s!=BC_CHECK)break;BCMoveList l;bc_generate_legal(bc_game_position(g),&l);seed=1664525u*seed+1013904223u;assert(bc_game_move(g,l.moves[seed%l.count]));}
 assert(bc_game_plies(g)>20);assert(bc_game_save(g,path));loaded=bc_game_load(path);same(g,loaded);
 while(bc_game_plies(g)){assert(bc_game_undo(g));assert(bc_game_undo(loaded));same(g,loaded);}bc_game_destroy(loaded);
 move(g,20,52);assert(bc_game_save(g,path));
 uint8_t data[64];FILE *f=fopen(path,"rb");assert(f);size_t n=fread(data,1,sizeof data,f);fclose(f);assert(n==21);
 for(size_t i=0;i<n;i++){write_data(path,data,i);assert(!bc_game_load(path));}
 data[n]=0;write_data(path,data,n+1);assert(!bc_game_load(path));
 for(size_t i=0;i<n;i++){data[i]^=1;write_data(path,data,n);assert(!bc_game_load(path));data[i]^=1;}
 /* A correctly checksummed but illegal move must still fail replay. */
 data[13]=119;uint32_t v=crc(data,n-4);for(unsigned i=0;i<4;i++)data[n-4+i]=(uint8_t)(v>>(8*i));write_data(path,data,n);assert(!bc_game_load(path));
 assert(bc_game_save(g,path));BCPosition custom=*bc_game_position(g);BCGame *nonstandard=bc_game_create(&custom);assert(!bc_game_save(nonstandard,path));loaded=bc_game_load(path);same(g,loaded);
 bc_game_destroy(nonstandard);bc_game_destroy(loaded);bc_game_destroy(g);unlink(path);rmdir(dir);
 puts("PASS: save replay, complete undo/draw history, atomic replacement and malformed/illegal rejection.");return 0;
}
