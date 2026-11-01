# Evaluator small/medium model control

The identical ordinary source `src/evaluate_candidate_probe.c` was freshly
compiled with pinned Microsoft C 5.00 using `/AS /Gs /Zi` and `/AM /Gs /Zi`.
Both profiles reproduce every byte of the complete 538-byte evaluator and
26-byte abs procedure, with independent CodeView3 extents and exact original
MZ relocation-site sets. The complete unlinked 854-byte CODE payload and every
public's segment/offset are also identical between profiles.

| Profile | CODE SEGDEF name | Attributes | Combine | Length |
| --- | --- | --- | --- | ---: |
| `/AS /Gs /Zi` | `_TEXT` | 48 hex | PUBLIC (2) | 854 |
| `/AM /Gs /Zi` | `UNIT_TEXT` | 48 hex | PUBLIC (2) | 854 |

Medium model changes the segment name, not its combine class: `UNIT_TEXT` is
still PUBLIC, not PRIVATE. `UNIT` is the runner's fixed DOS source basename
(`C:\UNIT.C`). Distinct real source basenames under this model would name
distinct CODE segments, allowing independently named code contributions rather
than requiring every file's code to coalesce into `_TEXT`. This is a viable
configuration lead for code spanning more than one 64 KiB segment. It does not
uniquely recover the original command line or prove the eventual original
full LINK layout. Existing unresolved helper placement differences remain.

The control script is `evidence/evaluator-memory-model-probe.py` (the original run script is retained
in `build/evaluator-model-control/probe.py`). Its runtime-only
override of `msc.compiler_config` appends `/AM` to the probe's allowed flags.
It changes no runner or configuration files; the ordinary-source policy and
all pinned compiler/tool manifest checks remain active. The script asserts
the canonical config bytes are unchanged before and after both builds.
Canonical registry, flags, and match credit are unchanged.

`evidence/evaluator_memory_model_control.json` retains both fresh object hashes
and paths, full compiler commands/logs/tool pins, source hash, SEGDEF records,
public records, complete compared procedure bytes, and relocation logs.

The runner now directly supports `/AM` for pinned MSC500 and an explicit
validated `source_name` such as `EVALA.C`. That later API extension preserves
the default `UNIT.C` behavior and all tool/source restrictions. Fresh tests
confirm named `/AS` and `/AM` builds preserve a complete far procedure while
changing its CODE segment name to EVALA_TEXT under medium model. The original
control's probe-local override is retained as historical reproduction data;
canonical unit flags still remain individually specified.
