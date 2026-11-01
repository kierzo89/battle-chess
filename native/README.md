# Native Linux port — first milestone

This is a **port in progress, not yet a playable native Battle Chess game**.
The executable currently browses recovered animations through SDL3. The initial
recovered board-state C functions build and are tested as a native library.
No DOSBox, x86 interpreter, original executable, DOS toolchain or runtime is used
by this native target. It runs as a normal Linux ELF executable.

## Isolation and preserved baseline

- Clean published matching copy: `/home/kierzo/battle-chess-publish`.
- Separate port checkout: `/home/kierzo/battle-chess-linux`, branch `native-linux`.
- Immutable starting commit: `0b2a2b36155984c7b23f904f60488b8be0feda8c`.
- All port work is under `native/`; original matching files and assets are unchanged.
- `provenance.json` records source hashes and intentional behaviour boundaries.
- This native branch has not been pushed to GitHub.

The top-level README describes the preserved DOS reconstruction. It does not
claim this Linux port is finished. The older Rust prototype was not imported;
its approximate search is not a substitute for porting the recovered engine.

## Build, run and test

Requires a C11 compiler, CMake, pkg-config, Python 3 and SDL3 development files
(version 3.2 or later). These dependencies are already installed on this machine.

```sh
/home/kierzo/battle-chess-linux/native/run.sh
```

Controls: left/right steps frames, up/down selects sequences, C swaps the native
colour mapping, Space loops a preview, Escape closes. Preview animation is 10 fps
for inspection; this is explicitly not the original game's task scheduling.

```sh
cmake -S native -B native/build -DCMAKE_BUILD_TYPE=Debug
cmake --build native/build -j 4
ctest --test-dir native/build --output-on-failure
python3 tools/verify_source_snapshot.py
python3 tools/verify_asset_snapshot.py
```

The render test uses SDL's dummy video/software renderer and renders every frame
in both colour variants. It tests native rendering execution, not visual identity
with the original game's entire screen. The interactive window uses native SDL
Wayland/X11 support and nearest-neighbour scaling.

`prepare_assets.py` validates source file hashes before packing 253 sequences /
2,365 indexed frames. The original decoded assets remain unchanged. It preserves
padding, anchor coordinates, palette and transparent index zero. Generated files
stay in the ignored build folder.

## Ported and tested so far

- Four-byte board-cell representation with explicit 16-bit indices.
- Original piece-list enumeration order and packed 33-byte board encoding.
- Board-state move application/undo: quiet moves, capture, en passant, castling
  and promotion. These functions require legal moves from the caller; they are
  not a move generator. Their search-side metadata must be saved by the caller.
- Invalid packed board rejection without modifying the current state.
- SDL window, events, palette expansion, anchor placement and colour variants.

## Rules milestone

Native legal move generation and king-safety checks now pass perft and special
move tests. Recovered C attack routines are compiled unchanged as a host reference
and compared with the port. See `rules-provenance.json` for validation scope and
intentional host adaptations. These rules are not yet connected to the viewer;
search, draw history and the full playable game remain incomplete.

## Remaining work, in dependency order

1. Port the authoritative ray tables, legal move generator, attack/check tests
   and turn state. Test against original fixtures, including special moves.
2. Port the original search/evaluation with explicit signed 16-bit arithmetic
   where observable, bounded search and a monotonic host clock. Do not silently
   replace it with the older approximate Rust engine.
3. Connect the original board projection, background composition, animation
   tasks and input/menu state machine to SDL. Keep game timing separate from
   presentation. The current viewer does not implement those tasks.
4. Port filesystem/save/load and sound drivers; preserve documented undefined
   audio-tail boundaries rather than inventing waveform data.
5. Run complete games and original comparison fixtures: legal moves, search,
   castling, promotion, en passant, checkmate/stalemate, save/load, every piece's
   movement/capture animations, keyboard/mouse, audio and window lifecycle.

Assembly-only routines and DOS interrupt/port accesses need explicit portable
implementations. Removing `far` and compiling with GCC is insufficient: original
`int` sizes, packed unions, pointer identity, wraparound and global storage aliases
must be reviewed. Native bytes will intentionally differ from CHESS.EXE; retain
behavioural tests and asset hashes while leaving the matching baseline intact.

## Recovered evaluator milestone

The complete root evaluator now builds from the hash-pinned recovered C and data
tables through `tools/port_evaluation.py`. DOS field widths are preserved;
globals are per-thread. See `evaluation-provenance.json`. The optional original
machine-code comparison verified 96 cases, including every piece-square table
word. This is bounded evaluator evidence, not full search/gameplay equivalence.

To rerun that optional oracle on this development machine:

```sh
cc -std=c11 -fPIC -shared -fno-strict-aliasing -I native/src \
  native/build/generated/evaluation.c native/src/board.c native/src/rules.c \
  -o native/build/libevaluation_oracle.so
/home/kierzo/chess/matching/build/test-env/bin/python native/tests/compare_original_evaluation.py
```

Unicorn and the original executable are used only by that comparison test.
Neither is a dependency of the native game or its normal build.
