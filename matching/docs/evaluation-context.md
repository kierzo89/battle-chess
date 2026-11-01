# Recovering the evaluator's correct CS context

The original full-image REA dossier at imageFE59 misdecodes near branches
after crossing linear20000. It reports only448 reachable bytes in a456-byte
span and warns about bad instruction data, including a false call to image0021.
Those observations cannot establish this function's complete original extent.
The retained weak dossier is `evidence/rea_full_evaluation_fe59.json`.

The original evaluator's known far-call frame is CS0FDF. Rebase its unchanged
imageFDF0..10D30 code into an analysis-only MZ with CS0 so its internal offsets
stay below64KiB. Original CS0FDF offsets then equal derived image offsets.
This preserves every original instruction and internal branch displacement.
External far pointers and DS globals still require original-address interpretation.
These original-derived carriers are never source-build inputs and earn no credit.

The [reproducer](../evidence/evaluation-context-probe.py) creates two carriers
and records original/carrier/code hashes and complete generated headers in
`evidence/evaluation-context-carriers.json`. EVALCS0 enters directly at0069;
it corrects control flow but the loader's program-entry stack assumptions harm
local-variable recovery. EVALCALL instead appends a separate ten-byte analysis
stub that calls the function and exits. Only that stub's far segment word is
loader-relocated. All3904 original code bytes remain identical.

The second carrier SHA is
`6e3399639c9b0157ea948c6f30e80030b99a50ec9b783026381fd694904d9f19`.
REA's [normal callee dossier](../evidence/rea_full_evaluation_rebased_callee.json),
`ev_add4d5a1349db9c1667ac3e71deff0dc34a0951e5d816d76422581ea30e91af9`,
recovers265 CFG blocks and2801 reachable bytes within the complete2803-byte
span0069..0B5B, mapping to originalFE59..1094B. It also recovers normal BP
locals rather than entry-stack globals. The original frame subtracts0602
bytes directly, without a stack-probe call, consistent with the other `/Gs`
evaluation procedures. Source array dimensions and local types remain inferred.

A [complete2851-byte raw read](../evidence/rea_full_evaluation_rebased_raw.json)
covers that span and the adjacent48-byte bit counter. Every byte independently
equals the pinned original prefix at FE59..1097B. The only omitted two-byte
gap is derived06C2..06C3, bytesEB2F, mapping to original104B2..104B3. The complete function now matches ordinary C with an independent 2,803-byte
CodeView extent. The dedicated `segmented_evaluation_v1` proof checks these
carriers, every CFG interval, the gap and next entry before credit is allowed.
See [full-evaluation-match.md](full-evaluation-match.md) for production evidence.

The corrected internal calls map to already matched absFDF2, maxFE0C,
pawn_score1097C and piece109F9. Together the observed far evaluator sequence is:

| Original image | Procedure | Bytes | State |
| --- | --- | ---: | --- |
| FDF2 | abs |26 | C match |
| FE0C | max |31 | C match |
| FE2B | min |31 | C match |
| FE4A | parity |15 | C match |
| FE59 | full evaluation |2803 | C match (strict segmented extent) |
|1094C | bit count |48 | C match |
|1097C | pawn score |125 | C match |
|109F9 | piece value |51 | C match |
|10A2C | pawn removal |103 | C differs |
|10A93 | pawn movement |130 | C differs |
|10B15 | candidate evaluation |538 | C match |

These observed procedure spans total3901 bytes, including3,901 independently matched
C bytes. Original10D2F is a separate90 byte before the next known entry10D30;
FDF0..FDF1 isCB90 before abs. A full3902-byte source contribution beginning at
FDF2 is a useful layout candidate, not proven historical translation-unit
identity. Its CS frame would naturally be FDF0 with initial offset2, consistent
with the independently tested word-aligned medium-model LINK placements.
A natural single-object source now matches the entire3,902-byte contribution,
including all11 procedure extents and its final alignment byte. Full executable
layout and linking remain unbuilt; see full-evaluation-match.md.

The root REA session currently holds EVALCALL.EXE. Reuse its saved evidence for
this scope, and explicitly switch targets before requesting original-image
addresses in subsequent investigations.
