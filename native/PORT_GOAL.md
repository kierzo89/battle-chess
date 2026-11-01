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
