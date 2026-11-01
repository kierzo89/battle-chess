# Far move evaluator at image 10B15

`src/evaluate_candidate_match.c` compiled with pinned Microsoft C 5.00
`/AS /Gs /Zi` reproduces the complete 538-byte evaluator, including its RETF.
The independently emitted CodeView3 procedure extent is exactly 538 bytes.
Retained original REA evidence is `evidence/rea_moves_af87_far_callee.json`,
covering loaded addresses 20B15..20D2E without holes. The production checker
verifies every linked byte and the exact original MZ relocation set {10B45}.

Address arithmetic is explicit: original CS paragraph 0FDF has image base FDF0;
0FDF:0D25 therefore maps to image 10B15 and, under REA's load bias 10000,
loaded address 20B15. `code_address` records this mapping. The linker receives
CS offset 0D25 and `image_origin=10B15`; near call arithmetic stays within CS,
while loader relocation positions use image offsets. No 16-bit truncation of
the linear image address is used. Near helper offsets are 0002 (far abs),
0C09 (piece value), 0C3C (pawn removal), and 0CA3 (pawn movement). The separate
far call to `castle_95df` has explicit placement 0000:95DF.

The evaluator updates the incremental score, copies both sides' pawn masks,
and accounts for promotion, castling, captures, and pawn movement. Its five
ordinary int locals retain the observed ten-byte frame; one local's purpose
is unknown and it is unused. The source's helper definitions are faithful
ordinary C reconstructions from separately retained REA assembly, not stub
bodies. Their presence makes MSC500 emit genuine same-TU PUSH CS/near CALL
lowering. The evaluator's complete byte match does not establish the original
source names.

The abs helper independently matches all 26 bytes at image FDF2..FE0B,
CS0FDF:0002, with complete fresh REA and CodeView extents and an exact empty
MZ relocation set. Its separate proof is `evidence/evaluation_abs_build.json`.

This is a pair of complete-function matches, not a complete object/module
layout match. The object emits the helper names as both EXTDEF and PUBDEF;
the evaluator's near-call fixups target the EXTDEF records. Its fragment linker
uses the declared original placements. Those placements differ from the
helper public locations if the entire current CODE contribution is placed
at the evaluator's original location. The piece helper now also matches all51 bytes after making ordinary byte strides
explicit in its table address expression. The two pawn helper bodies have not
been credited as byte matches; intervening original functions are omitted.
An eventual full source contribution and authentic LINK layout must resolve
these differences. `evidence/evaluate_candidate_build.json` records every
same-TU call fixup, public offset, current whole-contribution-derived CS offset,
and declared original CS offset explicitly.

The registration proposal is `build/evaluate-candidate-units.json`. Both proof
files retain complete linked and expected bytes plus source/object/compiler
hashes and relocation records. Both complete procedures are now registered using the canonical match source.
The original worker probe source is retained separately. Authentic LINK validates
the CS/image coordinate implementation in [nonzero-cs-linking.md](nonzero-cs-linking.md).
The [small/medium model control](evaluator-memory-model-control.md) preserves
these bytes under both profiles; the complete original link remains unresolved.

The separate low-bit helper at imageFE4A, CS0FDF:005A, also matches its complete
15-byte far procedure from `src/evaluation_parity_match.c`. Fresh CV3 length,
contiguous REA extent and the exact empty MZ set agree; reproduce with
`evidence/evaluation-parity-probe.py`. Its source is ordinary unsigned `value & 1`.
The two bytes at the evaluator CS frame base FDF0 are CB90, a retained raw
observation in `rea_evaluation_segment_prefix.json`. A CS frame base does not
by itself prove where an original compiler contribution began; those two bytes
receive no new credit.

The canonical piece-expression migration preserves the evaluator538 and abs26
bytes in fresh production checks; `evidence/evaluator-piece-canonical-migration.json`
retains all three full comparisons. The later pawn-score migration adds its exact125-byte definition, the exact
48-byte bit counter and the existing15-byte parity definition into this same
canonical source. All six matched procedures retain complete equality in
`evidence/pawn-score-canonical-migration.json`; see pawn-score-match.md. No whole-object layout
match is inferred from either source.
