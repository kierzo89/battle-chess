/* Coherent state, check and UI operations, image8F88..9419. */
typedef unsigned char Byte;
typedef union {unsigned word;struct{Byte kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
typedef struct {Byte kind,side;int index;} Cell;
typedef struct {Byte square,kind;} Piece;
typedef union {unsigned word;Piece bytes;} PieceWord;
extern int history_index,state_8fde,current_side,opponent,temporary,ready_9856,state_57cc;
extern int modes[],side_piece_counts[],mode_8176,mode_8188,command_active,view_mode_053a;
extern Move current,history,history_tail[],initial_move,state_8d12;
extern Cell board[];
extern Piece pieces[2][16];
extern void init_state(void),init_pieces(void),generate_a348(void),advance(void);
extern int probe_move_86d6(Move),attacked_9a50(),prompt_1296();
extern void present_check_91dc(void),refresh_1446(),animate_move(Move *),trim_history(void),setup_state();
extern int piece_attacks(int,int,int,int);
extern unsigned animation_stage(Move,int);
extern void set_limit(void),record_dfac(Move *),record_kind_dfe3(int),redraw_piece(int,int),change_piece(int,int);

typedef struct { int destination,king_home; } CastleEndpoints;
typedef union {struct{int pawn_step[2];unsigned piece_bits[6];}initialized;struct{int first_pawn_step;unsigned by_kind[7];}masks;} PawnAndMasks;
typedef struct {int ray_step[8],knight_step[8];PawnAndMasks pawn_and_masks;CastleEndpoints castle[2][2];int back_rank[8];} MoveLookupTables;
extern Cell board[];
extern Piece pieces[2][16];
extern MoveLookupTables move_lookup_tables;
extern int current_side,opponent;
extern void init_pieces(void),reset_state(void),fill_8a96(char *,int,int);
extern int attacked_9a50(int,int);
char *validate_editor_8e36(void)
{
 /* a=board cell, b=king counts, c=board square/white king, d=black king,
    e=direction/rank cursor, f=piece counts; every local is consumed. */
 Cell *a;
 int b[2],c,d,e,f[2];
 init_pieces();
 fill_8a96((char *)b,4,0);
 fill_8a96((char *)f,4,0);
 for(c=0;c<=119;c++)
  if(!(c&0x88)) {
   a=&board[c];
   if(a->kind) {
    f[a->side]++;
    if(a->kind==1)b[a->side]++;
   }
  }
 if(f[0]>16)return "Red has too many pieces.";
 if(f[1]>16)return "Blue has too many pieces.";
 if(b[0]>1)return "Red has too many Kings.";
 if(b[1]>1)return "Blue has too many Kings.";
 if(b[0]<1)return "Red needs a King.";
 if(b[1]<1)return "Blue needs a King.";
 c=pieces[0][0].square;
 d=pieces[1][0].square;
 for(e=0;e!=8;e++)
  if(move_lookup_tables.ray_step[e]+c==d)return "Kings are adjacent.";
 for(e=0;e!=7;e++)
  if(board[e].kind==6||board[e+112].kind==6)return "Pawns in final rank.";
 reset_state();
 if(attacked_9a50(current_side,pieces[opponent][0].square)) {
  if(current_side==0)return "Blue is in Check.";
  return "Red is in Check.";
 }
 return 0;
}

void reset_state(void)
{
    init_state();
    init_pieces();
    state_8fde = 0;
}

int min_i16(int a, int b)
{
    return a <= b ? a : b;
}

int max_i16(int a, int b)
{
    return a >= b ? a : b;
}

int abs_i16(int a)
{
    if (a > 0)
        return a;
    return -a;
}

int search_state_8fca(void)
{
    history_index++;
    generate_a348();
    history_index--;
    advance();
    if (!state_8d12.detail.bytes.kind)
        goto exhausted;
repeat:
    if (!probe_move_86d6(state_8d12))
        return 1;
    advance();
    if (state_8d12.detail.bytes.kind)
        goto repeat;
exhausted:
    return 0;
}

void no_move()
{
    int human, in_check, response;
    Cell *cell;
    human = (modes[0] == 0 && modes[1] != 2) ||
        (modes[1] == 0 && modes[0] != 2);
    if (in_check = attacked_9a50(opponent, pieces[current_side][0].square)) {
        present_check_91dc();
        temporary = current_side;
        current_side = opponent;
        opponent = temporary;
        if (current.detail.bytes.kind &&
            (response = animation_stage(current,1)))
            ready_9856 = response;
        response = prompt_1296("Check and mate...Game over.",12,human << 1);
    } else
        response = prompt_1296("Stalemate. How boring!",12,human << 1);
    refresh_1446();
    if (modes[0] != 2 && modes[1] != 2 && response != 4099) {
        if (in_check) {
            cell = &board[current.to];
            cell->kind = current.detail.bytes.capture;
            cell->side = opponent;
            cell = &board[current.from];
            cell->kind = current.detail.bytes.kind;
            cell->side = current_side;
            animate_move(&current);
        } else {
            temporary = opponent;
            opponent = current_side;
            current_side = temporary;
        }
        current = history_tail[history_index];
        cell = &board[current.to];
        cell->kind = current.detail.bytes.capture;
        cell->side = opponent;
        cell = &board[current.from];
        cell->kind = current.detail.bytes.kind;
        cell->side = current_side;
        animate_move(&history_tail[history_index]);
        history_tail[history_index] = initial_move;
        history_tail[history_index+1] = initial_move;
        --history_index;
        trim_history();
        init_pieces();
        state_57cc = 0;
    } else
        setup_state();
}

void present_check_91dc(void)
{
    {
        register int square;
        current = history;
        current.from = current.to;
        current.to = square = pieces[current_side][0].square;
        current.flag = 0;
        current.detail.bytes.capture = 1;
        if (!history.detail.bytes.kind) goto none;
        if (piece_attacks(history.detail.bytes.kind,opponent,history.to,square)) return;
    }
    {
        PieceWord a;
        int b,c;
        for (b=1,c=side_piece_counts[opponent];b<=c;b++) {
            a = *(PieceWord *)&pieces[opponent][b];
            if (a.bytes.kind && piece_attacks(a.bytes.kind,opponent,a.bytes.square,current.to)) {
                current.detail.bytes.kind = a.bytes.kind;
                current.from = a.bytes.square;
                return;
            }
        }
    }
none:
    current = initial_move;
}

void restore_ui_92ab(register unsigned char *p,unsigned char index)
{
    unsigned char flags;
    p += index * 2;
    ready_9856 = (unsigned)*p++ << 8;
    set_limit();
    ready_9856 = 0;
    flags = *p;
    modes[1] = flags & 3;
    modes[0] = (flags >> 2) & 3;
    mode_8176 = (flags & 64) != 0;
    mode_8188 = (flags & 32) != 0;
    command_active = (flags & 16) != 0;
}

void save_ui_931c(register unsigned char *p,unsigned char index)
{
    unsigned char flags;
    p += index * 2;
    *p++ = view_mode_053a;
    flags = modes[1] & 3;
    flags |= (modes[0] << 2) & 12;
    flags |= (mode_8176 << 6) + (mode_8188 << 5) + (command_active << 4);
    *p = flags;
}

int promote_ui_9371(void)
{
    int result;
    current = history;
    if (current.flag && current.detail.bytes.kind != 1 && current.detail.bytes.kind != 6) {
        current.detail.bytes.kind = 6;
        current.flag = 0;
        result = animation_stage(current,1);
        if (result) ready_9856 = result;
        return 1;
    }
    return 0;
}

void finish_move_93d6(void)
{
    if (modes[current_side] == 2) {
        record_dfac(&history);
        record_kind_dfe3(history.detail.bytes.kind);
    }
    redraw_piece(history.to,history.detail.bytes.kind);
    change_piece(history.detail.bytes.kind,history.to);
}

/* Original complete one-byte callee, referenced by seek_asset atCB84. */
void print_error(char *message) {}

/* Inferred storage and callees retain their observed address names. */
extern long ticks_ea5b(void);

void wait_941b(long delay)
{
    long start = ticks_ea5b();
    while (ticks_ea5b() < start + delay) { }
}
