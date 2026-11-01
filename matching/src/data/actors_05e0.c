typedef unsigned char Byte;
typedef struct Frame Frame;
typedef struct Actor {
 int x,y,old_x,old_y,flag;
 Byte colour,square;
 int left,right,top,bottom;
 Frame *frame;
 void far *resource;
 struct Actor *next;
} Actor;
Actor actors[70]={0};
