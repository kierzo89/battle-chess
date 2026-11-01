# Fully playable native Linux port

Status: **active**, requested 1 November 2026. The current application is an asset
viewer, not a playable game. Preserve the clean matching repository and all
original source/asset hashes; work only in this separate native-linux checkout.

## Completion criteria

- Native Linux C/SDL3 executable, no DOSBox or CPU emulator.
- Original recovered engine, legal move generation, search and difficulty;
  original comparison fixtures and explicitly documented fidelity limits.
- Castling, en passant, all promotions, check/checkmate/stalemate, draw handling.
- Playable board, input, menus, recovered graphics, movement/capture animations.
- Sound, save/load and responsive window/quit handling.
- Automated chess regression tests, full-game validation and runtime smoke tests.
- Verified desktop shortcut launching the playable game; remove Development label
  only when the application is playable. Do not overwrite the DOSBox shortcut.

## Completed foundation

- Separate native-linux checkout based on 0b2a2b36155984c7b23f904f60488b8be0feda8c.
- Native SDL3 rendering: 253 sequences, 2,365 frames, both colour variants.
- Initial recovered C board encoding, piece indexing, move application and undo.
- Core tests/sanitizers and both published snapshot verifiers pass.
- Desktop launcher installed as Battle Chess Native (Development).

## Next work

1. Trace authoritative recovered move-generation/attack dependencies and port
   explicit-width state, ray tables and legality. Validate perft and special cases.
2. Port recovered evaluation/search, clocks and turn state; keep UI responsive.
3. Integrate board composition, controls, menus and original animation tasks.
4. Add save/load and audio backend; exercise full games and original fixtures.
5. Final native runtime and desktop-launch validation, then mark goal complete.

The existing Rust prototype is not an accepted substitute for the recovered
engine. The original executable's byte identity remains a separate completed
result; native machine code will intentionally differ.

## Progress: recovered rules milestone

Previous goal turn classified as progress: durable goal and desktop launcher added.
This turn adds native legal move generation, attack detection and turn context.
All four CTest targets pass. Perft: start depth 4 = 197,281; Kiwipete depth 3 =
97,862; rook/pawn endgame depth 4 = 43,238. Special-case legality and mate/stalemate
tests pass, as do ASan/UBSan checks of core/rules tests. The recovered C attack
routines are compiled unchanged in a host reference harness and compared across
16 legal positions (786,432 piece-attack comparisons and 2,048 pawn queries).
This is source-semantic equivalence evidence, not original binary execution.

Rules are not connected to the UI yet. Draw-history handling, original phased
search/evaluation, difficulty, full board rendering, tasks, sound and save/load
remain incomplete. Next: original evaluation/search dependency inventory and
native turn/history integration. See rules-provenance.json for explicit host
adaptations, including larger move-list capacity and search-order limitations.

## Progress: recovered evaluator milestone

Previous goal turn: progress (rules and source-equivalence tests committed).
This turn ports the complete root evaluator by deterministic transformation of
hash-pinned matching source and tables, with DOS-width fields and thread-local
state. Native root evaluation passes 96 original machine-code comparisons:
24 played positions × both perspectives × both original temporary contexts.
All six scalars, 1,440 table words and pawn-mask words agree. REA evidence
`ev_17f76f688c9238dc9a3206becef280d5ed4704690d55fd03535b18f02e14eed3`
binds the evaluator bytes to the original image. Castle-rights history is an
explicit oracle contract, not emulated game history. Emulator is test-only.
Five CTest targets, ASan/UBSan evaluator checks and a source-mutation rejection
check passed. Full search/incremental evaluation and draw history remain next.

Search dependency findings: retain the original phase sequence (PV, recapture,
killers, captures, home-pawn quiets, castles, quiets, en passant), original
incremental pawn masks and frozen root tables, 24-ply PV storage, pruning and
aspiration windows. Pointer-containing frame copy size 222 and PV copies 192
must become host object-size copies; history/history_tail/history_storage
aliases must be represented explicitly. UI poll/time hooks must become bounded
native callbacks. Do not replace this with a generic alpha-beta implementation.

## Progress: turn history and repetition support

Previous goal turn classified as progress (original evaluator port and oracle).
Added a native game-session API with dynamically growing snapshots, legal move
validation, complete undo and normalized position identity. Added the original
9C34 repetition detector and 9BFD quiet-count predicate for search integration;
10,440 scans agree with unchanged recovered C in a host reference harness.
Separate host draw claims/automatic limits and conservative dead-material checks
are documented in history-provenance.json; these do not replace the original
search's pruning predicates or claim original DOS UI equivalence. Eight CTest
checks and the history sanitizer tests pass, including dynamic growth/undo.

Still incomplete: original incremental evaluation/search, difficulty and clocks,
board interaction/composition, original animation tasks, sound and save/load.
Desktop app remains the development viewer. Next action is connecting the shared
search state to the recovered search functions, using this history support and
the original evaluator rather than substituting a generic engine.

## Progress: incremental evaluation adapter

Previous goal turn classified as progress (turn history and original repetition).
Added BCSearchEvaluation with frozen root tables and all 26 pawn-history rows.
The original evaluate_candidate code is reused, not replaced by a score-difference
heuristic. The adapter preserves original promotion-before-parent-copy ordering,
validates indices and returns mutated scratch rows for the search to retain.
Original-machine-code comparison passes 234 cases covering both sides, three
ply depths, three best-score contexts, captures, both castles, en passant and
all four promotions with/without captures. Results match AX and every byte of
the 208-byte pawn-history region. Original helpers run unchanged in that test;
only the test return sentinel is intercepted. Emulator remains test-only.
Nine CTest targets and incremental ASan/UBSan checks pass. Desktop still viewer.

Next: port the recovered phased search using this adapter and the history API;
replace DOS frame/PV byte sizes by host object sizes, preserve aliases explicitly,
and bind time/input polling to native callbacks. Full search is not implemented.

## Progress: recovered phased search running natively

Previous goal turn classified as progress (incremental evaluator validated).
Generated the recovered search source with pinned input hashes, explicit DOS
scalar widths, thread-local state, host-size frame/PV copies and explicit history
aliases. Added adapters to the already-validated evaluation, rules and history.
Retained phase ordering and pruning; no generic alpha-beta substitute introduced.
Native depth-two search selects g1-f3 in 132 candidate visits; depth four completes
3,402 visits. Repeatability, 12-ply selfplay, checkmate/stalemate, cancellation,
node limits and ASan/UBSan pass. Whole-search original-binary equivalence is NOT
yet established. Graphics/input hooks remain unbound and time-based difficulty
is not implemented; source-level special mode is not yet calibrated.

Next: verify/adapt timed difficulty and original search mode handling, then
connect an SDL board/game interface and asynchronous search. Finish animations,
audio/save-load and full-game/original behaviour validation before completion.
Desktop shortcut continues to launch the development viewer for now.

## Progress: timed difficulty

Previous goal turn: progress (recovered phased search executing natively).
Source inspection establishes limits are seconds through time(0), NOT BIOS
ticks: levels 1..9 request 5..1280 seconds, novice requests 6 seconds but searches
two plies, custom time uses minutes*60. Internal search_level==5 must NOT be
labelled novice; that control's identity remains unresolved. Ordinary native
menu settings use internal mode 0, with recovered normal depth limit 23.
Added injected/default monotonic clocks, hard deadlines, timeout/elapsed result
fields, input rejection and last-PV-slot bounds. Fake and real-clock deadline
checks return legal results; timed ASan/UBSan tests pass. All 11 CTests pass.

Remaining: original timing and whole-search fidelity, opening book, special mode
identification, and all UI/gameplay integration. Next concrete work: connect SDL
board input and asynchronous search, with difficulty menu and clean cancellation
on undo/new game/quit. Desktop is still the development viewer, not finished.
