/* Compatible four-entry logical views; historical physical ownership unknown. */
typedef unsigned char Byte;
typedef struct { Byte width,height; signed char x,y; Byte huge *pixels; } Frame;
typedef struct AnimationTask AnimationTask;
Byte huge *metadata_records[4];
Frame frame_descriptors[4];
int values[4];
AnimationTask *task_pool[4];
