# Exact C fill and packed-pixel helpers

Three adjacent helpers now match ordinary C compiled with pinned MSC5.00
`/AS /Zi`, adding201 authored C bytes. Each has fresh complete contiguous REA
body evidence, a matching independent CodeView3 procedure extent and a full
production `check.build_unit` result of `c_matched`.

| Entry | Bytes | Source | Full production proof |
|---|---:|---|---|
|5A4F|45|[fill_far_match.c](../src/fill_far_match.c)|[fill proof](../evidence/fill_far_5a4f_build.json)|
|5A7C|132|[plot_region_match.c](../src/plot_region_match.c)|[pixel proof](../evidence/plot_region_5a7c_build.json)|
|5B00|24|[select_pattern_match.c](../src/select_pattern_match.c)|[selector proof](../evidence/select_pattern_5b00_build.json)|

5A4F is a normal C loop over a huge character pointer. Its postincrement carries
an offset wrap into the segment using the actual compiler absolute symbol
`__AHINCR=4096`, independently defined by the pinned runtime DIFFHLP member.
It emits no MZ relocation sites. The count decrement and checked zero-sized
frame match in full; this is not an assembly-only API.

5A7C computes `y*stride+x/2`, returns if the resulting signed offset exceeds
3248, chooses the high/low nibble mask and replaces that nibble in the symbolic
huge region buffer. It preserves the original behavior, including the absence
of a negative-offset guard. Its BASE16 fields at image5AC4 and5AF2 exactly
match both original loader relocation sites in that complete extent. The
`__AHSHIFT=12` use is absolute and is not a loader relocation.

5B00 selects a global word from an indexed word table. The user-facing meaning
of the pattern table remains inferred. The sources contain no byte emission,
inline assembly, masking, patches or target-size truncation.

The fresh neighbor [5B18 dossier](../evidence/rea_fill_neighbor_5b18.json)
establishes a37-byte routine which writes a color nibble through ES:000C,
loading ES directly from DS:4D94. That segment-only access has the same
unexplained source/compiler fingerprint as the pending7C99 helper. No C match
or assembly classification is claimed for5B18, and prior negative pointer
expression experiments were not repeated.

All three units are now registered in the canonical byte checker. The original
combined proposal remains at `build/fill-next-units.json`. No parser relaxation
was required for these sources.
