typedef union {unsigned word;struct{unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
extern unsigned long far *startup_offsets_9648,far *startup_lengths_a8b6;
extern unsigned char far splash_buffer[];
extern void select_asset_file(int),seek_asset(long),read_asset(unsigned char huge *,long);
extern void far graphics_end(void),far graphics_begin(void);
extern int rand(void);
extern char book_weights[];

extern int book_choice_offset,book_state_index,best,iteration,input_state;
extern Move working_move,working_follow_8bb6,state_8d12,initial_move;
extern void rotate_book_8515(int),generate_a348(void),advance(void);
void empty_82a4(void) {}
void load_book_82a5(void)
{
    select_asset_file(0);
    seek_asset(startup_offsets_9648[2]);
    read_asset((unsigned char huge *)splash_buffer,startup_lengths_a8b6[2]);
}
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

extern unsigned char search_active;
extern int book_choice_offset,history_move_counter,state_8fde,history_index,book_saved_index,book_matches;
extern Move history[];
extern void select_mode(int),trim_history(void),notify_86a1(Move),notify_866d(Move),scan_book_843f(void);
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

extern int equal_state(Move *,Move *);
extern void skip_book_8577(void),previous_book_858d(void);
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
void skip_book_8577(void)
{
    while(!(splash_buffer[(unsigned)book_choice_offset-1]&64))previous_book_858d();
}
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
