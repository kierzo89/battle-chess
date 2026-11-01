/* Load one group and retain its arena/directory boundaries, image35A0. */
typedef unsigned char Byte;
typedef struct {int huge *begin,huge *end;int **list_begin,**list_end,*words;unsigned frame_begin,frame_end;int last_use;} AssetGroup;
typedef union {struct {Byte loaded[6],requested[6],left,right;} named;Byte bytes[14];} AssetState;
extern AssetGroup asset_groups[];
extern AssetState asset_state;
extern Byte group_frame_counts[],frame_directory[];
extern int *frame_data_cursor,**frame_list_cursor;
extern unsigned frame_count;
extern Byte huge *arena_cursor;
extern void select_asset_file(int),load_group_frames(Byte *,Byte *,int);
void load_asset_group(register int group)
{
 register unsigned i;
 asset_state.named.loaded[group]=1;
 asset_groups[group].words=frame_data_cursor;
 asset_groups[group].list_begin=frame_list_cursor;
 asset_groups[group].frame_begin=frame_count;
 asset_groups[group].begin=(int huge *)arena_cursor;
 select_asset_file(1);
 for(i=0;i<group_frame_counts[group];i++)frame_directory[i]=i;
 frame_directory[i]=255;
 load_group_frames(frame_directory,frame_directory+i+2,group+3);
 asset_groups[group].list_end=frame_list_cursor;
 asset_groups[group].frame_end=frame_count;
 asset_groups[group].end=(int huge *)arena_cursor;
}
