# Battle Chess — native Linux port

A playable C/SDL3 port using the recovered game code, artwork, animation tasks
and opening book. It runs as a Linux ELF executable, without DOSBox, a CPU
interpreter, CHESS.EXE or the DOS compiler at runtime. The original reconstruction
remains preserved separately. The older Rust prototype is not used.

## Play

Open **Battle Chess Native** on the desktop, or run:

```sh
/home/kierzo/battle-chess-linux/native/run.sh
```

Click a piece and its destination. The side panel has all primary controls:
levels0–9, new game, undo, player mode, pause/resume, save/load, board view,
sound, draw claim, quit and custom minutes. Keyboard shortcuts appear on buttons.
A promotion dialog offers queen, rook, bishop or knight; Escape cancels that move.
Custom minutes accepts1–32767; Escape or zero preserves the previous setting.
Novice bypasses the book; other levels use it where history matches, then search.
The computer plays blue; H switches to two-player mode. U undoes a full turn
against the computer. Save/load uses the application preference directory.

Original perspective graphics include walking, turning, battles, neighbouring
piece reactions, both castling sides, en passant and promotion. V switches to the
rectangular board. Sound can be muted with M. Space pauses animation and audio.
The separate asset browser remains available through `native/run.sh --viewer`.

## Build and validate

Dependencies: C11 compiler, CMake, pkg-config, Python3 and SDL3 development files
(version3.2+); these are installed on this computer. The launcher builds locally.

```sh
cmake -S native -B native/build -DCMAKE_BUILD_TYPE=Debug
cmake --build native/build -j4
ctest --test-dir native/build --output-on-failure
python3 tools/verify_source_snapshot.py
python3 tools/verify_asset_snapshot.py
```

The final functional run passed42 tests, including full games, perft, original
behaviour fixtures, rendering, sound, input, save/load and clean shutdown.
A fully rendered book/search game completed140 plies and26 captures to stalemate.
See [COMPLETION_AUDIT.md](COMPLETION_AUDIT.md) for scope and evidence.

## Fidelity boundaries

This is a native source port, not a byte-identical Linux build or proof of
whole-game DOS execution equivalence. Generated evaluation/search, book ordering
and selection preserve recovered source; host adapters handle threads, time,
legal validation, memory widths and UI. Original comparison fixtures cover the
specific routines described in the tests and provenance files. Original internal
search mode5 and whole-session RNG/call-sequence parity are not claimed.

Menus and save files are native adaptations. DOS saves are not imported. The
promotion choice occurs before animation rather than reproducing the DOS popup
on arrival. Host draw claims/automatic limits are documented in
`history-provenance.json`; original search repetition predicates remain separate.

Audio uses the authenticated amplitude samples through a nominal linear PCM
mapping. Physical PSG/speaker acoustics, calibrated hardware timing and exact
blocking latency are not reproduced. All184 distinct sound pairs exercised by
legal default-profile captures, walks and turns are representable. Alternate
profile1 and illegal king-capture sequences are outside that coverage. Rectangular
view uses static-piece movement; perspective provides battle animation.

## Preservation

- Port: `/home/kierzo/battle-chess-linux`, branch `native-linux`.
- Clean published baseline: `/home/kierzo/battle-chess-publish`.
- Baseline commit: `0b2a2b36155984c7b23f904f60488b8be0feda8c`.
- All repository changes are under `native/`; original matching sources/assets
  retain their published hashes. This branch has not been pushed to GitHub.
- `PORT_GOAL.md` retains the historical implementation ledger; individual
  provenance files describe component-specific adaptations and validation.
