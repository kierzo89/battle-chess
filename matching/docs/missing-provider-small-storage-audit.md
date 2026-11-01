# Missing-provider small storage audit

The frozen C214 actual LINK has 356 unresolved provider names. This bounded audit changes no canonical input and awards no new matching bytes. Fresh REA reads use the explicitly derived unpacked carrier, not the original packed file identity.

## Priority 1: initialized UI scalars

Each row below is independently consumed storage. Adjacent rows are not a recovered array or historical contribution. Initial values are exact little-endian primary bytes; signedness remains constrained by consumer declarations.

| DS | Names | Bytes | Initial hex | Type views |
| --- | --- | ---: | --- | --- |
| 0x44 | _menu_open_0044 | 1 | 00 | unsigned char |
| 0x4a | _menu_button_004a | 1 | 00 | unsigned char |
| 0x4b | _previous_button_004b | 1 | 00 | unsigned char |
| 0x54 | _modal_0054 | 1 | 00 | unsigned char |
| 0x56 | _board_action_active_0056 | 1 | 00 | unsigned char |
| 0x57 | _highlight_flash_0057 | 1 | 00 | unsigned char |
| 0x58 | _highlight_colour_0058 | 1 | 0e | unsigned char |
| 0x5a | _mode_005a | 1 | 00 | unsigned char |
| 0x5b | _flag_005b | 1 | 00 | unsigned char |
| 0x5c | _input_x_005c | 2 | 0000 | int |
| 0x5e | _input_y_005e | 2 | 0000 | int |
| 0x60 | _pointer_hidden_0060 | 1 | 00 | unsigned char |
| 0x61 | _input_flag_0061 | 1 | 00 | char, unsigned char |
| 0x62 | _remote_move_ready_0062 | 1 | 00 | unsigned char |
| 0x63 | _remote_status_0063 | 1 | 00 | unsigned char |
| 0x53a | _level, _view_mode_053a | 2 | 0100 | int |
| 0x548 | _refresh_active_0548 | 2 | 0000 | int |
| 0xeee | _waiting_0eee | 2 | 0000 | int |
| 0xef0 | _help_ready_0ef0, _menu_enabled_0ef0 | 2 | 0100 | int |
| 0xef2 | _board_input_0ef2, _board_ready_0ef2 | 2 | 0000 | int |
| 0xef4 | _cursor_kind_0ef4 | 2 | 0000 | int |
| 0xef6 | _command_active, _silent | 2 | 0000 | int |
| 0xef8 | _arena_fallback | 2 | 0000 | int |
| 0xefa | _selected_square_0efa | 2 | ff00 | int, unsigned int |
| 0xefc | _adjacent_square, _cursor_square_0efc | 2 | ff00 | int, unsigned int |
| 0xefe | _hover_square_0efe | 2 | ff00 | unsigned int |
| 0x11a6 | _refresh_stop_11a6 | 1 | 00 | unsigned char |
| 0x11aa | _mode_11aa | 1 | 01 | unsigned char |
| 0x11ab | _palette_mode | 1 | 00 | unsigned char |
| 0x11b3 | _record_latch | 1 | 00 | unsigned char |
| 0x11b4 | _input_mask_11b4 | 1 | 3f | unsigned char |
| 0x2b2c | _dialog_button_state_2b2c | 2 | ffff | int |

The contiguous nine UI words at 0EEE–0EFE are the best first group: 18 independently justified bytes. Resolve same-address aliases and signed/unsigned consumer views before supplying definitions. The byte flags near 0044 and 11A6 are next; gaps receive no credit. Definitions initialized to zero must still emit actual DATA rather than merely COMMON. Pointer-bearing initializers are deferred because real fixups and ownership need separate proof.

## Priority 2: requested history/side storage

These six variables are beyond the initialized DS boundary 52CC. They are candidates for real BSS/COMMON provider closure, with zero initialized-byte credit. Aliases must be migrated to a single genuine symbol rather than additional storage.

| DS | Names | Bytes | Consumed C model |
| --- | --- | ---: | --- |
| 0x57c8 | _temporary | 2 | int |
| 0x9846 | _current_side, _side, _side_9846 | 2 | int |
| 0x984c | _history_move_counter | 2 | int |
| 0x9880 | _counter, _counter_9880, _history_index | 2 | int |
| 0xa836 | _opponent, _opposite, _opposite_side, _side_a836 | 2 | int |
| 0xb0ac | _selected_move | 8 | Move |

`notify_866d` / `notify_86a1` primary evidence establishes word increment/decrement and AX word swaps. `commit_move_8632` establishes the four-word Move copy at B0AC. These accesses do not prove historical scalar ownership, linker order or original MAP. Fresh attempted reads at 57C8 and 9846 return zero bytes with `complete:false`; they are not initialized zero byte evidence. The existing three-clock-long COMMON proposal remains separate, unadmitted and zero credit.

## Staged source review

The staged 363-byte animation and 850-byte square-outline exact records are historical padding-dependent controls, not ready providers. Animation current source SHA differs from its old exact proof; square outline still has unread automatic variables. Their withdrawal and genuine unpadded negative controls are documented in `docs/unexplained-frame-audit.md`. The already admitted eight-clock-function/274-byte proposal and initialized reset flag are excluded from pending credit.

[Machine-readable audit](../evidence/missing-provider-small-storage-audit.json) retains exact declaration views, all selected actual operand fields, primary evidence IDs and hash pins. No exhaustive missing-provider recovery, original source type recovery or final executable is claimed.
