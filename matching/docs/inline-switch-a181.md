# Complete C match for the A181 move generator

The pinned Microsoft C 5.00 compiler, `/AS /Zi`, emits all455 bytes of
the A181 function exactly, now canonically built from
`src/move_engine_9a50_full_match.c`. This includes441 bytes in REA's reachable
body, a12-byte six-entry switch table and a2-byte unreachable duplicate branch.
The independent CodeView procedure extent is455 bytes. The source contains
ordinary control flow, without assembly, byte macros or embedded original code.

REA's three inclusive ranges are A181..A324, A327..A336 and A343..A347.
The complete487-byte raw read also includes the next function at A348. Retained
evidence is `rea_moves_engine_a181.json`, `rea_moves_a181_raw.json` and
`rea_moves_a181_next.json`; `rea_moves_a181_match.json` records the initial
isolated compiler/linker investigation from the earlier standalone source. Canonical builds use the production
linker and boundary proof and record their fresh results in `build/report.json`.

The `inline_switch_table_v1` proof in `switch_extent.py` requires every omitted
byte to be explained. A325..A326 must be a short jump to A343, duplicating the
preceding retained jump, with no CFG block or successor entering that gap.
The dispatcher subtracts one, bounds the index at five, doubles it, exchanges
AX/BX and jumps through `CS:[BX+A337]`. The six table words must target retained
case-block starts, and their distinct targets must exactly equal the retained
dispatch CFG successors. No CFG block or successor may enter the table itself.
The shared epilogue and adjacent next entry are checked independently.

Fresh compiler OMF must supply seven actual own-CODE OFFSET16 fixups: one for
the dispatcher operand and six for the table. The restricted linker admits
these only for its known ungrouped, relocatable16-bit public CODE contribution,
with target or matching explicit SEGDEF frame. Both use the combined CS frame,
so each linked code offset is fragment placement plus emitted addend plus
explicit displacement. Other segments or frames fail. The arithmetic follows
the [TIS OMF1.1 SEGDEF and FIXUPP definitions](https://openwatcom.org/ftp/devel/docs/omf.pdf).

The proof additionally requires matching target identities and analysis
profiles, a complete raw read, an exact fresh CodeView extent, and equality of
every linked byte with both retained raw bytes and the pinned original. It
does not trim code, mask addresses, fill holes or accept arbitrary unreviewed
noncontiguous functions. Eight boundary tests attack table targets, bounds,
branches, profiles, compiler fixups, CFG exclusions and independent extents;
four new linker tests cover arithmetic and rejected segment/frame forms.
