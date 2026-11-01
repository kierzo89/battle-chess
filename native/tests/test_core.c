#include "board.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
static void roundtrip(BCBoard *b,BCMove m) {
 uint8_t before[33],after[33];bc_pack(b,before);
 bc_apply(b,m,false);assert(b->cells[m.to].kind==m.kind);
 bc_apply(b,m,true);bc_pack(b,after);assert(!memcmp(before,after,33));
}
static void put(uint8_t *data,unsigned square,unsigned nibble){
 unsigned i=(square/16)*8+square%16;
 unsigned shift=i%2?0:4;
 data[1+i/2]=(uint8_t)((data[1+i/2]&~(15<<shift))|(nibble<<shift));
}
int main(void) {
 BCBoard b;bc_initial(&b);
 assert(b.last_piece[0]==15&&b.last_piece[1]==15);
 assert(b.last_nonpawn[0]==7&&b.last_nonpawn[1]==7);
 assert(b.cells[4].kind==1&&b.cells[0x74].kind==1);
 for(unsigned s=0;s<120;s++)if(!(s&0x88)&&b.cells[s].kind) {
  BCCell c=b.cells[s];assert(b.pieces[c.side][c.index].square==s);
 }
 roundtrip(&b,(BCMove){0x14,0x34,0,6,0});
 uint8_t data[33]={0};put(data,4,1);put(data,0x74,9);put(data,0x34,6);put(data,0x45,14);
 assert(bc_unpack(&b,data));roundtrip(&b,(BCMove){0x34,0x45,0,6,6});
 memset(data,0,sizeof data);put(data,4,1);put(data,0x74,9);put(data,0x44,6);put(data,0x45,14);
 assert(bc_unpack(&b,data));roundtrip(&b,(BCMove){0x44,0x55,1,6,0});
 memset(data,0,sizeof data);put(data,4,1);put(data,0x74,9);put(data,7,3);
 assert(bc_unpack(&b,data));bc_apply(&b,(BCMove){4,6,1,1,0},false);
 assert(b.cells[5].kind==3&&b.cells[7].kind==0);
 bc_apply(&b,(BCMove){4,6,1,1,0},true);assert(b.cells[7].kind==3&&b.cells[4].kind==1);
 memset(data,0,sizeof data);put(data,4,1);put(data,0x74,9);put(data,0x60,6);
 assert(bc_unpack(&b,data));roundtrip(&b,(BCMove){0x60,0x70,1,2,0});
 BCBoard saved=b;data[0]=2;assert(!bc_unpack(&b,data));assert(!memcmp(&b,&saved,sizeof b));
 data[0]=0;put(data,0,7);assert(!bc_unpack(&b,data));
 memset(data,0x66,sizeof data);data[0]=0;assert(!bc_unpack(&b,data));
 puts("PASS: initial piece indexing, codec, ordinary/capture/en-passant/castle/promotion undo and invalid input.");
 return 0;
}
