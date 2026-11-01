/* Two separately consumed bytes: signed depth and unsigned button latch. */
typedef struct { signed char nesting; unsigned char button_latch; } InputFlags;
InputFlags input_flags_4952 = { 0, 0 };
