# Coherent asset arena source and group compaction

`src/asset_arena_flow_match.c` combines six genuine adjacent routines:
cache193B, manager902B, push41B, pop33B, release41B and allocate33B.
Pinned MSC5.00 `/AS /Gs /Os /Zi` emits the complete 1,244-byte CODE segment
at image3652..3B2D, including the final compiler NOP found in the original.
All137 raw fixups and the original four MZ sites agree; four loader-base
controls also pass. The source begins at an even address compatible with its
declared WORD alignment. `evidence/asset_arena_flow_match-contribution.json`
retains the complete independent proof. Reproduce with
`python3 matching/evidence/prove-c-contribution.py src/asset_arena_flow_match.c`.

This replaces isolated canonical cache, manager and pool sources without
duplicating credit. It resolves their enclosing CODE context within this
region; shared external definitions, historical translation-unit ownership
and full-program linking remain separate obligations. The original final NOP
earns no function credit. The manager and executor share one genuine
CurrentControls union with named left/right and indexed pointer views,
rather than separately placing shifted aliases.

The final canonical sources also share one fourteen-byte AssetState union:
six loaded flags, six requested flags and the left/right selectors, plus the
complete byte view. The command queue's old shifted kind-flag access becomes
`asset_state.bytes[5 + (cells[square] & 7)]`; the executor clears eight bytes
starting at6. This preserves every index and removes separate shifted globals.
Both full CODE contributions and the unloader remain exact. The independently
compiled definition in `src/data/asset_state.c` matches all14 original
initialized bytes: only the first request starts at255, the other bytes are0.
`evidence/asset-state-data-experiment.json` proves the complete initialized
DATA segment. This is14 new expanded DATA bytes and no packed-file credit.

The new `src/unload_asset_group_match.c` independently matches all870 bytes
at323A, including56 fixups and an empty original MZ set. Its eleven ordinary
used locals reproduce the natural38-byte frame when named in the C5 symbol
allocation order. No padding locals are introduced. The canonical AssetGroup
uses genuine huge pointers for begin/end; the cached Frame layout and list
count symbol agree with the surrounding reconstruction. The fresh complete
proof is `evidence/unload_asset_group_match-contribution.json`; the original
investigation and controls are in `unload-asset-group-experiment.json` and
`unload-loader-context-results.json`.

The group loader35A0 remains unmatched: the emitted178-byte candidate differs
at the frame size and seven temporary displacements. Eleven bounded genuine
source/profile controls, and both orders with the actual870-byte predecessor,
do not explain the original extra eight frame bytes. REA shows no accesses to
those eight bytes. `group-loader-context-findings.md` records this negative;
unused locals are not used to force a match.

The new51-byte active-arena restore and two41-byte pool-return operations
add133 C bytes. Six independent typed DATA definitions add44 expanded bytes:
two initialized pool cursors and four complete error strings. The DATA proof
is `evidence/pool-initialized-data-experiment.json`; these bytes earn no
physical packed-file coverage or function credit.

`evidence/value-task-link-probe.py` authentic-links the four real148-byte pool
routines and all six definitions, then executes every successful operation and
all four boundary error paths. Each definition appears once in the map; all
44 DATA bytes and each complete relocated function match the independently
compiled objects in the emitted image. Independent ordinary C definitions for
`values[4]` and `task_pool[4]` each emit a near COMMON8-byte allocation, without
initialized CODE/DATA. The authentic link places both wholly inside the real
CRT clearing range, outside the file image; the executable checks all entries
are zero before assigning fixture values. These definitions are recorded as
future allocation proposals in `config/uninitialized-definitions.json`, with
the required original map offsets but no claim to recover their historic
ordering or source ownership. The fixture task objects and error handler
remain harness-only. All these allocation controls grant zero matching credit.
LINK's response-file input is exercised because the complete object list
exceeds the DOS command-line limit. Full response text, map, object/tool/image
hashes and execution success are retained in `value-task-link-experiment.json`.
