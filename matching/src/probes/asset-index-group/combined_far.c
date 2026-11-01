typedef struct { unsigned long directory,pixels; } AssetLocation;
typedef struct { long value[4]; } DirectoryRecord;
/* Typed archive setup lengths records; byte spans are metadata, not payload. */
AssetLocation far setup_lengths_data[4] = {
 { 192L, 10097L },
 { 72L, 1427L },
 { 28L, 487L },
 { 28L, 471L }
};
/* Typed archive asset lengths records; byte spans are metadata, not payload. */
unsigned long far asset_lengths_data[31] = {
 5004L,
 1939L,
 6535L,
 2844L,
 3749L,
 7369L,
 5991L,
 4341L,
 3975L,
 3147L,
 3266L,
 2502L,
 3784L,
 3725L,
 7068L,
 1289L,
 363L,
 2779L,
 2429L,
 534L,
 3947L,
 1444L,
 1084L,
 625L,
 1242L,
 1737L,
 340L,
 1393L,
 1194L,
 2927L,
 2378L
};
/* Typed archive startup lengths records; byte spans are metadata, not payload. */
unsigned long far startup_lengths_data[13] = {
 6494L,
 4544L,
 32000L,
 11212L,
 640L,
 4547L,
 52L,
 7461L,
 2966L,
 3531L,
 3037L,
 2996L,
 2500L
};
/* Typed archive pair lengths records; byte spans are metadata, not payload. */
DirectoryRecord far pair_lengths_data[15] = {
 {{ 325L, 5570L, 527L, 12208L }},
 {{ 313L, 9613L, 507L, 13779L }},
 {{ 591L, 8347L, 674L, 21291L }},
 {{ 1015L, 29725L, 28L, 1402L }},
 {{ 683L, 20371L, 12L, 518L }},
 {{ 1162L, 25588L, 24L, 1081L }},
 {{ 966L, 25350L, 24L, 1322L }},
 {{ 1187L, 30050L, 24L, 1236L }},
 {{ 846L, 24635L, 8L, 297L }},
 {{ 368L, 12604L, 32L, 1805L }},
 {{ 986L, 21485L, 12L, 707L }},
 {{ 682L, 21674L, 20L, 1006L }},
 {{ 373L, 12740L, 16L, 846L }},
 {{ 231L, 4252L, 20L, 1183L }},
 {{ 668L, 16262L, 8L, 313L }}
};
/* Typed archive setup offsets records; byte spans are metadata, not payload. */
AssetLocation far setup_offsets_data[4] = {
 { 0L, 192L },
 { 10289L, 10361L },
 { 11788L, 11816L },
 { 12303L, 12331L }
};
/* Typed archive asset offsets records; byte spans are metadata, not payload. */
unsigned long far asset_offsets_data[31] = {
 12802L,
 17806L,
 19745L,
 26280L,
 29124L,
 32873L,
 40242L,
 46233L,
 50574L,
 54549L,
 57696L,
 60962L,
 63464L,
 67248L,
 70973L,
 78041L,
 79330L,
 79693L,
 82472L,
 84901L,
 85435L,
 89382L,
 90826L,
 91910L,
 92535L,
 93777L,
 95514L,
 95854L,
 97247L,
 98441L,
 101368L
};
/* Typed archive startup offsets records; byte spans are metadata, not payload. */
unsigned long far startup_offsets_data[13] = {
 103746L,
 110240L,
 114784L,
 146784L,
 157996L,
 158636L,
 163183L,
 163235L,
 170696L,
 173662L,
 177193L,
 180230L,
 183226L
};
/* Typed archive pair offsets records; byte spans are metadata, not payload. */
DirectoryRecord far pair_offsets_data[15] = {
 {{ 0L, 325L, 5895L, 6422L }},
 {{ 18630L, 18943L, 28556L, 29063L }},
 {{ 42842L, 43433L, 51780L, 52454L }},
 {{ 73745L, 74760L, 104485L, 104513L }},
 {{ 105915L, 106598L, 126969L, 126981L }},
 {{ 127499L, 128661L, 154249L, 154273L }},
 {{ 155354L, 156320L, 181670L, 181694L }},
 {{ 183016L, 184203L, 214253L, 214277L }},
 {{ 215513L, 216359L, 240994L, 241002L }},
 {{ 241299L, 241667L, 254271L, 254303L }},
 {{ 256108L, 257094L, 278579L, 278591L }},
 {{ 279298L, 279980L, 301654L, 301674L }},
 {{ 302680L, 303053L, 315793L, 315809L }},
 {{ 316655L, 316886L, 321138L, 321158L }},
 {{ 322341L, 323009L, 339271L, 339279L }}
};