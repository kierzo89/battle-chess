/* Packed-byte x coordinate and y row, advanced while drawing a string. */
typedef struct { unsigned int packed_x; unsigned int y; } TextCursor;
TextCursor text_cursor = { 0, 0 };
