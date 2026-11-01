# Far data fields and absolute compiler ABI words

Ordinary C5.00 huge-pointer code in the graphics routines emits separate
OFFSET16 and BASE16 fields for a symbolic far buffer. The restricted linker now
accepts both only against an explicit `{offset, segment}` placement. OFFSET16
selects the offset and applies its emitted addend/displacement; BASE16 selects
the segment and applies its emitted word addend. BASE16 currently requires a
segment-relative external target, frame=target and zero target displacement.
Other frames and targets fail. Every BASE16 field emits its actual MZ site;
an ordinary offset field does not. Existing FAR16 pointer handling remains.

Absolute compiler ABI symbols use a distinct `{absolute: value}` placement.
They are accepted only as ordinary segment-relative OFFSET16 references and
never create loader sites. The independently pinned SLIBC DIFFHLP member defines
`__AHSHIFT` as absolute12 and `__AHINCR` as absolute4096 in PUBDEF segment0/group0.
Its whole library/member hashes, exact unchanged bytes and public records are
retained in `evidence/huge_pointer_abi_diffhlp.json`. This supplies independent
ABI evidence for the compiler-generated huge-pointer shift reference.

`evidence/authentic_link_far_data.json` corroborates the lowering with fresh
C5.00 output and pinned Microsoft LINK3.65. Its actual far buffer is mapped at
segment4, offset0; LINK resolves the two separate code fields accordingly and
places only the BASE16 field in the MZ table. The huge-pointer shift uses the
archived absolute12 without a loader relocation. These diagnostic placements
are independent of Battle Chess and do not receive matching credit.

The graphics production builds use the same relocation forms at their explicit
original placements. The region helper matches248 bytes and two loader sites;
the renderer matches725 bytes and seven sites. Complete fresh byte comparisons
and original EXEPACK-site checks are retained in `mark_region_41a8_build.json`
and `render_42a0_build.json`. Both sources use symbolic buffers rather than
literal segment-word emission.

The checker now requires exact equality between emitted and original loader
site sets for every complete matched C or runtime extent. A missing site fails
even if the unrelocated bytes happen to match. Extra sites and loader words
crossing an extent boundary also fail. This does not mask loader-dependent
bytes or normalize far aliases. Three new linker tests cover separate fields,
absolute values and rejected forms; three site-coverage tests exercise omitted,
extra, crossing and non-loader fields.
