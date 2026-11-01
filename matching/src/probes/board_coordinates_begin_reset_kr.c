/* Selection state saved while collecting a new move, then restored. */
typedef union { int word; struct { unsigned char low, high; } bytes; } InputWord;
typedef struct { char text[20]; int enabled; char rest[6]; } InputCaption;
extern InputWord input_from, input_to, input_mode, input_file, input_rank;
extern unsigned char saved_to, saved_mode, saved_file, saved_rank;
extern InputCaption captions[];
extern int caption_index;
extern void highlight_square();
extern void show_caption();

void begin_coordinates()
{
    highlight_square(input_to.word, 0);
    highlight_square(input_from.word, 0);
    saved_to = input_to.bytes.low;
    input_to.word = input_from.word = 255;
    if (input_mode.word && captions[caption_index].enabled)
        show_caption(captions[caption_index].text);
    saved_mode = input_mode.bytes.low;
    saved_file = input_file.bytes.low;
    saved_rank = input_rank.bytes.low;
    input_file.word = 0;
    input_rank.word = 0;
    input_mode.word = 0;
}

void reset_coordinates()
{
    input_to.word = saved_to;
    highlight_square(input_to.word, 28);
    input_file.word = saved_file;
    input_rank.word = saved_rank;
    input_mode.word = saved_mode;
}
