typedef unsigned char Byte;
typedef struct { unsigned long directory, pixels; } AssetLocation;
typedef struct { long value[4]; } DirectoryRecord;
typedef union {struct {Byte loaded[6],requested[6],left,right;} named;Byte bytes[14];} AssetState;
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
extern AssetLocation far *setup_offsets, far *setup_lengths;
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
    seek_asset(setup_offsets[1].directory);
    read_asset(frame_directory,setup_lengths[1].directory);
    prepare_asset_decode();
    arena_cursor=decoded_arena;
    decode_frame_directory(frame_directory);
    save_arena_state();
}

/* Typed asset index selection, surface reset, and background delta decode. */
extern AssetLocation far *setup_offsets, far *setup_lengths;
extern unsigned long far *asset_offsets, far *asset_lengths;
extern unsigned long far *startup_offsets_9648, far *startup_lengths_a8b6;
extern DirectoryRecord far *pair_offsets, far *pair_directory_lengths;
extern AssetLocation far setup_offsets_data[],far setup_lengths_data[];
extern unsigned long far asset_offsets_data[],far asset_lengths_data[];
extern unsigned long far startup_offsets_data[],far startup_lengths_data[];
extern DirectoryRecord far pair_offsets_data[],far pair_lengths_data[];
extern unsigned selected_square_0efa,cursor_square_0efc;
extern AssetState asset_state;
extern Byte palette_mode;
extern int command_active;
extern Byte frame_directory[];
extern int *screen_y,*screen_x,*square_y,(*square_x)[9];
extern Byte *frame_index;
extern int screen_y_flat[],screen_x_flat[],square_y_flat[],square_x_flat[][9];
extern int screen_y_tilted[],screen_x_tilted[],square_y_tilted[],square_x_tilted[][9];
extern Byte frame_index_flat[],frame_index_tilted[];
extern char huge *screen;
extern void outline_square_543a(unsigned,unsigned),detach_all(void),restore_arena_state(void);
extern void select_asset_file(int),seek_asset(long),read_asset(Byte huge *,long);
extern void prepare_asset_decode(void),decode_frame_directory(Byte *);
extern long huff_frame_decode(Byte huge *,long);
extern void cache_asset_frame(int),reset_graphics_3e4f(void);
void configure_game(register int frame);

void setup_assets(void)
{
 setup_offsets=setup_offsets_data;
 asset_offsets=asset_offsets_data;
 startup_offsets_9648=startup_offsets_data;
 pair_offsets=pair_offsets_data;
 setup_lengths=setup_lengths_data;
 asset_lengths=asset_lengths_data;
 startup_lengths_a8b6=startup_lengths_data;
 pair_directory_lengths=pair_lengths_data;
}

void init_surface(void)
{
 register int i,mode;
 outline_square_543a(cursor_square_0efc,0);
 outline_square_543a(selected_square_0efa,0);
 cursor_square_0efc=255;
 selected_square_0efa=255;
 detach_all();
 restore_arena_state();
 i=0;goto test_first;
 first:asset_state.bytes[i++]=0;
 test_first:if(i<6)goto first;
 i=0;goto test_second;
 second:asset_state.bytes[6+i++]=255;
 test_second:if(i<8)goto second;
 if(command_active) {
  select_asset_file(0);
  mode=!palette_mode?3:2;
  seek_asset(setup_offsets[mode].directory);
  read_asset(frame_directory,setup_lengths[mode].directory);
  prepare_asset_decode();
  decode_frame_directory(frame_directory);
  screen_y=screen_y_tilted;screen_x=screen_x_tilted;
  square_y=square_y_tilted;square_x=square_x_tilted;
  frame_index=frame_index_tilted;
  configure_game(1);
 }else {
  select_asset_file(0);
  seek_asset(setup_offsets[0].directory);
  read_asset(frame_directory,setup_lengths[0].directory);
  prepare_asset_decode();
  decode_frame_directory(frame_directory);
  screen_y=screen_y_flat;screen_x=screen_x_flat;
  square_y=square_y_flat;square_x=square_x_flat;
  frame_index=frame_index_flat;
  configure_game(0);
  cache_asset_frame(10);
  cache_asset_frame(9);
 }
}

void configure_game(register int frame)
{
 /* a=source, b=next delta row, c=bytes left. Every local is used. */
 Byte huge *a,huge *b;
 long c;
 select_asset_file(0);
 if(!frame&&!palette_mode)frame=7;
 seek_asset(startup_offsets_9648[frame]);
 prepare_asset_decode();
 huff_frame_decode((Byte huge *)screen,32000L);
 a=(Byte huge *)screen;
 b=a+160;
 for(c=31840L;c;--c,a++,b++)
  *b^=*a;
 reset_graphics_3e4f();
}

/* Actual adjacent reciprocal checkpoint functions; no added declarations or bodies. */
extern int *frame_data_cursor, **frame_list_cursor;
extern unsigned count_0096,count_0094,frame_count,frame_list_count;
extern unsigned char huge *arena_cursor;
extern int *checkpoint_data_933e, **checkpoint_lists_a84e;
extern unsigned checkpoint_8180,checkpoint_8186,checkpoint_936e,checkpoint_987e;
extern unsigned char huge *checkpoint_arena_9368;

void save_arena_state(void)
{
    checkpoint_data_933e=frame_data_cursor;
    checkpoint_lists_a84e=frame_list_cursor;
    checkpoint_8180=count_0096;
    checkpoint_8186=count_0094;
    checkpoint_936e=frame_count;
    checkpoint_987e=frame_list_count;
    checkpoint_arena_9368=arena_cursor;
}

extern int *frame_data_cursor, **frame_list_cursor;
extern unsigned count_0096,count_0094,frame_count,frame_list_count;
extern unsigned char huge *arena_cursor;
extern int *checkpoint_data_933e, **checkpoint_lists_a84e;
extern unsigned checkpoint_8180,checkpoint_8186,checkpoint_936e,checkpoint_987e;
extern unsigned char huge *checkpoint_arena_9368;


void restore_arena_state(void)
{
    frame_data_cursor=checkpoint_data_933e;
    frame_list_cursor=checkpoint_lists_a84e;
    count_0096=checkpoint_8180;
    count_0094=checkpoint_8186;
    frame_count=checkpoint_936e;
    frame_list_count=checkpoint_987e;
    arena_cursor=checkpoint_arena_9368;
}
