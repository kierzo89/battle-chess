# Task, UI and shutdown source reconstruction

This checkpoint adds eleven complete C procedures, totaling 1,385 bytes, to
the prior 153-function registry. The compiler remains pinned Microsoft C 5.00.
An additional two-byte typed initializer is independently verified in the
expanded image. It earns no compressed-file coverage.

| New procedures | Bytes | Canonical source |
| --- | ---: | --- |
| Display reset and input update | 121 | input_display_flow_match.c |
| Two error wrappers | 65 | error_messages_match.c |
| Schedule, unlink and dispatch tasks | 340 | command_task_flow_match.c |
| Movement and effect task handlers | 783 | motion_effect_tasks_match.c |
| Staged shutdown | 75 | exit_wrapper_match.c |
| Asset-seek error hook | 1 | state_ui_flow_match.c |

Each procedure is compiled from ordinary C before the original bytes enter
comparison. Complete compiler CodeView extents, OMF fixups, original REA
observations and original relocation sites are mandatory. The default profile
`/AS /Zi` matches the new UI/task/shutdown sources; the coherent state source
uses `/AS /Gs /Os /Zi`. This establishes compatible profiles rather than unique
historical flags or translation-unit ownership. `/Zi` supplies independent
compiler procedure boundaries.

## Complete source context

The command/task source emits exactly 2,770 CODE bytes at image 5E18..68E9:
nine procedures, 178 fixups, no segment relocations, no padding or extra
procedures. Its WORD alignment is satisfied. The independent complete raw
fixup pass, all four load-base controls and production procedure checks pass.
See `evidence/command_task_flow_match-contribution.json`.

The state/UI source emits exactly 1,216 bytes at 8F88, covering thirteen
procedures and one original final NOP. All 149 fixups and four load-base
controls pass. The NOP receives no function credit. REA independently found
the one-byte RET at 941A, its original caller at CB84, and its complete
one-byte function extent. The existing asset-seek source calls this hook;
its empty C definition is supported by that evidence. See
`evidence/state_ui_flow_match-contribution.json` and
`evidence/rea-941a-seek-hook.json`.

The input/display source emits all 160 bytes at 083E..08DD, with its legal even
origin and both original far-call relocation sites, 0873 and 08B0. The existing
39-byte input routine migrates without duplicate credit. See
`evidence/input_display_flow_match-contribution.json`.

The movement/effect source contains 783 exact procedure bytes at 68EA..6BF8.
Its final compiler NOP differs from the next function's first byte; the complete
784-byte CODE segment remains visible to the source inventory, and its tail
earns no credit. Both handlers now share the observed byte-17 `framecounter`
field in the 24-byte task layout. The two error wrappers similarly retain
their unequal compiler tail. These fragments still need enclosing source
context before a whole-program link can be claimed.

## Original evidence and narrow extent policies

The task dispatcher contains a real inline eight-word jump table and a dead
two-byte branch. Its fixed policy requires the original 239-byte body, all
three retained ranges, 22 closed CFG blocks, eighteen empty global-xref
observations, nine own-CODE fixups and the entire next 455-byte function.
Every byte of both bodies is pinned. See `task-dispatch-67fb-extent.md`.

The effect handler contains a dead two-byte branch omitted from the reachable
body. Its separate fixed policy requires all 328 original bytes, thirteen
closed CFG blocks, both empty global-xref observations, twelve external
OFFSET16 fixups and the entire next 187-byte function. See
`effect-task-6ab1-extent.md`. Each policy has seventeen mutation tests;
the ordinary extent policy remains strict.

The shutdown wrapper matches all 75 bytes and three MZ sites, including the
observed empty stage-three check and authentic far segment:offset operands.
Its original stage variable at DS:0048 is a 16-bit comparison operand. REA
reads its complete initializer as 0000; `int init_stage = 0;` independently
emits those two bytes. See `evidence/exit-wrapper-match.json`,
`evidence/exit-error-interface-production.json`, and
`evidence/init-stage-data-experiment.json`. Its original storage owner and
absolute final source-link placement remain unresolved.

## Retained negative controls

The next task handler at 6BF9 has a 187-byte C candidate with 186 equal bytes.
Its stack-frame reservation is four instead of twelve. It receives no match
credit; unused padding locals would not explain the original source. Other
optimization profiles also fail. See `evidence/special-task-6bf9-negative.json`.
The 2D13, 2E34 and 35A0 frame/local allocation discrepancies remain unresolved.

All counts, fresh full-suite results and remaining whole-source context
obligations are recorded in `evidence/verification-164-checkpoint.json` and
the generated progress report. A complete independently built and packed
executable is still required for the full-byte goal.
