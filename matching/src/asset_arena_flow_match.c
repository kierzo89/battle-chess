/* Decode one selected compressed-bank asset into the advancing frame arena.
   The cache record's final word is unaccessed here; its ten-byte stride is observed. */
typedef struct {
    unsigned char huge *begin, huge *end;
    unsigned unclassified_word;
} AssetCache;
extern AssetCache asset_frames[];
extern unsigned char asset_loaded[], mode_11aa;
extern unsigned char huge *arena_cursor;
extern unsigned long far *asset_offsets;
extern unsigned char huge asset_buffer[];
extern void begin_asset_decode(unsigned char huge *), prepare_asset_decode(void);
extern long huff_frame_decode(unsigned char huge *, long);
extern void end_asset_decode(void);

void cache_asset_frame(register int slot)
{
    asset_loaded[slot]=1;
    asset_frames[slot].begin=arena_cursor;
    begin_asset_decode(asset_buffer+(asset_offsets[15*mode_11aa+slot]-asset_offsets[15*mode_11aa]));
    prepare_asset_decode();
    arena_cursor+=(huff_frame_decode(arena_cursor,11000L)+1L)&~1L;
    asset_frames[slot].end=arena_cursor;
    end_asset_decode();
}

typedef unsigned char Byte;
typedef struct {
    int huge *begin, huge *end;
    int **list_begin, **list_end, *words;
    unsigned frame_begin, frame_end;
    int last_use;
} AssetGroup;
typedef struct { long value[4]; } DirectoryRecord;
extern AssetGroup asset_groups[];
typedef union {struct {Byte loaded[6],requested[6],left,right;} named;Byte bytes[14];} AssetState;
extern AssetState asset_state;
extern Byte asset_loaded[],asset_wanted[];
extern unsigned long asset_group_lengths[],pair_lengths[6][6],arena_capacity;
extern Byte *left_controls[6][6],*right_controls[6][6];
extern Byte *left_lists[6][6],*right_lists[6][6];
typedef union {struct {Byte *left,*right;} named;Byte *by_side[2];} CurrentControls;
extern CurrentControls current_controls;
extern Byte huge *arena_cursor;
extern Byte huge decoded_arena[];
extern int arena_fallback;
extern Byte frame_directory[],left_list_scratch[],right_list_scratch[];
extern DirectoryRecord far *pair_offsets,far *pair_directory_lengths;
extern void unload_asset_group(int),load_asset_group(int),save_active_arena(void);
extern void load_group_frames(Byte *,Byte *,int),seek_asset(long),read_asset(Byte huge *,long);
extern void prepare_asset_decode(void),decode_frame_directory(Byte *),cache_asset_frame(int);
extern int error_message(char *);

void manage_asset_arena(void)
{
    /* p/f are register loop/right indices; remaining names preserve ordinary
       C5 identifier-bucket allocation of semantically observed locals. */
    register int p,f;
    Byte *a;
    int b,d,e,h;
    unsigned long c,g;
    Byte i;
    g=arena_capacity-(long)(arena_cursor-decoded_arena);
    c=0;
    for(p=0;p<6;p++)
        if(asset_state.named.requested[p]!=255 && !asset_state.named.loaded[p])
            c+=asset_group_lengths[p];
    if(asset_state.named.left!=255) {
        b=asset_state.named.left-1;
        f=asset_state.named.right-1;
        current_controls.named.left=left_controls[b][f];
        current_controls.named.right=right_controls[f][b];
        c+=pair_lengths[b][f];
        for(p=0;p<16;asset_wanted[p++]=0)
            ;
        for(a=left_controls[b][f];(i=*a)!=255;a++)
            if(i&128)asset_wanted[*a++&15]=1;
        for(a=right_controls[f][b];(i=*a)!=255;a++)
            if(i&128)asset_wanted[*a++&15]=1;
    }
    d=0;
    while(g<c) {
        h=32767;
        for(p=0;p<6;p++) {
            if(asset_state.named.requested[p]==255 && asset_state.named.loaded[p]) {
                h=asset_groups[p].last_use;
                e=p;
            }
        }
        if(h==32767) {
            if(asset_state.named.left!=255 && !arena_fallback) {
                c-=pair_lengths[asset_state.named.left-1][asset_state.named.right-1];
                d=asset_state.named.left;
            } else error_message("error  not enough memory");
        } else unload_asset_group(e);
        g=arena_capacity-(long)(arena_cursor-decoded_arena);
    }
    for(p=0;p<6;p++)
        if(asset_state.named.requested[p]!=255 && !asset_state.named.loaded[p])
            load_asset_group(p);
    arena_fallback=d;
    if(asset_state.named.left!=255 && !d) {
        save_active_arena();
        load_group_frames(left_lists[b][f],left_list_scratch,2*b+9);
        seek_asset(pair_offsets[b+3].value[2]);
        read_asset(frame_directory,pair_directory_lengths[b+3].value[2]);
        prepare_asset_decode();
        decode_frame_directory(frame_directory);
        load_group_frames(right_lists[f][b],right_list_scratch,2*f+21);
        seek_asset(pair_offsets[f+9].value[2]);
        read_asset(frame_directory,pair_directory_lengths[f+9].value[2]);
        prepare_asset_decode();
        decode_frame_directory(frame_directory);
        for(p=0;p<16;asset_loaded[p++]=0)
            ;
        asset_loaded[10]=1;
        asset_loaded[9]=1;
        for(p=0;p<16;p++)
            if(asset_wanted[p] && !asset_loaded[p])cache_asset_frame(p);
    }
    g=arena_capacity-(long)(arena_cursor-decoded_arena);
}

/* Four genuine adjacent value/task pool operations, image3A99..3B2C. */
typedef struct AnimationTask AnimationTask;
extern int value_index,values[4];
extern int task_index;
extern AnimationTask *task_pool[4];
extern int error_message(char *);
void push_value(int value)
{
 if(value_index){values[--value_index]=value;return;}
 error_message("error 104");
}
int pop_value(void)
{
 if(value_index<4)return values[value_index++];
 return error_message("error 103");
}
void release_task_3ae3(AnimationTask *task)
{
 if(task_index){task_pool[--task_index]=task;return;}
 error_message("error 102");
}
AnimationTask *allocate_task_3b0c(void)
{
 if(task_index<4)return task_pool[task_index++];
 return (AnimationTask *)error_message("error 101");
}
