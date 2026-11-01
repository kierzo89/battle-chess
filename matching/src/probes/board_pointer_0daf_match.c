/* Map pointer coordinates through the rendered board's row thresholds,
 * update playable/empty-square hover outlines, and clear out-of-board marks. */
typedef unsigned char Byte;
extern int (*square_x)[9],*square_y;
extern unsigned selected_square_0efa,cursor_square_0efc,hover_square_0efe;
extern int menu_state;
extern Byte marked_square_8dd6,mode_005a,row_mask_9230[8];
extern unsigned selection_colour_52ce,selection_xor_52cc;
extern void outline_square_543a(unsigned,unsigned);
extern void far input_select_11ef_001e(void),far input_init_11ef_0000(void);
void board_pointer_0daf(int x,int y)
{
 /* a=hover square, b=row boundary cursor, c=row (SI), d=column (DI).
  * Every local is used; C5 naturally retains both register debug homes. */
 unsigned a;
 int *b;
 register int c,d;
 for(c=0;c<9&&square_y[c]<=y;c++);
 if(c>0&&c<9) {
  --c;b=square_x[c];
  for(d=0;d<9&&*b++<=x;d++);
  if(d>0&&d<9) {
   --d;a=(c<<3)|d;hover_square_0efe=a;
   if(a!=selected_square_0efa&&a!=marked_square_8dd6) {
    outline_square_543a(selected_square_0efa,0);
    outline_square_543a(marked_square_8dd6,0);
    if(selected_square_0efa!=255||marked_square_8dd6!=255)outline_square_543a(cursor_square_0efc,12);
    marked_square_8dd6=selected_square_0efa=255;
    if(row_mask_9230[c]&(1<<d)) {
     if(!menu_state){selection_colour_52ce=1;selection_xor_52cc=14;}
     else{selection_colour_52ce=9;selection_xor_52cc=8;}
     outline_square_543a(a,selection_colour_52ce);selected_square_0efa=a;
    }else if(!mode_005a) {
     if(!menu_state){selection_colour_52ce=12;selection_xor_52cc=3;}
     else{selection_colour_52ce=10;selection_xor_52cc=8;}
     marked_square_8dd6=a;outline_square_543a(a,selection_colour_52ce);
    }
   }else if(!mode_005a||a==selected_square_0efa) {
    selection_colour_52ce^=selection_xor_52cc;outline_square_543a(a,selection_colour_52ce);
   }
  }else {
   hover_square_0efe=255;input_select_11ef_001e();
   outline_square_543a(selected_square_0efa,0);
   outline_square_543a(cursor_square_0efc,28);
   outline_square_543a(marked_square_8dd6,0);
   input_init_11ef_0000();marked_square_8dd6=selected_square_0efa=255;
  }
 }else {
  hover_square_0efe=255;
  outline_square_543a(selected_square_0efa,0);
  outline_square_543a(cursor_square_0efc,28);
  outline_square_543a(marked_square_8dd6,0);
  marked_square_8dd6=selected_square_0efa=255;
 }
}
