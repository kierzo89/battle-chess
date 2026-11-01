typedef unsigned char Byte;
typedef struct {
    int far *begin, far *end;
    int **list_begin, **list_end, *words;
    unsigned frame_begin, frame_end;
    int last_use;
} AssetGroup;
typedef struct { long value[4]; } DirectoryRecord;
extern AssetGroup asset_groups[];
extern Byte asset_group_requested[], asset_group_loaded[];
extern Byte selected_left,selected_right,asset_loaded[],asset_wanted[];
extern unsigned long asset_group_lengths[],pair_lengths[6][6],arena_capacity;
extern Byte *left_controls[6][6],*right_controls[6][6];
extern Byte *left_lists[6][6],*right_lists[6][6],*current_left,*current_right;
extern Byte huge *arena_cursor;
extern Byte huge decoded_arena[];
extern int arena_fallback;
extern Byte arena_exhausted_message[],frame_directory[],left_list_scratch[],right_list_scratch[];
extern DirectoryRecord far *pair_offsets,far *pair_directory_lengths;
extern void unload_asset_group(int),load_asset_group(int),save_active_arena(void);
extern void load_group_frames(Byte *,Byte *,int),seek_asset(long),read_asset(Byte huge *,long);
extern void prepare_asset_decode(void),decode_frame_directory(Byte *),cache_asset_frame(int);
extern int error_message(char *);

extern AssetGroup asset_groups[];
extern Byte asset_group_loaded[], asset_group_frame_counts[], frame_directory[];
extern int *frame_data_cursor, **frame_list_cursor;
extern unsigned frame_count;
extern Byte huge *arena_cursor;
extern void select_asset_file(int),load_group_frames(Byte *,Byte *,int);

void load_asset_group(register int slot)
{
    register unsigned i;
    asset_group_loaded[slot]=1;
    asset_groups[slot].words=frame_data_cursor;
    asset_groups[slot].list_begin=frame_list_cursor;
    asset_groups[slot].frame_begin=frame_count;
    asset_groups[slot].begin=(int far *)arena_cursor;
    select_asset_file(1);
    for(i=0;i<asset_group_frame_counts[slot];i++)
        frame_directory[i]=i;
    frame_directory[i]=255;
    load_group_frames(frame_directory,frame_directory+i+2,slot+3);
    asset_groups[slot].list_end=frame_list_cursor;
    asset_groups[slot].frame_end=frame_count;
    asset_groups[slot].end=(int far *)arena_cursor;
}

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
        if(asset_group_requested[p]!=255 && !asset_group_loaded[p])
            c+=asset_group_lengths[p];
    if(selected_left!=255) {
        b=selected_left-1;
        f=selected_right-1;
        current_left=left_controls[b][f];
        current_right=right_controls[f][b];
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
            if(asset_group_requested[p]==255 && asset_group_loaded[p]) {
                h=asset_groups[p].last_use;
                e=p;
            }
        }
        if(h==32767) {
            if(selected_left!=255 && !arena_fallback) {
                c-=pair_lengths[selected_left-1][selected_right-1];
                d=selected_left;
            } else error_message(arena_exhausted_message);
        } else unload_asset_group(e);
        g=arena_capacity-(long)(arena_cursor-decoded_arena);
    }
    for(p=0;p<6;p++)
        if(asset_group_requested[p]!=255 && !asset_group_loaded[p])
            load_asset_group(p);
    arena_fallback=d;
    if(selected_left!=255 && !d) {
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
