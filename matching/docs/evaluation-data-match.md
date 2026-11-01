# Typed evaluation DATA

Eight ordinary C definitions in `src/data/evaluation_*.c` independently compile
with Microsoft C5.00 `/AS /Zl /Zi` and match114 initialized expanded-image bytes.
The complete standalone DATA SEGDEF, DGROUP membership, public at offset zero,
contiguous LEDATA and absence of other allocations/fixups are checked for each.
Original bytes are comparison input only. Full provenance and fresh REA reads
are retained in `evidence/runtime-data-eval-experiment.json` and associated
`runtime-data-eval-*-raw.json` records. Reproduce with
`python3 matching/evidence/runtime-data-eval-probe.py`.

| DGROUP | Definition | Type | Bytes |
| --- | --- | --- | ---: |
| 054C | piece values | int[7] |14 |
| 055A | center distance | int[8] |16 |
| 056A | pawn rank bonus | int[8] |16 |
| 057A | passed rank bonus | int[8] |16 |
| 058A | pawn file weight | int[8] |16 |
| 059A | castle bonus | int[2] |4 |
| 059E | rank weight | int[8] |16 |
| 05AE | file masks | unsigned[8] |16 |

These reconstructed dimensions follow the consuming piece/file/rank domains.
The pawn and passed-rank consumers read ranks1..6; the eight-rank definitions
also retain independently observed zero edge entries. Exact historical array
boundaries, names and aggregate identity are inferred. No filler or arbitrary
allocation policy is permitted. All definitions remain separate until a full
source/link layout establishes their placement. Together with the existing80B
move table, authored DATA totals194 bytes in9 contributions. This receives
zero C-function or compressed-file coverage credit.

Three further typed definitions now add19 bytes: `kind_map[7]` at DS0F00,
`pawn_home[2]` at DS05C0 and the eight-byte `Move initial_move` at DS04E2.
Complete raw reads, consumer domains and fresh compiler proofs are retained
in `evidence/runtime-data-game-next-experiment.json` and its findings.
The animation and redraw consumers now use the same kind_map declaration
as the queue consumer; all433 changed-source function bytes remain exact,
with no alias definition or extra function credit. Separate DS11AC capture
mapping remains distinct. Total authored DATA is12 contributions /213 bytes.

Four further UI/player definitions add69 initialized bytes, bringing authored
DATA to16 contributions/282 bytes: modes[2] and three complete NUL-terminated
strings. Consumer-domain and NUL-scan evidence is retained in
`evidence/runtime-data-ui-findings.md`; fresh full objects/raw reads are in
`evidence/runtime-data-ui-experiment.json`. These receive no function or
compressed-file credit.
