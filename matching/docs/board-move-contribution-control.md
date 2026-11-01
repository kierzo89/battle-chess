# Complete board and move contribution

`src/board_move_contribution_probe.c` builds a complete1016-byte CODE
contribution matching original image9448..983F using pinned MSC500 `/AS /Zi`.
All ten functions occupy their original natural public offsets. Their complete
1015 procedure bytes and the compiler-emitted final90 at983F are exact.

The first nine procedures are equal_state39, clear_board29, reset_pieces129,
init_pieces210, castle61, swap96, remove51, add74, and change80. The genuine
adjacent apply_9749 procedure contributes its complete246 bytes. Every retained
REA extent, independently emitted CodeView extent, linked byte, and original
MZ relocation-site set verifies. The aggregate complete CODE relocation set
also agrees with the original, including the final padding position.

Shared Cell/Piece/Move declarations avoid duplicate incompatible board types.
equal_state accepts Move pointers and casts only for the actual byte comparator.
clear_board likewise casts the Cell array for the char-pointer fill utility.
reset/init use the canonical typed memcpy interface. apply_9749 accepts one
by-value Move and an int undo parameter, matching the search caller declaration;
its field accesses reproduce the previous flattened-parameter246-byte body
exactly. It uses the canonical opponent symbol rather than a shifted or
duplicate alias. The same-TU far castle definition naturally generates the
original PUSH CS/near CALL form. No artificial helper extraction is used.

The earlier nine-procedure control remains preserved separately: its770-byte
CODE output mismatched the original solely at its final padding byte. Extending
with this real adjacent function moves the compiler's final padding to983F,
where the original also contains90 before init_rays9840. Nothing was trimmed,
patched, masked, or synthesized as instruction bytes. This establishes a valid
source-built contribution, not unique historical translation-unit identity.

`evidence/board_move_contribution_control.json` contains the complete source,
compiler command/log/tool pins and hashes, object hash/artifact, all procedure
bytes and metadata, relocation logs, and whole CODE comparison. The ten-unit
source-consolidation proposal is `build/board-move-procedure-units.json`;
reproducer `build/board-contribution/probe-move.py`. This adds no new function
credit and edits no canonical source, configuration, registry, or checker.

The root integration now selects the canonical
`src/board_move_contribution_match.c` for all ten procedures. A fresh production
and independent raw-relocation proof is retained in
`evidence/board_move_contribution_match-contribution.json`; see
source-contribution-layout.md. Historical proposal/negative statements above
describe the isolated worker experiment.
