#define _GNU_SOURCE
#include "stockfish.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <spawn.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <poll.h>
#include <signal.h>
#include <time.h>
#include <errno.h>
extern char **environ;
bool bc_uci_fen(const BCPosition *p,char *out,size_t capacity){
 char b[160],*s=b;const char *pieces=" KQRBNP";
 for(int rank=7;rank>=0;rank--){unsigned empty=0;
  for(unsigned file=0;file<8;file++){BCCell c=p->board.cells[rank*16+file];if(!c.kind){empty++;continue;}
   if(c.kind>6||c.side>1)return false;
   if(empty){*s++='0'+empty;empty=0;}char v=pieces[c.kind];*s++=c.side?v+('a'-'A'):v;
  }if(empty)*s++='0'+empty;if(rank)*s++='/';
 }
 *s++=' ';*s++=p->board.side?'b':'w';*s++=' ';
 char *rights=s;if(p->castle[0]&2)*s++='K';if(p->castle[0]&1)*s++='Q';if(p->castle[1]&2)*s++='k';if(p->castle[1]&1)*s++='q';if(s==rights)*s++='-';
 *s++=' ';if(p->ep>=0&&p->ep<120&&!(p->ep&0x88)){*s++='a'+(p->ep&7);*s++='1'+(p->ep>>4);}else *s++='-';
 snprintf(s,(size_t)(b+sizeof b-s)," %u %u",p->halfmove,p->fullmove?p->fullmove:1);
 if(strlen(b)+1>capacity)return false;
 strcpy(out,b);return true;
}
void bc_uci_move(BCMove m,char out[6]){out[0]='a'+(m.from&7);out[1]='1'+(m.from>>4);out[2]='a'+(m.to&7);out[3]='1'+(m.to>>4);out[4]=0;
 if(m.special&&m.kind>=2&&m.kind<=5){out[4]="  qrbn"[m.kind];out[5]=0;}}
bool bc_uci_parse(const BCPosition *p,const char *text,BCMove *move){BCMoveList legal;bc_generate_legal(p,&legal);for(size_t i=0;i<legal.count;i++){char v[6];bc_uci_move(legal.moves[i],v);if(!strcmp(v,text)){*move=legal.moves[i];return true;}}return false;}
static unsigned long long now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return (unsigned long long)t.tv_sec*1000+t.tv_nsec/1000000;}
typedef struct {int fd;bool (*cancel)(void *);void *context;char buffer[16384];size_t used;} Client;
static bool alive(Client *c,unsigned long long deadline){return now()<deadline&&(!c->cancel||!c->cancel(c->context));}
static bool send_text(Client *c,const char *text,unsigned long long deadline){size_t n=strlen(text);while(n&&alive(c,deadline)){ssize_t k=send(c->fd,text,n,MSG_NOSIGNAL|MSG_DONTWAIT);if(k>0){text+=k;n-=k;}else if(errno==EAGAIN||errno==EWOULDBLOCK||errno==EINTR){struct pollfd p={c->fd,POLLOUT,0};poll(&p,1,20);}else return false;}return n==0;}
static bool line(Client *c,char *out,size_t size,unsigned long long deadline){
 while(alive(c,deadline)){char *end=memchr(c->buffer,'\n',c->used);if(end){size_t n=(size_t)(end-c->buffer);if(n>=size)return false;memcpy(out,c->buffer,n);out[n]=0;memmove(c->buffer,end+1,c->used-n-1);c->used-=n+1;return true;}
  if(c->used==sizeof c->buffer)return false;
  struct pollfd p={c->fd,POLLIN,0};int r=poll(&p,1,20);if(r<0&&errno!=EINTR)return false;if(r>0){ssize_t k=recv(c->fd,c->buffer+c->used,sizeof c->buffer-c->used,MSG_DONTWAIT);if(k>0)c->used+=(size_t)k;else if(k==0||(errno!=EINTR&&errno!=EAGAIN))return false;}
 }return false;
}
static bool wait_for(Client *c,const char *expected,unsigned long long deadline){char b[16384];while(line(c,b,sizeof b,deadline))if(!strcmp(b,expected))return true;return false;}
bool bc_stockfish(const BCPosition *initial,const BCPosition *current,const BCMove *history,size_t count,unsigned depth,bool (*cancel)(void *),void *context,BCMove *move,char *error,size_t error_size){
 if(depth<1||depth>128){snprintf(error,error_size,"Stockfish depth must be 1-128.");return false;}
 bool ok=false;int sockets[2];pid_t pid;char path[4096],fen[160],b[16384];
 snprintf(error,error_size,"Stockfish unavailable; install it or set BC_STOCKFISH.");
 const char *exe=getenv("BC_STOCKFISH");if(!exe||!*exe){exe="/usr/games/stockfish";if(access(exe,X_OK)){snprintf(path,sizeof path,"%s/.local/share/battle-chess/stockfish/usr/games/stockfish",getenv("HOME")?getenv("HOME"):"");exe=access(path,X_OK)?"stockfish":path;}}
 if(socketpair(AF_UNIX,SOCK_STREAM|SOCK_CLOEXEC,0,sockets))return false;
 posix_spawn_file_actions_t actions;posix_spawn_file_actions_init(&actions);
 posix_spawn_file_actions_adddup2(&actions,sockets[1],0);posix_spawn_file_actions_adddup2(&actions,sockets[1],1);posix_spawn_file_actions_adddup2(&actions,sockets[1],2);posix_spawn_file_actions_addclose(&actions,sockets[0]);posix_spawn_file_actions_addclose(&actions,sockets[1]);
 char *argv[]={(char *)exe,NULL};int result=posix_spawnp(&pid,exe,&actions,NULL,argv,environ);posix_spawn_file_actions_destroy(&actions);close(sockets[1]);if(result){close(sockets[0]);return false;}
 Client c={.fd=sockets[0],.cancel=cancel,.context=context};unsigned long long deadline=now()+5000;
 snprintf(error,error_size,"Stockfish handshake failed or timed out.");
 if(!send_text(&c,"uci\n",deadline)||!wait_for(&c,"uciok",deadline))goto finish;
 if(!send_text(&c,"setoption name Threads value 1\nsetoption name Hash value 32\nucinewgame\nisready\n",deadline)||!wait_for(&c,"readyok",deadline))goto finish;
 snprintf(error,error_size,"Stockfish position could not be sent.");if(!bc_uci_fen(initial,fen,sizeof fen))goto finish;
 snprintf(b,sizeof b,"position fen %s moves",fen);if(!send_text(&c,b,deadline))goto finish;
 for(size_t i=0;i<count;i++){char v[6];bc_uci_move(history[i],v);snprintf(b,sizeof b," %s",v);if(!send_text(&c,b,deadline))goto finish;}
 if(!send_text(&c,"\n",deadline))goto finish;
 snprintf(b,sizeof b,"go depth %u\n",depth);if(!send_text(&c,b,deadline))goto finish;
 /* Depth search has no original-engine time limit; cancellation remains polled. */
 deadline=~0ULL;
 snprintf(error,error_size,"Stockfish stopped, timed out or returned an invalid move.");
 while(line(&c,b,sizeof b,deadline)){if(!strncmp(b,"bestmove ",9)){char v[16];if(sscanf(b+9,"%15s",v)==1)ok=bc_uci_parse(current,v,move);break;}}
finish:
 /* A dedicated process per turn keeps cancellation and game resets isolated. */
 close(c.fd);kill(pid,SIGKILL);while(waitpid(pid,NULL,0)<0&&errno==EINTR){}if(ok&&error_size)error[0]=0;return ok;
}
