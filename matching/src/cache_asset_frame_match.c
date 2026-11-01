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
