/* Typed archive pair lengths records; byte spans are metadata, not payload. */
typedef struct { long value[4]; } DirectoryRecord;
DirectoryRecord pair_lengths_data[15] = {
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
