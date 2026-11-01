/* Four consumed bytes: two attributes and one near text pointer. */
typedef unsigned char Byte;
typedef struct { Byte colour,attribute; char *text; } Text;
Text dialog_text = {0,0,0};
