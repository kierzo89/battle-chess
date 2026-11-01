# Pawn score and bit count

`src/pawn_score_match.c` compiled with pinned Microsoft C 5.00 `/AS /Gs /Zi`
reproduces two additional complete far procedures:

| Procedure | Image extent | CS0FDF offset | Bytes |
| --- | --- | --- | ---: |
| `pawn_bit_count` | 1094C..1097B | 0B5C | 48 |
| `pawn_score` | 1097C..109F8 | 0B8C | 125 |

Both have independent complete CodeView3 extents, retained contiguous REA
bodies, complete relocation-resolved byte equality, and exact empty original
MZ relocation-site sets. Production builds independently confirm the existing
piece evaluator (51 bytes), main evaluator (538), and abs (26) remain exact.

`pawn_score` identifies isolated pawn files and combines three bit counts with
weights eight, twenty, and forty, then negates the sum. Using an explicit
register local for the mask in the previous candidate reserved an extra stack
slot. The matching source uses the repeated signed field expression; MSC500
holds the common value in SI itself. Ordinary local declarations put the
pointer at BP-2, result at BP-4, and isolated mask at BP-6, with the compiler's
temporary at BP-8, matching the complete original eight-byte frame.

The bit-count helper calls the genuine same-TU parity definition and shifts
its signed argument until zero. Its count lives at BP-4; an unused first local
retains the original four-byte frame. That unused slot's source-level purpose
is unknown. The parity definition agrees with the independently matched
existing helper and earns no duplicate credit here. No implementation uses
assembly, emitted-byte macros, postpatching, or function trimming.

The pawn removal and movement candidates still emit 105 and 132 bytes versus
103 and 130. Replacing the dependency with exact `pawn_score` did not change
their DI temporary/save-restore difference. Two further bounded controls used
an unsigned-array representation and comma sequencing; neither resolved that
difference. The released source restores the canonical PawnMask union and
straightforward separate statements. These functions remain uncredited.

`evidence/pawn_score_build.json` contains full production proof and regression
bytes, source/object/tool hashes, exact loader sites, and final unmatched
helper comparisons. Supporting REA evidence is
`evidence/rea_evaluate_pawn_score.json` and
`evidence/rea_evaluate_pawn_bit_count.json`. The two-unit proposal is
`build/pawn-score-units.json`.

The combined object is still a partial contribution with explicitly bound
original call destinations. Full original module layout is not established;
the uncredited pawn helpers and omitted intervening procedures remain. No
canonical source, registry, checker, or parser was edited.

The six matched evaluator procedures now share the canonical source
`src/evaluate_candidate_match.c`; this also migrates the existing parity unit
away from its standalone source, avoiding a second canonical parity definition.
The worker source remains retained as `src/pawn_score_match.c`. Fresh migration
proof `evidence/pawn-score-canonical-migration.json` checks evaluator538, abs26,
parity15, piece51, pawn_score125 and pawn_bit_count48 with exact original MZ
sets. Original full module layout remains unresolved.

The current canonical consumer now declares the proper `piece_square[2][6][120]`
grid at DGROUP B0DC, with kind-minus-one indexing. The earlier AFEC flat view
is retained only in historical probes. Fresh seven-unit production equality
is recorded in `evidence/full-evaluation-production-match.json`; see
[full-evaluation-match.md](full-evaluation-match.md).

The later lexical-scope correction now matches pawn removal103 and movement130
without changing C object lifetimes or declared global addresses. All eleven
evaluation procedures share the complete canonical source and naturally match
the whole3,902-byte contribution. Earlier unmatched statements above are
historical; see full-evaluation-match.md and evaluation-scope-independent-audit.md.
