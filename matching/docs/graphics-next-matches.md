# Exact C dirty-region and renderer matches

Pinned MSC5.00 `/AS /Zi` now reproduces the complete248-byte mark-region helper
at41A8 and the complete725-byte actor renderer at42A0, adding973 authored C
bytes. Both have fresh complete contiguous REA dossiers and independent
CodeView3 procedure extents. Final sources were rebuilt through the production
`check.build_unit` path; both report `c_matched`. The full original MZ
relocation set within each extent also matches exactly.

| Entry | Source | Full fresh production proof | MZ sites |
|---|---|---|---:|
|41A8|[mark_region_match.c](../src/mark_region_match.c)|[248-byte proof](../evidence/mark_region_41a8_build.json)|2|
|42A0|[render_match.c](../src/render_match.c)|[725-byte proof](../evidence/render_42a0_build.json)|7|

The retained proofs contain complete generated/expected bytes, source/object/
tool hashes, compiler commands, normal relocation arithmetic and exact original
loader-site lists. There is no byte patching, source-byte emission, inline
assembly, output masking or expected-size truncation.

41A8 expands the dirty rectangle to pixels, derives its word stride and height,
checks the3248-byte buffer bound, configures source/destination/masks and either
copies the screen background or clears the temporary region buffer.42A0 walks
the actor chain, clips intersecting actors to that rectangle, sets edge masks
and source/destination offsets, composites each frame and presents the region
through the original far graphics calls or the alternate near-copy path.
These are static behavior inferences, not runtime observations.

## Far data and historical compiler ABI

The temporary buffer is a symbolic huge object placed at120D:3F90. Its separate
OFFSET16 and BASE16 fixups are linked using explicit offset/segment placement.
Each BASE16 field is emitted as an MZ loader relocation.41A8's sites are425D
and4291.42A0's seven sites are44B0,44E8,4524,452A,4543,454B and4553. The three
far graphics aliases remain exactly11EF:001E,110D:0000 and11EF:0000; equivalent
linear aliases are not substituted.

Huge pointer arithmetic uses the compiler external `__AHSHIFT`. The actual
pinned C5 runtime's72-byte DIFFHLP member defines that symbol as an absolute
PUBDEF with segment0 and value12. [Complete independent member evidence](../evidence/huge_pointer_abi_diffhlp.json)
retains its bytes and library/member hashes. It is passed as `{"absolute":12}`,
and earns no loader relocation.

A [fresh authentic LINK experiment](../evidence/authentic_link_far_data.json)
independently corroborates the split relocation semantics: a compiler-generated
far array address links to the FAR_DATA symbol's offset/segment, and only its
BASE16 segment immediate enters the MZ relocation table. The same experiment
links huge arithmetic with DIFFHLP's absolute shift value. The generated probe
was linked for inspection and was not executed.

## Source layout details and limits

The C5 `huge` distance qualifier must be repeated for each pointer declarator;
separate source/destination declarations reproduce both four-byte fields. In
the renderer, ordinary local declaration order within colliding compiler symbol
buckets reproduces the original stack slots. The source names are reconstruction
choices. Five unread ordinary frame words remain explicitly declared; their
historical purpose is unknown. Register locals account for two further reserved
frame words. The source's unsigned word cast preserves the original order of
subtracting one before adding a row offset.

The two canonical proposals are combined in `build/graphics-next-units.json`,
with separate `build/mark-region-units.json` and `build/render-units.json` also
available. Registry/checker were not changed by this worker; production far-data
linker support was implemented independently by the main worker.
