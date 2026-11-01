# Huffman inputs and natural C contexts checkpoint

Matching C now totals **206 complete functions / 41,008 bytes**. The new input
reset contributes a complete 42-byte native/CV/source allocation with three
actual fields. Its two command words are meaningful source data; the reset flag
remains an explicit external byte. A real one-byte RET entry adds the other C
function. Its natural 34-byte source context includes the already credited
33-byte exit prompt. Those existing 33 bytes are not credited again.

Initialized C DATA now totals **102 contributions / 1,983 bytes**. The previous
nine-byte Huff mask contribution is replaced by a complete typed 20-byte context
with masks, scalar state and a far memory cursor, adding eleven bytes. A separate
source-declared 512-byte transfer-window definition supplies the initialized
Huff input buffer. Native reads establish the consumed minimum; the historical
array capacity and translation-unit partition remain unknown.

The 512-byte object remains unchanged. Its first byte uses actual LEDATA and the
remaining 511 bytes use the actual compiler LIDATA leaf. A separately pinned,
narrow backend verifies its complete SEGDEF, PUBLIC/CV array shape, raw record
sequence and exact repeat profile. The ordinary OMF reader retains unsupported
LIDATA, and the ordinary C DATA validator is not relaxed. No bytes are fabricated
to fill storage holes, and no initialized output is sliced.

## Multi-entry assembly allocation

The Huff refill/trap contribution adds **one complete 95-byte CODE allocation**
and one original MZ site. The actual PUBLIC offsets are 0 and 38. Refill owns
94 live bytes in disjoint ranges [0,38) and [39,95); the one-byte INT3 entry at
38 resumes at the shared code at 39. PUBLIC offsets do not define two function
partitions. The source, complete ten-field OMF profile, native ranges, raw95,
MZ arithmetic and actual two-order LINK controls are checked independently.

Assembly function credit remains **11 functions / 994 bytes**. The separate
95-byte CODE allocation receives zero C or assembly-function credit. The actual
inventory contains 3 relocatable CODE objects with
13 PUBLIC labels / 1089 total CODE bytes,
including the separately counted allocation. The 896-byte assembly DATA object
and 4,240 runtime bytes remain unchanged.

## Verified results and limits

All 370 units match. **All 658 tests pass in one run with zero
skips**, in 821.314 seconds, with 844 unchanged inputs.
The prior nine checkpoints retain all 7,154 archived paths and all 27 versioned
source-link files. The first regression attempt was stopped after the interface
audit found an unjustified `exit_07f3(int)` declaration. It earns no PASS credit.
The corrected caller retains an unspecified argument list, matching existing
source declarations, and preserves the actual extra zero push. The callee reads
no argument; the original historical prototype remains unknown. A fresh complete
34-byte compiler/native control verifies the correction. Original-file spans cover 46,167/83,415
(55.346%); expanded spans cover
49,216/401,131. These coordinate systems are reported
separately. MZ verification is 110/173 (107 C source / 1 assembly CODE / 2 runtime).
No whole-program completion percentage is claimed.

The actual interface audit covers 161 C source paths,
with no duplicate provided globals, actionable provided-definition type conflicts
or unread local declarations. The CODE layout audit records
32 verified contexts,
16 enclosing-alignment cases,
15 unequal whole CODE spans and
7 concrete byte collisions. These unresolved
constraints still prevent a complete original image layout.

An authentic aggregate LINK consumes 165 actual source
objects plus SLIBC and LIBH. It fails with linker L2029 and **359 undefined
names**. No stubs, target bytes, synthetic PUBLIC aliases or edited objects enter
LINK; the failed partial executable remains unexecuted. Actual dependencies are:

- actual assembly DATA definition: 8
- actual matched source definition: 227
- actual relocatable assembly CODE definition: 6
- actual source COMMON allocation: 8
- available pinned runtime library: 27
- emitted uncredited source definition: 4
- missing actual source definition: 359

See the [dependency findings](../evidence/source-link-dependency-findings-206-huff-input.md),
[actual LINK proof](../evidence/source-link-attempt-206-huff-input-final.json),
[interface audit](../evidence/c206-huff-input-source-interface-audit.json) and
[immutable checkpoint](../evidence/verification-206-huff-input-checkpoint.json).
The earlier [204 checkpoint](source-link-closure-204-checkpoint.md) remains immutable.

A full independently source-built executable is still absent. Recover real
missing providers and storage, resolve every enclosing context and final MAP
allocation, reproduce the original header and all 173 relocations, then apply
genuine EXEPACK to that independent image and require every final file byte and
SHA256. Exact historical compiler commands and source partitions remain nonunique.
