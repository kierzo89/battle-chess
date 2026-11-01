/* Included after recovered search while source symbols are namespaced. */
_Thread_local uint8_t search_side,search_active,packed_pen;
_Thread_local int16_t current_side,interrupted,finished,ready_9856,input_state,search_level;
_Thread_local int16_t position_score,iteration,best,window_limit,first_score;
_Thread_local int32_t clock_value,limit;
_Thread_local int16_t modes[2],check_state[26],home_pawn[26],pawn_home[2]={16,96};
_Thread_local Move initial_move,working_pv[24],search_pair_moves[24][2];
_Thread_local SearchFrame *search_frame;
_Thread_local int16_t history_index,opponent,side_piece_counts[2],piece_counts[2];
_Thread_local Piece pieces[2][16];
_Thread_local Cell board[120];
_Thread_local Move history_storage[130],*history,*history_tail;
_Thread_local SearchOptions search_options;
_Thread_local int16_t state_index,state_count,paused;
_Thread_local Move state_8d12,move_list[256];
_Thread_local MoveLookupTables move_lookup_tables={
 {1,-1,16,-16,17,-17,15,-15},{14,-14,18,-18,31,-31,33,-33},
 {{{16,-16},{1,2,4,8,16,32}}},{{{2,4},{6,4}},{{114,116},{118,116}}},{3,5,4,2,1,4,5,3}};
static _Thread_local BCPosition positions[25];
static _Thread_local BCSearchEvaluation evaluation;
static _Thread_local BCSearchConfig configuration;
static _Thread_local const BCMove *played_history;
static _Thread_local size_t played_count;
static _Thread_local uint64_t nodes;
static _Thread_local uint32_t random_state;
static _Thread_local uint64_t started_ms;
static _Thread_local bool timed_out;
static uint64_t now_ms(void){return configuration.clock_ms?configuration.clock_ms(configuration.clock_userdata):bc_monotonic_ms();}
static BCMove host_move(Move m){return (BCMove){(uint8_t)m.from,(uint8_t)m.to,(uint8_t)m.flag,m.detail.bytes.kind,m.detail.bytes.capture};}
static Move dos_move(BCMove m){Move d={m.to,m.from,m.special,{0}};d.detail.bytes.kind=m.kind;d.detail.bytes.capture=m.capture;return d;}
/* board and pieces are macros here; avoid host member macro expansion. */
#undef board
#undef pieces
static void sync_position(const BCPosition *p) {
 for(int s=0;s<120;s++) {sr_board[s].kind=p->board.cells[s].kind;sr_board[s].side=p->board.cells[s].side;sr_board[s].index=p->board.cells[s].index;}
 for(int side=0;side<2;side++) {
  for(int i=0;i<16;i++){sr_pieces[side][i].kind=p->board.pieces[side][i].kind;sr_pieces[side][i].square=p->board.pieces[side][i].square;}
  side_piece_counts[side]=p->board.last_piece[side];piece_counts[side]=p->board.last_nonpawn[side];
 }
}
static BCPosition current_position(void){BCPosition p=positions[history_index];p.board.side=(uint8_t)current_side;return p;}
static BCMove *combined_history(size_t *length) {
 size_t count=played_count+(size_t)history_index+1;
 BCMove *moves=malloc(count*sizeof *moves);if(!moves)return NULL;
 if(played_count)memcpy(moves,played_history,played_count*sizeof *moves);
 for(int i=0;i<=history_index;i++)moves[played_count+(size_t)i]=host_move(history_tail[i]);
 *length=count;return moves;
}
int16_t count_9bfd(void){size_t n;BCMove *m=combined_history(&n);if(!m){hard_cancelled=interrupted=1;return 0;}unsigned r=bc_original_quiet_count(m,n);free(m);return (int16_t)(r>32767?32767:r);}
int16_t repetition_9c34(int16_t required){size_t n;BCMove *m=combined_history(&n);if(!m){hard_cancelled=interrupted=1;return 1;}unsigned r=bc_original_repetitions(m,n,required!=0);free(m);return (int16_t)r;}
int16_t min_i16(int16_t a,int16_t b){return a<b?a:b;}
int16_t max_i16(int16_t a,int16_t b){return a>b?a:b;}
int16_t abs_i16(int16_t a){return a<0?(int16_t)-a:a;}
int16_t rand(void){random_state=random_state*214013u+2531011u;return (int16_t)((random_state>>16)&32767);}
int16_t equal_state(Move *a,Move *b){return memcmp(a,b,sizeof *a)==0;}
void exit_07f3(int error){(void)error;hard_cancelled=interrupted=1;}
static int host_cancel(void) {
 nodes++;
 if(configuration.time_budget_ms) {
  uint64_t now=now_ms();
  if(now==UINT64_MAX||now<started_ms)hard_cancelled=1;
  else if(now-started_ms>=configuration.time_budget_ms){timed_out=true;hard_cancelled=1;}
 }
 if((configuration.node_limit&&nodes>configuration.node_limit)||
    (configuration.cancel&&configuration.cancel(configuration.userdata)))hard_cancelled=1;
 if(hard_cancelled)interrupted=1;
 return hard_cancelled;
}
void graphics_end(void){}void graphics_begin(void){}
void select_mode(int16_t mode){(void)mode;}void prepare_85c4(void){}void prepare_85c5(void){}
void refresh(void){}void poll_input(void){}void accept_input(void){}
int16_t obtain_input(void){return 0;}
void evaluate_full(void){BCEvaluation root;bc_evaluate(&positions[0],configuration.temporary,&root);bc_search_evaluation_init(&evaluation,&root);position_score=root.score;}
int16_t evaluate_candidate(Move m){int16_t delta=0;if(!bc_evaluate_delta(&evaluation,host_move(m),(unsigned)current_side,(unsigned)history_index,best,configuration.temporary,&delta))hard_cancelled=interrupted=1;return delta;}
void apply_9749(Move m,int16_t undo) {
 if(undo){sync_position(&positions[history_index]);return;}
 positions[history_index+1]=current_position();bc_play_unchecked(&positions[history_index+1],host_move(m));sync_position(&positions[history_index+1]);
}
int16_t attacked_9a50(int16_t side,int16_t square) {
 /* Called after apply, before history_index increments: use synchronized cells. */
 BCBoard b=positions[history_index].board;
 for(int s=0;s<120;s++)b.cells[s]=(BCCell){sr_board[s].kind,sr_board[s].side,sr_board[s].index};
 for(int c=0;c<2;c++) {b.last_nonpawn[c]=piece_counts[c];b.last_piece[c]=side_piece_counts[c];for(int i=0;i<16;i++)b.pieces[c][i]=(BCPiece){sr_pieces[c][i].square,sr_pieces[c][i].kind};}
 return bc_attacked(&b,(unsigned)side,square);
}
int16_t piece_attacks(int16_t kind,int16_t side,int16_t from,int16_t to) {
 BCBoard b=positions[history_index].board;
 for(int s=0;s<120;s++)b.cells[s]=(BCCell){sr_board[s].kind,sr_board[s].side,sr_board[s].index};
 return bc_piece_attacks(&b,(unsigned)kind,(unsigned)side,from,to);
}
int16_t legal_move(Move m) {
 BCPosition p=current_position();BCMoveList list;bc_generate_legal(&p,&list);
 for(size_t i=0;i<list.count;i++){Move d=dos_move(list.moves[i]);if(equal_state(&d,&m))return 1;}
 return 0;
}

#undef interrupted
bool bc_search(const BCPosition *root,const BCMove *past,size_t count,
 const BCSearchConfig *config,BCSearchResult *result) {
 if(!root||!config||!result||(!past&&count)||config->max_depth<1||config->max_depth>23||config->temporary>1)return false;
 memset(result,0,sizeof *result);configuration=*config;timed_out=false;started_ms=configuration.time_budget_ms?now_ms():0;
 if(configuration.time_budget_ms&&started_ms==UINT64_MAX)return false;
 played_history=past;played_count=count;
 positions[0]=*root;sync_position(root);current_side=root->board.side;opponent=current_side^1;
 memset(frames,0,sizeof frames);search_frame=frames;
 memset(history_storage,0,sizeof history_storage);history_tail=history_storage+104;history=history_tail-1;
 if(count)history[-0]=dos_move(past[count-1]);
 memset(working_pv,0,sizeof working_pv);memset(check_state,0,sizeof check_state);memset(home_pawn,0,sizeof home_pawn);
 initial_move=(Move){0};history_index=0;sr_interrupted=hard_cancelled=finished=ready_9856=paused=0;
 nodes=0;random_state=config->seed;search_level=(int16_t)config->original_level;modes[0]=modes[1]=1;
 run_search((int16_t)config->max_depth);
 result->score=best;result->depth=(unsigned)iteration;result->nodes=nodes;result->interrupted=sr_interrupted!=0;result->timed_out=timed_out;
 if(configuration.time_budget_ms){uint64_t now=now_ms();result->elapsed_ms=now>=started_ms&&now!=UINT64_MAX?now-started_ms:0;}
 BCMoveList legal;bc_generate_legal(root,&legal);
 for(size_t i=0;i<legal.count;i++){Move d=dos_move(legal.moves[i]);if(equal_state(&d,&working_pv[0])){result->move=legal.moves[i];result->has_move=true;break;}}
 for(int i=0;i<24;i++)result->pv[i]=host_move(working_pv[i]);
 return true;
}
