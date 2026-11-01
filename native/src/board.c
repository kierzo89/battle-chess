/* Native adaptation of matching/src/{board_codec,board_move_contribution}_match.c.
 * Explicit field widths, object sizes, and board context replace DOS ABI/globals.
 * No original turn/graphics side effects are claimed by this isolated core. */
#include "board.h"
#include <string.h>
_Static_assert(sizeof(BCCell)==4, "DOS cell layout");
static void init_pieces(BCBoard *b) {
 for(int s=0;s<120;s++) b->cells[s].index=16;
 memset(b->pieces,0,sizeof b->pieces);
 b->last_piece[0]=b->last_piece[1]=-1;
 b->last_nonpawn[0]=b->last_nonpawn[1]=-1;
 for(int kind=1;kind<=6;kind++) {
  if(kind==6) memcpy(b->last_nonpawn,b->last_piece,sizeof b->last_piece);
  unsigned s=0;
  do {
   BCCell *c=&b->cells[s];
   if(c->kind==kind) {
    int i=++b->last_piece[c->side];
    b->pieces[c->side][i]=(BCPiece){(uint8_t)s,(uint8_t)kind};
    c->index=(int16_t)i;
   }
   s^=119;
   if(!(s&4)) s=s>=112 ? (s+17)&115 : s+16;
  } while(s);
 }
}
bool bc_unpack(BCBoard *b,const uint8_t data[33]) {
 BCBoard next={0}; unsigned count[2]={0};
 if(data[0]>1) return false;
 next.side=data[0];
 for(unsigned i=0;i<64;i++) {
  unsigned nib=(data[1+i/2]>>(i%2 ? 0:4))&15;
  unsigned kind=nib&7, side=nib>>3;
  if(kind==7 || (kind && ++count[side]>16)) return false;
  next.cells[(i/8)*16+i%8]=(BCCell){(uint8_t)kind,(uint8_t)side,0};
 }
 init_pieces(&next); *b=next; return true;
}
void bc_pack(const BCBoard *b,uint8_t data[33]) {
 data[0]=b->side;
 for(unsigned r=0;r<8;r++) for(unsigned c=0;c<8;c+=2) {
  BCCell a=b->cells[r*16+c],d=b->cells[r*16+c+1];
  data[1+r*4+c/2]=(uint8_t)(((a.side<<3|a.kind)<<4)|(d.side<<3|d.kind));
 }
}
void bc_initial(BCBoard *b) {
 const uint8_t data[33]={0,0x35,0x42,0x14,0x53,0x66,0x66,0x66,0x66,
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0xee,0xee,0xee,0xee,0xbd,0xca,0x9c,0xdb};
 (void)bc_unpack(b,data);
}
static void swap(BCBoard *b,unsigned a,unsigned d) {
 BCCell t=b->cells[a]; b->cells[a]=b->cells[d]; b->cells[d]=t;
 BCCell c=b->cells[a];
 /* Original writes sentinel slot 16 on some empty-cell paths; no host OOB. */
 if(c.index>=0 && c.index<16) b->pieces[c.side][c.index].square=(uint8_t)a;
}
static void remove_piece(BCBoard *b,unsigned s) {
 BCCell *c=&b->cells[s]; c->kind=0; b->pieces[c->side][c->index].kind=0;
}
static void add(BCBoard *b,unsigned s,uint8_t kind,uint8_t side) {
 BCCell *c=&b->cells[s];c->kind=kind;c->side=side;
 b->pieces[side][c->index]=(BCPiece){(uint8_t)s,kind};
}
static void change(BCBoard *b,unsigned s,uint8_t kind) {
 BCCell *c=&b->cells[s];c->kind=kind;b->pieces[c->side][c->index].kind=kind;
 if(b->last_nonpawn[c->side]<c->index)b->last_nonpawn[c->side]=c->index;
}
void bc_apply(BCBoard *b,BCMove m,bool undo) {
 uint8_t opponent=b->side^1;
 if(undo) {swap(b,m.from,m.to);if(m.capture)add(b,m.to,m.capture,opponent);}
 else {if(m.capture)remove_piece(b,m.to);swap(b,m.to,m.from);}
 if(m.special) {
  if(m.kind==1) {
   unsigned u=(m.to&7)>=4 ? m.to-1:m.to+1;
   unsigned t=(m.to&7)>=4 ? m.to+1:m.to-2;
   if(undo)swap(b,t,u);else swap(b,u,t);
  } else if(m.kind==6) {
   unsigned q=(m.to&7)+(m.from&0x70);
   if(undo)add(b,q,6,opponent);else remove_piece(b,q);
  } else {if(undo)change(b,m.from,6);else change(b,m.to,m.kind);}
 }
}
