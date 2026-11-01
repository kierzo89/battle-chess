/* Diagnostic archive metadata reads only; zero game implementation credit. */
typedef struct { unsigned long directory,pixels; } AssetLocation;
typedef struct { long value[4]; } DirectoryRecord;
extern AssetLocation far setup_offsets_data[],far setup_lengths_data[];
extern unsigned long far asset_offsets_data[],far asset_lengths_data[];
extern unsigned long far startup_offsets_data[],far startup_lengths_data[];
extern DirectoryRecord far pair_offsets_data[],far pair_lengths_data[];
int main(void)
{
 if(setup_offsets_data[3].pixels!=12331L)return 1;
 if(setup_lengths_data[3].pixels!=471L)return 2;
 if(asset_offsets_data[30]!=101368L)return 3;
 if(asset_lengths_data[30]!=2378L)return 4;
 if(startup_offsets_data[12]!=183226L)return 5;
 if(startup_lengths_data[12]!=2500L)return 6;
 if(pair_offsets_data[14].value[3]!=339279L)return 7;
 if(pair_lengths_data[14].value[3]!=313L)return 8;
 return 0;
}
