# Board helper source consolidation control

`src/board_helpers_contribution_probe.c` combines nine genuine matched
procedures with shared Cell, Piece, Move, and Square types, compiled with
pinned MSC500 `/AS /Zi`:

| Original image | Procedure | Complete bytes |
| --- | --- | ---: |
| 9448 | equal_state | 39 |
| 946F | clear_board | 29 |
| 948C | reset_pieces | 129 |
| 950D | init_pieces | 210 |
| 95DF | castle_95df | 61 |
| 961C | swap_cells | 96 |
| 967C | remove_piece | 51 |
| 96AF | add_piece | 74 |
| 96F9 | change_piece | 80 |

All769 procedure bytes match at their natural object public offsets plus
image9448. Each complete retained REA extent, independent CodeView extent,
linked function byte, and exact original MZ relocation set verifies. There
are no unknown public placements or artificial extracted helper definitions.

The shared equality signature accepts Move pointers, agreeing with the search
callers. Its byte comparison casts to char pointers. clear_board likewise
casts the shared Cell array to the actual byte utility's char-pointer type.
The initialization routines use the canonical typed memcpy declaration and
symbol rather than a separate copy_bytes alias. These changes preserve every
original procedure byte and avoid incompatible duplicate board declarations.

The complete CODE contribution, however, is770 bytes. MSC500 emits a final90
alignment byte after the769 procedure bytes. That byte would occupy original
9749, where the next apply_9749 function starts with55. This is the sole full
CODE mismatch. No byte was trimmed or patched, and this source is not proposed
as a complete original769-byte contribution. Extending a later contribution
requires genuine additional original functions and compatible interfaces;
the observed nine-function span does not establish a historical module boundary.

`evidence/board_helpers_contribution_control.json` retains the full source,
fresh compiler command/log/tool pins, object hash, all procedure metadata and
bytes, relocations, complete770-byte CODE and original comparison, and the
single mismatch offset769. `build/board-helper-procedure-units.json` is a
per-procedure-only consolidation proposal, not a full contribution proposal
or new function credit. The reproducer is `build/board-contribution/probe.py`.
Canonical source, configuration, registry, and checker files were not edited.
