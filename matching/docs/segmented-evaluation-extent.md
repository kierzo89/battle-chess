# Fixed corrected-CS evaluator boundary proof

`segmented_extent.validate_segmented_extent` is routed by `extent.py` only for
`extended_extent.kind = segmented_evaluation_v1`. It accepts exactly image
FE59, CS0FDF:0069, size2803, ordinary C. It does not relax ordinary contiguous
REA validation or support arbitrary carriers, targets, mappings, or sizes.
The canonical `full_evaluation_fe59` unit is registered in `config/units.json`;
`build/segmented-evaluation-extent.json` retains the initial metadata proposal.

The validator reads `project.parent/CHESS.EXE` and checks its pinned original
hash and MZ header. It reconstructs both analysis carriers in memory from the
unchanged original FDF0..10D30 prefix, their exact32-byte headers, and the sole
fixed EVALCALL stub. Both carrier hashes, header bytes, entry addresses, stub,
single stub relocation, original-code hash, and mapping must agree with the
retained manifest. Carrier files are not compilation or matching inputs.

The retained original weak dossier stays bound to original FE59. Corrected
callee and raw dossiers must identify the recomputed EVALCALL hash and exact
retained analysis profile. The original bit-count dossier stays bound to
CHESS.EXE. The complete2851-byte derived raw read must equal the pinned
original prefix, covering the entire2803-byte function and the following48
bytes. Both body ranges,2801 reachable bytes,2803 span,265 distinct closed CFG
blocks, exact gap-free block coverage outside the sole gap, and entry
reachability of all blocks are required.

Derived106C2..106C3 is the sole dead gap, EB2F. Its immediately preceding EB31
and both forward targets are checked against the pinned bytes and retained
CFG; both target106F3. Incoming/outgoing retained references cannot enter the
gap. Fresh independent global REA xref queries for each byte returned empty;
their complete evidence is `rea_full_evaluation_gap_6c2.json` and `6c3.json`.
The next original function must start exactly at1094C with its complete48-byte
body, covered by the full raw read. No boundary is inferred from source size.

The call contract additionally requires the fresh object's complete CodeView3
procedure metadata to name the unit symbol and cover exactly2803 bytes, and
every freshly linked byte to equal the pinned original span. A2804-byte or
otherwise unequal source candidate cannot pass. Unit tests use explicitly
synthetic CodeView metadata only to exercise validation; that fixture is not
compilation evidence and grants no reconstruction credit.

Thirteen focused tests cover the positive retained proof and mutations of
original/carrier hashes, CS mapping, header/stub/relocation fields, every
evidence subject/profile/operation, body/next extents, raw and linked bytes,
CFG coverage/closure/reachability, gap references, xrefs, and CodeView metadata.
Existing extent tests remain unchanged and pass. Checker whitelist integration,
fresh source compilation and canonical registration are complete. The full
2,803-byte source match and six consumer regressions are retained in
`evidence/full-evaluation-production-match.json`. See full-evaluation-match.md
for the separate, still-incomplete natural contribution layout.
