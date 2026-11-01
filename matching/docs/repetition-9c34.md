# Exact 383-byte repetition detector and a proved dead-return gap

[repetition_match.c](../src/repetition_match.c), compiled by pinned MSC5.00
`/AS /Zi`, generates every byte of the original image span `9C34..9DB2`,
including a five-byte unreachable return left after its infinite loop.
The fresh CodeView3 procedure length independently reports383 bytes.
[Complete build evidence](../evidence/repetition_9c34_build.json) retains
source/object/tool hashes, normal relocation arithmetic, all generated and
expected bytes, and the extended boundary proof. There is no byte patch,
assembly substitution, expected-size truncation or source-byte emission.

The routine scans eight-byte move-history records and follows linked source
and destination squares to count repetition boundaries. It calls the quiet-move
predicate9BBC and low-bit helperA514. Bitwise boolean expressions preserve
both evaluated conditions; the explicit final `return a` remains unreachable
in the C source but is nevertheless emitted by this compiler. Lettered local
names produce the original stack-slot order; comments state their roles.
The `pairs` array begins at DS:88E4, and `&pairs[i]-1` supplies the preceding
record to the predicate at DS:88DC plus8*i. No overlapping object declarations
are required.

## Boundary evidence

The [REA function dossier](../evidence/rea_repetition_9c34.json) establishes
378 reachable instruction bytes in two inclusive ranges: `19C34..19DA8` and
`19DAE..19DB2`. It correctly omits the five unreachable bytes at
`19DA9..19DAD`; this is not a contiguous378-byte function.

The separate [complete raw query](../evidence/rea_repetition_9c34_fullspan.json)
reads399 bytes from19C34, covering the entire383-byte compiler span and the
following prologue. The gap bytes are exactly `8B 46 FE EB 00`, meaning
`MOV AX,[BP-2]; JMP +0`, which reaches the shared epilogue at19DAE. Immediately
before the gap, `E9 FB FE` unconditionally jumps backward to19CA4. The retained
CFG corroborates that edge and has no block or successor entering the gap.
The [next-function dossier](../evidence/rea_repetition_next_9db3.json) places
the next entry exactly at19DB3, with its own complete body and BP prologue.

## Scoped checker support

[extent.py](../extent.py) validates only an explicit
`unreachable_return_gap_v1` proof. The unit must carry the function dossier,
complete raw-span evidence and adjacent next-entry evidence. Validation checks
matching target and analysis profiles, exactly two function-body ranges with
one five-byte gap, the precise nonmutating return instruction sequence, the
preceding backward jump and CFG edges, exact adjacency of the next function,
and a fresh CodeView3 extent covering the whole span. It compares all linked
bytes to the retained raw span. Ordinary full pinned-image comparison remains
required by the caller.

Missing proofs, partial raw reads, mismatched bytes, incoming gap CFG edges,
unproved next entries and inferred compiler extents fail. The original
contiguous-body policy is not changed by this helper. Nine focused tests in
[test_extent.py](../tests/test_extent.py) passed. The registration proposal is
`build/repetition-units.json`; canonical integration belongs to the main worker.
