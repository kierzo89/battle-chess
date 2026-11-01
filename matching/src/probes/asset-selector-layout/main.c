/* Target-free synthetic ownership/CRT diagnostic; zero game byte credit. */
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
extern void setup_assets(void);
int main(void)
{
 if(setup_offsets || setup_lengths || asset_offsets || asset_lengths ||
    startup_offsets_9648 || startup_lengths_a8b6 || pair_offsets || pair_directory_lengths)return 1;
 setup_assets();
 if(setup_offsets!=setup_offsets_data || setup_lengths!=setup_lengths_data)return 2;
 if(asset_offsets!=asset_offsets_data || asset_lengths!=asset_lengths_data)return 3;
 if(startup_offsets_9648!=startup_offsets_data || startup_lengths_a8b6!=startup_lengths_data)return 4;
 if(pair_offsets!=pair_offsets_data || pair_directory_lengths!=pair_lengths_data)return 5;
 if(setup_lengths[3].pixels!=471L || asset_lengths[30]!=2378L)return 6;
 if(startup_lengths_a8b6[12]!=2500L || pair_directory_lengths[14].value[3]!=313L)return 7;
 return 0;
}
