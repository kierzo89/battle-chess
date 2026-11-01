# Fixed 6167 dual-switch extent proof

`dual_switch_extent.py` implements only `dual_inline_switch_6167_v1`. The existing ordinary contiguous-function policy remains unchanged. An explicit branch in `extent.validate_extended_extent` and the production checker's supported-profile list route this fixed proof. The function is now canonical.

This proof admits exactly image6167..6795 (1583 bytes), `_run_command_6167`, unit `run_command_6167`, genuine Microsoft C5 OMF under `/AS /Zi`, and the pinned original CHESS identity. It permits no code-address remapping, other function, size, compiler profile, extra proof field, masked comparison, cropped extent, or caller-supplied byte pattern.

Original Ghidra retains five ranges totaling1547 reachable bytes across1583 bytes. Two dead two-byte jumps and two sixteen-byte compiler switch tables account for all36 omitted bytes. Both dead jumps are EB20 and duplicate their preceding live jump to the corresponding post-table continuation. Each dispatcher subtracts1, bounds AX by7, doubles the index, and jumps through eight CS-relative offset words. The exact original words target retained case-block starts; the first table has repeated cases, so eight entries do not imply eight distinct blocks.

The proof contract requires:

- One original DOS real-mode analysis profile for all records, exact subject/operation/load/language/format, and distinct retained evidence identities.
- Exact five ranges,1547 reachable bytes,1583 span bytes,87 closed CFG blocks and their independently pinned complete edge graph. CFG intervals cover every retained byte exactly once, no gap/table byte, and all blocks are reachable from the entry.
- Fresh full-context raw read of1636 bytes: the entire1583-byte executor plus the entire adjacent53-byte function at6796. The complete linked executor must equal the retained original bytes. Fixed body and next-body SHA256 values are independently checked against the hash-pinned original unpacked image and its unmodified file prefix in the tests; every byte of both bodies is authenticated, not just the next prologue.
- A separate empty original global-xref result for every omitted byte:4 dead-code bytes plus32 table bytes. These are39 evidence records in total including body/raw/next. Incoming dossier references cannot enter an omitted byte. These observations are static-provider evidence, not a claim to enumerate every possible dynamically computed reference.
- An independent fresh1583-byte CodeView3 procedure. Both dispatch operands and all16 table words require actual own-CODE, segment-relative OFFSET16 OMF fixups, with their observed explicit own-segment table frames and target-derived dispatcher frames. All18 are mandatory. Extra/overlapping/out-of-bounds fixups, fixups overlapping a dead gap, or nonrequired fixups entering a table are rejected. A nonzero natural object public offset is supported; the helper never changes public/segment metadata.
- The exact final six-byte register/stack restoration. Production compilation, source validation, strict linking, complete original-image comparison, full raw-fixup audit and exact MZ-set comparison remain independent requirements owned by the existing builder/source proof.

The retained original records are `evidence/rea_animation_driver_6167.json`, `evidence/rea_dual_switch_6167_full_context.json`, `evidence/rea_command_next_6796.json` and36 `rea_dual_switch_xrefs_<loaded-address>.json` files. The source worker's proof is `evidence/command-executor-6167-match.json`; its canonical candidate and100-fixup proof remain separately owned by that worker/root.

The focused tests compile the final genuine source freshly and first validate the complete unmodified evidence. Mutation fixtures omit only unrelated native value-flow/raw duplication for performance. Tests challenge every executor byte even when raw and linked mutants agree, all53 following-body bytes, every retained CFG block boundary and edge, every range boundary, all36 xref addresses/results/identities, every one of18 required fixups, duplicate/out-of-bounds/wrong-frame/overlapping fixups, fixed target/profile identity, raw completeness and independent CV boundaries. The verifier itself never edits original or compiler bytes.

Pinned body SHA256: `95f0a8797b4462a0e965035362ba8ef68d9e98cdb453f0e6f091bbf38e13cfa2`.
Pinned next-body SHA256: `d7a237b4ba1983a8bbe4be0445d1a7cb1869e580a47795a00029bf2f4828f7b4`.
Pinned normalized87-block CFG SHA256: `b3e92a29ce57493bbab98533ed9866d2bcc98e34f9e8a06a59e90644a283147e`.

The canonical source is now `src/command_render_flow_match.c`: two board/display
routines, three command-queue routines and this executor form one complete
2,430-byte CODE contribution at5E18..6795, under `/AS /Zi`. All151 fixups and
the empty original MZ set agree, including four loader-base controls. Its even
start satisfies WORD alignment and no CODE byte lies outside the six complete
procedures. The previous isolated tail/alignment conflicts therefore need no
metadata edits or fabricated helpers. The complete proof is
`evidence/command_render_flow_match-contribution.json`.

Actual initialization advances the task pool in24-byte strides, corroborating
the executor's24-byte AnimationTask record. Word0 and unnamed record bytes
retain their observed accesses without invented semantics. CurrentControls
and AssetState unions supply shared named/indexed views across the queue,
executor, manager and unloader; the asset-state initializer is independently
source-defined. Historical module names and the full source-link manifest
remain unproved.
