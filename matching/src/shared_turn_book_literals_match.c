/* Genuine shared 7C52..85C4 context proposal. No byte/layout credit before fresh verification. */
typedef unsigned char Byte;
typedef union {unsigned word;struct{unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
/* 0x88 board movement, attack-bit, castling and initial piece tables.
   The mask view starts one word into the pawn/mask union: mask zero shares
   the negative pawn step and is unused by the reconstructed consumers. */
typedef struct { int destination, king_home; } CastleEndpoints;
typedef union {
    struct { int pawn_step[2]; unsigned piece_bits[6]; } initialized;
    struct { int first_pawn_step; unsigned by_kind[7]; } masks;
} PawnAndMasks;
typedef struct {
    int ray_step[8];
    int knight_step[8];
    PawnAndMasks pawn_and_masks;
    CastleEndpoints castle[2][2];
    int back_rank[8];
} MoveLookupTables;
/* REA 7DBF: assign two bytes in a four-byte board cell.
 * The remaining bytes and original field names are not established here.
 */
typedef struct {
    unsigned char kind, side;
    int index;
} Cell;
/* REA 7DDB. C5.00 /AS /Gs /Os emits all144 original bytes.
 * Address names describe observed storage and calls, not original symbols.
 */
typedef struct {
    unsigned char square;
    char remaining[31];
} SideInfo;

extern int history_index;
extern Move history_tail[];
extern Move initial_move;
extern Move saved_state;
extern unsigned char far splash_buffer[];
extern int setup_word_9844;
extern int state_8fde;
extern int setup_word_9646;
extern int temporary;
extern int history_move_counter;
extern int current_side;
extern int modes[2];
extern int state_57cc;
extern int setup_word_934a;
extern long timer_b[2];
extern Move history[];
extern int piece_square[2][6][120];
extern void reset_board(void);
extern void init_state(void);
extern void reset_display_0865(void);
extern void fill_8a96(char *,int,int);
extern MoveLookupTables move_lookup_tables;
extern void clear_board();
extern void init_pieces();
extern void set_cell_bytes(char, char, int);
extern int opponent;
extern Cell board[];
extern int state_cbd2;
extern int state_934c;
extern int search_state_8fca(void);
extern void no_move(void);
extern SideInfo side_info_9604[];
extern int attacked_9a50(int, int);
extern char check_8f44;
extern int waiting_0eee;
extern void far draw_fce8(int);
extern void poll_input(void);
extern int ready_9856;
extern int obtain_input(void);
extern void step_872a(void);
extern int input_083e(void);
extern void dispatch_8d73(unsigned char *);
extern int prompt_1296(char*,int,int);
extern int promote_ui_9371(void);
extern char select_promotion(int);
extern unsigned animation_stage(Move,int);
extern void setup_state(void);
extern void reset_df71(void);
extern void save_cc72();
extern void save_dialog_ced4();
extern void notify_86a1(Move);
extern void notify_866d(Move);
extern void animate_move(Move*);
extern void undo_animation(Move*);
extern void prompt_893c();
extern int validate_current_8ca1(void);
extern void trim_history(void);
extern void commit_move_8632();
extern void shift_state(void);
extern void finish_move_93d6(void);
extern void reset_position_08de();
extern int view_mode_053a;
extern int book_choice_offset;
extern Byte search_active;
extern void search_turn_8061(void);
extern void commit_turn_810c(void);
extern void empty_82a4(void);
extern void prepare_85c5(void);
extern void begin_turn(void);
extern void prepare_hint_8384(void);
extern void select_mode(int);
extern void accept_hint_82db(void);
extern void run_search(int);
extern void charge_clock_85fd(int);
extern Move working_move;
extern Move hint_line;
extern int best;
extern void notify_wrapper_861b(Move);
extern void refresh_1446(void);
extern void write_bytes_dbb5(Byte*,int);
extern int count_9bfd(void);
extern int repetition_9c34(int);
extern unsigned long far *startup_offsets_9648;
extern unsigned long far *startup_lengths_a8b6;
extern void select_asset_file(int);
extern void seek_asset(long);
extern void read_asset(unsigned char huge *,long);
extern void far graphics_end(void);
extern void far graphics_begin(void);
extern int rand(void);
extern char book_weights[];
extern int book_state_index;
extern int iteration;
extern int input_state;
extern Move working_follow_8bb6;
extern Move state_8d12;
extern void rotate_book_8515(int);
extern void generate_a348(void);
extern void advance(void);
extern int book_saved_index;
extern int book_matches;
extern void scan_book_843f(void);
extern int equal_state(Move *,Move *);
extern void skip_book_8577(void);
extern void previous_book_858d(void);

/* Unchanged genuine definition: shift / shift_state */
void shift_state(void)
{
    int i;
    --history_index;
    for (i = -104; i <= history_index; ++i)
        history_tail[i] = history_tail[i + 1];
    saved_state = initial_move;
}

/* Unchanged genuine definition: setup / setup_state */
void setup_state(void)
{
 setup_word_9844=0;
 state_8fde=0;
 setup_word_9646=23;
 reset_board();
 init_state();
 if(!splash_buffer[0])state_8fde=0;
 else state_8fde=200;
 timer_b[0]=timer_b[1]=0L;
 history[0].detail.bytes.capture=1;
 temporary=0;
 history_move_counter=0;
 fill_8a96((char *)piece_square,2880,0);
 switch(modes[current_side]) {
 case 0:case 2:state_57cc=0;break;
 case 1:state_57cc=2;break;
 }
 setup_word_934a=0;
 reset_display_0865();
}

/* Unchanged genuine definition: board / reset_board */
void reset_board()
{
    int i;
    clear_board();
    i = 0;
    do {
        set_cell_bytes(move_lookup_tables.back_rank[i], 0, i);
        set_cell_bytes(6, 0, i + 16);
        set_cell_bytes(6, 1, i + 96);
        set_cell_bytes(move_lookup_tables.back_rank[i], 1, i + 112);
        ++i;
    } while (i <= 7);
    init_pieces();
    current_side = 0;
    opponent = 1;
}

/* Unchanged genuine definition: board / init_state */
void init_state(void)
{
    history_index = -1;
    history[0] = initial_move;
}

/* Unchanged genuine definition: board / set_cell_bytes */
void set_cell_bytes(char first, char second, int square)
{
    board[square].kind = first;
    board[square].side = second;
}

/* Unchanged genuine definition: board / turn_7ddb */
void turn_7ddb(void)
{
    int result;
    state_cbd2 = 0;
    state_934c = 0;
    if (!search_state_8fca()) {
        no_move();
    } else {
        check_8f44 = attacked_9a50(opponent, side_info_9604[current_side].square);
        waiting_0eee = 1;
        draw_fce8(current_side);
        do {
            poll_input();
            if (!ready_9856)
                ready_9856 = obtain_input();
            if (ready_9856)
                step_872a();
            result = input_083e();
            if (result) {
                dispatch_8d73((unsigned char *)result);
                return;
            }
        } while (!ready_9856);
        waiting_0eee = 0;
        state_57cc = 1;
    }
}

/* Unchanged genuine definition: board / alternate_view */
void alternate_view(void)
{
 int result;
 state_57cc=0;
 switch((unsigned char)ready_9856) {
 case 1:
  if(prompt_1296("O.K. to start New Game?",12,1)==0x1003){setup_state();reset_df71();}
  clear: ready_9856=0;goto done;
 case 14:save_cc72();goto clear;
 case 15:save_dialog_ced4();goto clear;
 case 4:
  if(history[history_index+1].detail.bytes.kind){notify_86a1(history[history_index+1]);animate_move(&history[history_index+2]);}
  goto clear;
 case 5:
  if(history[history_index+2].detail.bytes.kind && history_index < -1){notify_866d(history[history_index+2]);undo_animation(&history[history_index+1]);}
  goto clear;
 case 11:prompt_893c();goto clear;
 case 2:if(modes[current_side]==1)state_57cc=2;goto clear;
 case 6:
  validate_current_8ca1();trim_history();commit_move_8632();shift_state();
  history[2]=initial_move;ready_9856=0;
  if(promote_ui_9371()){history[0].detail.bytes.kind=select_promotion(opponent);finish_move_93d6();}
  else if(result=animation_stage(history[0],0))ready_9856=result;
  if(modes[current_side]==1)state_57cc=2;
  else if(!search_state_8fca())no_move();
  goto done;
 case 18:
  reset_position_08de();init_state();ready_9856=0;
  if(modes[current_side]==1)ready_9856=2;
  else if(!search_state_8fca())no_move();
  goto done;
 default:goto clear;
 }
 done:poll_input();
}

/* Unchanged genuine definition: cycle / computer_cycle_801a */
void computer_cycle_801a(void)
{
 setup_word_934a=0;
 do {
  waiting_0eee=0;
  switch(setup_word_934a) {
  case 0:search_turn_8061();break;
  case 1:commit_turn_810c();break;
  case 2:empty_82a4();break;
  }
 }while(state_57cc==2 && modes[current_side]==1);
 state_57cc=0;
}

/* Unchanged genuine definition: cycle / search_turn_8061 */
void search_turn_8061(void)
{
 prepare_85c5();
 begin_turn();
 trim_history();
 if(view_mode_053a)prepare_hint_8384();
 history_index=0;
 waiting_0eee=0;
 if(!view_mode_053a) {
  setup_word_9844=0;
  run_search(2);
 }else if(book_choice_offset>0) {
  search_active=1;
  select_mode(3);
  setup_word_9844=1;
  accept_hint_82db();
  search_active=0;
  if((modes[0]==modes[1])==1) {
   if(!ready_9856)ready_9856=obtain_input();
   if(ready_9856)step_872a();
  }
 }else {
  setup_word_9844=0;
  run_search(setup_word_9646);
 }
 history_index=-1;
 setup_word_934a=1;
 charge_clock_85fd(temporary);
}

/* Unchanged genuine definition: commit / commit_turn_810c */
void commit_turn_810c(void)
{
 int result;
 history_tail[0]=working_move;
 hint_line=initial_move;
 history_tail[1]=initial_move;
 if(!history_tail[0].detail.bytes.kind) {
  hint_line=initial_move;
  if((modes[0]==modes[1])==1){no_move();setup_word_934a=0;return;}
  if(!history[0].detail.bytes.kind){setup_state();state_57cc=0;return;}
 }else {
  notify_wrapper_861b(history_tail[history_index+1]);
  shift_state();
  if((modes[0]==modes[1])==1) {
   if(history_move_counter>=120||count_9bfd()>=100||repetition_9c34(0)>=3||best<=-2176) {
    if(!current_side) {
     prompt_1296("Blue resigns",12,0);reset_df71();
     write_bytes_dbb5((Byte*)"Blue resigns\r",13);
    }else {
     prompt_1296("Red resigns",12,0);reset_df71();
     write_bytes_dbb5((Byte*)"Red resigns\r",12);
    }
    refresh_1446();setup_state();return;
   }
   setup_word_934a=0;
   if(promote_ui_9371()){finish_move_93d6();return;}
   if((result=animation_stage(history_tail[0],0))!=0)ready_9856=result;
   return;
  }else {
   setup_word_934a=2;
   if(promote_ui_9371())finish_move_93d6();
   else if((result=animation_stage(history_tail[0],0))!=0)ready_9856=result;
   if(search_state_8fca())return;
  }
 }
 no_move();
}

/* Unchanged genuine definition: book / empty_82a4 */
void empty_82a4(void) {}

/* Unchanged genuine definition: book / load_book_82a5 */
void load_book_82a5(void)
{
    select_asset_file(0);
    seek_asset(startup_offsets_9648[2]);
    read_asset((unsigned char huge *)splash_buffer,startup_lengths_a8b6[2]);
}

/* Unchanged genuine definition: book / accept_hint_82db */
void accept_hint_82db(void)
{
    struct {int spins,walk,draw,threshold;} selection;
    graphics_end();
    selection.draw=rand()&15;
    for(selection.threshold=0;book_weights[selection.threshold]<=selection.draw;selection.threshold++);
    for(selection.spins=1;selection.spins<=selection.threshold;selection.spins++)rotate_book_8515(1);
    book_state_index=splash_buffer[(unsigned)book_choice_offset]&0x3f;
    generate_a348();
    for(selection.walk=0;selection.walk<=book_state_index;selection.walk++)advance();
    working_move=state_8d12;
    working_follow_8bb6=initial_move;
    best=0;
    iteration=0;
    input_state=0;
    graphics_begin();
}

/* Unchanged genuine definition: book / prepare_hint_8384 */
void prepare_hint_8384(void)
{
    search_active=1;
    select_mode(3);
    trim_history();
    book_choice_offset=0;
    if(history_move_counter<state_8fde) {
        book_saved_index=history_index;
        while(history[history_index+1].detail.bytes.kind)notify_86a1(history[history_index+1]);
        book_matches=0;
        if(history[history_index+1].detail.bytes.capture==1) {
            history_index++;
            scan_book_843f();
            history_index--;
        }
        while(history_index<book_saved_index)notify_866d(history[history_index+2]);
        if(book_matches)state_8fde=200;
        else {state_8fde=history_move_counter;book_choice_offset=0;}
    }
    search_active=0;
}

/* Unchanged genuine definition: book / scan_book_843f */
void scan_book_843f(void)
{
    book_choice_offset++;
    if(history_index>book_saved_index) {book_matches=1;return;}
    book_state_index=-1;
    generate_a348();
    do {
        book_state_index++;
        advance();
        if(!state_8d12.detail.bytes.kind)break;
    }while(!equal_state(&state_8d12,&history[history_index+1]));
    if(state_8d12.detail.bytes.kind) {
        while((splash_buffer[book_choice_offset]&63)!=book_state_index) {
            if(splash_buffer[book_choice_offset]>=128)break;
            rotate_book_8515(0);
        }
        if((splash_buffer[book_choice_offset]&127)==book_state_index+64) {
            notify_866d(history[history_index+1]);
            scan_book_843f();
            notify_86a1(history[history_index]);
        }
    }
}

/* Unchanged genuine definition: book / rotate_book_8515 */
void rotate_book_8515(int flag)
{
    int depth;
    if(splash_buffer[(unsigned)book_choice_offset]<128) {
        depth=0;
        do {
            if(splash_buffer[(unsigned)book_choice_offset]&64)depth++;
            if(splash_buffer[(unsigned)book_choice_offset]>=128)depth--;
            book_choice_offset++;
        }while(depth);
        if(!(flag & (splash_buffer[(unsigned)book_choice_offset]==63)))return;
    }
    skip_book_8577();
}

/* Unchanged genuine definition: book / skip_book_8577 */
void skip_book_8577(void)
{
    while(!(splash_buffer[(unsigned)book_choice_offset-1]&64))previous_book_858d();
}

/* Unchanged genuine definition: book / previous_book_858d */
void previous_book_858d(void)
{
    int depth;
    depth=0;
    do {
        book_choice_offset--;
        if(splash_buffer[(unsigned)book_choice_offset]>=128)depth++;
        if(splash_buffer[(unsigned)book_choice_offset]&64)depth--;
    }while(depth);
}
