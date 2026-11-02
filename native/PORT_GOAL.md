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

### Promotion presentation normalization resolved (2026-11-02)

Recovered9371 explicitly copies the history move, changes promotion kind to
pawn6, clears its special flag and calls BB0E before9371's caller invokes
finish93D6 to redraw the selected piece. The recovered redraw7A61 uses queue_piece
at the destination. Stage generation now pins promote_ui_match.c and applies
this normalization after validating the original legal promotion. Promotion
captures therefore use pawn attack choreography, not the future piece's battle.
Choreography remembers the selected kind and redraws its standing pose only
when the complete pawn task program finishes. Both quiet and capture promotion
moves are routed through this presentation in the desktop game.

Validation: unchanged recovered9371 C confirms normalization for all legal
kind/flag classes. All16 full combinations (both sides, four choices, quiet and
capture) complete with pawn motion, correct capture task count/cleanup, selected
final actor, source removal and immutable input. The general stage-plan test no
longer excludes promotions. Existing original-kind mapping and standing-frame
proofs apply to final redraw; no invented transformation animation was added.

UI difference remains explicit: Q/R/B/K preselect a piece before moving; the
original blocking sprite popup after pawn arrival has not been reproduced.
Audio, remaining menu/search fidelity and broader end-to-end presentation
coverage remain open. The full-port goal stays active and originals unchanged.

### Native sound data and nominal PCM conversion (2026-11-02)

Added BCA1 sound packaging for all15 complete amplitude-nibble cache slots.
The generator authenticates snapshot hashes and compares every sample's inverse
attenuation command against the retained original native port stream, including
its81/00 setup bytes. sound.c loads bounded slots and preserves the original
C868 integer interval formula (1e9/denominator + pitch*1120, clamped at zero).
A separate explicitly host-adapted renderer holds those amplitudes at the nominal
interval and maps them to centered linear float PCM at quarter gain. This is
not a physical PSG/speaker transfer-function or absolute-calibration proof.

Native conversion tests and ASan/UBSan pass:1827 nonzero-period pitch conversions
across15 slots, with93 zero-period combinations explicitly rejected. All emitted
PCM samples and frame counts are checked. The new focused CTest passes; prior
30-test runtime suite was not rerun because this component is not yet linked to
the game. No SDL audio playback is claimed yet.

A scan of all recovered piece/capture control streams finds307 distinct authored
sound event pairs. Three are not currently representable:slot11,pitch-64 gives
zero nominal interval, and slot15,pitches-27/-18 have no complete nibble record
in the15-slot package. Resolve the native loader/dispatch context for those
before claiming full sound coverage; do not substitute adjacent bytes or guessed
rates. Physical speaker calibration and alternate speaker-run path remain
separate evidence limits. Next: SDL playback plus explicit event handling and
investigation of these three exceptions. Full goal remains active.

### SDL sound playback connected (2026-11-02)

Added audio_output.c with a mono48kHz float SDL stream, authenticated BCA1 loading,
bounded queued duration, mute/pause/clear and deterministic shutdown. Wired sound
callbacks through both serial motion and concurrent choreography, including
first-frame controls. Original nibble wrapper ignores the colour argument; the
SDL adapter does likewise. UI M toggles mute, Space pauses stream and animation,
and new/load/undo/view/controller changes clear pending sound. Missing audio
hardware leaves the game usable with an explicit unavailable label. The display
shows nominal sound mode and the count of held unsupported events.

To approximate original blocking sound without blocking host input, subsequent
animation dispatches wait while SDL still has queued source data. This is a
host scheduling adaptation, not an exact hardware latency proof; device buffering
may outlast the source queue. Main UI smoke is explicitly muted to keep gameplay
checks deterministic. A separate audio test drives a real capture event through
the callback, verifies queued PCM, pause/mute/clear/rejection and actual stream
drain. It passes with SDL's dummy driver and the local default audio backend.
ASan/UBSan pass the audio glue/converter test (linked presentation libraries were
not rebuilt with sanitizers in that invocation). Audibility/listener quality was
not independently judged. No emulator is used by runtime audio.

Three authored combinations remain held:slot11/-64 zero interval and slot15 at
-27/-18 without a proven complete nibble payload. Linear sample mapping and
nominal timing are still explicitly different evidence claims from calibrated
original PSG/speaker output. Investigate these contexts next; do not call full
sound fidelity complete. Remaining menu/search/end-to-end obligations and the
full-port goal remain active. Original baselines are unchanged.

Integration verification: all 32 CTests passed, including native game, flat view,
full games, capture rendering, sound conversion and SDL output. Repeated the
audio glue/converter ASan/UBSan check successfully. Desktop shortcut and its
launcher remain executable and point to this isolated native port.

### Interactive promotion choice (2026-11-02)

Replaced advance piece preselection with a native modal opened only for legal
promotion destinations. Click Queen/Rook/Bishop/Knight or press Q/R/B/K; Escape
cancels without altering position or history. Other game commands are held while
the choice is open, preventing stale destinations or accidental moves. The
chosen legal move enters the existing pawn-first animation and final redraw.
This improves usable promotion but deliberately does not claim DOS popup artwork
or after-arrival prompt timing: the host dialog currently precedes commitment.

Two real SDL event-path tests cover selecting a pawn/destination, cancelling and
reopening without a move, choosing knight by mouse and by keyboard, completing
the animation and verifying exactly one history move and a knight on a8. Existing
16-case promotion tests retain both colours, four choices and quiet/capture
coverage. All 34 CTests pass (41.55 seconds). Inspected the rendered modal at
1200x732: four choices and cancel instruction are legible and within the window.
No original reconstruction/published files changed; full goal remains active.

### Opening-book move order recovered (2026-11-02)

The book contains pseudo-legal move indexes, not square coordinates. Added
port_book_order.py to authenticate the canonical move_engine_9a50_full_match.c
and generate its append/capture/quiet/A348 functions with explicit native context.
Piece-list identity/order is retained, including the original 80-entry cap.
Host castling rights/legality supply the special castle predicate; en-passant
uses retained position/history context without filtering pinned pawn candidates.
Final-rank unpromoted pawns are rejected before the original unchecked generator.
The result is explicitly pseudo-legal: callers must validate chosen moves.

Authenticated startup-02.raw.bin (32000 bytes, SHA256
 da69b9c1f784f0ea21bec125078d339fc70ad98ed9a095360fbf7045829fc7fb)
contains the original book tree. A recursive traversal consumes 29828 bytes,
including its root marker, and checks all 28636 move edges against the independent
legal generator, with 1191 list sentinels, nine root choices and maximum42 plies.
Root moves resolve to e4/d4/Nf3/c4/f4/b3/g3/b4/g4. No illegal/out-of-range index
was found. This is whole-tree consistency evidence, not a machine execution
comparison or proof of original random selection/stateful book traversal.

Focused CTest passes (1.46 seconds); ASan/UBSan also pass with generated order,
board and rule code all instrumented. The game is not yet linked to the book.
Next: restore weighted sibling rotation and history lookup against the recovered
book_context functions, then integrate book-first play and search fallback.
Full goal remains active. Original reconstruction and published baseline unchanged.

### Original book lookup and weighted selection connected (2026-11-02)

Generated the actual accept_hint_82db, scan_book_843f, rotate_book_8515,
skip_book_8577 and previous_book_858d bodies from authenticated book_context
source, plus authenticated book_weights and embedded startup-02 bytes. Native
adapters replay standard-start legal history, retain original piece identities,
and reject root/history mismatches. Selected moves must pass legal validation;
no-book/invalid-input leaves caller output untouched. TLS isolates worker state.
Host replay replaces original mutable history/UI ownership; no DOS runtime.

An independent structural tree oracle initially exposed a mistaken assumption:
63 sentinels delimit preferred siblings, so weighted rotation wraps before the
remaining recognized alternatives. Corrected the independent oracle to honor
that delimiter; recovered runtime bodies were retained. All1680 sampled weighted
history lookups (all16 draws at selected root/deeper nodes) now agree;44 sampled
leaf histories correctly fall back without changing output. Entire28636-edge
legality/order regression remains separately tested. Full ASan/UBSan instrumentation
of book, order, board and rules passes this selection/replay test.

Computer workers now try book at non-novice levels, then existing original-search
port on a miss. Novice bypasses book as in recovered search_turn_8061. UI reports
"Original opening book" for accepted book moves. The host uses an independent
MS-style deterministic RNG stream, so whole DOS-session RNG sequence fidelity
is not claimed. Original search special mode and broader game/audio/menu fidelity
remain open. Original source/published baseline remain untouched.

Integration validation: all37 CTests pass (59.99 seconds), including a new real
SDL game test that plays a human move, confirms exactly one accepted book reply,
then exercises save/new/load/undo and clean shutdown. The existing novice and
flat-view tests continue to pass. Book selection is now live, not just diagnostic.

### En-passant choreography and retained facing (2026-11-02)

A new rendering regression reproduced a real failure: en-passant moves carry
special=1/kind=6/capture=0, so motion had routed them to the non-capture executor.
The pinned BB0E source explicitly stages a pawn battle on the adjacent victim
square and then a separate pawn walk to the actual destination. Route this move
through concurrent choreography and supply victim kind6 despite capture=0.
Keep authoritative move validation unchanged. The previously failing test now
renders28 en-passant cases (both colours, both directions, every adjacent file)
and all4 colour/side castles to the exact legal final occupancy, with no ghost
victim or input mutation. It checks a completed capture barrier and real battle
frames, rather than accepting a silent redraw fallback.

Also retain the completed choreography's actor facings against the validated
final board, instead of discarding visual state at completion. This prevents
pieces snapping back to default facing and allows the next move to inherit the
actual terminal facing. Failed choreography still invalidates retained visuals.
The special-move tests verify every retained facing and final board-cell identity.
These are native source/runtime checks; no full original machine rendering or
audio latency parity is inferred. Remaining sound/menu/search fidelity work and
the full goal remain active; preserved original trees are unchanged.

Integration verification: all38 CTests pass (62.84 seconds), including the new
special-move rendering regression, captures, promotion, audio and book UI play.

### Mouse-accessible game controls (2026-11-02)

Added a native side-panel control menu: levels0–9, new game, undo, player mode,
pause/resume, save/load, board view, mute, draw claim and quit. Button captions
reflect current mode and the selected level is highlighted. Mouse events use
SDL logical viewport conversion and are translated into the existing keyboard
command dispatch, before board move guards. This keeps controls usable while
paused or during computer search without duplicating command semantics. Pending
promotion remains modal and cannot accidentally dispatch sidebar commands.

The menu is a Linux UI adaptation, not reproduced DOS menu artwork. Custom-minute
difficulty remains available in the configuration API but not yet in this menu.
Inspected the actual1200x732 render: all controls and status text fit and remain
legible. An SDL event-path test clicks player mode, difficulty, pause/resume,
save/new/load, view, mute, draw and undo, then closes via the quit button. Undo
is exercised with an actual worker thread active and must join/cancel it without
committing an extra move. Existing keyboard paths are retained.

Verification: all six affected SDL UI tests pass (45.97 seconds), covering
normal/flat/book play, both promotion inputs and the new control menu. The
previous full38-test run remains the core/presentation baseline; no claim that
all39 were rerun for this UI-only change. Full goal remains active.

### Custom time control exposed (2026-11-02)

Connected recovered level10's minutes*60 budget to the native menu and search
worker. C or the Custom minutes button opens a bounded numeric dialog; Enter or
Apply commits1–32767 minutes. Backspace deletes; Escape, Cancel or a zero entry
preserves the previous level, following set_limit's zero-cancellation behaviour.
The dialog cancels/joins any current worker and pauses animation/audio; closing
restores the previous pause state and resets animation time to avoid catch-up.
Other commands remain held while editing. Existing levels0–9 remain unchanged.

The SDL event-path test opens via the actual mouse button, enters two minutes,
checks a120000ms worker configuration, then verifies both Escape and zero-entry
cancellation retain that level. Difficulty deadline tests separately exercise
actual timed search interruption. The dialog is a native UI adaptation rather
than a reproduction of DOS numeric-dialog artwork. The full port goal remains
active pending remaining sound exceptions and final fidelity/requirements audit.

Verification: all five affected difficulty/UI tests pass (28.12 seconds).
Inspected the rendered custom-time dialog: text, Apply/Cancel and sidebar fit
at1200x732 without clipping. Preserved original trees remain untouched.

### Sound exceptions classified by reachable runtime scope (2026-11-02)

REA static byte evidence ev_0b7373433fc7da0d54324ef3385622abf40ba9a94f7b5f9276454fc38bbbf309
at loaded linear0x20e30 confirms the130-byte original nibble player. The first
0x10e30 query was the wrong load coordinate and is not used as playback evidence.
The native delay is unsigned interval/speed then signed16 quotient-minus10,
clamped to one loop; zero wrapper interval is not a native silence instruction.
No physical clock/sample-rate claim follows from this static observation.

The previous broad control scan included unreachable sequences. Retained timing
records place slot15/-18 and15/-27 only in alternate profile1. Live native tasks
select profile0. Slot11/-64 occurs only for the left/victim graphics kind2 (king)
against kind5 (queen): legal chess never captures a king. These are not missing
sounds in the legal profile0 game. Preserved classification is in
native/evidence/sound-reachability.json; no fabricated slot15 or guessed minimum
interval was introduced. Unsupported-event rejection remains intact.

Added runtime callback coverage: all30 legal attacker/victim pairings (victim
king excluded),48 walking orientations and288 valid turn transitions produce
455 callbacks /184 distinct pairs. Every pair has a loaded sample, positive
nominal duration and a per-event frame count within the SDL adapter's10-second
limit. Existing exhaustive converter tests verify actual PCM generation.
This resolves the three-event blocker for the native game's selected profile;
it does not claim alternate-profile support, physical PSG/speaker emulation,
queue-latency accuracy or subjective listening verification. REA session closed.
