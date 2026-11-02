# Playable native port completion audit

Verified 2 November 2026. The requested playable Linux port and desktop shortcut
are delivered. This audit does not claim byte identity with CHESS.EXE, perfect
hardware emulation, or whole-game DOS execution equivalence. The objective's
required fidelity limits are explicit below and in the component provenance.

## Requirement evidence

| Requirement | Current implementation and verification | Result |
|---|---|---|
| Separate clean baseline | Work is under `native/` on native-linux. Published checkout is clean at `0b2a2b36155984c7b23f904f60488b8be0feda8c`. Source verifier passes1904 files/916 pinned inputs. | Met |
| Recovered assets preserved | Asset verifier passes13996 files and rebuilds both archive banks byte-exactly. Source/asset generators authenticate their consumed inputs. | Met |
| Native Linux, no DOSBox/CPU emulator | `battle-chess-game` is an x86-64 Linux ELF linked to SDL3/libc and platform libraries. `run.sh` builds C and executes it directly. CPU emulation is confined to development reference fixtures, not game runtime. | Met |
| Original code-based engine/search | Generated hash-pinned recovered evaluator and phased search, source-derived board/attack/move operations, original book generator/scan/rotation/weights. Tests cover recovered attack/evaluation/incremental/history/search fixtures. It is not the older Rust prototype. | Met with limits below |
| Difficulty | Novice and levels1–9 plus custom minutes reach worker configuration. Fake/real deadline tests and actual custom-dialog/worker tests pass. Novice bypasses the book. | Met |
| Chess rules and endings | Perft fixtures; castling, en passant, all promotions, checks/mate/stalemate and history/draw tests. Three search self-play games and a combined rendered game reach terminal states. | Met |
| Playable input and menus | Real SDL mouse/keyboard smoke tests cover board moves, player modes, levels, pause, worker cancellation/undo, save/new/load, board view, mute, draw, promotion, custom time and quit. Actual window render inspected. | Met |
| Artwork and animation | Original perspective/rectangular boards, authenticated sprites/deltas, turn/walk/placement/capture/task-queue/sidestep fixtures; capture renderer,16 promotion cases,28 en-passant cases, four castles. | Met with presentation limits below |
| Sound | Authenticated samples, exhaustive PCM converter tests, SDL queue/pause/mute/drain tests on dummy and local default backends. Reachability test covers455 callbacks/184 distinct pairs across30 legal capture pairings,48 walks and288 turns. | Met with acoustic limits below |
| Save/load | Atomic native BCS1 saves, bounded input/CRC and legal history replay; roundtrip/rejection tests and actual UI save/new/load. | Met |
| Responsive lifecycle | Search thread cancellation/join tested, sound pause/clear tested, regular SDL event processing. Actual desktop launch and WM_DELETE_WINDOW shutdown verified. | Met |
| Full game through presentation | Complete140-ply book/search game to stalemate,34 book moves,26 captures,9053 rendered animation dispatches,1316 valid sound callbacks; no failed animation/fallback accepted. | Met |
| Desktop shortcut | Trusted executable `/home/kierzo/Desktop/BattleChessNative.desktop`, application-menu copy, exact native launcher. `gio launch` produced the native game process/window and clean WM_DELETE_WINDOW shutdown; evidence saved. Development label removed only after playable validation. Existing DOSBox shortcut untouched. | Met |

## Verification run

All42 CTests passed in70.62 seconds. This included the new full-game presentation
test, all previous component/native comparison tests and UI tests. A subsequent
label-only build passed the menu test again. Source and asset snapshot verifiers
were run independently and passed. The final desktop entry was then launched
through GIO on the real X11 display, bound by window PID to the native executable,
and closed through its normal window-manager event; its log confirms clean exit.
See `evidence/desktop-launch-verification.json`. Earlier actual native-window
capture was visually inspected with sound enabled and no held events.

## Explicit fidelity boundaries

- This is a source port. Host threads, monotonic timing, memory sizes, legal
  validation and input ownership replace DOS platform/ABI machinery. Whole
  search/game execution identity is unproven; recovered internal search mode5
  and whole-session RNG/call ordering are not claimed. Normal game difficulty
  uses the documented normal search mode; the recovered opening book is live.
- Native menus, BCS1 saves and host draw policy are adaptations, not DOS-format
  compatibility. The promotion choice precedes the original pawn/capture
  animation rather than reproducing the original after-arrival popup.
- Original perspective task sequences and composition are retained. Some host
  rendering ordering/timing is adapted; rectangular mode uses static pieces
  rather than perspective battles. Full original machine concurrent-frame parity
  is not claimed beyond the specific retained comparison fixtures.
- SDL sound maps authenticated nibble amplitudes to nominal linear PCM. Actual
  PSG/speaker transfer curves, CPU/PIT calibration, alternate audio profile1,
  exact blocking latency and subjective listening quality are not verified.
  Three exceptional authored pairs are outside legal default-profile gameplay;
  they remain rejected rather than receiving invented payloads or rates.
- The desktop launcher needs the installed build dependencies. The port is
  local on native-linux; no GitHub push or distributable package was requested
  for this port and none is claimed.

These boundaries remain visible to users; no tests or original matching gates
were weakened to declare a bit-perfect or emulator-equivalent result. There is
no remaining missing feature in the requested playable native game/shortcut
scope. Further DOS fidelity refinements are separate from that delivery.

### Facing regression correction

Corrected the native engine-side to original graphics-colour mapping: the near
red army uses colour bit 64, and the far blue army uses zero. Standing frames
and post-move terminal turns now face the opposing army. Movement direction
indices and recovered source are unchanged. Verified the rendered starting
board visually; explicit frame tests cover both armies and bishop diagonals,
and motion tests cover all 40 opening moves across both sides. The full suite
passed 41 tests initially; the old mandatory pawn-turn assertion was corrected
(pawns now already face forward), and the expanded motion test passed.

### Optional Stockfish opponent

Added independent Human / Original / Stockfish selectors for red and blue,
including engine-versus-engine play. Stockfish is an external UCI dependency;
the recovered original engine remains the default. The adapter sends the
initial FEN and complete history, verifies returned moves against native legal
moves, and bounds handshake/search waits with cancellable process cleanup.
Failures pause rather than silently switching engines.

Validation: all 45 CTests passed (58.23 seconds), including real Stockfish 17.1
history/cancellation checks and a rendered four-ply UI match switching both
engine colour assignments through mouse and keyboard controls. The new panel
was visually inspected. Stockfish is installed outside the repository in the
user's local share directory; no original source or asset files were changed.

### Theatrical checkmate

Checkmate now invokes recovered capture choreography against the losing king
through an explicit visual-only API. The ordinary stage/move APIs still reject
king captures. Selection prefers the last mover when it attacks the king,
following the recovered present_check logic. Completed actors remain visible
behind the original game-over wording; New Game and Undo clear the tableau.
Flat mode retains a result-only presentation. No synthetic move is appended to
history or applied to the authoritative position.

All 47 tests passed (77.35 seconds), including both losing colours, completed
king capture tasks, unchanged legal state, rejection through the normal move
gate, and a rendered checkmate UI run. Final tableau/dialog inspected visually.

### Public source publication — 2 November 2026

Final full suite: 47/47 passed (81.39 seconds). A clean staged checkout in a
separate temporary directory configured and built the Linux game and assets
successfully, without the development build directory. Source inventory:
1,904 files intact and 916 pinned inputs accounted for. Asset inventory:
13,996 files intact; both banks rebuilt byte-exactly. The root README hash in
the publication inventory was updated for the directory guide and screenshots;
original build source, recipes and binary acceptance evidence were unchanged.
