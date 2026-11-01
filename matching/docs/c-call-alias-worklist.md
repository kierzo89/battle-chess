# Call aliases before a complete source link

`evidence/c-call-alias-inventory.py` re-links every current C object, verifies
its object/source/body hashes against the fresh report, and decodes explicit
near E8/E9 or far9A/EA operands at the actual compiler fixup sites. It groups
external names by their encoded physical target in original image coordinates.
It neither discovers new functions nor grants new matching credit.

The fresh `c-call-alias-inventory-164-input-io.json` contains535 call/jump sites
to171 target addresses. Seven targets retain multiple provisional external
names, but no credited definition has a mismatched call-site name. Thirteen
former aliases were reconciled in six sources; all49 credited procedures in
those sources retain complete byte equality after fresh compilation. Examples:

| Image target | Definition now used | Former call-site alias |
| --- | --- | --- |
| 07F3 | exit_07f3 | fatal_error |
| 3E4F | reset_graphics_3e4f | clear_actors |
| 7A61 | redraw_piece | animate_7a61 |
| 8F95 | min_i16 | clamp |
| 950D | init_pieces | update_950d |
| BB0E | animation_stage | apply_bb0e |
| FE59 | evaluate_full | draw_progress |

The former draw_progress call encodes the same0FDF:0069 target as the matched
full evaluator; the canonical declaration now uses evaluate_full(void).
Unsigned animation-stage and low-bit types and the byte-fill pointer were also
reconciled with definitions. Original shutdown zero/one-word argument counts
are preserved through the old-style declaration; their historical prototype
remains unresolved. The original command append/begin interfaces also need
further ABI work. See input-io-alias-checkpoint.md and the complete migration
experiment. The historical inventory remains preserved for checkpoint159.

Every inventory row retains the caller, complete body digest, REA evidence ID,
instruction position and actual call mode. Only direct encoded calls/jumps with
explicit fixups enter this worklist; computed calls and complete runtime graph
coverage remain outside its scope. External placements still originate as
reviewed comparison assertions, rather than independent source definitions.
