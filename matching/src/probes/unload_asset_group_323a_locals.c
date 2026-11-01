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
    int huge *b, huge *e;
    int **c, **f;
    int *h, *j;
    long k, g, d;
    unsigned long i, a;

    asset_group_loaded[slot]=0;
    b=asset_groups[slot].begin;
    e=asset_groups[slot].end;
    g=k=(long)(e-b);
    asset_groups[slot].begin=0;
    asset_groups[slot].end=0;
    for(i=0;i<6;i++) {
        if(asset_groups[i].begin>b) {
            asset_groups[i].begin-=k;
            asset_groups[i].end-=k;
        }
    }
    k=(long)(arena_cursor-e);
    while(k--) *b++=*e++;
    arena_cursor=b;
    c=asset_groups[slot].list_begin;
    f=asset_groups[slot].list_end;
    k=f-c;
    asset_groups[slot].list_begin=0;
    asset_groups[slot].list_end=0;
    a=asset_groups[slot].frame_end-asset_groups[slot].frame_begin;
    h=asset_groups[slot].words;
    d=*f-h;
    for(i=0;i<6;i++) {
        if(asset_groups[i].list_begin>c) {
            asset_groups[i].list_begin-=k;
            asset_groups[i].list_end-=k;
            asset_groups[i].frame_begin-=a;
            asset_groups[i].frame_end-=a;
            asset_groups[i].words-=d;
        }
    }
    list_count-=k;
    k=frame_list_cursor-f;
    while(k--) {
        j=*f;
        *h++=*j++;
        while(*j!=-1)
            *h++=*j++-a;
        *h++=*j++;
        *c++=*f++-d;
    }
    frame_list_cursor=c;
    frame_data_cursor=h;
    a=g*2;
    for(i=asset_groups[slot].frame_end;i<frame_count;i++)
        cached_frames[i].data-=a;
    h=(int *)&cached_frames[asset_groups[slot].frame_begin];
    j=(int *)&cached_frames[asset_groups[slot].frame_end];
    a=(int *)&cached_frames[frame_count]-j;
    while(a--) *h++=*j++;
    frame_count-=asset_groups[slot].frame_end-asset_groups[slot].frame_begin;
}
