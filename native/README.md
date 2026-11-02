# Battle Chess — native Linux port

A playable C/SDL3 port using the recovered game code, artwork, animation tasks
and opening book. It runs as a Linux ELF executable, without DOSBox, a CPU
interpreter, CHESS.EXE or the DOS compiler at runtime. The original reconstruction
remains preserved separately. The older Rust prototype is not used.

## Play

Open **Battle Chess Native** on the desktop, or run:

```sh
./native/run.sh
```

Click a piece and its destination. The side panel has all primary controls:
levels0–9, new game, undo, player mode, pause/resume, save/load, board view,
sound, draw claim, quit and custom minutes. Keyboard shortcuts appear on buttons.
A promotion dialog offers queen, rook, bishop or knight; Escape cancels that move.
Custom minutes accepts1–32767; Escape or zero preserves the previous setting.
Novice bypasses the book; other levels use it where history matches, then search.
The default is Human (red) versus Original (blue). Click the **F1 Red** or
**F2 Blue** buttons (or press F1/F2) to cycle each side through Human, Original,
and Stockfish. Select Stockfish for one side and Original for the other to watch
an engine match; either colour can use either engine. After a controller change,
engine play waits 1.5 seconds from the last selection so you can cycle through
choices. The panel shows “Choosing controller...” during this delay.
Space pauses/resumes.
H resets to two human players or the default human-versus-original pairing.
U undoes a full turn against a computer, or one move in an engine match.
Save/load preserves the game history; engine choices remain session settings.

Stockfish 17.1 is installed locally on this computer. The adapter searches
`BC_STOCKFISH` (an executable path), `/usr/games/stockfish`, the local installation
under `~/.local/share/battle-chess/stockfish/usr/games/stockfish`, then PATH.
On other machines install Stockfish separately or set `BC_STOCKFISH`.
It runs as a separate UCI process with one thread and 32 MB hash. Stockfish has
an independent target depth, default **18**. Click **F3 Depth -** / **F4 Depth +**
(or press F3/F4) to select 1–128. Both Stockfish sides use that setting.
There is no thinking-time cutoff: it searches until the target depth is reached
(or the engine finishes earlier, such as on a solved mate). Space cancels and
pauses; changing depth cancels the current Stockfish search and restarts at the
new depth when unpaused. High depths can take a long time. Original-engine
levels and custom minutes do not control Stockfish. Depth is not an Elo setting.
Depth and engine selections are session settings.
Initial position and complete move history are sent to preserve repetition
context. Every returned move must match a native legal move before play.
Missing engines, protocol failures or invalid moves pause the game with a
message; change engine and press Space to resume. No silent engine fallback.

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

The latest full functional run passed 47 tests, including full games, perft, original
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

## Checkmate finale

In perspective view, checkmate plays a visual-only battle against the losing
king using the recovered capture choreography. As in `present_check_91dc`, the
last mover is preferred when it attacks the king; otherwise another checking
piece is selected. The final tableau remains behind the original wording,
“Check and mate...Game over.” Press N for a new game or U to take back and
continue. Flat view shows the result without the battle. Save/load and the
legal chess position retain the king and the actual mating move: the theatrical
capture is never admitted as a legal move. The result panel uses native controls,
not the DOS modal dialog implementation.
