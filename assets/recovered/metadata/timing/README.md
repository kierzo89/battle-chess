# Animation timing metadata and startup selector — v2

New stage only; v1/native files and Workbench are unchanged. Commands:

```
matching/build/test-env/bin/python -B asset_recovery/animation_timing_v2/verify.py
matching/build/test-env/bin/python -B asset_recovery/animation_timing_v2/event_tick_oracle.py
matching/build/test-env/bin/python -B asset_recovery/animation_timing_v2/export_timelines.py
```

## Nonzero offset is a failed-startup path, not missing normal tables

The original comparison block700C checks entered text against the challenge's
XOR6A encoded move. On success, its input pointer addresses the terminating NUL.
Native708D uses that byte twice: source table base+byte; destination pointer table
base+48*byte. Thus a successful response selects **zero** and populates the normal
144 piece-control pointers. 832 native comparisons covering416 distinct original
move strings and case-swapped forms all select0 on the first attempt.

The shipped executable has patched flow at707E/7087 allowing initialization after
three failed attempts. A nonempty unmatched third response can select its first
unmatched byte, shifting the pointer writes away from the normal piece table.
An empty or matching-prefix third response also selects0. Twelve native wrong/
prefix/attempt-count cases verify that distinction. None of these bytes denotes
an additional legitimate animation profile.

Native selector block708D..70E5 was tested for all256 values for each of the two
source bases (512 cases). The source1C62 scans complete in all256 test cases;
source2A98 completes only for0..18. The other237 cases reach beyond original
initialized DGROUP bytes; the harness stops at that first read and records a
hold. It never zero-fills or invents data to claim a valid stream. Nonzero cases
are invalid-path diagnostics, not accepted alternative assets. Both selector0
runs exactly reproduce the previous144 exported control pointers per profile.

## Exports and timing units

`report.json` binds288 piece-control mappings to kind/orientation/direction and
bank-list indices, and retains144 capture controls and72 capture sequence
mappings. `timelines.json` maps144 profile-specific capture sequences (4,304 frame
events) and96 moving-piece sequences (1,172 frame events) to exact control event
positions. Every capture sequence has exactly one nonterminal readiness record
per emitted frame. An FF control tail stays ready on subsequent calls; it does
not cut an animation short when the explicit delays run out.

These are source-derived mappings using native-verified control-event traces;
this stage does not claim full task/display execution. Effect/offset variants
can consume half or all of a list. Continued turns can skip entries/reset the
control stream; capture completion synchronizes both actors. Those caller rules
remain in the recovered sources and are stated as boundaries in the export.

Five original next_event184D + ticksEA5B probes establish native timing behavior:
normal mode requires at least two BIOS ticks since its previous generated tick
event, queued/physical events take priority, and late polls set the previous time
to now rather than issuing catch-up frames. Alternate mode pumps queued input
instead of this BIOS fallback. The BIOS INT1A results and input queue producers
are explicitly substituted; the actual wrappers and comparison branches run.
No constant FPS or measured seconds-per-frame is asserted. Metadata is expressed
in eligible task-readiness/dispatch calls; pause, modal input, audio dispatch,
queue priority and machine speed may alter elapsed wall-clock time.

## Evidence boundaries

Native bytes are authenticated against the original complete EXE hash. Retained
REA initializer evidence is `ev_e5b249b7ccbe3be330d71dc039c00f5a75bf2ce36767e27655d31b662025eaec`.
The comparison oracle starts with declared answer/input/attempt state; it does
not emulate text entry or random selection. Its restore-region call is a no-op.
The selector block runs unchanged with bounded original source reads. Reports
pin consumed source/evidence files. No canonical matching credit is granted.

Asset table coverage for normal startup is now explicit. Remaining timing scope
is **whole task-variant playback and runtime wall-clock observation**, not an
unknown normal control-table offset or a need to guess FPS.
