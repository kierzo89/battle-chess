/* Pending; not an exact byte match. */
/* Pending semantic reconstruction from REA. No byte match is claimed.
 * Original 9749 also requires same-segment far-call relaxation. */
typedef union { unsigned word; struct { unsigned char lo, hi; } byte; } MoveKind;
extern void move_961c(int,int);
extern void remove_967c(int);
extern void add_96af(int,int,int);
extern void change_96f9(int,int);
extern void far castle_95df(int,int *,int *);
extern int side_a836;
void apply_9749(int a,int b,int c,MoveKind d,int undo)
{
    int src;
    int dest;
    int unused;
    int square;
    if (undo) {
        move_961c(b,a);
        if (d.byte.hi) add_96af(d.byte.hi,side_a836,a);
    } else {
        if (d.byte.hi) remove_967c(a);
        move_961c(a,b);
    }
    if (c) {
        if (d.byte.lo==1) {
            castle_95df(a,&src,&dest);
            if (undo) move_961c(dest,src);
            else move_961c(src,dest);
        } else if (d.byte.lo==6) {
            square=(a&7)+(b&0x70);
            if (undo) add_96af(6,side_a836,square);
            else remove_967c(square);
        } else {
            if (undo) change_96f9(6,b);
            else change_96f9(d.byte.lo,a);
        }
    }
}

