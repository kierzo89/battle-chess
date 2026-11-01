typedef struct {
 int shift,mode,width,height,source_skip,dest_skip,left_mask,right_mask;
 char huge *destination;
 char huge *source;
} Blit;
Blit blit={0};
