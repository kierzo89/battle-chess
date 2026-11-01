/* Typed archive setup lengths records; byte spans are metadata, not payload. */
typedef struct { unsigned long directory,pixels; } AssetLocation;
AssetLocation setup_lengths_data[4] = {
 { 192L, 10097L },
 { 72L, 1427L },
 { 28L, 487L },
 { 28L, 471L }
};
