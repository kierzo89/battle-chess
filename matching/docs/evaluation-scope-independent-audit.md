# Independent evaluator scope audit

A fresh independent pinned MSC500 `/AS /Gs /Zi` compilation reproduces the
coordinator's scoped source and exact OMF object hash. Its complete3902-byte
CODE contribution equals original image FDF2..10D2F, including emitted final
alignment. All eleven independent CodeView procedures match the original
complete bytes and exact MZ relocation sets when each public is placed at
its natural object offset plus two in CS0FDF. Internal call targets use these
actual public positions; no contradictory per-function placement is needed.

The two mutation helpers now match their complete103/130 bytes. The only
source change from the frozen prior candidate is an ordinary lexical block
around each helper's mutation statements, closed before the return expression.
Existing local variables remain declared in the outer function block.

An independent negative control puts a lexical block around only the return
expression instead. That source still emits the old105/132-byte helpers and
a3906-byte CODE contribution. Merely adding braces therefore does not explain
the result. Ending the scope in which the mutation expressions were generated
allows this compiler to reuse SI for the subtraction temporary, eliminating
the previous DI save/restore. This is an inference about compiler intermediate
expression lifetimes based on the controlled instruction changes, not a claim
that the C globals or outer automatic objects have shorter language lifetimes.
The original historical source's brace placement is not uniquely established.

`evidence/evaluation_scope_independent_audit.json` retains both complete source
snapshots, fresh compiler commands/logs/pins, object hashes/artifacts, every
CodeView extent, complete linked/expected bytes, loader-site verification,
and full CODE comparison. The audit records equality with the coordinator's
independently retained object and linked bytes. The reproducer is
`build/evaluation-scope-audit/audit.py`.

The requested option matrix was stopped when the coordinator found the source
scope explanation. It produced no successful retained option-control object
or matching credit; no configuration conclusion is claimed from that aborted
work. This audit changes no canonical source, configuration, registry, or
checker and introduces no duplicate registration credit.

A subsequent fresh two-profile control on the latest canonical scoped source
confirms `/AS /Gs /Zi` and `/AM /Gs /Zi` both reproduce all3902 CODE bytes and
all eleven complete procedures in natural public order. Unlinked CODE bytes,
linked CODE bytes, all PUBDEF records, EXTDEF index/name maps, CodeView procedure
metadata, complete MZ sites, and CODE fixup semantics are identical. Only the
CODE segment name changes from `_TEXT` to `UNIT_TEXT`; attributes remain48 hex
(PUBLIC combine2, word alignment). No claim uniquely recovering the original
command line follows from this equivalence.

The new control is retained separately in
`evidence/evaluation_scoped_memory_model_control.json`, with full source snapshot,
source/object/tool hashes, command/log records, normalized fixups, every linked
procedure byte, and complete CODE bytes. Fixup normalization removes only raw
record placement/encoding while retaining location, width/type, relative mode,
frame/target methods and indices, and displacement. The full object artifacts
remain available for raw-record inspection. Reproducer:
`build/evaluation-scoped-model-control/probe.py`. The historical3906-byte medium
model control is preserved separately and unchanged.
