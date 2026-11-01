/* Genuine observed setup function; diagnostic linked consumer, no new credit. */
typedef struct { unsigned long directory,pixels; } AssetLocation;
typedef struct { long value[4]; } DirectoryRecord;
extern AssetLocation far *setup_offsets,far *setup_lengths;
extern unsigned long far *asset_offsets,far *asset_lengths;
extern unsigned long far *startup_offsets_9648,far *startup_lengths_a8b6;
extern DirectoryRecord far *pair_offsets,far *pair_directory_lengths;
extern AssetLocation far setup_offsets_data[],far setup_lengths_data[];
extern unsigned long far asset_offsets_data[],far asset_lengths_data[];
extern unsigned long far startup_offsets_data[],far startup_lengths_data[];
extern DirectoryRecord far pair_offsets_data[],far pair_lengths_data[];
void setup_assets(void)
{
 setup_offsets=setup_offsets_data;
 asset_offsets=asset_offsets_data;
 startup_offsets_9648=startup_offsets_data;
 pair_offsets=pair_offsets_data;
 setup_lengths=setup_lengths_data;
 asset_lengths=asset_lengths_data;
 startup_lengths_a8b6=startup_lengths_data;
 pair_directory_lengths=pair_lengths_data;
}
