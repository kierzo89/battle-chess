#define _POSIX_C_SOURCE 200809L
#include "savegame.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#define MAX_PLIES 32768u
static uint32_t crc(const uint8_t *p,size_t n) {
 uint32_t v=UINT32_MAX;
 while(n--){v^=*p++;for(unsigned b=0;b<8;b++)v=(v>>1)^(0xedb88320u& (0u-(v&1u)));}
 return ~v;
}
static void put32(uint8_t *p,uint32_t n){for(unsigned i=0;i<4;i++)p[i]=(uint8_t)(n>>(8*i));}
static uint32_t get32(const uint8_t *p){return (uint32_t)p[0]|(uint32_t)p[1]<<8|(uint32_t)p[2]<<16|(uint32_t)p[3]<<24;}
static bool standard(const BCGame *g) {
 BCPosition p;bc_position_initial(&p);const BCPosition *s=bc_game_initial_position(g);
 uint8_t a[33],b[33];bc_pack(&p.board,a);bc_pack(&s->board,b);
 return !memcmp(a,b,33)&&s->castle[0]==p.castle[0]&&s->castle[1]==p.castle[1]&&s->ep==p.ep&&s->halfmove==p.halfmove&&s->fullmove==p.fullmove;
}
bool bc_game_save(const BCGame *g,const char *path) {
 if(!g||!path||!standard(g)||bc_game_plies(g)>MAX_PLIES)return false;
 size_t n=bc_game_plies(g),size=12+5*n+4;
 uint8_t *data=calloc(1,size);BCMove *moves=n?malloc(n*sizeof *moves):NULL;
 if(!data||(n&&!moves)){free(data);free(moves);return false;}
 memcpy(data,"BCS1",4);put32(data+4,(uint32_t)n);data[8]=bc_game_status(g)==BC_DRAW_CLAIMED;
 bool ok=bc_game_copy_moves(g,moves,n);
 for(size_t i=0;i<n;i++){uint8_t *p=data+12+5*i;BCMove m=moves[i];p[0]=m.from;p[1]=m.to;p[2]=m.special;p[3]=m.kind;p[4]=m.capture;}
 free(moves);put32(data+size-4,crc(data,size-4));
 size_t len=strlen(path);char *temp=malloc(len+12);
 if(!temp){free(data);return false;}
 snprintf(temp,len+12,"%s.tmp.XXXXXX",path);
 int fd=mkstemp(temp);if(fd<0)ok=false;
 if(fd>=0){
  FILE *f=fdopen(fd,"wb");
  if(!f){close(fd);ok=false;}
  else {if(fwrite(data,1,size,f)!=size||fflush(f)||fsync(fd))ok=false;if(fclose(f))ok=false;}
  if(ok&&rename(temp,path))ok=false;
  if(!ok)unlink(temp);
 }
 free(temp);free(data);return ok;
}
BCGame *bc_game_load(const char *path) {
 if(!path)return NULL;
 FILE *f=fopen(path,"rb");if(!f)return NULL;
 uint8_t header[12];if(fread(header,1,12,f)!=12||memcmp(header,"BCS1",4)||header[8]>1||header[9]||header[10]||header[11]){fclose(f);return NULL;}
 uint32_t n=get32(header+4);if(n>MAX_PLIES){fclose(f);return NULL;}
 size_t size=12+5*(size_t)n+4;uint8_t *data=malloc(size);
 if(!data){fclose(f);return NULL;}
 memcpy(data,header,12);bool ok=fread(data+12,1,size-12,f)==size-12;
 if(fgetc(f)!=EOF||ferror(f))ok=false;
 fclose(f);
 if(!ok||get32(data+size-4)!=crc(data,size-4)){free(data);return NULL;}
 BCGame *g=bc_game_create(NULL);if(!g){free(data);return NULL;}
 for(uint32_t i=0;i<n;i++) {
  const uint8_t *p=data+12+5*i;BCMove m={p[0],p[1],p[2],p[3],p[4]};
  if(!bc_game_move(g,m)){ok=false;break;}
 }
 if(ok&&header[8]&&!bc_game_claim_draw(g))ok=false;
 free(data);if(!ok){bc_game_destroy(g);return NULL;}return g;
}
