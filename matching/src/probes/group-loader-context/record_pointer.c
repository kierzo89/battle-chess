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
    AssetGroup *group = &asset_groups[slot];
    asset_group_loaded[slot]=1;
    group->words=frame_data_cursor;
    group->list_begin=frame_list_cursor;
    group->frame_begin=frame_count;
    group->begin=(int far *)arena_cursor;
    select_asset_file(1);
    for(i=0;i<asset_group_frame_counts[slot];i++)
        frame_directory[i]=i;
    frame_directory[i]=255;
    load_group_frames(frame_directory,frame_directory+i+2,slot+3);
    group->list_end=frame_list_cursor;
    group->frame_end=frame_count;
    group->end=(int far *)arena_cursor;
}
