/* Selection state saved while collecting a new move, then restored. */
typedef union { int word; struct { unsigned char low, high; } bytes; } InputWord;
typedef struct { char text[20]; int enabled; char rest[6]; } InputCaption;
extern InputWord input_from, input_to, input_mode, input_file, input_rank;
extern unsigned char saved_to, saved_mode, saved_file, saved_rank;
extern InputCaption captions[];
extern int caption_index;
extern void highlight_square(int, int);
extern void show_caption(char *);

void reset_coordinates(void)
{
 unsigned char file, rank;
 input_to.word=saved_to;highlight_square(input_to.word,28);
 file=saved_file;input_file.word=file;rank=saved_rank;input_rank.word=rank;input_mode.word=saved_mode;
}
