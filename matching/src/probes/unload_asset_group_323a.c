typedef unsigned char Byte;
typedef struct {
    int huge *begin, huge *end;
    int **list_begin, **list_end, *words;
    unsigned frame_begin, frame_end;
    int last_use;
} AssetGroup;
typedef struct { unsigned metadata[2]; Byte huge *data; } CachedFrame;
extern AssetGroup asset_groups[];
extern Byte asset_group_loaded[];
extern int huge *arena_cursor;
extern int **frame_list_cursor, *frame_data_cursor;
extern unsigned frame_count, list_count;
extern CachedFrame cached_frames[];

void unload_asset_group(register int slot)
{
    int huge *destination, huge *source;
    int **list_destination, **list_source;
    int *word_destination, *word_source;
    long count, removed_words, removed_list_words;
    unsigned long index, removed_frames;

    asset_group_loaded[slot]=0;
    destination=asset_groups[slot].begin;
    source=asset_groups[slot].end;
    removed_words=count=(long)(source-destination);
    asset_groups[slot].begin=0;
    asset_groups[slot].end=0;
    for(index=0;index<6;index++) {
        if(asset_groups[index].begin>destination) {
            asset_groups[index].begin-=count;
            asset_groups[index].end-=count;
        }
    }
    count=(long)(arena_cursor-source);
    while(count--) *destination++=*source++;
    arena_cursor=destination;
    list_destination=asset_groups[slot].list_begin;
    list_source=asset_groups[slot].list_end;
    count=list_source-list_destination;
    asset_groups[slot].list_begin=0;
    asset_groups[slot].list_end=0;
    removed_frames=asset_groups[slot].frame_end-asset_groups[slot].frame_begin;
    word_destination=asset_groups[slot].words;
    removed_list_words=*list_source-word_destination;
    for(index=0;index<6;index++) {
        if(asset_groups[index].list_begin>list_destination) {
            asset_groups[index].list_begin-=count;
            asset_groups[index].list_end-=count;
            asset_groups[index].frame_begin-=removed_frames;
            asset_groups[index].frame_end-=removed_frames;
            asset_groups[index].words-=removed_list_words;
        }
    }
    list_count-=count;
    count=frame_list_cursor-list_source;
    while(count--) {
        word_source=*list_source;
        *word_destination++=*word_source++;
        while(*word_source!=-1)
            *word_destination++=*word_source++-removed_frames;
        *word_destination++=*word_source++;
        *list_destination++=*list_source++-removed_list_words;
    }
    frame_list_cursor=list_destination;
    frame_data_cursor=word_destination;
    removed_frames=removed_words*2;
    for(index=asset_groups[slot].frame_end;index<frame_count;index++)
        cached_frames[index].data-=removed_frames;
    word_destination=(int *)&cached_frames[asset_groups[slot].frame_begin];
    word_source=(int *)&cached_frames[asset_groups[slot].frame_end];
    removed_frames=(int *)&cached_frames[frame_count]-word_source;
    while(removed_frames--) *word_destination++=*word_source++;
    frame_count-=asset_groups[slot].frame_end-asset_groups[slot].frame_begin;
}
