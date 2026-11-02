#define _POSIX_C_SOURCE 200809L
#include <SDL3/SDL.h>
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "difficulty.h"
#include "savegame.h"
#include "motion.h"
#include "board_view.h"
#include "audio_output.h"
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
static const char *status_name(BCGameStatus s){static const char *names[]={"Playing","Check","Checkmate","Stalemate","Draw: insufficient material","Draw claimed","Draw: fivefold repetition","Draw: 75 moves"};return names[s];}
static void text(SDL_Renderer *r,int y,const char *s){SDL_SetRenderDrawColor(r,235,235,240,255);SDL_RenderDebugText(r,700,(float)y,s);}
static bool move_between(BCGame *g,int from,int to,unsigned promotion,BCMotion *motion,bool perspective,BCAudio *audio) {
 BCMoveList list;bc_generate_legal(bc_game_position(g),&list);
 for(size_t i=0;i<list.count;i++){BCMove m=list.moves[i];if(m.from!=from||m.to!=to)continue;
  if(m.special&&m.kind>=2&&m.kind<=5&&m.kind!=promotion)continue;
  BCPosition before=*bc_game_position(g);
  if(!bc_game_move(g,m))return false;
  (void)bc_motion_begin_audio(motion,&before,m,SDL_GetTicks()*1193182u/65536000u,perspective,motion->visual_valid&&!memcmp(motion->display.cells,before.board.cells,sizeof before.board.cells)?motion->facing:NULL,bc_audio_event,audio);
  return true;
 }
 return false;
}
int main(int argc,char **argv) {
 if(argc<2||argc>3){fprintf(stderr,"Usage: %s pieces.bcp [--smoke]\n",argv[0]);return 2;}
 bool perspective=!(argc==3&&!strcmp(argv[2],"--smoke-flat"));
 bool initial_perspective=perspective;
 bool smoke=argc==3&&(!strcmp(argv[2],"--smoke")||!strcmp(argv[2],"--smoke-flat"));if(argc==3&&!smoke)return 2;
 if(!SDL_Init(SDL_INIT_VIDEO))fail("SDL");SDL_Window *window;SDL_Renderer *r;
 if(!SDL_CreateWindowAndRenderer("Battle Chess Native - Development",1200,732,smoke?SDL_WINDOW_HIDDEN:SDL_WINDOW_RESIZABLE,&window,&r))fail("Window");
 SDL_SetRenderLogicalPresentation(r,1024,624,SDL_LOGICAL_PRESENTATION_LETTERBOX);
 BCBoardView *view=bc_view_load(r,argv[1]);if(!view)fail("Board assets");
 BCAudio audio={0};const char *slash=strrchr(argv[1],'/');size_t prefix=slash?(size_t)(slash-argv[1]+1):0;
 char *sound_path=malloc(prefix+16);if(!sound_path)fail("Sound path");memcpy(sound_path,argv[1],prefix);strcpy(sound_path+prefix,"sounds.bca");
 (void)bc_audio_open(&audio,sound_path);free(sound_path);if(smoke)bc_audio_mute(&audio,true);
 BCGame *g=bc_game_create(NULL);if(!g)fail("Game allocation");
 char *pref=SDL_GetPrefPath("battle-chess-native","game");
 char *save_path=NULL;
 if(pref){size_t n=strlen(pref)+16;save_path=malloc(n);if(save_path)snprintf(save_path,n,"%sgame.bcs",pref);SDL_free(pref);}
 if(smoke){
  free(save_path);save_path=strdup("/tmp/bc-ui-save-XXXXXX");
  if(!save_path)fail("Smoke path");
  int fd=mkstemp(save_path);if(fd<0)fail("Smoke temporary file");close(fd);
 }
 BCMotion motion={0};
 Worker *worker=NULL;bool running=true,computer=true,paused=false;int selected=-1;
 unsigned level=0,promotion=2,smoke_stage=0;uint64_t started=SDL_GetTicks();char message[160]="Click a piece, then its destination.";
 while(running) {
  SDL_Event e;bool had_input=false;
  while(SDL_PollEvent(&e)) {
   if(e.type==SDL_EVENT_KEY_DOWN||e.type==SDL_EVENT_MOUSE_BUTTON_DOWN)had_input=true;
   if(e.type==SDL_EVENT_QUIT)running=false;
   if(e.type==SDL_EVENT_KEY_DOWN) {
    SDL_Keycode k=e.key.key;
    if(k==SDLK_S)snprintf(message,sizeof message,"%s",save_path&&bc_game_save(g,save_path)?"Game saved.":"Save failed; previous file retained.");
    if(k==SDLK_L){
     BCGame *loaded=save_path?bc_game_load(save_path):NULL;
     if(loaded){stop(&worker);bc_game_destroy(g);g=loaded;selected=-1;paused=false;motion.active=false;motion.visual_valid=false;bc_audio_clear(&audio);bc_audio_pause(&audio,false);snprintf(message,sizeof message,"Game loaded with complete move history.");}
     else snprintf(message,sizeof message,"Load failed; current game retained.");
    }
    if(k==SDLK_V){motion.active=false;motion.visual_valid=false;bc_audio_clear(&audio);bc_audio_pause(&audio,false);perspective=!perspective;selected=-1;}
    if(k==SDLK_M)bc_audio_mute(&audio,!audio.muted);
    if(k==SDLK_ESCAPE)running=false;
    if(k==SDLK_N){stop(&worker);bc_game_destroy(g);g=bc_game_create(NULL);if(!g)fail("New game");selected=-1;paused=false;motion.active=false;motion.visual_valid=false;bc_audio_clear(&audio);bc_audio_pause(&audio,false);}
    if(k==SDLK_U){stop(&worker);bc_game_undo(g);if(computer&&bc_game_position(g)->board.side==1)bc_game_undo(g);selected=-1;paused=false;motion.active=false;motion.visual_valid=false;bc_audio_clear(&audio);bc_audio_pause(&audio,false);}
    if(k==SDLK_H){stop(&worker);computer=!computer;paused=false;selected=-1;motion.active=false;motion.visual_valid=false;bc_audio_clear(&audio);bc_audio_pause(&audio,false);}
    if(k==SDLK_SPACE){stop(&worker);paused=!paused;bc_audio_pause(&audio,paused);motion.last_tick=SDL_GetTicks()*1193182u/65536000u;}
    if(k>=SDLK_0&&k<=SDLK_9){stop(&worker);level=(unsigned)(k-SDLK_0);paused=false;bc_audio_pause(&audio,false);}
    if(k==SDLK_Q)promotion=2;if(k==SDLK_R)promotion=3;if(k==SDLK_B)promotion=4;if(k==SDLK_K)promotion=5;
    if(k==SDLK_D){stop(&worker);if(bc_game_claim_draw(g))snprintf(message,sizeof message,"Draw claimed.");else snprintf(message,sizeof message,"No draw claim available.");}
   }
   if(e.type==SDL_EVENT_MOUSE_BUTTON_DOWN&&e.button.button==SDL_BUTTON_LEFT&&!worker&&!paused&&!motion.active&&(!computer||bc_game_position(g)->board.side==0)) {
    float x,y;SDL_RenderCoordinatesFromWindow(r,e.button.x,e.button.y,&x,&y);int s=bc_view_hit(perspective,x,y);
    if(s>=0) {
     if(selected>=0&&move_between(g,selected,s,promotion,&motion,perspective,&audio)){selected=-1;snprintf(message,sizeof message,"Move played.");}
     else {BCCell cell=bc_game_position(g)->board.cells[s];selected=cell.kind&&cell.side==bc_game_position(g)->board.side?s:-1;}
    }
   }
  }
  if(bc_audio_busy(&audio))motion.last_tick=SDL_GetTicks()*1193182u/65536000u;
  else if(!paused)bc_motion_tick(&motion,SDL_GetTicks()*1193182u/65536000u,had_input);
  if(worker&&atomic_load_explicit(&worker->done,memory_order_acquire)) {
   BCPosition before=*bc_game_position(g);
   if(worker->ok&&worker->result.has_move&&!cancelled(worker)&&bc_game_move(g,worker->result.move)){
    (void)bc_motion_begin_audio(&motion,&before,worker->result.move,SDL_GetTicks()*1193182u/65536000u,perspective,motion.visual_valid&&!memcmp(motion.display.cells,before.board.cells,sizeof before.board.cells)?motion.facing:NULL,bc_audio_event,&audio);
    snprintf(message,sizeof message,"Engine depth %u, %llu candidates",worker->result.depth,(unsigned long long)worker->result.nodes);
   }
   else {snprintf(message,sizeof message,"Search stopped. Space resumes.");paused=true;}
   stop(&worker);
  }
  BCGameStatus state=bc_game_status(g);const BCPosition *p=bc_game_position(g);
  if(running&&computer&&!paused&&!worker&&!motion.active&&!bc_audio_busy(&audio)&&p->board.side==1&&(state==BC_PLAYING||state==BC_CHECK)){worker=start(g,level,smoke);if(!worker){paused=true;snprintf(message,sizeof message,"Could not start search.");}}
  SDL_SetRenderDrawColor(r,23,27,35,255);SDL_RenderClear(r);
  bc_view_draw(view,r,p,&motion,selected,perspective);
  SDL_SetRenderDrawColor(r,235,235,240,255);SDL_RenderDebugText(r,24,16,"BATTLE CHESS / NATIVE DEVELOPMENT");
  text(r,52,computer?"Human vs computer":"Two players");text(r,78,p->board.side?"Blue to move":"Red to move");text(r,104,status_name(state));
  text(r,130,worker?"Computer thinking...":paused?"Paused":motion.active?"Piece moving...":"Ready");
  char line[80];snprintf(line,sizeof line,"Level: %s",level?"timed":"Novice");if(level)snprintf(line,sizeof line,"Level %u (%u seconds)",level,5u<<(level-1));text(r,170,line);
  text(r,204,"0-9: difficulty");text(r,228,"N: new game   U: undo");text(r,252,"H: one / two players");text(r,276,"Space: pause / resume");text(r,300,"D: claim draw");text(r,324,"Q/R/B/K: promotion");snprintf(line,sizeof line,"Promotion: %s",promotion==2?"queen":promotion==3?"rook":promotion==4?"bishop":"knight");text(r,348,line);
  text(r,372,"S: save   L: load");
  text(r,396,"V: perspective / flat");snprintf(line,sizeof line,"M: sound %s (%u held)",!audio.stream?"unavailable":audio.muted?"off":"on / nominal",audio.rejected);text(r,420,line);
  SDL_SetRenderDrawColor(r,235,235,240,255);SDL_RenderDebugText(r,24,600,message);
  if(smoke&&!smoke_stage&&getenv("BC_SCREENSHOT")) {
   SDL_Surface *shot=SDL_RenderReadPixels(r,NULL);
   if(!shot||!SDL_SaveBMP(shot,getenv("BC_SCREENSHOT")))fail("Screenshot");
   SDL_DestroySurface(shot);
  }
  if(smoke&&motion.active&&motion.operation==2&&motion.pixel_count==3&&getenv("BC_TURN_SCREENSHOT")) {
   SDL_Surface *shot=SDL_RenderReadPixels(r,NULL);
   if(!shot||!SDL_SaveBMP(shot,getenv("BC_TURN_SCREENSHOT")))fail("Turn screenshot");
   SDL_DestroySurface(shot);
  }
  if(smoke&&motion.active&&motion.frame==4&&getenv("BC_MOTION_SCREENSHOT")) {
   SDL_Surface *shot=SDL_RenderReadPixels(r,NULL);
   if(!shot||!SDL_SaveBMP(shot,getenv("BC_MOTION_SCREENSHOT")))fail("Motion screenshot");
   SDL_DestroySurface(shot);
  }
  if(!SDL_RenderPresent(r))fail("Present");
  if(smoke) {
   if(!smoke_stage){
    /* Exercise the actual mouse-event path through the logical viewport. */
    for(int row=6;row>=4;row-=2) {
     SDL_Event click={0};click.type=SDL_EVENT_MOUSE_BUTTON_DOWN;
     click.button.button=SDL_BUTTON_LEFT;
     float px,py;bc_view_square_point(perspective,(7-row)*16+4,&px,&py);
     if(!SDL_RenderCoordinatesToWindow(r,px,py,&click.button.x,&click.button.y)||!SDL_PushEvent(&click))fail("Smoke click");
    }
    smoke_stage=1;
   }
   else if(smoke_stage==1&&bc_game_plies(g)==2&&!worker&&!motion.active){
    const SDL_Keycode keys[]={SDLK_S,SDLK_N,SDLK_L};
    for(unsigned i=0;i<3;i++){SDL_Event key={0};key.type=SDL_EVENT_KEY_DOWN;key.key.key=keys[i];if(!SDL_PushEvent(&key))fail("Smoke save/load key");}
    smoke_stage=2;
   }
   else if(smoke_stage==2){
    if(bc_game_plies(g)!=2||bc_game_position(g)->board.side!=0)fail("Smoke restored history");
    worker=start(g,9,true);if(!worker)fail("Smoke worker");stop(&worker);
    bc_game_undo(g);bc_game_undo(g);if(bc_game_plies(g))fail("Smoke undo");
    SDL_Event key={0};key.type=SDL_EVENT_KEY_DOWN;key.key.key=SDLK_V;
    if(!SDL_PushEvent(&key))fail("Smoke view toggle");
    smoke_stage=3;
   }
   else if(smoke_stage==3){
    if(perspective==initial_perspective||bc_game_plies(g))fail("Smoke view state");
    smoke_stage=4;running=false;
   }
   if(SDL_GetTicks()-started>25000){fprintf(stderr,"Smoke state: stage=%u plies=%zu active=%d failed=%d pc=%u/%u op=%u frame=%u actor=%u\n",smoke_stage,bc_game_plies(g),motion.active,motion.failed,motion.pc,motion.plan.count,motion.operation,motion.frame,motion.actor);fail("Smoke timeout");}
  }
  SDL_Delay(8);
 }
 stop(&worker);bc_game_destroy(g);if(smoke)unlink(save_path);free(save_path);
 bc_audio_close(&audio);
 bc_view_destroy(view);
 SDL_DestroyRenderer(r);SDL_DestroyWindow(window);SDL_Quit();
 if(smoke&&smoke_stage!=4)return 1;
 puts("Native board closed cleanly.");return 0;
}
