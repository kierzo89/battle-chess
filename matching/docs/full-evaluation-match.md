# Full evaluator C match

`src/full_evaluation_match.c`, compiled with pinned Microsoft C 5.00
`/AS /Gs /Zi`, reproduces the complete 2,803-byte far evaluator at original
image FE59..1094B (CS0FDF:0069). The independent CodeView length is 2,803;
every linked byte and the complete original loader-site set `{1004C}` match.
The ordinary C source retains the 1,538-byte local frame, material/phase
calculation, board and ray scoring, pawn structure and final position score.
Observed unusual precedence and the nonexecuting pawn-bonus loop are retained.

The procedure's correct analysis requires the unchanged-code CS carrier
explained in [evaluation-context.md](evaluation-context.md). The strict
[segmented extent proof](segmented-evaluation-extent.md) verifies its exact
2,803-byte span, 265 blocks, adjacent bit counter and two-byte dead jump.
This is a fixed evidence-backed proof; it permits no arbitrary skipped bytes.
The carrier is comparison evidence only and contributes no source bytes.
A fresh REA read is retained in `evidence/rea_full_evaluation_final_raw.json`.

The full consumer establishes a typed score grid `int piece_square[2][6][120]`
at DGROUP B0DC. Piece kinds 1..6 select `kind-1`; side and square select the
other dimensions. The older AFEC flat view was biased one row before the
proper grid. Both canonical evaluator sources now use the typed grid, whose
ordinary compiler addends naturally reproduce the original instructions.
This change supplies no grid initializer or DATA credit. All six existing
canonical consumer procedures still match; their seven-unit production proof,
including the large evaluator, is `evidence/full-evaluation-production-match.json`.

C5 local placement uses 16 identifier buckets; declaration order within a
bucket determines local slots. Ordinary identifiers and local declarations
produce the observed frame without inline assembly or emitted byte constants.
The Boolean operand order `(f!=0)&(f!=7)` also matters to register allocation.
These are compatible reconstruction choices, not recovered historical names.
`/Zi` provides an independent compiler extent, not proof of original debug flags.

The entire eleven-function natural CODE contribution now matches all3,902 bytes
at FDF2..10D2F, including the independently emitted final90 alignment byte.
Complete procedure credit is3,901 bytes; alignment earns no function credit.
All182 OMF fixups are owned once by complete compiler extents. An independent
raw-FIXUPP arithmetic pass agrees with the production linker. The complete
emitted/original loader-site sets are `{1004C,10B45}`, also verified at four
load paragraphs. Every own function target uses its actual PUBDEF offset+2.

The key correction puts each pawn mutation's statements in an ordinary lexical
block ending before the two-call score subtraction. Outer C objects keep the
same lifetime; C5 releases its synthesized common-subexpression address
temporary at the scope boundary and reuses SI for the first call's result.
Pawn removal/movement now match103/130 bytes. An independent fresh compilation
confirms every byte; the negative control that wraps only the return statement
still emits105/132 bytes. See [independent scope audit](evaluation-scope-independent-audit.md).

All eleven canonical evaluator procedures now use `src/full_evaluation_match.c`,
including min/max and candidate evaluation. Their original REA/CV/boundary
contracts still apply independently. The complete proof and reproducible fresh
build are `evidence/evaluation-contribution-match.json` and
`evidence/evaluation-contribution-probe.py`.

The previous3,906-byte candidate,3,130-byte exact prefix and `/AS` versus `/AM`
control remain historical evidence. Their reproducers now use the preserved
`src/full_evaluation_probe.c` snapshot. The complete source contribution does
not establish historical translation-unit identity or original full-link
ordering. Reviewed external placements are still comparison assertions; the
remaining game, DATA/BSS layout, full linking and source-built EXEPACK output
remain unfinished.

The canonical scoped source also passes a fresh complete `/AS` versus `/AM`
control: all3,902 linked/unlinked CODE bytes,11 CodeView extents and182 fixup
operations agree. The medium model changes `_TEXT` to `UNIT_TEXT`, preserving
PUBLIC/word alignment attributes0x48. Evidence is
`evidence/evaluation_scoped_memory_model_control.json`. This supports the
named-segment configuration without uniquely recovering the historical command.
