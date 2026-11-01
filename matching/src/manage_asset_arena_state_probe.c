typedef unsigned char Byte;
typedef struct {
    int huge *begin, huge *end;
    int **list_begin, **list_end, *words;
    unsigned frame_begin, frame_end;
    int last_use;
} AssetGroup;
typedef struct { long value[4]; } DirectoryRecord;
extern AssetGroup asset_groups[];
extern Byte asset_group_loaded[];
typedef union {struct {Byte group[6],left,right;} named;Byte bytes[8];} RequestState;
extern RequestState request_state;
extern Byte asset_loaded[],asset_wanted[];
extern unsigned long asset_group_lengths[],pair_lengths[6][6],arena_capacity;
extern Byte *left_controls[6][6],*right_controls[6][6];
extern Byte *left_lists[6][6],*right_lists[6][6];
typedef union {struct {Byte *left,*right;} named;Byte *by_side[2];} CurrentControls;
extern CurrentControls current_controls;
extern Byte huge *arena_cursor;
extern Byte huge decoded_arena[];
extern int arena_fallback;
extern Byte arena_exhausted_message[],frame_directory[],left_list_scratch[],right_list_scratch[];
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
        if(request_state.named.group[p]!=255 && !asset_group_loaded[p])
            c+=asset_group_lengths[p];
    if(request_state.named.left!=255) {
        b=request_state.named.left-1;
        f=request_state.named.right-1;
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
            if(request_state.named.group[p]==255 && asset_group_loaded[p]) {
                h=asset_groups[p].last_use;
                e=p;
            }
        }
        if(h==32767) {
            if(request_state.named.left!=255 && !arena_fallback) {
                c-=pair_lengths[request_state.named.left-1][request_state.named.right-1];
                d=request_state.named.left;
            } else error_message(arena_exhausted_message);
        } else unload_asset_group(e);
        g=arena_capacity-(long)(arena_cursor-decoded_arena);
    }
    for(p=0;p<6;p++)
        if(request_state.named.group[p]!=255 && !asset_group_loaded[p])
            load_asset_group(p);
    arena_fallback=d;
    if(request_state.named.left!=255 && !d) {
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
