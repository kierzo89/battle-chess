typedef struct {int kind,code,status,reserved,x,y,data[4];} Event;
typedef struct {int words[5];int queue;} EventContext;
EventContext *event_context;
Event *current_event;
