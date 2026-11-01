/* Complete event record copied as ten native words. kind 3 denotes a tick. */
typedef struct {int kind,code,status,reserved,x,y,data[4];} Event;
Event event_tick_0072={3,0,0,0,0,0,{0,0,0,0}};
