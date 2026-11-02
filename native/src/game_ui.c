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
#include "controls.h"
#include "stockfish.h"
typedef struct {
 SDL_Thread *thread;atomic_bool cancel,done;BCPosition position,initial;unsigned engine,stockfish_depth;char error[160];
 BCMove *history;size_t count;BCSearchConfig config;BCSearchResult result;bool ok,use_book,book_hit;unsigned book_draw;
} Worker;
static bool cancelled(void *p){return atomic_load_explicit(&((Worker *)p)->cancel,memory_order_relaxed);}
static int search_thread(void *p){Worker *w=p;if(w->engine==2){w->ok=bc_stockfish(&w->initial,&w->position,w->history,w->count,w->stockfish_depth,cancelled,w,&w->result.move,w->error,sizeof w->error);w->result.has_move=w->ok;}else if(w->use_book&&!cancelled(w)&&bc_book_move(&w->position,w->history,w->count,w->book_draw,&w->result.move)){
 w->book_hit=w->ok=w->result.has_move=true;
 }else w->ok=bc_search(&w->position,w->history,w->count,&w->config,&w->result);atomic_store_explicit(&w->done,true,memory_order_release);return 0;}
static Worker *start_engine(BCGame *g,unsigned level,unsigned minutes,bool smoke,unsigned engine,unsigned depth) {
 Worker *w=calloc(1,sizeof *w);if(!w)return NULL;
 atomic_init(&w->cancel,false);atomic_init(&w->done,false);
 w->stockfish_depth=smoke?4:depth;w->engine=engine;w->initial=*bc_game_initial_position(g);w->position=*bc_game_position(g);w->count=bc_game_plies(g);
 if(w->count){w->history=malloc(w->count*sizeof *w->history);if(!w->history){free(w);return NULL;}}
 if(!bc_game_copy_moves(g,w->history,w->count)){free(w->history);free(w);return NULL;}
 bc_difficulty_config(level,minutes,&w->config);w->config.temporary=w->position.board.side;
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
static Worker *start(BCGame *g,unsigned level,unsigned minutes,bool smoke){return start_engine(g,level,minutes,smoke,1,18);}
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
 bool smoke_result=argc==3&&!strcmp(argv[2],"--smoke-result");
 bool smoke_engines=argc==3&&!strcmp(argv[2],"--smoke-engines");
 bool smoke_time=argc==3&&!strcmp(argv[2],"--smoke-time");
 bool smoke_controls=argc==3&&!strcmp(argv[2],"--smoke-controls");
 bool smoke_book=argc==3&&!strcmp(argv[2],"--smoke-book");
 bool smoke_promotion=argc==3&&!strcmp(argv[2],"--smoke-promotion");
 bool smoke=smoke_result||smoke_engines||smoke_time||smoke_controls||smoke_book||smoke_promotion||(argc==3&&(!strcmp(argv[2],"--smoke")||!strcmp(argv[2],"--smoke-flat")));if(argc==3&&!smoke)return 2;
 if(!SDL_Init(SDL_INIT_VIDEO))fail("SDL");SDL_Window *window;SDL_Renderer *r;
 if(!SDL_CreateWindowAndRenderer("Battle Chess Native",1200,732,smoke?SDL_WINDOW_HIDDEN:SDL_WINDOW_RESIZABLE,&window,&r))fail("Window");
 SDL_SetRenderLogicalPresentation(r,1024,624,SDL_LOGICAL_PRESENTATION_LETTERBOX);
 BCBoardView *view=bc_view_load(r,argv[1]);if(!view)fail("Board assets");
 BCAudio audio={0};const char *slash=strrchr(argv[1],'/');size_t prefix=slash?(size_t)(slash-argv[1]+1):0;
 char *sound_path=malloc(prefix+16);if(!sound_path)fail("Sound path");memcpy(sound_path,argv[1],prefix);strcpy(sound_path+prefix,"sounds.bca");
 (void)bc_audio_open(&audio,sound_path);free(sound_path);if(smoke)bc_audio_mute(&audio,true);
 BCGame *g=bc_game_create(NULL);if(!g)fail("Game allocation");
 if(smoke_result){const char *moves[]={"f2f3","e7e5","g2g4","d8h4"};
  for(unsigned i=0;i<4;i++){BCMove m;if(!bc_uci_parse(bc_game_position(g),moves[i],&m)||!bc_game_move(g,m))fail("Checkmate fixture");}
  if(bc_game_status(g)!=BC_CHECKMATE||bc_game_position(g)->board.side!=0)fail("Blue winner fixture");
 }
 char *pref=SDL_GetPrefPath("battle-chess-native","game");
 char *save_path=NULL;
 if(pref){size_t n=strlen(pref)+16;save_path=malloc(n);if(save_path)snprintf(save_path,n,"%sgame.bcs",pref);SDL_free(pref);}
 if(smoke){
  free(save_path);save_path=strdup("/tmp/bc-ui-save-XXXXXX");
  if(!save_path)fail("Smoke path");
  int fd=mkstemp(save_path);if(fd<0)fail("Smoke temporary file");close(fd);
 }
 BCMotion motion={0};
 bool time_dialog=false,time_was_paused=false;unsigned minutes=1,time_value=0;
 int promote_from=-1,promote_to=-1;
 if(smoke_promotion)smoke_promotion_position(&g);
 Worker *worker=NULL;bool running=true,computer=!smoke_promotion,paused=false;int selected=-1;unsigned engines[2]={0,smoke_promotion?0:1};unsigned stockfish_depth=18;size_t finale_plies=SIZE_MAX;uint64_t controller_ready=0;
 unsigned level=smoke_book?1:0,smoke_stage=0;unsigned book_moves=0;uint64_t started=SDL_GetTicks();char message[160]="Click a piece, then its destination.";
 while(running) {
  SDL_Event e;bool had_input=false;
  while(SDL_PollEvent(&e)) {
   if(e.type==SDL_EVENT_KEY_DOWN||e.type==SDL_EVENT_MOUSE_BUTTON_DOWN)had_input=true;
   if(e.type==SDL_EVENT_QUIT)running=false;
   /* Route native menu clicks through exactly the keyboard command handler,
    * before board-input guards, so pause/undo work while search is running. */
   if(e.type==SDL_EVENT_MOUSE_BUTTON_DOWN&&e.button.button==SDL_BUTTON_LEFT&&promote_from<0){
    float x,y;if(SDL_RenderCoordinatesFromWindow(r,e.button.x,e.button.y,&x,&y)){
     SDL_Keycode action=0;
     if(time_dialog){if(y>=340&&y<376){if(x>=220&&x<360)action=SDLK_RETURN;else if(x>=400&&x<540)action=SDLK_ESCAPE;}}
     else action=bc_controls_hit(x,y);if(action){e.type=SDL_EVENT_KEY_DOWN;e.key.key=action;}
    }
   }
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
    if(time_dialog){
     if(k>=SDLK_0&&k<=SDLK_9){unsigned next=time_value*10+(unsigned)(k-SDLK_0);if(next<=32767)time_value=next;}
     if(k==SDLK_BACKSPACE)time_value/=10;
     if(k==SDLK_ESCAPE||k==SDLK_RETURN){
      if(k==SDLK_RETURN&&time_value){minutes=time_value;level=10;snprintf(message,sizeof message,"Custom limit: %u minutes per move.",minutes);}
      else snprintf(message,sizeof message,"Time limit unchanged.");
      time_dialog=false;paused=time_was_paused;bc_audio_pause(&audio,paused);motion.last_tick=SDL_GetTicks()*1193182u/65536000u;
     }continue;
    }
    if(k==SDLK_C){stop(&worker);time_was_paused=paused;paused=true;bc_audio_pause(&audio,true);time_value=0;time_dialog=true;continue;}
    if(k==SDLK_S)snprintf(message,sizeof message,"%s",save_path&&bc_game_save(g,save_path)?"Game saved.":"Save failed; previous file retained.");
    if(k==SDLK_L){
     BCGame *loaded=save_path?bc_game_load(save_path):NULL;
     if(loaded){stop(&worker);bc_game_destroy(g);g=loaded;selected=-1;paused=false;motion.active=false;motion.visual_valid=false;motion.finale=false;bc_audio_clear(&audio);bc_audio_pause(&audio,false);snprintf(message,sizeof message,"Game loaded with complete move history.");}
     else snprintf(message,sizeof message,"Load failed; current game retained.");
    }
    if(k==SDLK_V){motion.active=false;motion.visual_valid=false;motion.finale=false;bc_audio_clear(&audio);bc_audio_pause(&audio,false);perspective=!perspective;selected=-1;}
    if(k==SDLK_M)bc_audio_mute(&audio,!audio.muted);
    if(k==SDLK_ESCAPE)running=false;
    if(k==SDLK_N){stop(&worker);bc_game_destroy(g);g=bc_game_create(NULL);if(!g)fail("New game");selected=-1;paused=false;motion.active=false;motion.visual_valid=false;motion.finale=false;bc_audio_clear(&audio);bc_audio_pause(&audio,false);}
    if(k==SDLK_U){stop(&worker);bc_game_undo(g);if(engines[bc_game_position(g)->board.side]&&(!engines[0]||!engines[1]))bc_game_undo(g);selected=-1;paused=false;motion.active=false;motion.visual_valid=false;motion.finale=false;bc_audio_clear(&audio);bc_audio_pause(&audio,false);}
    if(k==SDLK_H){stop(&worker);controller_ready=SDL_GetTicks()+1500;computer=!computer;engines[0]=0;engines[1]=computer?1:0;paused=false;selected=-1;motion.active=false;motion.visual_valid=false;motion.finale=false;bc_audio_clear(&audio);bc_audio_pause(&audio,false);}
    if(k==SDLK_F1||k==SDLK_F2){stop(&worker);controller_ready=SDL_GetTicks()+1500;unsigned side=k==SDLK_F2;engines[side]=(engines[side]+1)%3;computer=engines[0]||engines[1];selected=-1;snprintf(message,sizeof message,"%s: %s",side?"Blue":"Red",engines[side]==2?"Stockfish":engines[side]==1?"Original engine":"Human");}
    if(k==SDLK_F3||k==SDLK_F4){if(worker&&worker->engine==2)stop(&worker);if(k==SDLK_F3&&stockfish_depth>1)stockfish_depth--;if(k==SDLK_F4&&stockfish_depth<128)stockfish_depth++;snprintf(message,sizeof message,"Stockfish target depth %u (no time limit)",stockfish_depth);}
    if(k==SDLK_SPACE){stop(&worker);paused=!paused;bc_audio_pause(&audio,paused);motion.last_tick=SDL_GetTicks()*1193182u/65536000u;}
    if(k>=SDLK_0&&k<=SDLK_9){if(worker&&worker->engine!=2)stop(&worker);level=(unsigned)(k-SDLK_0);paused=false;bc_audio_pause(&audio,false);}
    if(k==SDLK_D){stop(&worker);if(bc_game_claim_draw(g))snprintf(message,sizeof message,"Draw claimed.");else snprintf(message,sizeof message,"No draw claim available.");}
   }
   if(e.type==SDL_EVENT_MOUSE_BUTTON_DOWN&&e.button.button==SDL_BUTTON_LEFT&&!worker&&!paused&&!motion.active&&!engines[bc_game_position(g)->board.side]) {
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
    if(worker->engine==2)snprintf(message,sizeof message,"Stockfish move (validated by native rules).");
    else if(worker->book_hit){book_moves++;snprintf(message,sizeof message,"Original opening book.");}
    else snprintf(message,sizeof message,"Engine depth %u, %llu candidates",worker->result.depth,(unsigned long long)worker->result.nodes);
   }
   else {snprintf(message,sizeof message,"%s",worker->error[0]?worker->error:"Search stopped. Space resumes.");paused=true;}
   stop(&worker);
  }
  BCGameStatus state=bc_game_status(g);const BCPosition *p=bc_game_position(g);
  if(state!=BC_CHECKMATE)finale_plies=SIZE_MAX;
  if(state==BC_CHECKMATE&&perspective&&!paused&&!motion.active&&!bc_audio_busy(&audio)&&finale_plies!=bc_game_plies(g)){
   finale_plies=bc_game_plies(g);int preferred=-1;size_t n=bc_game_plies(g);BCMove *moves=n?malloc(n*sizeof *moves):NULL;
   if(moves&&bc_game_copy_moves(g,moves,n))preferred=moves[n-1].to;free(moves);
   if(!bc_motion_finale(&motion,p,preferred,SDL_GetTicks()*1193182u/65536000u,motion.visual_valid?motion.facing:NULL,bc_audio_event,&audio))snprintf(message,sizeof message,"Final battle unavailable; checkmate stands.");
  }
  if(running&&SDL_GetTicks()>=controller_ready&&promote_from<0&&engines[p->board.side]&&!paused&&!worker&&!motion.active&&!bc_audio_busy(&audio)&&(state==BC_PLAYING||state==BC_CHECK)){worker=start_engine(g,level,minutes,smoke,engines[p->board.side],stockfish_depth);if(!worker){paused=true;snprintf(message,sizeof message,"Could not start search.");}}
  SDL_SetRenderDrawColor(r,23,27,35,255);SDL_RenderClear(r);
  bc_view_draw(view,r,p,&motion,selected,perspective);
  SDL_SetRenderDrawColor(r,235,235,240,255);SDL_RenderDebugText(r,24,16,"BATTLE CHESS / NATIVE LINUX");
  text(r,52,engines[0]&&engines[1]?"Engine vs engine":computer?"Human vs computer":"Two players");text(r,78,state>=BC_CHECKMATE?"Game over":p->board.side?"Blue to move":"Red to move");text(r,104,state==BC_CHECKMATE?(p->board.side?"CHECKMATE - Red wins":"CHECKMATE - Blue wins"):status_name(state));
  text(r,130,motion.finale&&motion.active?"Final battle...":state>=BC_CHECKMATE?"N: New game / U: Undo":promote_from>=0?"Choose promotion...":worker?"Computer thinking...":paused?"Paused":engines[p->board.side]&&SDL_GetTicks()<controller_ready?"Choosing controller...":motion.active?"Piece moving...":"Ready");
  char line[80];snprintf(line,sizeof line,"Original: %s",level?"timed":"Novice");if(level==10)snprintf(line,sizeof line,"Original: %u minutes",minutes);else if(level)snprintf(line,sizeof line,"Original %u (%u seconds)",level,5u<<(level-1));text(r,170,line);
  bc_controls_draw(r,level,computer,paused,perspective,audio.muted);
  bc_controls_engines(r,engines,stockfish_depth);
  snprintf(line,sizeof line,"Sound %s (%u held)",!audio.stream?"unavailable":audio.muted?"off":"on / nominal",audio.rejected);text(r,522,line);
  SDL_SetRenderDrawColor(r,235,235,240,255);SDL_RenderDebugText(r,24,612,state>=BC_CHECKMATE?(state==BC_CHECKMATE?(p->board.side?"Game over: Red wins by checkmate.":"Game over: Blue wins by checkmate."):status_name(state)):message);
  if(state>=BC_CHECKMATE&&!motion.active&&!bc_audio_busy(&audio)){
   SDL_FRect result_box={120,248,464,92};SDL_SetRenderDrawColor(r,32,38,50,245);SDL_RenderFillRect(r,&result_box);
   SDL_SetRenderDrawColor(r,245,225,175,255);SDL_RenderDebugText(r,140,266,state==BC_CHECKMATE?"Check and mate...Game over.":state==BC_STALEMATE?"Stalemate. How boring!":status_name(state));
   SDL_RenderDebugText(r,140,290,state==BC_CHECKMATE?(p->board.side?"Red wins.":"Blue wins."):"Game drawn.");
   SDL_RenderDebugText(r,140,316,"N: New game     U: Take back / continue");
   if(smoke_result&&getenv("BC_FINALE_SCREENSHOT")){SDL_Surface *shot=SDL_RenderReadPixels(r,NULL);if(!shot||!SDL_SaveBMP(shot,getenv("BC_FINALE_SCREENSHOT")))fail("Finale screenshot");SDL_DestroySurface(shot);}
  }
  if(time_dialog){
   SDL_FRect box={200,236,480,156};SDL_SetRenderDrawColor(r,32,38,50,255);SDL_RenderFillRect(r,&box);
   SDL_SetRenderDrawColor(r,235,235,240,255);SDL_RenderDebugText(r,220,256,"Custom time per move (1-32767 minutes)");
   snprintf(line,sizeof line,"Minutes: %u",time_value);SDL_RenderDebugText(r,220,284,line);
   SDL_RenderDebugText(r,220,310,"Type digits; Backspace deletes; 0 cancels");
   SDL_FRect ok={220,340,140,36},cancel={400,340,140,36};SDL_SetRenderDrawColor(r,67,78,98,255);SDL_RenderFillRect(r,&ok);SDL_RenderFillRect(r,&cancel);
   SDL_SetRenderDrawColor(r,255,255,255,255);SDL_RenderDebugText(r,230,354,"Enter: Apply");SDL_RenderDebugText(r,410,354,"Esc: Cancel");
  }
  if(time_dialog&&smoke_time&&getenv("BC_TIME_SCREENSHOT")){
   SDL_Surface *shot=SDL_RenderReadPixels(r,NULL);if(!shot||!SDL_SaveBMP(shot,getenv("BC_TIME_SCREENSHOT")))fail("Time screenshot");SDL_DestroySurface(shot);
  }
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
  if(smoke_result){if(worker)fail("Search after checkmate");if(motion.failed)fail("Final battle failed");if(motion.finale&&!motion.active){smoke_stage=4;running=false;}if(SDL_GetTicks()-started>30000)fail("Final battle timeout");}
  else if(smoke_time){
   static const SDL_Keycode keys[]={SDLK_C,SDLK_2,SDLK_RETURN,SDLK_C,SDLK_9,SDLK_ESCAPE,SDLK_C,SDLK_RETURN};
   if(smoke_stage==3||smoke_stage==6||smoke_stage==8){
    BCSearchConfig check;if(time_dialog||paused||level!=10||minutes!=2||!bc_difficulty_config(level,minutes,&check)||check.time_budget_ms!=120000)fail("Custom time state");
   }
   if(smoke_stage==3){worker=start(g,level,minutes,false);if(!worker||worker->config.time_budget_ms!=120000)fail("Custom worker limit");stop(&worker);}
   if(smoke_stage<8){SDL_Event key={0};key.type=SDL_EVENT_KEY_DOWN;key.key.key=keys[smoke_stage];
    if(smoke_stage==0){key.type=SDL_EVENT_MOUSE_BUTTON_DOWN;key.button.button=SDL_BUTTON_LEFT;if(!SDL_RenderCoordinatesToWindow(r,710,560,&key.button.x,&key.button.y))fail("Custom time click");}
    if(!SDL_PushEvent(&key))fail("Custom time key");smoke_stage++;
   }else running=false;
   if(SDL_GetTicks()-started>5000)fail("Custom time timeout");
  }
  else if(smoke_engines){
   if(paused)fail(message);
   if(smoke_stage==0){
    /* Exercise independent depth buttons and restore 18 before starting. */
    for(unsigned i=0;i<2;i++){SDL_Event click={0};click.type=SDL_EVENT_MOUSE_BUTTON_DOWN;click.button.button=SDL_BUTTON_LEFT;
     if(!SDL_RenderCoordinatesToWindow(r,i?858:710,590,&click.button.x,&click.button.y)||!SDL_PushEvent(&click))fail("Depth selector click");}
    /* First select Original, then wait across frames before selecting Stockfish. */
    for(unsigned i=0;i<1;i++){SDL_Event click={0};click.type=SDL_EVENT_MOUSE_BUTTON_DOWN;click.button.button=SDL_BUTTON_LEFT;
     if(!SDL_RenderCoordinatesToWindow(r,710,468,&click.button.x,&click.button.y)||!SDL_PushEvent(&click))fail("Engine selector click");}smoke_stage=10;
   }else if(smoke_stage==10){
    if(worker||bc_game_plies(g))fail("Intermediate Original selection started play");
    if(controller_ready&&SDL_GetTicks()+900>=controller_ready){SDL_Event key={0};key.type=SDL_EVENT_KEY_DOWN;key.key.key=SDLK_F1;if(!SDL_PushEvent(&key))fail("Delayed Stockfish selection");smoke_stage=11;}
   }else if(smoke_stage==11){
    if(SDL_GetTicks()<controller_ready){if(worker||bc_game_plies(g))fail("Controller debounce was not reset");}
    else smoke_stage=1;
   }else if(smoke_stage==1&&bc_game_plies(g)>=2&&!motion.active){
    if(stockfish_depth!=18)fail("Independent Stockfish depth controls");
    if(engines[0]!=2||engines[1]!=1)fail("Stockfish vs Original selectors");
    const SDL_Keycode keys[]={SDLK_F1,SDLK_F1,SDLK_F2};
    for(unsigned i=0;i<3;i++){SDL_Event key={0};key.type=SDL_EVENT_KEY_DOWN;key.key.key=keys[i];if(!SDL_PushEvent(&key))fail("Engine switch");}smoke_stage=2;
   }else if(smoke_stage==2&&bc_game_plies(g)>=4&&!motion.active){
    if(engines[0]!=1||engines[1]!=2)fail("Original vs Stockfish selectors");running=false;
   }
   if(SDL_GetTicks()-started>30000)fail("Engine match timeout");
  }
  else if(smoke_controls){
   /* Every click goes through viewport mapping and the normal command path. */
   static const float clicks[][2]={{710,312},{710,222},{880,222},{858,312},{858,312},{710,348},{710,276},{858,348},{710,384},{858,384},{710,420},{858,276},{858,420}};
   if(smoke_stage==1&&computer)fail("Controls player toggle");
   if(smoke_stage==3&&level!=3)fail("Controls difficulty");
   if(smoke_stage==4&&!paused)fail("Controls pause");
   if(smoke_stage==5&&paused)fail("Controls resume");
   if(smoke_stage==8&&strcmp(message,"Game loaded with complete move history."))fail("Controls save/load");
   if(smoke_stage==9&&perspective)fail("Controls view");
   if(smoke_stage==10&&audio.muted)fail("Controls mute");
   if(smoke_stage==11){worker=start(g,9,minutes,true);if(!worker)fail("Controls active worker");}
   if(smoke_stage==12&&(worker||bc_game_plies(g)))fail("Controls undo cancels worker");
   if(smoke_stage<sizeof clicks/sizeof clicks[0]){
    SDL_Event click={0};click.type=SDL_EVENT_MOUSE_BUTTON_DOWN;click.button.button=SDL_BUTTON_LEFT;
    if(!SDL_RenderCoordinatesToWindow(r,clicks[smoke_stage][0],clicks[smoke_stage][1],&click.button.x,&click.button.y)||!SDL_PushEvent(&click))fail("Controls click");smoke_stage++;
   }
   if(SDL_GetTicks()-started>5000)fail("Controls smoke timeout");
  }
  else if(smoke_promotion){
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
    worker=start(g,9,minutes,true);if(!worker)fail("Smoke worker");stop(&worker);
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
 if(smoke&&smoke_stage!=(smoke_time?8u:smoke_engines?2u:smoke_controls?13u:4u))return 1;
 if(smoke_book&&book_moves!=1){fprintf(stderr,"Expected one book reply, got %u\n",book_moves);return 1;}
 puts("Native board closed cleanly.");return 0;
}
