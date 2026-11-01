# Input commands and archive DATA checkpoint

Matching C totals **203 complete functions / 40,358 bytes**. Three new genuine
Microsoft C5.00 `/AS /Zi` functions add 721 bytes:

| Function | Bytes |
| --- | ---: |
| Menu choice, 2008 | 113 |
| Queue position command, 22C5 | 60 |
| Pump input, 2301 | 548 |

Together with the existing rectangle, board-action and bank-loader routines,
they form a complete **1,540-byte CODE contribution at 2008..260B**. All six
CodeView extents cover it without holes or tails. All 132 actual OMF fields,
16 original MZ sites and four load bases agree. Its word-aligned origin resolves
the previous odd rectangle/board and bank-loader placements. Existing 819 bytes
keep their previous credit. Historical translation-unit ownership remains unknown.

The keyboard caller now passes the actual near `MenuItem *` read through
`Menu.items`, replacing its opaque integer declaration. Its complete 1,170-byte
CODE contribution remains unchanged. The fixed board-action native-gap gate
accepts the freshly tested offset205 context while retaining every original
CFG, gap-byte, next-entry, compiler-extent and 39-fixup check. Adjacent unreviewed
placements are rejected. No padding locals, artificial helpers, masks, byte
patches, OMF edits or compiler-tail trimming are used.

## Separately counted assembly DATA

One authored NASM source supplies **896 initialized bytes and eight real
DGROUP publics** for archive offset/length tables. The tables describe complete
contiguous partitions of ALLCANM1 and ALLCANM2. The strict backend admits its
entire numeric-DD WORD PUBLIC _DATA/DGROUP allocation, with mandatory source
and assembler hash pins. It rejects includes, INCBIN, instructions, reservations,
preprocessing, other allocations, partial public slices, fixups and false frames.
An independent numeric model authenticates every emitted byte and public offset.

Real pinned LINK3.65 plus a C far-extern caller resolves all eight BASE16 words
to DGROUP. These subset links preserve actual EXE words, MAPs, MZ sites and four
loader-base controls. They do not prove a complete game link. Genuine far C
controls retain paragraph alignment/group0 and cannot silently replace this
source. Assembly DATA receives **zero C, function or packed-file credit**.

## Verification and remaining work

All **362 registered units** pass the fresh checker. All **488 unique tests pass across two runs**: 475 in the main run and all13
emulation cases in the pinned Python/Unicorn environment (701.368
seconds combined). The main run skipped those13 because Unicorn was absent;
no test remains unexecuted. All271 frozen inputs remain unchanged. The
[per-test coverage record](../evidence/regression-203-coverage.json) identifies
every outcome and both logs. The `--require-complete` command still exits1 because no independently
source-built complete executable exists. The
[immutable verification record](../evidence/verification-203-input-archive-checkpoint.json)
retains sources, primary REA evidence, compiler/assembler identities, objects,
controls, logs and inventories. All 2,893 earlier archived paths remain intact.

C DATA remains 98 contributions / 1,436 bytes; assembly CODE remains 11 functions /
994 bytes; runtime remains 49 units / 4,240 bytes. Verified original-file spans
cover **45,422 / 83,415 bytes (54.453%)**;
expanded spans cover 47,924 / 401,131 bytes. Relocation
coverage is **101 / 173 sites**, comprising 99 source and two runtime. These
coverage figures are not a whole-program completion percentage.

The fresh C layout audit has 59 objects,
31 legal complete CODE/MZ contexts,
16 objects needing enclosing
alignment and 15 unequal whole CODE
spans. The dependency inventory retains actual missing names, six known byte
collisions, uncredited emitted procedures and unresolved storage ownership.
Private BSS earns zero byte credit. Exact historical compiler flags and global
allocation order remain unproved. Continue recovering real definitions and
natural source boundaries, link the full image/header/all173 relocations, then
EXEPACK the independent image and require final byte/hash identity.
