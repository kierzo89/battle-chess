/* Compatible four displayed choices followed by the independently consumed near pointers.
 * The native x==224 path reads beyond the four choices; no fifth item is invented.
 * Original source grouping, array bound, and queue allocation ownership are unknown. */
typedef unsigned char Byte;
extern int command_words_8d2c[];
Byte promotion_choices[]={2,4,5,3};
int *command_head_006e=command_words_8d2c;
int *command_cursor_0070=command_words_8d2c;
