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
