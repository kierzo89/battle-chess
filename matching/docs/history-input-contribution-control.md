# History/input contribution

`src/history_input_contribution_probe.c` compiles with pinned MSC500 `/AS /Zi`
into a complete340-byte CODE contribution matching original B9BA..BB0D.
All four publics occupy their natural original offsets:

| Original image | Procedure | Complete bytes |
| --- | --- | ---: |
| B9BA | unwind_history_b9ba | 125 |
| BA37 | restore_history_ba37 | 120 |
| BAAF | accept_input | 82 |
| BB01 | empty_bb01 | 12 |

The339 procedure bytes have complete retained REA boundaries and independently
emitted CodeView extents. Every linked byte and exact original MZ relocation
set verifies, including the aggregate whole contribution. The final90 atBB0D
is emitted by the compiler and matches the original before stageBB0E. No
padding was authored, removed, masked, or patched.

The source shares the same eight-byte Move union/struct and genuine by-value
apply_9749/notification interfaces used by the history callers. Duplicate
external call aliases are unified with existing source names: message_1296
becomes prompt_1296 with its int-return prototype (the result is ignored here),
and process_872a becomes step_872a. Their original placements are unchanged.
Internal calls bind to actual publics in the same contribution. No artificial
helper extraction or mixed profile is required.

`evidence/history_input_contribution_control.json` retains the full source,
compiler command/log/tool pins, source/object hashes and artifact, complete
procedure bytes and metadata, relocation logs, and whole CODE comparison.
`build/history-input-procedure-units.json` proposes the four-unit source
migration; reproducer `build/history-input-contribution/probe.py`.
This establishes a valid coherent source-built contribution, not unique
historical translation-unit identity or additional function credit. No
canonical source, configuration, registry, or checker file was edited.

## Canonical integration

The live registry now selects src/history_input_full_match.c for allfour
procedures. The canonical340-byte CODE contribution passes both production
checking and the independent raw-FIXUPP pass; see
 evidence/history_input_full_match-contribution.json. The earlier proposal and
control remain historical evidence. No duplicate function or padding credit
was added by this migration.
