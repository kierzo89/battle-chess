# Unexplained automatic variables and matching credit

The 164-function checkpoint included five ordinary C sources whose exact output
depended on unread automatic variables. Those compiler comparisons were real:
the historical compiler emitted the entire matching function, without patching
its output. However, an observed stack reservation does not identify the
original variables or their types. These assumptions conflict with the current
rule against inventing padding locals to force an allocation.

The fresh audit removes only the unread declarations, compiles each complete
source with its registered compiler/profile, retains every complete procedure,
and compares all bytes with the hash-pinned original. Every affected procedure
keeps its original length but has different frame/local-displacement bytes.
Other registered procedures in the shared board and search sources still match.

| Procedure | Previous bytes | Unsupported declarations |
| --- | ---: | --- |
| animate_move_78f6 | 363 | Two unread byte locals |
| queue_move_77af | 327 | Three unread integer locals |
| apply_9749 | 246 | One unread integer local |
| search_window_a799 | 80 | One unread integer local |
| init_rays_9840 | 185 | One unread integer local |

Those five, totaling 1,201 bytes, are removed from canonical matching credit.
Their complete former registry records and historical source hashes are in
`config/unresolved-frame-units.json`; the former sources are retained under
`src/probes/frame_assumptions/`. Canonical source files now omit those
declarations. The unresolved functions remain source candidates, and callers'
explicit comparison addresses remain observations rather than proof of a
complete source link.

`evidence/unexplained-locals-audit.json` retains independent compiler/tool/object
provenance, full unpadded sources, full generated procedures, fixups and every
differing position. Reproduce the experiment with
`python3 matching/evidence/unexplained-locals-audit.py`.

The previously proposed 874-byte task-tail contribution included the old
padding-dependent queue_move and is therefore historical diagnostic evidence
only. Its new canonical source contains just three genuine handlers totaling
547 procedure bytes. Its final compiler NOP remains visible and uncredited.

## Broader audit

A separate host syntax diagnostic parsed all 53 currently credited C sources,
suppressing only the historical far/huge type qualifiers in that diagnostic.
It identified further never-referenced locals in graphics and evaluation code.
Fresh target-compiler controls then established their actual byte effects:

| Additional dependent procedure | Withdrawn bytes |
| --- | ---: |
| draw_actor_3f9e | 522 |
| mark_region_41a8 | 248 |
| render_42a0 | 725 |
| build_menu_466b | 1,545 |
| outline_square_543a | 850 |
| close_menu_4c74 | 489 |
| finish_menu_5035 | 122 |
| pawn_bit_count_1094c | 48 |
| evaluate_candidate_10b15 | 538 |

Removing 26 unreferenced graphics declarations changes only those seven
procedures, totaling4,501 bytes. Fifteen neighbors totaling2,761 bytes remain
exact. Removing the two evaluation declarations changes only48/538-byte
procedures; nine neighbors totaling3,316 bytes remain exact. All complete
procedure lengths and public offsets remain unchanged. The symbolic fixups
and original MZ sets are retained, including reordered external indices in
otherwise equivalent compiler objects.

Canonical sources now use these unpadded variants. The final withdrawal is
fourteen functions /6,288 bytes, including sixteen previously credited MZ
sites. See `graphics-unpadded-audit.json` and
`evaluation-unread-local-control.json` for complete sources, fresh objects,
CodeView extents, generated/original bytes and fixups. Their historical input
registry is preserved as `evidence/interim-168-units.json`.

The final host diagnostic reports no parse failures and no never-referenced
automatic declarations across all53 current C sources. It separately records
assigned-but-unread values, which have genuine source operations and were not
removed by this declaration-only audit. This diagnostic is not a target-byte
matching backend, a claim to recover original variable identities, or a proof
that every possible source assumption has been eliminated. Actual MSC builds
and complete target comparisons remain mandatory.

The intermediate168-function byte-checking run passed all272 tests before
the additional nine withdrawals. Its retained checkpoint is explicitly
provisional. The final registry/report is the159-function checkpoint.

The adjacent unregistered special handler at 6BF9 has the same kind of unresolved
allocation issue. Authentic C4, C5.00, C5.10 and immediate genuine-neighbor
controls do not explain its extra eight-byte original frame. The turn handler
at 730C similarly has a two-byte reservation difference. None receives credit
through invented unused locals. Genuine source/type/compiler explanations are
still required; absence of observed reads does not establish what the original
source declared.

Older snapshots and exact-output records remain historical findings. Current
claims must use the fresh registry and reports, including the source inventory's
uncredited-procedure and full-CODE-context obligations.
