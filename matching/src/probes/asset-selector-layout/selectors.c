/* Pointer objects live near in DGROUP; each points to a far archive table. */
typedef struct { unsigned long directory, pixels; } AssetLocation;
typedef struct { long value[4]; } DirectoryRecord;
AssetLocation far *setup_offsets, far *setup_lengths;
unsigned long far *asset_offsets, far *asset_lengths;
unsigned long far *startup_offsets_9648, far *startup_lengths_a8b6;
DirectoryRecord far *pair_offsets, far *pair_directory_lengths;
