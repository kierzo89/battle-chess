# Evaluator helper source-shape checkpoint

`src/evaluate_helpers_probe.c` reproduces the complete 51-byte
`evaluation_piece` procedure at image 109F9..10A2B, CS0FDF:0C09, with pinned
Microsoft C 5.00 `/AS /Gs /Zi`. Production checking verifies the complete
retained REA body, independent 51-byte CodeView3 extent, every linked byte,
and the exact empty original MZ relocation set.

The matching expression uses ordinary table address arithmetic:

```c
*(int *)((char *)piece_square+kind*240+side*1440+square*2)
    + piece_value[kind]
```

It describes the same table layout as the earlier flat int indexing. Making
the byte strides explicit reproduces the original multiplication and index
register order. No assembly, byte replacement, cropping, or shifted external
global alias is used.

The same alternate source independently rebuilds the complete evaluator's
538 bytes and abs helper's 26 bytes unchanged. Their exact original MZ sets
are respectively {10B45} and empty. These are regression controls, not new
registration proposals. `build/evaluator-helper-units.json` proposes only the
new 51-byte piece helper.

The pawn removal and movement helpers remain unresolved at this checkpoint:
105 versus 103 bytes and 132 versus 130 bytes. A genuine REA-derived
`pawn_score` definition makes their calls emit the original same-TU
PUSH CS/near CALL form. Both remaining bodies otherwise require an extra DI
save/restore because MSC500 selects DI for the subtraction temporary while
the original reuses SI. Equivalent address views, signed struct fields,
volatile access, flattened indices, and an explicit register temporary did
not produce complete equality. Some variants changed additional instructions;
none earn matching credit. The retained final candidate uses the canonical
PawnMask union and `pawn_state[history_index+1][side]`, with no shifted alias.

Fresh dependency evidence for `pawn_score` is retained in
`evidence/rea_evaluate_pawn_score.json`. Its faithful candidate is not itself
a byte match (128 versus 125 bytes). Supporting helpers are ordinary C
definitions, but neither they nor the full CODE contribution are claimed as
matching the original module layout. Complete source/layout reconstruction
is still needed to reconcile their current PUBDEF offsets with explicitly
bound original call destinations.

`evidence/evaluator_helpers_build.json` retains full production proof for the
piece helper and two regression controls, plus complete byte comparisons for
the final unmatched helper candidates. Canonical sources, registry, checker,
and parser files were not edited.

The exact piece expression is now migrated into `src/evaluate_candidate_match.c`
and registered as evaluation_piece_109f9 with its two actual table externals.
Fresh canonical production checks retain complete evaluator538/abs26 equality.
See `evidence/evaluator-piece-canonical-migration.json`. The canonical source
does not incorporate this alternate source's unfinished pawn_score changes.

Later work matches pawn_score125 and pawn_bit_count48; see pawn-score-match.md.
The canonical source now incorporates their genuine definitions and the parity
definition. The historical128-byte candidate and its two-byte caller differences
remain recorded here as bounded controls; no longer treat the pawn_score
dependency as unmatched. The two pawn mutation helpers remain unmatched.

The later scope control resolves both mutation functions: a lexical block
around mutation statements ends the compiler CSE temporary before the return
expression. All eleven procedures and their complete3,902-byte CODE contribution
now match `src/full_evaluation_match.c`; see full-evaluation-match.md. The current
proper score-grid base is DGROUPB0DC with kind-1 indexing; the AFEC expression
above describes only the retained historical probe.
