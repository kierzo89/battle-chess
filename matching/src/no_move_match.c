typedef unsigned char Byte;
typedef union { unsigned word; struct { Byte kind,capture; } byte; } Extra;
typedef struct { int from,to,flag; Extra extra; } Move;
typedef struct { Byte kind,side; int index; } Cell;
typedef struct { Byte square,kind; } Piece;
extern int modes[], side, opposite, temporary, input, counter, state;
extern Move current, history_tail[], initial;
extern Cell board[];
extern Piece pieces[2][16];
extern char check_text[], stalemate_text[];
extern int attacked_9a50(), effect_bb0e(), prompt_1296();
extern void prepare_91dc(), refresh_1446(), animate_78f6(), refresh_7bf9();
extern void init_pieces_950d(), setup_7c99();

void no_move()
{
    int human, in_check, response;
    Cell *cell;
    human = (modes[0] == 0 && modes[1] != 2) ||
        (modes[1] == 0 && modes[0] != 2);
    if (in_check = attacked_9a50(opposite, pieces[side][0].square)) {
        prepare_91dc();
        temporary = side;
        side = opposite;
        opposite = temporary;
        if (current.extra.byte.kind &&
            (response = effect_bb0e(current.from,current.to,current.flag,current.extra.word,1)))
            input = response;
        response = prompt_1296(check_text,12,human << 1);
    } else
        response = prompt_1296(stalemate_text,12,human << 1);
    refresh_1446();
    if (modes[0] != 2 && modes[1] != 2 && response != 4099) {
        if (in_check) {
            cell = &board[current.from];
            cell->kind = current.extra.byte.capture;
            cell->side = opposite;
            cell = &board[current.to];
            cell->kind = current.extra.byte.kind;
            cell->side = side;
            animate_78f6(&current);
        } else {
            temporary = opposite;
            opposite = side;
            side = temporary;
        }
        current = history_tail[counter];
        cell = &board[current.from];
        cell->kind = current.extra.byte.capture;
        cell->side = opposite;
        cell = &board[current.to];
        cell->kind = current.extra.byte.kind;
        cell->side = side;
        animate_78f6(&history_tail[counter]);
        history_tail[counter] = initial;
        history_tail[counter+1] = initial;
        --counter;
        refresh_7bf9();
        init_pieces_950d();
        state = 0;
    } else
        setup_7c99();
}
