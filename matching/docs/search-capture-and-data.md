# Search continuation and authored DATA

Five further ordinary C functions match with Microsoft C 5.00 `/AS /Zi`:

| Entry | Complete bytes | Reconstructed role |
|---|---:|---|
| AF87 | 807 | Prepare a candidate, evaluate it and establish child-search state |
| B2AE | 213 | Detect draw/pruning conditions and adjust child bounds |
| B383 | 99 | Copy a principal variation and update the root result |
| B3E6 | 100 | Try the four promotion piece kinds |
| B44A | 416 | Try pawn and non-pawn captures onto a destination |

All now use [search_engine_a528_b5ea_full_match.c](../src/search_engine_a528_b5ea_full_match.c).
Together with ten previously matched neighbors, its fifteen independent
compiler procedure extents cover the entire 4,290-byte CODE contribution
A528..B5E9. Every one of its 404 fixups belongs to those extents exactly once.
The [full proof](../evidence/search-engine-a528-b5ea-full.json) verifies an
independent relocation pass over the raw complete segment, all original MZ
sites A536/A55F/A683/B0DB and exact bytes under four load bases. There are no
holes, alignment placeholders, patches or duplicate matching credit.

The standalone AF87 object had one extra alignment byte outside its complete
807-byte compiler procedure. Consolidation removes that standalone boundary
problem through real adjacent source. This establishes a compatible complete
contribution, without claiming the historical translation-unit partition.

AF87 calls a far evaluator using the original pointer alias `0FDF:0D25`.
The raw call at B0D8 is `9A 25 0D DF 0F`; its segment field B0DB is an original
MZ relocation site. Fresh REA analysis of the real loaded callee at 20B15
establishes a complete 538-byte routine ending in RETF at 20D2E. The source
passes an eight-byte Move by value and receives an integer score; there is no
extra segment argument. See [callee evidence](../evidence/rea_moves_af87_far_callee.json).

B44A shares the existing history-storage view at 85A4 with a 104-move bias,
and distinguishes the piece-count array at B0A6 from the side counts at 8DCE.
Signed conditions and bitwise boolean evaluation reproduce the original
expression order. The meaningful local names reproduce compiler stack-slot
allocation; they are analyst choices, not recovered identifiers. The complete
standalone [production proof](../evidence/capture_search_b44a_build.json) and
bounded name experiments remain retained.

The first authored game DATA contribution is independently described in
[game-move-lookup-data.md](game-move-lookup-data.md): 80 typed bytes of movement,
piece masks, castling and initial-rank tables. The canonical checker uses a
separate `c-data` category and `c_data_matched` status, with zero function
credit. Its full DATA allocation must be independently emitted at public
offset zero in DGROUP, with no other nondebug allocations, holes, reserved
tail, fixups, communal or iterated data. Only the unused compiler startup
marker is admitted. Existing function extraction rules are unchanged.

Fresh source compilation, source-race checks, compiler/tool pins, complete
DATA extent and all-byte REA/reference comparisons precede data credit. The
80 bytes lie in the compressed region, so they contribute only to expanded
image coverage. The full source-built executable remains unavailable.

The canonical search source now extends further back through advanceA4D4 and
lowbitA514: twenty procedures form the entire5,350-byte CODE contribution
A4D4..B9B9. All503 fixups, four MZ sites and exact complete source bytes pass
a fresh independent relocation and production proof. The canonical source is
`src/search_engine_a4d4_b9ba_match.c`; earlier sources/proofs above remain
historical. See source-contribution-layout.md.
