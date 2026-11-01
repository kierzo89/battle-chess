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
extern Byte huge *arena_cursor;
extern int **frame_list_cursor, *frame_data_cursor;
extern unsigned frame_count, list_count;
extern CachedFrame cached_frames[];

extern AssetGroup asset_groups[];
extern Byte asset_group_loaded[], asset_group_frame_counts[], frame_directory[];
extern int *frame_data_cursor, **frame_list_cursor;
extern unsigned frame_count;
extern Byte huge *arena_cursor;
extern void select_asset_file(int),load_group_frames(Byte *,Byte *,int);

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
    k=(long)((int huge *)arena_cursor-e);
    while(k--) *b++=*e++;
    arena_cursor=(Byte huge *)b;
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
