# Pawn mutation register-lifetime controls

This checkpoint tests five concrete variations of the current canonical
ordinary C source, with no canonical edits:

1. Medium model `/AM /Gs /Zi` instead of `/AS /Gs /Zi`.
2. K&R definitions for the two mutation helpers.
3. Signed `int pawn_mask`, retaining the unsigned file-mask array.
4. Commuted operands in the combined OR expressions.
5. Neutral parameter and local names within the two mutation functions.

All five variants emit identical procedure bytes for all eight checked
functions. The six existing complete matches remain exact: abs 26, parity 15,
bit count 48, pawn score 125, piece evaluator 51, and evaluator 538. The two
mutation functions remain 105/132 bytes versus the original 103/130.
None of these hypotheses resolves the extra DI save/restore and subtraction
temporary selection. Exact dependency definitions therefore do not suffice,
and model selection, declaration style, tested signedness, operand order, and
neutral names are bounded negatives for these bodies.

`evidence/pawn_mutation_variants.json` retains every full alternate source,
source/object/compiler hashes, compiler commands and logs, complete CodeView
metadata, linked/expected byte strings, difference positions, and relocation
records. Its source snapshots are retained inline so the ignored build scratch
directory is not required to recover the experiments. Both scripts are under
`build/pawn-mutation/`; the canonical source SHA is retained in the evidence.
No byte patch, assembly, trimming, shifted external alias, or matching credit
was introduced. Full source contribution/layout reconstruction remains open.

These are historical bounded negatives. A later lexical block around only the
mutation statements releases C5 synthesized address temporaries before the
score subtraction, and both functions now match completely. A block around
only the return remains a verified negative. See full-evaluation-match.md and
evaluation-scope-independent-audit.md.
