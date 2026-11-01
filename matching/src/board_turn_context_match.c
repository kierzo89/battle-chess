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

extern MoveLookupTables move_lookup_tables;
extern void clear_board(), init_pieces();
extern void set_cell_bytes(char, char, int);
extern int current_side, opponent;

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

/* REA image 7DA8: reconstruct the eight-byte state as four 16-bit words.
 * Original field names are unknown. Placements are linker configuration.
 */
typedef union {unsigned word;struct{unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;

extern int history_index;
extern Move history[];
extern Move initial_move;

void init_state(void)
{
    history_index = -1;
    history[0] = initial_move;
}

/* REA 7DBF: assign two bytes in a four-byte board cell.
 * The remaining bytes and original field names are not established here.
 */
typedef struct {
    unsigned char kind, side;
    int index;
} Cell;

extern Cell board[];

void set_cell_bytes(char first, char second, int square)
{
    board[square].kind = first;
    board[square].side = second;
}

/* REA 7DDB. C5.00 /AS /Gs /Os emits all144 original bytes.
 * Address names describe observed storage and calls, not original symbols.
 */
typedef struct {
    unsigned char square;
    char remaining[31];
} SideInfo;

extern int state_cbd2;
extern int state_934c;
extern int search_state_8fca(void);
extern void no_move(void);
extern int current_side;
extern int opponent;
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
extern int state_57cc;

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

extern int state_57cc,ready_9856,current_side,opponent,history_index,modes[];
extern Move history[],initial_move;
extern char alternate_prompt[];
extern int prompt_1296(),search_state_8fca(),promote_ui_9371(void);
extern char select_promotion(int);
extern unsigned animation_stage(Move,int);
extern void setup_state(),reset_df71(),save_cc72(),save_dialog_ced4(),notify_86a1(Move),notify_866d(Move),animate_move(Move*),undo_animation(Move*),prompt_893c();
extern int validate_current_8ca1(void);
extern void trim_history(),commit_move_8632(),shift_state(),finish_move_93d6(),no_move(),reset_position_08de(),init_state(),poll_input();
void alternate_view(void)
{
 int result;
 state_57cc=0;
 switch((unsigned char)ready_9856) {
 case 1:
  if(prompt_1296(alternate_prompt,12,1)==0x1003){setup_state();reset_df71();}
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
