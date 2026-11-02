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

## Progress: interactive native game and desktop launch

Connected legal rules, history and recovered C search to an SDL3 board. Search
runs on a cancellable background thread with a copied position/history. Added
human/computer and two-player modes, click selection with legal destinations,
undo/new game, difficulty, draw claims and promotion selection. Authenticated
setup-02 artwork uses a visually checked engine-kind mapping; archive order is
not engine-kind order. The square board is host presentation, not a claim of
original projection fidelity. Screenshot inspection caught and corrected the
initial mapping error.

The desktop shortcut now launches this development game; `run.sh --viewer`
retains the independent animation browser. Verified mouse-event e2-e4, asynchronous
computer reply, cancellation, undo and clean close on both SDL dummy/software
and the real desktop video backend. All 12 CTests pass. Source snapshot verifies
1904 files/916 pinned inputs; 13996 asset files and byte-exact banks remain intact.

Goal remains active. Next: persistent save/load, longer full-game validation,
original projection and animation integration, audio and remaining original
search/book/mode fidelity. This is playable chess development, not completion
of the full original Battle Chess experience.

## Progress: save/load and complete native self-play

Previous turn was progress: interactive game and desktop shortcut verified.
Added BCS1 native save files with complete chronological legal history and draw
claim state, CRC32, bounded parsing, legal replay and atomic file replacement.
Failed loads leave the current game untouched. S/L are bound in the UI; loading
joins any running search before replacing state. Smoke tests exercise actual
save/new/load keyboard events in an isolated temporary save file. Original DOS
save compatibility is not claimed; current format supports standard starts only.

Replay/undo, repetitions, draw claims, random history, all byte truncations,
corruption, trailing data and a correctly checksummed illegal move pass. ASan /
UBSan save tests pass. Real-desktop SDL smoke passes. Three full depth-two native
self-play games reach checkmate: seed1 77 plies/120355 candidates; seed2 45/81150;
seed3 98/66643. This is bounded gameplay evidence, not original full-search parity.

Remaining primary obligations: recovered original board projection, movement /
capture animation task execution, sound, opening-book and special-mode fidelity,
original full-search comparisons and further end-to-end visual/gameplay review.
The goal stays active and shortcut remains labelled Development.

## Progress: original presentation timing foundation

Previous turn was progress: native save/load plus complete self-play validation.
Inspected recovered motion/task/audio sources and retained native-byte timing
metadata. Added bounded native task_ready_772d adaptation: countdown calls,
embedded sound dispatch IDs/colour/pitch, and stationary FF ready tails. Tilted
mode bypasses control reads while retaining pending countdown semantics. Added
original signed position interpolation (bounded nonoverflow screen domain), and
two-BIOS-tick fallback with input priority/no late-poll catch-up.

144 authenticated original capture-control streams match 4448 readiness events
and 488 sound dispatches. 20000 interpolation comparisons match the unchanged,
SHA-pinned recovered C function body compiled as a host reference. Retained
original event-clock fixtures cover two-tick threshold, late poll and queued
input priority. Bounds and malformed control tests pass. This is a library
foundation: it is not yet connected to board actors and does NOT claim capture
animation or physical sound playback is implemented.

Audio evidence specifically preserves amplitudes/toggle runs without asserting
absolute sample rates; do not invent a WAV rate and call it original fidelity.
Useful next sources: matching/src/animation_stage_match.c (move/capture command
construction), motion_effect_tasks_match.c and task_tail_handlers_match.c;
assets/recovered/metadata/timing/timelines.json (4304 capture frame events),
metadata/tasks/* and decoded animations. Next connect actor/sequence execution
and original projection, then adapt calibrated sound timing. Goal stays active.

## Progress: on-board native motion integration

Previous turn was progress: task readiness/interpolation verified against retained
evidence. Connected the recovered command-active static-sprite move primitive to
SDL board presentation. Eight positions are emitted, followed by completion;
castling moves king then rook. The display snapshot is separate from authoritative
chess state. Input/search waits for motion; undo/new/load cancels the old display
snapshot; pause preserves motion. Input events suppress that iteration's timer
fallback. Nominal PC PIT-derived host ticks (1193182/65536 Hz) adapt monotonic SDL
time; original physical timing is not claimed.

All 20 legal opening moves and both castling directions pass state/completion
checks; ASan/UBSan passes. Dummy and real-desktop UI smoke tests pass. Mid-move
screenshot visually confirms the moving sprite and vacated origin. Captures are
explicitly excluded from this adapter, retaining immediate chess-state display
until the dual-actor battle executor is integrated. Likewise the original
animation_stage multi-command movement paths and perspective projection are NOT
claimed by this direct endpoint primitive; they remain the next integration.

New source evidence resolves the artwork mapping directly:
matching/src/data/game_kind_map.c maps engine K/Q/R/B/N/P to graphics2/5/6/1/3/4,
explaining the archive ordering found in the prior screenshot review.
Goal remains active: finish original command-stage paths, frame/actor sequences,
perspective board, captures and audio, then remaining search fidelity and UI audit.

## Progress: recovered BB0E path construction

Previous turn was progress: board static-motion integration. Added a hash-pinned
source generator for animation_stage_match.c, capture mapping and graphics-kind
mapping. Original command construction is retained; host sinks collect parent /
operation / square / argument / explicitly-known-extra fields. Omitted DOS call
arguments remain unknown. Record/input waiting is replaced by bounded collection;
transfer effects model recursive stage inputs, not complete task execution.

Quiet board movement now follows recovered per-square waypoints, including the
three-part knight path and king/rook castling paths. Intermediate waypoints do
not mutate occupied display squares; only completed actors transfer occupancy.
The command planner retains capture branches for the forthcoming executor, but
capture playback is not yet implemented. Promotion animation caller normalization
is explicitly held, while promotion chess rules continue to work.

17 CTests pass. Known pawn/knight paths, both castling directions and 2910 legal
command plans pass; source mutation gates reject all three altered inputs even
with Python -O. Sanitized planner/motion checks and real-desktop smoke pass.
These are source/host tests, not full original command-scheduler equivalence.
Next: native turn/face/avoidance/capture execution, original coordinate tables and
background, actual animation frames and audio dispatch. Full goal stays active.

## Progress: original board geometry and standing frames

Previous turn was progress: BB0E quiet-path planner integration. REA read648
initialized bytes at loaded address6CE06, original DGROUP486..1133; evidence
`ev_33511f3aaf0bee60f4b17fd11fa98dd9601b6430e2d4dd2fa8dd96c78046a66f`.
Compared the entire range to independently EXEPACK-expanded original bytes and
confirmed no overlapping relocations. Both original/carrier hashes retained.
The REA session was closed. An initial mistyped address returned zeros and was
rejected; only the independently corroborated range is admitted.

Exported eight coordinate tables to the native geometry module: perspective /
rectangular board anchors and pointer thresholds. Recovered naming is counter-
intuitive: `flat` is the perspective character board, `tilted` is rectangular.
130088 pixel hit results match the unchanged recovered board-pointer C compiled
with observation-only UI hooks. All128 anchors match tables and map back to their
square. Standing sprite selection follows queue_piece_7AA7, graphics kind map
and original frame table; 768 choices match the unchanged recovered C.

All18 CTests pass. These geometry/selection APIs are not yet used by game_ui;
next replace its host square presentation with original background00/01, setup00
character sprites and anchors, retaining clickable selection and motion. Then
connect actor turn/capture streams and sound. Full goal remains active.

## Progress: original boards in the playable SDL window

Previous turn was progress: geometry and standing-frame selection verified.
Replaced the host square-board artwork with authenticated original backgrounds
00/01 and 53 setup00/setup02 frames. BCP2 retains signed anchors and indexed
palette pixels. Background zero stays opaque; sprite zero stays transparent.
Default perspective mode uses original character frames, position-dependent
standing orientations and y-depth order; V toggles the rectangular iconic board.
Both hit testing and segment interpolation use original coordinates. The scene
is clipped at 320x200 and scaled uniformly, with native controls alongside it.

Visual screenshots of both initial boards checked. Both UI smoke paths exercise
mouse-driven e2-e4, a computer reply, save/new/load, undo and a queued V toggle
without changing chess state. Full19-test suite passes; real desktop smoke passes.
Sanitized UI/renderer run is recorded after completion below. Source/asset banks
remain unchanged; all changes are within native/.

Remaining: use walking/turning/delta frames instead of sliding standing sprites,
neighbour avoidance and paired capture executor, sound playback, remaining
book/search fidelity and final controls/gameplay audit. The current eight-step
static primitive applied to perspective view is an explicitly interim rendering
adapter, not original walking playback. Goal remains active.

UI/renderer ASan+UBSan run completed cleanly (engine libraries retain their
separate prior sanitizer coverage). Both updated smoke tests pass after V-toggle
checks were added. No full-game visual-equivalence claim is made.

## Progress: original walking frames in native gameplay

Previous turn was progress: original board/standing renderer integration.
Reconstructed all96 movement control streams from native-verified events and
checked each reconstructed byte string against its retained SHA256. Generated
native descriptors map engine kind/orientation/profile to original bank/list.
BCP3 contains465 authenticated composed walking frames. Perspective motion now
advances actual frames through task readiness and uses original frame-count
interpolation/completion; rectangular mode retains eight static positions.
Current gameplay selects profile0; both profiles are available and tested.

All96 original machine-code move-task traces match complete frame identities,
eligible-dispatch timestamps and completion calls. Full20-test suite passes,
including both UI views. Walking screenshot checked; real-desktop smoke passes.
Sanitized native motion and UI/renderer runs pass. Prior engine sanitizer scope
remains separate. No original binaries/emulation are used at game runtime.

Remaining: turn/face sequences, neighbouring-piece reactions, capture dual-actor
executor and audio. Sound opcodes are retained but runtime callback is not yet
connected. The walk selector uses the planned movement orientation; missing
turning transitions are not claimed solved. Remaining book/search and complete
menu/gameplay fidelity work also remains. Goal stays active.

### Native turning executor (2026-11-02)

Added native turn_animation.c, following recovered turn_task_730c control flow:
shortest signed direction, two-orientation steps for graphics kinds1/3/6,
continuation skip of two entries for kinds1/2/5, and control installation with
same-dispatch readiness consumption. Generated original sequence/control tables
are authenticated against the asset snapshot and individual control hashes.
The executor exposes composed-frame coordinates and sound dispatch callbacks;
it is not yet wired into live motion or credited as complete turning visuals.

All480 retained original-machine-code cases agree on every emitted frame token,
dispatch timestamp and completion call, across both control profiles. Invalid
inputs reject and completion is stable. Full21-test suite passed. An additional
pixel precondition audit checks all40 continuing turn-list boundaries:39 agree,
but graphics kind5 (queen), orientation5, negative direction differs. The
original applies the new delta to the previous actor image, whereas directly
selecting the precomposed next-list frame would assume a different starting
image. This exception is retained explicitly as an unresolved rendering issue,
not accepted as equivalent. Next: reproduce that original XOR composition,
then integrate turn operations and persistent facing into live motion.

No original source/assets were changed. Full port goal remains active; capture
battles, neighbour reactions, sound and remaining search/menu fidelity still
remain as recorded above.

### Queen continuation composition resolved (2026-11-02)

The differing queen boundary is one indexed pixel at relative(1,3), value8 in
list21's final frame and0 in list20's step1. It must not be erased by selecting
an independently precomposed list20 frame. Added native compositor.c preserving
the original descriptor union, four-pixel padded rows and indexed XOR, including
original padding spill semantics. This is a reusable C renderer component,
without an emulator or original executable runtime dependency.

Validation: all2112 cumulative animation frames reproduce the retained original
compositor's complete descriptors and indexed pixel buffers. Added bounded
buffer/palette rejection tests; the same corpus passes UBSan. Fresh developer-
only original-machine checks execute compositor3B3A, fill5A4F and blitterE57A
for all5 deltas in queen turn5->1, including the divergent continuation. The
C result matches every native descriptor and packed-pixel SHA256. Evidence is
native/evidence/queen-turn-composition.json; reproducible using
native/tools/verify_turn_composition.py with the preserved reconstruction as a
read-only reference. The executable is needed only for that developer proof.
No whole native task/renderer execution is claimed: selection follows the
previously checked730C contract, while actual composition is executed natively.

The rendering discrepancy now has a verified implementation. Integration into
live motion remains: retain operation2 turn commands (including terminal turns),
operation6 face transitions and per-actor facing; feed raw delta planes to the
new compositor and renderer. The current desktop game still shows walking,
without these turning operations. Do not equate this component milestone with
finished visible turns or a complete port. Capture/audio/search/menu obligations
remain unchanged; full goal stays active.

### Live turns and rook face transitions (2026-11-02)

Connected the recovered operation2 turn executor and operation6 rook face lists
to perspective non-capture gameplay. The motion adapter now retains terminal
turns and explicit transfers instead of extracting walking commands alone.
BCP4 bundles authenticated raw piece delta planes and logical base widths;
board_view uses the verified C XOR compositor and caches each emitted visual
revision. Persistent facing carries across moves when the visual board agrees
with the next authoritative position; new/load/undo/view changes invalidate it.
The rectangular board keeps its existing static eight-step movement.

Validation: all20 opening moves now exercise turning, walking, terminal turns
and exact final occupied-cell kind/side transfer, without changing chess state.
Both castling tests pass including rook face sequences. Original480 turn traces
and2112 compositor comparisons remain unchanged. Native UI smoke now takes
about13.1 seconds with turn delays; its bound is25 seconds (CTest30), retaining
all move, reply, save/load, undo, cancellation and view-switch assertions.
A rendered turn screenshot was inspected. Full22-test suite passes.

Limits: this serial non-capture adapter does not implement the complete original
command-tree scheduler. Neighbour operation8 is explicitly skipped, captures
are still excluded, and original wallclock/input-dispatch equivalence is not
claimed. Rook face list selection follows recovered6167/724D; the complete
original simultaneous actor scheduling remains to port. Capture battles,
neighbour reactions, audio and remaining search/menu fidelity are still open.

### Native capture task and shared barrier (2026-11-02)

Added capture.c and authenticated generated capture_data.c for original75F6
behaviour: pending1 holds without consuming frames/control, each actor advances
through original lists, sequence exhaustion increments the shared counter once,
and both wait until pending4. Only the right actor adds4 to animation_counter
and requests normal-mode arena cleanup. Host registration rejects duplicate
sides. Cleanup is a notification, not yet the original arena/render integration.
List boundaries explicitly select a fresh initial frame rather than XORing
across lists. The two original empty king/king sequences are retained as empty,
not fabricated; legal play never captures a king.

Validated all288 original retained task cases: frame tuple stream and readiness
timestamps agree with authenticated timing data, terminal calls/frame counts
agree with native task evidence, pending1/pending3 holds and completion cleanup
are checked. Additionally144 real paired host runs cover36 engine-kind pairings,
both timing profiles and both dispatch orders, with actual peer completion and
one-time cleanup. These paired runs validate the native port's barrier; they do
not claim an original whole-game dual-actor renderer execution. UBSan passes the
same cases. The component is linked but not yet called by live board motion.

Next: integrate original placement/offset tasks and concurrent capture branches
with the board renderer, preserving the recovered command dependencies. Current
live captures still update the board without a battle; no capture presentation
completion claim. Neighbour reactions, sound, search/menu fidelity remain open.

### Capture positioning task primitives (2026-11-02)

Added placement.c for recovered6AB1 effect and70EF offset tasks, consuming the
same authenticated piece lists/control streams as walking. Effect emits
floor(frame_count/2)+1 frames and reaches the target on its final frame. Half/
full offsets emit floor(frame_count/2) or frame_count frames, finish on that
last emission, and update actor.old_x/y to the target while preserving the
last rendered position at interpolation step(count-1). Do not force that final
visible position to the target or confuse it with the subsequent task anchor.
Sound dispatch hooks and original command_active readiness handling are kept.

Validation: all576 retained native task cases agree on every emitted frame,
readiness call and completion call across modes, profiles, kinds/orientations
and command_active values. Coordinate outputs separately match the recovered
signed-interpolation formula, already exercised against recovered C elsewhere;
these coordinates are source-derived, since original task traces substituted
interpolation. Invalid modes/kinds/orientations/coordinate bounds reject.
UBSan passes the same corpus. This proves task primitives, not original command
producer policy (which may skip/replace tasks in command_active mode).

The component is linked but not yet used by live capture choreography. Next:
connect a dependency-aware multi-actor command executor, retain both displayed
positions and task anchors, then bind placement and synchronized capture tasks
to renderer frames. The current desktop gameplay remains non-capture animated;
visible capture battles and neighbour reactions remain unfinished, along with
audio and recorded remaining search/menu fidelity obligations. Goal stays active.

### Four-slot dependency scheduler (2026-11-02)

Added commands.c: children start after their parent completes; siblings enqueue
concurrently. The recovered four-slot pool and append scheduling are preserved,
including dispatch67FB reading the completed task's next pointer after freeing
and possibly reusing that exact slot for a child. A naive copied-next iterator
would change which actors advance within a dispatch. Separate recorded roots
remain serialized for recursive castle/EP stages. Invalid topology, unsupported
callbacks and pool exhaustion fail rather than inventing extra actor capacity.

Validation: 1000 deterministic two-branch programs with varied task durations
match unchanged recovered task_queue_match.c on every dispatch return, visit
order and live-slot count. The test substitutes only individual task completion,
command initialization and the recovered pool contracts; it is a source-level
queue equivalence check, not whole original-machine capture proof. ASan/UBSan
pass the same harness. Additional tests cover captured plan dependencies from
e2-e4,d7-d5,e4xd5, serialized roots, reused-slot ordering and rejection cases.

The scheduler is linked as a reusable component. Live board motion still uses
the older serial non-capture adapter. Next integration must attach per-slot
turn/move/placement/capture state and render both actors while preserving source
anchors, visible positions, actor identity and transfer/removal timing. No new
visible-battle completion is claimed. Full port remains active with capture,
neighbour, audio and remaining search/menu obligations intact.

### First live concurrent capture battles (2026-11-02)

Connected commands/turn/walk/placement/capture primitives in choreography.c with
32 stable actor identities, a square-to-actor map, four reusable task contexts,
separate displayed/anchor positions, per-actor facing and original transfer/
removal ordering. Frame programs remain intact until a replacement actually
emits its first frame. Authoritative chess state is never mutated by animation.
BCMotion now routes perspective captures to this executor. BCP5 contains the
original composed capture frames in addition to walking and raw turn deltas;
the renderer depth-sorts all visible actors and draws both battle participants.
Missing capture textures reject bundle loading.

Verified: e4xd5 runs153 eligible dispatches, shows52 dispatches with two battle
actors and finishes with one cleanup,31 visible pieces and exact final board.
All30 legal attacker/victim kind pairings (six attacker kinds, five non-king
victims) complete host choreography and final occupancy correctly in constructed
positions. The rendered e4xd5 smoke test passes and screenshot was inspected.
All28 tests passed across the completed runs; the first full invocation was
terminated with143 during UI smoke, so tests12..28 were rerun and passed, with
modified capture tests rerun after the final frame-retention fix.

Limits: plans containing neighbour operation8 are rejected up front and the
current UI falls back to an immediate board update for those captures. This is
not complete battle coverage; implement the neighbour task next. Exact original
whole-game scheduling, simultaneous pixel ordering and real-machine wallclock
behaviour remain beyond these component/source comparisons. Capture sound
callbacks are not wired to an audio device. The interface now labels battles
partial. Promotion presentation and remaining sound/search/menu obligations
remain open; full goal stays active and the baseline copies are unchanged.

### Live neighbouring-piece reactions (2026-11-02)

Implemented recovered6BF9 operation8: seven eligible dispatches interpolate a
static actor frame through signed direction-table offsets, then update the
anchor. It does not consume a piece-control delay stream. Shared direction
selection now also supplies effect positioning. Choreography no longer rejects
plans containing operation8. Non-capture perspective moves with neighbours use
the multi-actor scheduler too, replacing the old adapter's skipped reactions.

Validation:968 coordinate/direction scenarios agree on every visible position,
anchor update and completion result with unchanged recovered special_task_probe.c
compiled using explicit16-bit DOS words/union overlays. Its interpolation hook
uses the separately verified native interpolation primitive. ASan/UBSan pass.
All20 opening move programs still finish with correct final occupancy/facing.
An occupied-path knight capture b1xc3 exercises both neighbouring c1/c2 actors,
retains them and restores their exact displayed/anchor coordinates. The UI smoke
passes with the computer knight using concurrent neighbour motion (~13.7sec).

This removes the explicit operation8 fallback for captures. Full battle coverage
is still not claimed: promotion presentation, all board contexts and complete
original-machine scheduler/renderer equivalence require further work. Sound and
remaining search/menu fidelity stay open. Original snapshots are unchanged and
the full-port goal remains active.
