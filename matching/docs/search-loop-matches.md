# Search loop and move preferences

The canonical search source is now
[search_engine_a528_b9ba_full_match.c](../src/search_engine_a528_b9ba_full_match.c):
eighteen complete functions,5,266 CODE bytes,493 fixups and four original MZ
sites. The [full proof](../evidence/search-engine-a528-b9ba-full.json) includes
an independent raw relocation pass and four load-base comparisons. There are
no holes, unowned bytes or padding. [Quiet search and interface notes](quiet-search-switch.md)
describe the later additions; earlier consolidation stages are retained below.

Fresh REA MCP observations support four further ordinary C matches under the
pinned Microsoft C 5.00 `/AS /Zi` configuration:

| Entry | Bytes | Source | Behavior inferred from the complete body |
|---|---:|---|---|
| A943 | 533 | [moves_search_loop_a943_match.c](../src/moves_search_loop_a943_match.c) | Try the saved line, captures, stored candidates and generated moves in stages |
| AE11 | 169 | [store_line_match.c](../src/store_line_match.c) | Maintain two distinct candidate moves for each search level |
| AEBA | 155 | [preferred_move_match.c](../src/preferred_move_match.c) | Recognize a saved line move or eligible stored candidate |
| AF55 | 50 | [update_best_match.c](../src/update_best_match.c) | Accept a score at or below the frame bound and update its best value |

Each function has an independent complete contiguous REA body, a fresh compiler
CodeView3 procedure length and a full linked-byte comparison. Sources contain
no inline assembly, emitted opcode arrays or target-length trimming. The main
checker remains the authority for registration and aggregate counts.

The search frame is 222 bytes. The reconstructed prefix contains three words,
a six-byte SearchOptions value, a near Move pointer, and two more words; the
stage word lies at offset 28. Earlier standalone sources reserve the then
unknown fields as character arrays; the consolidated source identifies child
depth at 18, child options at 20, re-search state at 26 and 24 moves at 30.
Move values occupy eight bytes and are passed by value where observed.
These names and types are reconstructed, not recovered original identifiers.

The earlier standalone A943 object contains a 534-byte CODE segment. Only its
complete 533-byte compiler procedure matches; the extra trailing alignment
byte receives no credit. That object is not a complete original contribution.

An earlier eight-function consolidation of A528..AEB9 used
[search_engine_a528_aeba_full_match.c](../src/search_engine_a528_aeba_full_match.c).
This extends the earlier six-function 1,584-byte contribution into a complete
2,450-byte CODE segment. Eight independent compiler extents cover every
initialized byte without holes or padding. All 245 code fixups belong to those
extents exactly once. A separate relocation pass over the raw complete segment
agrees with production per-function linking and the original bytes. Both emit
exactly the three original MZ sites A536, A55F and A683; four load-base
comparisons also remain exact.

This source shares the eight-byte Move, six-byte SearchOptions and fully typed
222-byte SearchFrame, uses the indexed home_pawn and check_state views
consistently, and expresses driver bounds through SearchOptions fields. Its
three far-call pointer aliases remain exact. The
[full contribution proof](../evidence/search-engine-a528-aeba-full.json)
provides additional layout evidence and earns no duplicate coverage. It
establishes a compatible reconstructed contribution, not historical
translation-unit identity. The earlier
[six-function proof](../evidence/search-engine-a528-full.json) remains retained.

Evidence includes [A943](../evidence/rea_moves_a943_match.json),
[AE11](../evidence/rea_store_line_ae11.json),
[AEBA](../evidence/rea_preferred_move_aeba.json), and
[AF55](../evidence/rea_search_next_af55.json). The generated per-unit report
records the current sources, tools, flags, relocations and full byte comparisons.

The adjacent 697-byte candidate validator AB58..AE10 also matches from ordinary
C. It identifies child depth, child options, re-search state and a 24-move
principal-variation array in the formerly reserved frame fields. Its complete
[verification and integration notes](validator-ab58.md) include the corrected
shared global views and fresh canonical build proof. It now uses the eighteen-function canonical contribution described above.
