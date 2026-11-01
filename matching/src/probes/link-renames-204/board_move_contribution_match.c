/* Ordinary C consolidation of the ten board-state/move procedures9448..983E. */
typedef union {unsigned word;struct{unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
typedef struct {unsigned char kind,side;int index;} Cell;
typedef struct {unsigned char square,kind;} Piece;
typedef union {int word;struct{unsigned char lo,hi;} byte;} Square;
extern Cell board[];
extern Piece pieces[2][16];
extern int counts[],piece_counts[];
extern int memcmp(const void *,const void *,unsigned);
extern void fill_8a96(char *,int,int);
extern void *memcpy(void *,const void *,unsigned);

int equal_state(Move *a,Move *b)
{
    return memcmp((char *)a,(char *)b,8)==0;
}

void clear_board(void)
{
    fill_8a96((char *)board,480,0);
}

void reset_pieces()
{
    int square, colour, entry;
    for(square=0;square<=119;square++) board[square].index=16;
    for(colour=0;colour<=1;colour++)
        for(entry=0;entry<=15;entry++) pieces[colour][entry].kind=0;
    counts[0]=-1;
    counts[1]=-1;
    memcpy(piece_counts,counts,4);
}

void init_pieces()
{
    int *count;
    int kind;
    Square s;
    Piece *entry;
    reset_pieces();
    for (kind = 1; kind <= 6; ++kind) {
        if (kind == 6)
            memcpy(piece_counts, counts, 4);
        s.word = 0;
        do {
            if (board[s.word].kind == kind) {
                count = &counts[board[s.word].side];
                ++counts[board[s.word].side];
                entry = pieces[board[s.word].side] + *count;
                entry->kind = kind;
                entry->square = s.word;
                board[s.word].index = counts[board[s.word].side];
            }
            s.byte.lo ^= 119;
            if (!(s.byte.lo & 4)) {
                if (s.word >= 112)
                    s.word = (s.word + 17) & 115;
                else
                    s.word += 16;
            }
        } while (s.word != 0);
    }
}

void far castle_95df(a,s,d) int a,*s,*d;
{
 if (((unsigned char)a & 7) >= 4) { *s=a-1; *d=a+1; }
 else { *s=a+1; *d=a-2; }
}



void swap_cells(a,b)
int a,b;
{
    Cell temporary;
    temporary = board[a];
    board[a] = board[b];
    board[b] = temporary;
    pieces[board[a].side][board[a].index].square = a;
}

void remove_piece(square)
int square;
{
    board[square].kind = 0;
    pieces[board[square].side][board[square].index].kind = 0;
}

void add_piece(kind,side,square)
int kind,side,square;
{
    Piece *piece;
    piece = &pieces[side][board[square].index];
    board[square].kind = kind;
    board[square].side = side;
    piece->kind = kind;
    piece->square = square;
}

void change_piece(kind,square)
int kind,square;
{
    int *count;
    board[square].kind = kind;
    pieces[board[square].side][board[square].index].kind = kind;
    count = &piece_counts[board[square].side];
    if (*count < board[square].index)
        *count = board[square].index;
}


extern int opponent;
void apply_9749(Move move,int undo)
{
    int u; /* castling rook source */
    int t; /* castling rook destination */
    int q; /* en-passant capture square */
    if (undo) {
        swap_cells(move.from,move.to);
        if (move.detail.bytes.capture) add_piece(move.detail.bytes.capture,opponent,move.to);
    } else {
        if (move.detail.bytes.capture) remove_piece(move.to);
        swap_cells(move.to,move.from);
    }
    if (move.flag) {
        if (move.detail.bytes.kind==1) {
            castle_95df(move.to,&u,&t);
            if (undo) swap_cells(t,u);
            else swap_cells(u,t);
        } else if (move.detail.bytes.kind==6) {
            q=(move.to&7)+(move.from&0x70);
            if (undo) add_piece(6,opponent,q);
            else remove_piece(q);
        } else {
            if (undo) change_piece(6,move.from);
            else change_piece(move.detail.bytes.kind,move.to);
        }
    }
}

