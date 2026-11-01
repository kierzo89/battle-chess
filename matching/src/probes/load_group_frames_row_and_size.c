typedef unsigned char Byte;
typedef struct {Byte width,height;signed char x,y;char huge *pixels;} Frame;
typedef struct {unsigned long directory, pixels;} AssetLocation;
extern AssetLocation far *pair_offsets,far *pair_directory_lengths;
extern Byte frame_metadata[],frame_indices[];
extern Byte *directory_lists;
extern int **frame_list_cursor,*frame_data_cursor;
extern unsigned frame_count,list_count,control_base;
extern Byte huge *arena_cursor;
extern Frame cached_frames[];
extern void seek_asset(unsigned long),read_asset(Byte huge *,unsigned long);
extern void prepare_asset_decode(void),skip_frame_bits(unsigned);
extern Byte huge *decode_frame_pixels(Byte huge *,unsigned long,unsigned);

void load_group_frames(Byte *requested,Byte *mapping,int group)
{
    register int i,j;
    int total_frames,items,lists,skipped,found;
    Byte huge *cursor,huge *scan;
    Frame *frame;
    unsigned *words;
    unsigned long bits;
    unsigned row_bytes,decoded_size;

    group-=3;
    seek_asset(pair_offsets[group].directory);
    read_asset(frame_metadata,pair_directory_lengths[group].directory);
    for(i=0;i<256;frame_indices[i++]=0) ;
    words=(unsigned *)frame_metadata;
    while(words[0]||words[1]) words+=3;
    words+=3;
    directory_lists=(Byte *)words;
    cursor=directory_lists;
    lists=*cursor++;
    for(i=0;i<lists;i++) {
        found=0;
        scan=requested;
        for(j=0;*scan!=255;scan++,j++) {
            if(*scan==i) {
                found=1;
                mapping[j]=list_count;
            }
        }
        mapping[j]=255;
        items=*cursor++;
        cursor++;
        if(found) {
            list_count++;
            for(j=items;j;j--) frame_indices[*cursor++]=1;
        } else cursor+=items;
    }
    for(i=0,j=0;i<256;i++) {
        if(frame_indices[i]) frame_indices[i]=j++;
        else frame_indices[i]=255;
    }
    total_frames=j;
    cursor=directory_lists;
    words=(unsigned *)frame_data_cursor;
    lists=*cursor++;
    for(i=0;i<lists;i++) {
        scan=requested;
        for(;*scan!=255;scan++) if(*scan==i) break;
        items=*cursor++;
        if(*scan==i) {
            *frame_list_cursor++=(int *)words;
            *words++=(*cursor&128)?(*cursor++&127)+17:*cursor+++control_base;
            for(j=items;j;j--)
                *words++=frame_indices[*cursor++]+frame_count;
            *words++=-1;
        } else cursor+=items+1;
    }
    frame_data_cursor=(int *)words;
    prepare_asset_decode();
    skipped=0;
    bits=0;
    words=(unsigned *)frame_metadata;
    cursor=arena_cursor;
    frame=cached_frames+frame_count;
    for(i=0;words[0]||words[1];i++) {
        *(unsigned *)&frame->width=*words++;
        *(unsigned *)&frame->x=*words++;
        if(frame_indices[i]!=255) {
            if(frame->width&&frame->height) {
                if(skipped) {
                    seek_asset((bits>>3)+pair_offsets[group].pixels+8);
                    skip_frame_bits(bits&7);
                    skipped=0;
                }
                row_bytes=(frame->width+1)>>1;
                decoded_size=frame->height*row_bytes;
                scan=decode_frame_pixels(cursor,(unsigned long)decoded_size,row_bytes);
            } else scan=cursor;
            frame->pixels=(char huge *)cursor;
            cursor=scan;
            frame++;
        } else if(frame->width&&frame->height) skipped=1;
        bits+=*words++;
    }
    frame_count=frame-cached_frames;
    arena_cursor=cursor;
}
