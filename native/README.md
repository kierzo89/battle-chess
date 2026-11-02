# Native Linux port — interactive development build

This is an **interactive development build, not the completed native port**.
It supports human-versus-computer and two-player chess, with the recovered C
search running on a background thread and original recovered piece artwork.
The original perspective and rectangular boards are available (V switches views).
Walking frames are connected; turning, battle animations and audio are pending.
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

Click a piece and its destination. N starts a game, U undoes a turn, H toggles
one/two players, Space pauses, 0–9 selects difficulty, D claims an available draw,
and Q/R/B/K chooses promotion (K = knight). S saves; L loads. V changes board view.
Escape closes the game.
The desktop shortcut launches this development game.

For the separate recovered animation browser, run `native/run.sh --viewer`.
Its controls are left/right (frame), up/down (sequence), C (colour), Space (preview).
Preview timing is not original task scheduling.

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
intentional host adaptations. Rules, draw history and search are now connected to the interactive board.
Full original presentation and game fidelity remain incomplete.

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

## Turn history milestone

`history.h` supplies legal move commits, complete undo and draw-state queries.
The recovered search repetition scan is tested against the unchanged source in
10,440 cases. Host position-repetition keys include rights and legally usable
en-passant opportunities. `history-provenance.json` separates original search
behaviour from the host UI draw policy. This API is not yet connected to the
viewer, and does not change the application's not-yet-playable status.

## Incremental evaluation

`BCSearchEvaluation` holds frozen root tables and the original per-ply pawn masks.
`bc_evaluate_delta` runs the recovered candidate evaluator, including its original
scratch-row ordering. Bounds are checked before calling the recovered routine.
The optional `native/tests/compare_original_delta.py` uses the same test library
build as the root evaluator oracle and matches 234 original-machine-code cases.
This is a search prerequisite, not an implemented search or playable game yet.

## Native search milestone

`search.h` exposes the original phased search compiled from pinned recovered C,
using native rules, original evaluators and repetition predicates. It accepts
explicit depth, seed, node bound and cancellation callback. Depth-four, terminal,
repeatability and short selfplay tests pass. See `search-provenance.json` for the
host adaptations and unresolved original-engine fidelity checks.

The engine is not yet connected to the viewer. Original timed difficulty and
input hooks are still pending; the app is not yet a playable native game.

## Timed difficulty

`bc_difficulty_config` maps the recovered menu levels to time budgets: Level 1
is 5 seconds, doubling to Level 9's 1,280 seconds; custom time is minutes.
Novice searches two plies. These are seconds from the original `time(0)` clock,
not BIOS ticks. The internal special search mode 5 is not labelled novice.
Native monotonic deadlines and caller cancellation prevent blocking indefinitely;
`difficulty-provenance.json` documents the differences from DOS timing. The UI
still needs its difficulty menu and engine integration.

## Native saved games

S saves to SDL's application data directory, normally
`~/.local/share/battle-chess-native/game/game.bcs`; L restores that game. The
current game survives a failed load. Saving uses a temporary file, flush/fsync
and atomic rename, keeping the previous file if writing fails. The BCS1 format
contains the entire move log from the standard initial position plus draw-claim
state, with a version signature, count limit and CRC32. Loading validates every
move by legal replay, preserving undo, castling, en passant, promotion, repetition
and search context. Custom starting positions are deliberately rejected by this
format. It is not compatible with original DOS saves. Difficulty and player-mode
settings remain session settings rather than saved-game fields.

Tests cover replay/undo, draw claims, random legal history, truncated/corrupt
files, correctly checksummed illegal moves, and UI save/new/load events using
an isolated temporary file. Three bounded depth-two engine self-play fixtures
reach checkmate; these are gameplay regression evidence, not whole-engine DOS
binary equivalence or exhaustive chess validation.

## Presentation timing foundation

`presentation.c` ports the recovered task countdown/sound-command interpreter
and signed movement interpolation. It preserves FF tails (ready on every later
eligible call) and does not treat timer bytes as fixed-FPS durations. The native
library is checked against 144 authenticated retained capture-control streams,
including 4,448 readiness events and 488 sound dispatches, plus 20,000 comparisons
with the recovered interpolation C. A two-tick gate models the original event
fallback without late-frame catch-up. Interpolation and tick gating now drive non-capture board motion. The control
stream interpreter still awaits capture integration; battle animation and physical
sound playback remain pending.

The interactive board now uses the recovered static-sprite movement primitive
for non-captures, including sequential king/rook movement when castling. It uses
a separate display snapshot; undo, new game and load discard an in-flight visual
move. Pause holds it. Host ticks use the nominal PC PIT frequency and the verified
two-tick fallback; this does not establish exact original wall-clock timing.
Original turn/avoidance execution and animated capture battles remain unfinished.
Captures currently update the board immediately.

## Recovered move-command planning

The SHA-pinned BB0E source now constructs native command plans. Quiet movement
uses its intermediate waypoints rather than a direct line: pawn double steps
visit both squares and knights take the original three-part path. Castling uses
both actor paths. Intervening pieces remain present in the display snapshot.
The planner retains parent relationships, operation arguments, capture branches
and whether the original call actually supplied its extra argument; omitted
arguments are not silently admitted as known zero values.

The static-sprite adapter currently executes move waypoints only. Turn/face,
neighbour avoidance, paired capture tasks and audio
still need their full executor. Promotion remains legal chess but its animation
caller normalization is not yet established, so it uses immediate presentation.
Tests cover known paths/capture branch structure and 2,910 generated legal plans;
these do not establish full command-scheduler or original binary equivalence.

Original perspective/rectangular geometry is now available through `geometry.h`.
The data is bound to a retained REA read and independently compared with the
original expanded image; no original executable is needed at game runtime.
Tests compare every 320×200 pixel plus borders with the recovered pointer routine,
and all standing-frame choices with recovered `queue_piece`. This module now supplies placement and hit testing for the playable board. The source names `flat`/`tilted` mean perspective/rectangular respectively.

## Original board rendering

The default view renders background00 and the recovered setup00 character frames;
V switches to background01 and setup02 icons. BCP3 packages authenticated indexed
pixels with signed anchors. Index zero is opaque on backgrounds and transparent
on sprites. The renderer preserves aspect ratio at 2× logical scale and clips to
the original 320×200 scene. Actors are sorted back-to-front by their original y
anchor. Standing-frame choice and mouse hits use the verified geometry module.
Perspective movement uses recovered walking frames and their native control
streams; rectangular movement retains the original static eight-position mode.
Turning and battle playback are not yet implemented.
The surrounding controls are native UI, not a reproduction of the DOS menus.

## Walking playback

BCP3 also contains 465 authenticated composed walking frames. Native motion
selects the sequence from the recovered command direction and graphics piece
mapping, steps its exact control bytes through `bc_task_ready`, and interpolates
with the original frame-count divisor. Completion occurs on the next ready call
after the final frame. No arbitrary animation FPS or invented delta frames are
used. All 96 profile/kind/orientation move-task traces match retained original
machine-code frame identities, readiness calls and completion calls. The game
currently selects control profile 0; both profiles are exported and tested.
Sound opcodes remain preserved in control data, but runtime audio dispatch is
not connected yet. Turn transitions and neighbouring-piece reactions remain
separate pending tasks; this milestone covers walking along the planned paths.

The native turning task executor is now tested against all480 retained native
turn traces, but is not yet connected to the game display. One queen turn-list
continuation needs original XOR composition rather than direct selection of a
precomposed frame; `recovered_turn_tasks` records this rendering limitation.

The queen continuation discrepancy now has a native XOR compositor solution.
It matches all2112 retained cumulative frames and fresh original-machine checks
of the affected turn. These components still need live command/render integration;
the desktop game currently retains its walking-only movement presentation.

Perspective gameplay now plays original turning frames, terminal resting turns
and rook face sequences through native XOR composition. Facing is retained
between moves. The rectangular view remains the faster static-piece view.
Capture battles, neighbour reactions and sound remain pending; the development
label and full-port goal remain in place.

The capture-task engine now has original frame/control sequences and a tested
attacker/defender completion barrier (288 retained cases and144 paired runs).
It is not yet connected to board motion: visible capture battles remain pending.

Capture-positioning primitives are now implemented and checked against576
retained effect/offset task traces. They preserve the original distinction
between a displayed position and the anchor used by the following task.
Multi-actor command execution and visible battle integration remain pending.

A four-slot command dependency scheduler is now validated against unchanged
recovered queue code across1000 programs. It preserves concurrent branches and
original slot-reuse dispatch ordering. Its connection to live capture rendering
is still pending.

Perspective captures now use the concurrent actor renderer: both participants
perform their recovered battle sequences, then the defeated actor is removed.
The e4xd5 scene is render-tested;30 legal piece-kind pairings complete the host
executor. Battle coverage remains partial: captures requiring the unfinished
neighbour reaction currently fall back to an immediate board update. Sound is
still pending. The desktop launcher uses this updated development build.
