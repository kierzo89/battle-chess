# Native animation task variants

This follow-up executes original CHESS.EXE task bytes and the original readiness interpreter in Unicorn. It adds no canonical matching credit. Run `matching/build/test-env/bin/python -B asset_recovery/animation_tasks_v3/verify.py` and `matching/build/test-env/bin/python -B asset_recovery/animation_tasks_v3/extended.py` from repository root.

## Exhaustive exported-data checklist

- PASS 960 move, effect, offset-half, offset-full and face scenarios: both control profiles, all 6 piece kinds × 8 orientation mappings, normal and command-active modes. Full emitted frame token sequence and readiness call numbers checked independently against the previously native-verified control metadata. Completion calls checked separately.
- PASS 480 turn scenarios: both profiles, all source/destination orientations for kinds 2/4/5 and all even source/destination orientations for collapsed kinds 1/3/6. Native completion, frame identities, continuation skips and last source orientation checked against independent sequence selection. Native frame/resource call numbers exported; no separate independent whole-turn timing simulator claimed.
- PASS 288 capture scenarios: both profiles × 72 side/piece/opponent sequence records × normal/command-active modes. Entire frame token stream and readiness timestamps checked. Pending=1 blocks, sequence exhaustion sets state255 and increments pending2→3, pending3 waits, pending4 completes. Right-side completion alone adds4 to animation_counter; normal mode restores/manages arena and command-active mode does not. This injects partner completion at the synchronization barrier; it is not a dual-actor renderer integration run.

## State and timing rules

Move emits all f frames and completes on the following ready call. Command-active move uses the same static frame for eight ready calls and completes on call8 (zero-based); it does not consume delta frames. Effect emits floor(f/2)+1 frames and completes on its last frame. Offset emits floor(f/2) or f frames according to its initial inverted flag, completing on its last frame. Face advances once per eligible task invocation, independent of control-stream delays. Turn installs the orientation-specific control stream and consumes its first ready instruction on the same call as the initial frame; continuation kinds1/2/5 skip their first two list entries. Collapsed kinds1/3/6 turn by two orientations; opposite-parity destinations are outside the enumerated reachable domain.

Capture crosses each list boundary by switching to a new initial frame; it does not XOR across distinct lists. Its terminal control FF remains ready, allowing a subsequent call to observe sequence termination. State255 is a task synchronization state, distinct from the control FF byte. Cleanup requires the shared pending counter to reach4.

See prior animation_timing_v2 for the source-linked 432 control streams and startup offset interpretation: ordinary valid startup uses selector0; failed third challenge nonzero offsets are not alternate animation timing profiles. The normal event fallback waits at least two BIOS ticks, while queued/input/alternate-mode processing has other paths. These call counts are not fixed FPS or guaranteed wallclock durations.

## Proof boundaries

The original task machine code and readiness routine run unmodified. Native writes are bounded to task/actor/known motion/synchronization state and stack. Rendering, resource dispatch, scratch allocation and interpolation are substituted named contracts. Composition records frame identities rather than pixels (parent's separate composition proofs cover pixels). Attach uses source-linked coordinate/frame state updates but does not execute display sorting or blitting. Interpolation records native arguments and returns deterministic coordinates; exact native interpolation is not independently tested here. Therefore this stage proves animation selection, delay use, task transitions and capture barriers under these contracts, not full game scheduling/render/audio integration.

Remaining integration boundaries: command-list dispatch and producer scheduling, simultaneous two-actor capture processing in the real caller, exact interpolation/position arithmetic, resource/audio side effects, and observed real-machine wallclock cadence. Transfer and special operations do not become decoded animation frame metadata merely from these tests. No invented durations or FPS are added to recovered assets.

Source anchors: matching/src/move_task_match.c (68EA), effect_task_match.c (6AB1), offset_task_match.c (70EF), face_task_match.c (724D), turn_task_probe.c (730C), task_tail_handlers_match.c (capture75F6/readiness772D), graphics_actor_menu_match.c (attach/compose contracts).
