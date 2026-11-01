# One typed legal_move interface

The canonical engine now uses `src/move_engine_9a50_tables_match.c`; its
bytes are identical to the retained alternate source below. The canonical
search source is `src/search_engine_a528_b9ba_full_match.c`, with all eighteen
procedures and the same typed aggregate legality interface verified in the
complete5,266-byte contribution.

The ordinary C interface `int legal_move(Move)` is compatible with every tested
caller and the complete original legality implementation. The alternate engine
source is `src/move_engine_9a50_aggregate_probe.c`. Its definition accepts one
Move parameter and accesses its fields; its internal calls pass `candidate_move`
by value. There are no unspecified prototypes or casts between incompatible
function types.

The Move type is the shared eight-byte layout: three ints `to`, `from`, `flag`,
then a MoveKind union containing unsigned `word` and the two-byte struct
`bytes.kind`, `bytes.capture`. The alternate engine removes its redundant
`byte.lo`/`byte.hi` union view and uses these same member names as the search
translation unit, so the complete struct and union types agree across units.

Pinned Microsoft C 5.00 with `/AS /Zi` emits an exact 2692-byte CODE SEGDEF for
the alternate engine, covering 9A50..A4D3. All twelve independent CodeView3
procedure extents match the original complete bytes, including legal_move's
556 bytes. Their extents cover the complete segment without gaps. Every
retained REA extent and original MZ relocation-site set was validated.

As a positive caller control, the same prototype and aggregate history-record
call leave A943 unchanged at 533 bytes. An additional already-running control
built `src/search_engine_a528_b5ea_aggregate_probe.c`: all fifteen procedures,
covering its complete 4290-byte CODE SEGDEF, remain exact, with independent
CodeView extents, retained REA boundaries, and complete MZ sets verified. The
earlier `evidence/search_special_helpers_build.json` independently verifies the
same aggregate interface at B860 and B8F4 (148 and 198 bytes).

This demonstrates a single compatible C interface, beyond merely equivalent
eight-byte machine argument layouts. Four separately declared arguments produce
the same machine interface but cause the B8F4 call to push a local stack slot
instead of AX, adding two bytes. The aggregate declaration and actual Move
expression reproduce all tested outputs with consistent C types.

Full byte strings, compiler pins, source/object hashes, complete segment
coverage, procedure metadata, and fixups are retained in
`evidence/legal_move_aggregate_probe.json`. The twelve-unit engine migration
proposal is `build/legal-move-engine-units.json`. These engine units and the
consolidated search callers are now registered in the canonical checker.
