typedef unsigned char Byte;
typedef struct {Byte kind,side;int index;} Cell;
typedef struct {Byte square,kind;} Piece;
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
