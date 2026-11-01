typedef unsigned char Byte;
typedef union {struct {Byte loaded[6],requested[6],left,right;} named;Byte bytes[14];} AssetState;
AssetState asset_state = {{{0,0,0,0,0,0},{255,0,0,0,0,0},0,0}};
