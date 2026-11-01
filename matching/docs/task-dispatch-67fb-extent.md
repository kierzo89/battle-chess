# Fixed 67FB eight-word switch proof

`task_dispatch_extent.py` admits only `task_dispatch_switch_67fb_v1`: ordinary Microsoft C5 `/AS /Zi`, `_dispatch_tasks_67fb`, image67FB..68E9, complete239-byte CV procedure and the pinned original CHESS identity. The existing switch and dual-switch profiles are unchanged; `extent.py` adds only a separate explicit route. No general byte-gap permission is introduced.

The retained body has exactly three ranges and221 reachable bytes. The omitted bytes are the dead EB20 at687C..687D and the eight CS-offset words at688E..689D. The former repeats the preceding live jump to689E. The dispatcher at687E subtracts1 and bounds AX by7 before its indexed CS jump; its exact words target the eight retained case-block starts. The final six bytes are the observed register/stack restoration.

Required evidence is the original dossier `rea_task_next_67fb.json`, full694-byte read `rea_task_dispatch_full_context.json`, adjacent complete455-byte function dossier `rea_task_next_68ea.json`, and18 distinct empty global-xref records covering every omitted byte. All records must share the same pinned target and DOS real-mode profile. The helper authenticates every byte of both the239-byte function and its entire455-byte successor; it does not rely on a next-function prologue alone. The tests independently derive both fixed digests from the hash-pinned original unpacked image and unmodified file prefix.

The exact22-block CFG must be closed, reachable from the entry, cover all221 retained bytes once, and cover no table/dead byte. All block boundaries and edges are pinned. Incoming dossier references cannot enter an omitted byte. Empty global xrefs are retained static-provider observations, without a claim to enumerate every possible dynamically computed reference.

A fresh whole CodeView239 procedure is mandatory. The dispatcher operand and all eight table words require nine actual own-CODE segment-relative OFFSET16 fixups, with their observed frames, zero displacement and the actual compiler segment. Every supplied fixup must remain within the full procedure without overlap; extra fixups cannot touch a dead gap or table byte. A natural nonzero public offset is supported and tested (the genuine three-function queue source places this function at object101). Code/metadata are never cropped or patched.

Body SHA256: `be3523108d77df90d37e3d0e54258f71135a4ca99ac9cb7fa2ea93d417fa24ab`.
Next455-byte body SHA256: `cf746bc9b7ec08cdbcee16c297363242fadf62b407f23273a84733060f83638d`.
Normalized22-block CFG SHA256: `dd5f1b08f7a9a8a0aa10e0a6dce488e8f5f51d6af06d5242dbd31c7d983a053a`.

`tests/test_task_dispatch_extent.py` compiles the genuine source freshly and first validates the unmodified complete dossiers. It prefers the canonical unit after registration; a checked-in retained unit supports pre-registration tests without an ignored-build dependency. Mutations cover every linked/raw body byte even when both mutants agree, all455 next-body bytes, all18 xref results/addresses/identities, every CFG block boundary/edge and each retained range boundary, all9 required fixups, duplicates, overlaps, out-of-bounds or wrong-frame fixups, fixed scope/profile identity, raw completeness and independent CV boundaries. Unrelated large native-value-flow duplication is omitted only from the mutation fixtures for performance.

Production source compilation, complete target comparison, full raw OMF relocation audit, complete MZ-site equality and coherent contribution proof remain independent requirements. The source worker retains those in `evidence/task-queue-move-6796-6ab0-match.json`; this helper does not substitute for them or grant assembly/table bytes separate authored-C credit.
