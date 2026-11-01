/* REA 9AD5, complete113-byte C4 /AS /Zi match. */
extern int castle_side_52d0;
extern int original_piece_9b46();
void far castle_flags_9ad5(side,flags) int side; unsigned *flags;
{
    int rank;
    castle_side_52d0=side;
    rank=0;
    if(side==1) rank=0x70;
    *flags=0;
    if(original_piece_9b46(rank+4,1)) {
        if(original_piece_9b46(rank,3)) *flags=1;
        if(original_piece_9b46(rank+7,3)) *(unsigned char *)flags |=2;
    }
}
