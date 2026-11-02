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
#include "book.h"
typedef struct {
 SDL_Thread *thread;atomic_bool cancel,done;BCPosition position;
 BCMove *history;size_t count;BCSearchConfig config;BCSearchResult result;bool ok,use_book,book_hit;unsigned book_draw;
} Worker;
static bool cancelled(void *p){return atomic_load_explicit(&((Worker *)p)->cancel,memory_order_relaxed);}
static int search_thread(void *p){Worker *w=p;if(w->use_book&&!cancelled(w)&&bc_book_move(&w->position,w->history,w->count,w->book_draw,&w->result.move)){
 w->book_hit=w->ok=w->result.has_move=true;
 }else w->ok=bc_search(&w->position,w->history,w->count,&w->config,&w->result);atomic_store_explicit(&w->done,true,memory_order_release);return 0;}
static Worker *start(BCGame *g,unsigned level,bool smoke) {
 Worker *w=calloc(1,sizeof *w);if(!w)return NULL;
 atomic_init(&w->cancel,false);atomic_init(&w->done,false);
 w->position=*bc_game_position(g);w->count=bc_game_plies(g);
 if(w->count){w->history=malloc(w->count*sizeof *w->history);if(!w->history){free(w);return NULL;}}
 if(!bc_game_copy_moves(g,w->history,w->count)){free(w->history);free(w);return NULL;}
 bc_difficulty_config(level,1,&w->config);w->config.temporary=w->position.board.side;
 w->config.cancel=cancelled;w->config.userdata=w;w->config.seed=1;
 /* Novice bypasses book in recovered search_turn_8061. The host owns its
  * own deterministic MS-style RNG stream; whole-session DOS RNG parity is not claimed. */
 static uint32_t book_random=1;
 w->use_book=level>0;book_random=book_random*214013u+2531011u;
 w->book_draw=smoke?0:((book_random>>16)&15);
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
/* Only legal promotion destinations open the modal; position/history stay unchanged
 * until a choice is made. This is a host UI, not a copy of the DOS popup. */
static bool promotion_destination(const BCGame *g,int from,int to){
 BCMoveList list;bc_generate_legal(bc_game_position(g),&list);
 for(size_t i=0;i<list.count;i++){BCMove m=list.moves[i];
  if(m.from==from&&m.to==to&&m.special&&m.kind>=2&&m.kind<=5)return true;
 }return false;
}
static unsigned promotion_hit(float x,float y){
 if(x<220||x>=660||y<300||y>=352)return 0;
 unsigned col=(unsigned)(x-220)/110;
 return x<220+col*110+100?col+2:0;
}
static void promotion_draw(SDL_Renderer *r){
 SDL_FRect box={200,236,480,140};SDL_SetRenderDrawColor(r,32,38,50,255);SDL_RenderFillRect(r,&box);
 SDL_SetRenderDrawColor(r,235,235,240,255);SDL_RenderDebugText(r,220,256,"Promote pawn: choose a piece");
 const char *labels[]={"Q Queen","R Rook","B Bishop","K Knight"};
 for(unsigned i=0;i<4;i++){SDL_FRect b={220+i*110,300,100,52};
  SDL_SetRenderDrawColor(r,67,78,98,255);SDL_RenderFillRect(r,&b);
  SDL_SetRenderDrawColor(r,255,255,255,255);SDL_RenderDebugText(r,b.x+10,b.y+20,labels[i]);
 }SDL_RenderDebugText(r,220,366,"Escape: cancel move");
}
static void smoke_promotion_position(BCGame **g){
 /* Red pawn a7, kings e1/e8. Standard packed board nibble encoding. */
 uint8_t packed[33]={0};packed[3]=0x10;packed[25]=0x60;packed[31]=0x90;
 BCPosition p={0};if(!bc_unpack(&p.board,packed))fail("Promotion fixture");p.ep=-1;p.fullmove=1;
 bc_game_destroy(*g);*g=bc_game_create(&p);if(!*g)fail("Promotion fixture game");
}
int main(int argc,char **argv) {
 if(argc<2||argc>3){fprintf(stderr,"Usage: %s pieces.bcp [--smoke]\n",argv[0]);return 2;}
 bool perspective=!(argc==3&&!strcmp(argv[2],"--smoke-flat"));
 bool initial_perspective=perspective;
 bool smoke_book=argc==3&&!strcmp(argv[2],"--smoke-book");
 bool smoke_promotion=argc==3&&!strcmp(argv[2],"--smoke-promotion");
 bool smoke=smoke_book||smoke_promotion||(argc==3&&(!strcmp(argv[2],"--smoke")||!strcmp(argv[2],"--smoke-flat")));if(argc==3&&!smoke)return 2;
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
 int promote_from=-1,promote_to=-1;
 if(smoke_promotion)smoke_promotion_position(&g);
 Worker *worker=NULL;bool running=true,computer=!smoke_promotion,paused=false;int selected=-1;
 unsigned level=smoke_book?1:0,smoke_stage=0;unsigned book_moves=0;uint64_t started=SDL_GetTicks();char message[160]="Click a piece, then its destination.";
 while(running) {
  SDL_Event e;bool had_input=false;
  while(SDL_PollEvent(&e)) {
   if(e.type==SDL_EVENT_KEY_DOWN||e.type==SDL_EVENT_MOUSE_BUTTON_DOWN)had_input=true;
   if(e.type==SDL_EVENT_QUIT)running=false;
   if(e.type==SDL_EVENT_KEY_DOWN) {
    SDL_Keycode k=e.key.key;
    if(promote_from>=0){
     unsigned choice=k==SDLK_Q?2:k==SDLK_R?3:k==SDLK_B?4:k==SDLK_K?5:0;
     if(k==SDLK_ESCAPE){promote_from=promote_to=-1;selected=-1;snprintf(message,sizeof message,"Promotion cancelled; position unchanged.");}
     else if(choice&&move_between(g,promote_from,promote_to,choice,&motion,perspective,&audio)){
      promote_from=promote_to=-1;selected=-1;snprintf(message,sizeof message,"Promotion selected.");
     }
     continue;
    }
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
    if(k==SDLK_D){stop(&worker);if(bc_game_claim_draw(g))snprintf(message,sizeof message,"Draw claimed.");else snprintf(message,sizeof message,"No draw claim available.");}
   }
   if(e.type==SDL_EVENT_MOUSE_BUTTON_DOWN&&e.button.button==SDL_BUTTON_LEFT&&!worker&&!paused&&!motion.active&&(!computer||bc_game_position(g)->board.side==0)) {
    float x,y;SDL_RenderCoordinatesFromWindow(r,e.button.x,e.button.y,&x,&y);
    if(promote_from>=0){unsigned choice=promotion_hit(x,y);
     if(choice&&move_between(g,promote_from,promote_to,choice,&motion,perspective,&audio)){
      promote_from=promote_to=-1;selected=-1;snprintf(message,sizeof message,"Promotion selected.");
     }continue;
    }
    int s=bc_view_hit(perspective,x,y);
    if(s>=0) {
     if(selected>=0&&promotion_destination(g,selected,s)){
      promote_from=selected;promote_to=s;snprintf(message,sizeof message,"Choose queen, rook, bishop or knight.");
     }
     else if(selected>=0&&move_between(g,selected,s,2,&motion,perspective,&audio)){selected=-1;snprintf(message,sizeof message,"Move played.");}
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
    if(worker->book_hit){book_moves++;snprintf(message,sizeof message,"Original opening book.");}
    else snprintf(message,sizeof message,"Engine depth %u, %llu candidates",worker->result.depth,(unsigned long long)worker->result.nodes);
   }
   else {snprintf(message,sizeof message,"Search stopped. Space resumes.");paused=true;}
   stop(&worker);
  }
  BCGameStatus state=bc_game_status(g);const BCPosition *p=bc_game_position(g);
  if(running&&promote_from<0&&computer&&!paused&&!worker&&!motion.active&&!bc_audio_busy(&audio)&&p->board.side==1&&(state==BC_PLAYING||state==BC_CHECK)){worker=start(g,level,smoke);if(!worker){paused=true;snprintf(message,sizeof message,"Could not start search.");}}
  SDL_SetRenderDrawColor(r,23,27,35,255);SDL_RenderClear(r);
  bc_view_draw(view,r,p,&motion,selected,perspective);
  SDL_SetRenderDrawColor(r,235,235,240,255);SDL_RenderDebugText(r,24,16,"BATTLE CHESS / NATIVE DEVELOPMENT");
  text(r,52,computer?"Human vs computer":"Two players");text(r,78,p->board.side?"Blue to move":"Red to move");text(r,104,status_name(state));
  text(r,130,promote_from>=0?"Choose promotion...":worker?"Computer thinking...":paused?"Paused":motion.active?"Piece moving...":"Ready");
  char line[80];snprintf(line,sizeof line,"Level: %s",level?"timed":"Novice");if(level)snprintf(line,sizeof line,"Level %u (%u seconds)",level,5u<<(level-1));text(r,170,line);
  text(r,204,"0-9: difficulty");text(r,228,"N: new game   U: undo");text(r,252,"H: one / two players");text(r,276,"Space: pause / resume");text(r,300,"D: claim draw");text(r,324,"Promotion: asks before move");text(r,348,"Q/R/B/K or click a choice");
  text(r,372,"S: save   L: load");
  text(r,396,"V: perspective / flat");snprintf(line,sizeof line,"M: sound %s (%u held)",!audio.stream?"unavailable":audio.muted?"off":"on / nominal",audio.rejected);text(r,420,line);
  SDL_SetRenderDrawColor(r,235,235,240,255);SDL_RenderDebugText(r,24,600,message);
  if(promote_from>=0){promotion_draw(r);
   if(smoke_promotion&&getenv("BC_PROMOTION_SCREENSHOT")){
    SDL_Surface *shot=SDL_RenderReadPixels(r,NULL);
    if(!shot||!SDL_SaveBMP(shot,getenv("BC_PROMOTION_SCREENSHOT")))fail("Promotion screenshot");SDL_DestroySurface(shot);
   }
  }
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
  if(smoke_promotion){
   if(smoke_stage==0||smoke_stage==2){
    if(bc_game_plies(g)||motion.active)fail("Promotion changed before choice");
    for(unsigned rank=6;rank<=7;rank++){SDL_Event click={0};click.type=SDL_EVENT_MOUSE_BUTTON_DOWN;click.button.button=SDL_BUTTON_LEFT;
     float px,py;bc_view_square_point(perspective,rank*16,&px,&py);
     if(!SDL_RenderCoordinatesToWindow(r,px,py,&click.button.x,&click.button.y)||!SDL_PushEvent(&click))fail("Promotion click");
    }smoke_stage++;
   }else if(smoke_stage==1){
    if(promote_from!=96||promote_to!=112||bc_game_plies(g))fail("Promotion modal");
    SDL_Event key={0};key.type=SDL_EVENT_KEY_DOWN;key.key.key=SDLK_ESCAPE;if(!SDL_PushEvent(&key))fail("Promotion cancel");smoke_stage=2;
   }else if(smoke_stage==3){
    if(promote_from!=96||bc_game_plies(g))fail("Promotion reopened");
    SDL_Event click={0};click.type=SDL_EVENT_MOUSE_BUTTON_DOWN;click.button.button=SDL_BUTTON_LEFT;
    if(getenv("BC_PROMOTION_KEY")){click.type=SDL_EVENT_KEY_DOWN;click.key.key=SDLK_K;}
    else if(!SDL_RenderCoordinatesToWindow(r,600,326,&click.button.x,&click.button.y))fail("Promotion coordinates");
    if(!SDL_PushEvent(&click))fail("Promotion choice");smoke_stage=4;
   }else if(smoke_stage==4&&!motion.active){
    if(promote_from>=0||bc_game_plies(g)!=1||bc_game_position(g)->board.cells[112].kind!=5)fail("Promotion committed");
    running=false;
   }
   if(SDL_GetTicks()-started>25000)fail("Promotion smoke timeout");
  }
  else if(smoke) {
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
 if(smoke_book&&book_moves!=1){fprintf(stderr,"Expected one book reply, got %u\n",book_moves);return 1;}
 puts("Native board closed cleanly.");return 0;
}
