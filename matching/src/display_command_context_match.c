typedef unsigned char Byte;
typedef struct {Byte kind,side;int index;} Cell;
extern Cell board[];
extern Byte cells[],kind_map[];
void far clear_display_fbf6(void)
{
    /* a: output square (DI); d: mapped piece (SI). Both registers are consumed. */
    register int d,a;
    /* b: side flag; c: orientation; e: source board square. */
    int b,c,e;
    for(a=0;a<64;a++) {
        e=(((a<<1)&112)^112)|(a&7);
        d=kind_map[board[e].kind];
        if(d==6) {
            if((a&7)<4)c=3;else c=7;
        } else if(d==1) {
            if((a&7)<4)c=board[e].side?3:1;
            else c=board[e].side?5:7;
        } else c=board[e].side?4:0;
        b=board[e].side==0;
        cells[a]=d?(b<<6)|(c<<3)|d:0;
    }
}

extern Byte cells[],row_mask_9230[8];
void far draw_fce8(int side)
{
 /* a: row in SI, b: column in DI; authentic register homes are compiler output. */
 register int a,b;
 /* c: consumed packed cell byte (BP-6). */
 Byte c;
 for(a=0;a<8;a++) {
  row_mask_9230[a]=0;
  for(b=0;b<8;b++) {
   c=cells[a*8+b];
   if(c&7) {
    if(c&64) {
     if(side==0)row_mask_9230[a]|=(Byte)1<<b;
    } else {
     if(side!=0)row_mask_9230[a]|=(Byte)1<<b;
    }
   }
  }
 }
}

/* Incomplete backing array: native wrap window does not prove allocation size. */
extern int command_words_8d2c[];
int *far write_command_fd4e(int *cursor)
{
    cursor+=10;
    if(cursor==command_words_8d2c+80)cursor=command_words_8d2c;
    return cursor;
}

extern int cursor_column_0086,cursor_row_0088;
int far command_key_fd6a(int key)
{
    /* Native explicitly sign-extends the low byte of the actual word argument. */
    switch((char)key) {
    case 0x48:
        cursor_row_0088=cursor_row_0088>=1?cursor_row_0088-1:7;
        return 1;
    case 0x4d:
        cursor_column_0086=cursor_column_0086<=6?cursor_column_0086+1:0;
        return 1;
    case 0x50:
        cursor_row_0088=cursor_row_0088<=6?cursor_row_0088+1:0;
        return 1;
    case 0x4b:
        cursor_column_0086=cursor_column_0086>=1?cursor_column_0086-1:7;
        return 1;
    }
    return 0;
}
