#define _POSIX_C_SOURCE 200809L
#include <SDL3/SDL.h>
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "difficulty.h"
#include "savegame.h"
typedef struct {
 SDL_Thread *thread;atomic_bool cancel,done;BCPosition position;
 BCMove *history;size_t count;BCSearchConfig config;BCSearchResult result;bool ok;
} Worker;
static bool cancelled(void *p){return atomic_load_explicit(&((Worker *)p)->cancel,memory_order_relaxed);}
static int search_thread(void *p){Worker *w=p;w->ok=bc_search(&w->position,w->history,w->count,&w->config,&w->result);atomic_store_explicit(&w->done,true,memory_order_release);return 0;}
static Worker *start(BCGame *g,unsigned level,bool smoke) {
 Worker *w=calloc(1,sizeof *w);if(!w)return NULL;
 atomic_init(&w->cancel,false);atomic_init(&w->done,false);
 w->position=*bc_game_position(g);w->count=bc_game_plies(g);
 if(w->count){w->history=malloc(w->count*sizeof *w->history);if(!w->history){free(w);return NULL;}}
 if(!bc_game_copy_moves(g,w->history,w->count)){free(w->history);free(w);return NULL;}
 bc_difficulty_config(level,1,&w->config);w->config.temporary=w->position.board.side;
 w->config.cancel=cancelled;w->config.userdata=w;w->config.seed=1;
 if(smoke){w->config.max_depth=2;w->config.time_budget_ms=100;}
 w->thread=SDL_CreateThread(search_thread,"Battle Chess search",w);
 if(!w->thread){free(w->history);free(w);return NULL;}return w;
}
static void stop(Worker **worker){Worker *w=*worker;if(!w)return;atomic_store(&w->cancel,true);SDL_WaitThread(w->thread,NULL);free(w->history);free(w);*worker=NULL;}
static void fail(const char *s){fprintf(stderr,"%s: %s\n",s,SDL_GetError());exit(1);}
static unsigned word(FILE *f){int a=fgetc(f),b=fgetc(f);if(a<0||b<0)fail("Truncated pieces");return (unsigned)a|((unsigned)b<<8);}
static void load(SDL_Renderer *r,const char *path,SDL_Texture *textures[2][7]) {
 FILE *f=fopen(path,"rb");if(!f){perror(path);exit(1);}char magic[4];uint8_t pal[768];
 if(fread(magic,1,4,f)!=4||memcmp(magic,"BCP1",4)||fread(pal,1,768,f)!=768)fail("Piece asset header");
 for(int k=1;k<=6;k++) {
  unsigned w=word(f),h=word(f);if(!w||w>64||!h||h>64)fail("Piece dimensions");
  uint8_t indices[4096],rgba[16384];if(fread(indices,1,w*h,f)!=w*h)fail("Piece data");
  for(int side=0;side<2;side++) {
   for(unsigned i=0;i<w*h;i++){unsigned v=indices[i];if(v>15)fail("Palette index");if(!side&&(v==1||v==9))v+=3;memcpy(rgba+4*i,pal+v*3,3);rgba[4*i+3]=v?255:0;}
   SDL_Surface *s=SDL_CreateSurfaceFrom((int)w,(int)h,SDL_PIXELFORMAT_RGBA32,rgba,(int)w*4);if(!s)fail("Surface");
   textures[side][k]=SDL_CreateTextureFromSurface(r,s);SDL_DestroySurface(s);if(!textures[side][k])fail("Texture");
   SDL_SetTextureScaleMode(textures[side][k],SDL_SCALEMODE_NEAREST);SDL_SetTextureBlendMode(textures[side][k],SDL_BLENDMODE_BLEND);
  }
 }
 if(fgetc(f)!=EOF)fail("Trailing pieces");fclose(f);
}
static const char *status_name(BCGameStatus s){static const char *names[]={"Playing","Check","Checkmate","Stalemate","Draw: insufficient material","Draw claimed","Draw: fivefold repetition","Draw: 75 moves"};return names[s];}
static void text(SDL_Renderer *r,int y,const char *s){SDL_SetRenderDrawColor(r,235,235,240,255);SDL_RenderDebugText(r,554,(float)y,s);}
static int square_at(float x,float y){int f=(int)((x-24)/64),row=(int)((y-48)/64);if(x<24||y<48||f>=8||row>=8)return -1;return (7-row)*16+f;}
static bool move_between(BCGame *g,int from,int to,unsigned promotion) {
 BCMoveList list;bc_generate_legal(bc_game_position(g),&list);
 for(size_t i=0;i<list.count;i++){BCMove m=list.moves[i];if(m.from!=from||m.to!=to)continue;
  if(m.special&&m.kind>=2&&m.kind<=5&&m.kind!=promotion)continue;
  return bc_game_move(g,m);
 }
 return false;
}
int main(int argc,char **argv) {
 if(argc<2||argc>3){fprintf(stderr,"Usage: %s pieces.bcp [--smoke]\n",argv[0]);return 2;}
 bool smoke=argc==3&&!strcmp(argv[2],"--smoke");if(argc==3&&!smoke)return 2;
 if(!SDL_Init(SDL_INIT_VIDEO))fail("SDL");SDL_Window *window;SDL_Renderer *r;
 if(!SDL_CreateWindowAndRenderer("Battle Chess Native - Development",1000,700,smoke?SDL_WINDOW_HIDDEN:SDL_WINDOW_RESIZABLE,&window,&r))fail("Window");
 SDL_SetRenderLogicalPresentation(r,832,624,SDL_LOGICAL_PRESENTATION_LETTERBOX);
 SDL_Texture *textures[2][7]={{0}};load(r,argv[1],textures);
 BCGame *g=bc_game_create(NULL);if(!g)fail("Game allocation");
 char *pref=SDL_GetPrefPath("battle-chess-native","game");
 char *save_path=NULL;
 if(pref){size_t n=strlen(pref)+16;save_path=malloc(n);if(save_path)snprintf(save_path,n,"%sgame.bcs",pref);SDL_free(pref);}
 if(smoke){
  free(save_path);save_path=strdup("/tmp/bc-ui-save-XXXXXX");
  if(!save_path)fail("Smoke path");
  int fd=mkstemp(save_path);if(fd<0)fail("Smoke temporary file");close(fd);
 }
 Worker *worker=NULL;bool running=true,computer=true,paused=false;int selected=-1;
 unsigned level=0,promotion=2,smoke_stage=0;uint64_t started=SDL_GetTicks();char message[160]="Click a piece, then its destination.";
 while(running) {
  SDL_Event e;
  while(SDL_PollEvent(&e)) {
   if(e.type==SDL_EVENT_QUIT)running=false;
   if(e.type==SDL_EVENT_KEY_DOWN) {
    SDL_Keycode k=e.key.key;
    if(k==SDLK_S)snprintf(message,sizeof message,"%s",save_path&&bc_game_save(g,save_path)?"Game saved.":"Save failed; previous file retained.");
    if(k==SDLK_L){
     BCGame *loaded=save_path?bc_game_load(save_path):NULL;
     if(loaded){stop(&worker);bc_game_destroy(g);g=loaded;selected=-1;paused=false;snprintf(message,sizeof message,"Game loaded with complete move history.");}
     else snprintf(message,sizeof message,"Load failed; current game retained.");
    }
    if(k==SDLK_ESCAPE)running=false;
    if(k==SDLK_N){stop(&worker);bc_game_destroy(g);g=bc_game_create(NULL);if(!g)fail("New game");selected=-1;paused=false;}
    if(k==SDLK_U){stop(&worker);bc_game_undo(g);if(computer&&bc_game_position(g)->board.side==1)bc_game_undo(g);selected=-1;paused=false;}
    if(k==SDLK_H){stop(&worker);computer=!computer;paused=false;selected=-1;}
    if(k==SDLK_SPACE){stop(&worker);paused=!paused;}
    if(k>=SDLK_0&&k<=SDLK_9){stop(&worker);level=(unsigned)(k-SDLK_0);paused=false;}
    if(k==SDLK_Q)promotion=2;if(k==SDLK_R)promotion=3;if(k==SDLK_B)promotion=4;if(k==SDLK_K)promotion=5;
    if(k==SDLK_D){stop(&worker);if(bc_game_claim_draw(g))snprintf(message,sizeof message,"Draw claimed.");else snprintf(message,sizeof message,"No draw claim available.");}
   }
   if(e.type==SDL_EVENT_MOUSE_BUTTON_DOWN&&e.button.button==SDL_BUTTON_LEFT&&!worker&&!paused&&(!computer||bc_game_position(g)->board.side==0)) {
    float x,y;SDL_RenderCoordinatesFromWindow(r,e.button.x,e.button.y,&x,&y);int s=square_at(x,y);
    if(s>=0) {
     if(selected>=0&&move_between(g,selected,s,promotion)){selected=-1;snprintf(message,sizeof message,"Move played.");}
     else {BCCell cell=bc_game_position(g)->board.cells[s];selected=cell.kind&&cell.side==bc_game_position(g)->board.side?s:-1;}
    }
   }
  }
  if(worker&&atomic_load_explicit(&worker->done,memory_order_acquire)) {
   if(worker->ok&&worker->result.has_move&&!cancelled(worker)&&bc_game_move(g,worker->result.move))snprintf(message,sizeof message,"Engine depth %u, %llu candidates",worker->result.depth,(unsigned long long)worker->result.nodes);
   else {snprintf(message,sizeof message,"Search stopped. Space resumes.");paused=true;}
   stop(&worker);
  }
  BCGameStatus state=bc_game_status(g);const BCPosition *p=bc_game_position(g);
  if(running&&computer&&!paused&&!worker&&p->board.side==1&&(state==BC_PLAYING||state==BC_CHECK)){worker=start(g,level,smoke);if(!worker){paused=true;snprintf(message,sizeof message,"Could not start search.");}}
  SDL_SetRenderDrawColor(r,23,27,35,255);SDL_RenderClear(r);
  BCMoveList moves;bc_generate_legal(p,&moves);
  for(int rank=0;rank<8;rank++)for(int file=0;file<8;file++) {
   int square=rank*16+file;SDL_FRect cell={24+file*64.0f,48+(7-rank)*64.0f,64,64};
   bool light=(rank+file)&1;SDL_SetRenderDrawColor(r,light?185:88,light?170:101,light?145:104,255);
   SDL_RenderFillRect(r,&cell);
   if(square==selected){SDL_SetRenderDrawColor(r,250,210,70,255);SDL_RenderRect(r,&cell);}
   if(selected>=0)for(size_t i=0;i<moves.count;i++)if(moves.moves[i].from==selected&&moves.moves[i].to==square){SDL_FRect dot={cell.x+27,cell.y+27,10,10};SDL_SetRenderDrawColor(r,45,180,95,255);SDL_RenderFillRect(r,&dot);break;}
   BCCell piece=p->board.cells[square];if(piece.kind){SDL_FRect dst={cell.x+12,cell.y+4,40,56};SDL_RenderTexture(r,textures[piece.side][piece.kind],NULL,&dst);}
  }
  SDL_SetRenderDrawColor(r,235,235,240,255);SDL_RenderDebugText(r,24,16,"BATTLE CHESS / NATIVE DEVELOPMENT");
  for(int i=0;i<8;i++){char label[2]={(char)('a'+i),0};SDL_RenderDebugText(r,52+i*64.0f,570,label);label[0]=(char)('8'-i);SDL_RenderDebugText(r,8,76+i*64.0f,label);}
  text(r,52,computer?"Human vs computer":"Two players");text(r,78,p->board.side?"Blue to move":"Red to move");text(r,104,status_name(state));
  text(r,130,worker?"Computer thinking...":paused?"Paused":"Ready");
  char line[80];snprintf(line,sizeof line,"Level: %s",level?"timed":"Novice");if(level)snprintf(line,sizeof line,"Level %u (%u seconds)",level,5u<<(level-1));text(r,170,line);
  text(r,204,"0-9: difficulty");text(r,228,"N: new game   U: undo");text(r,252,"H: one / two players");text(r,276,"Space: pause / resume");text(r,300,"D: claim draw");text(r,324,"Q/R/B/K: promotion");snprintf(line,sizeof line,"Promotion: %s",promotion==2?"queen":promotion==3?"rook":promotion==4?"bishop":"knight");text(r,348,line);
  text(r,372,"S: save   L: load");
  text(r,396,"Original engine + artwork");text(r,420,"Animations/audio pending");
  SDL_SetRenderDrawColor(r,235,235,240,255);SDL_RenderDebugText(r,24,600,message);
  if(smoke&&!smoke_stage&&getenv("BC_SCREENSHOT")) {
   SDL_Surface *shot=SDL_RenderReadPixels(r,NULL);
   if(!shot||!SDL_SaveBMP(shot,getenv("BC_SCREENSHOT")))fail("Screenshot");
   SDL_DestroySurface(shot);
  }
  if(!SDL_RenderPresent(r))fail("Present");
  if(smoke) {
   if(!smoke_stage){
    /* Exercise the actual mouse-event path through the logical viewport. */
    for(int row=6;row>=4;row-=2) {
     SDL_Event click={0};click.type=SDL_EVENT_MOUSE_BUTTON_DOWN;
     click.button.button=SDL_BUTTON_LEFT;
     if(!SDL_RenderCoordinatesToWindow(r,24+4*64+32,48+row*64+32,&click.button.x,&click.button.y)||!SDL_PushEvent(&click))fail("Smoke click");
    }
    smoke_stage=1;
   }
   else if(smoke_stage==1&&bc_game_plies(g)==2&&!worker){
    const SDL_Keycode keys[]={SDLK_S,SDLK_N,SDLK_L};
    for(unsigned i=0;i<3;i++){SDL_Event key={0};key.type=SDL_EVENT_KEY_DOWN;key.key.key=keys[i];if(!SDL_PushEvent(&key))fail("Smoke save/load key");}
    smoke_stage=2;
   }
   else if(smoke_stage==2){
    if(bc_game_plies(g)!=2||bc_game_position(g)->board.side!=0)fail("Smoke restored history");
    worker=start(g,9,true);if(!worker)fail("Smoke worker");stop(&worker);
    bc_game_undo(g);bc_game_undo(g);if(bc_game_plies(g))fail("Smoke undo");
    smoke_stage=3;running=false;
   }
   if(SDL_GetTicks()-started>5000)fail("Smoke timeout");
  }
  SDL_Delay(8);
 }
 stop(&worker);bc_game_destroy(g);if(smoke)unlink(save_path);free(save_path);
 for(int s=0;s<2;s++)for(int k=1;k<=6;k++)SDL_DestroyTexture(textures[s][k]);
 SDL_DestroyRenderer(r);SDL_DestroyWindow(window);SDL_Quit();
 if(smoke&&smoke_stage!=3)return 1;
 puts("Native board closed cleanly.");return 0;
}
