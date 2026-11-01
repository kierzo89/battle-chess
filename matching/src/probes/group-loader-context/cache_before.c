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
    int far *begin, far *end;
    int **list_begin, **list_end, *words;
    unsigned frame_begin, frame_end;
    int last_use;
} AssetGroup;
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
