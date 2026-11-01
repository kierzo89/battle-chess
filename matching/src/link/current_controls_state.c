typedef unsigned char Byte;
typedef union {struct {Byte *left,*right;} named;Byte *by_side[2];} CurrentControls;
CurrentControls current_controls;
