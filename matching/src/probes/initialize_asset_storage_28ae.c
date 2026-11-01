typedef unsigned char Byte;
typedef struct { Byte width,height; signed char x,y; Byte huge *pixels; } Frame;
typedef struct AnimationTask AnimationTask;
extern Byte far graphics_workspace[];
extern Byte huge metadata_workspace[];
extern Byte huge decoded_arena[];
extern Byte huge *arena_cursor, huge *metadata_records[4];
extern Byte metadata_record_counts[4];
extern Frame frame_descriptors[4];
extern int values[4];
extern Byte animation_tasks[];
extern AnimationTask *task_pool[4];
extern int **frame_list_cursor, *frame_data_cursor;
extern int *frame_lists[], frame_words[];
extern long far *setup_offsets, far *setup_lengths;
extern Byte frame_directory[];
extern void select_asset_file(int),seek_asset(long),read_asset(Byte huge *,long);
extern void prepare_asset_decode(void),decode_frame_directory(Byte *),save_arena_state(void);

void initialize_asset_storage(void)
{
    register int i;
    Byte far *p;
    arena_cursor=metadata_workspace;
    for(i=0;i<4;i++) {
        metadata_records[i]=arena_cursor;
        arena_cursor+=(unsigned)(metadata_record_counts[i]*4+12);
    }
    p=graphics_workspace;
    for(i=0;i<4;i++) {
        values[i]=(int)&frame_descriptors[i];
        frame_descriptors[i].pixels=p;
        p+=3256;
    }
    p=animation_tasks;
    for(i=0;i<4;i++) {
        task_pool[i]=(AnimationTask *)p;
        p+=24;
    }
    frame_list_cursor=frame_lists;
    frame_data_cursor=frame_words;
    select_asset_file(0);
    seek_asset(setup_offsets[2]);
    read_asset(frame_directory,setup_lengths[2]);
    prepare_asset_decode();
    arena_cursor=decoded_arena;
    decode_frame_directory(frame_directory);
    save_arena_state();
}
