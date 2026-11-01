# Fixed 6AB1 dead-return-jump proof

`effect_task_extent.py` implements only `effect_task_gap_6ab1_v1`: `_effect_task_6ab1`, image6AB1..6BF8, complete328-byte ordinary Microsoft C5 `/AS /Zi` output and the pinned original CHESS target. The single new route in `extent.py` changes no existing profile or ordinary contiguous-body rule. Production checker whitelisting and registration remain owned by the parent.

The exact retained Ghidra body has two ranges totaling326 bytes. Its omitted EB09 at6BE8..6BE9 follows the live return jump at6BE6 and reaches the same six-byte epilogue at6BF3. The profile admits neither other gaps nor other function/size/compiler combinations.

Required evidence comprises the original `rea_task_next_6ab1.json`, complete515-byte `rea_effect_task_6ab1_full_context.json`, adjacent complete187-byte successor dossier `rea_task_next_6bf9.json`, and two distinct empty global-xref records for16BE8 and16BE9. All must identify the same pinned target and DOS real-mode profile. Every byte of the328-byte procedure and every byte of the entire187-byte successor is authenticated with independently fixed SHA256 values; tests derive them from both the original unpacked image and its unmodified file prefix after checking the complete original-file hash. A next-function prologue alone is insufficient.

The complete13-block observed CFG is pinned, closed and reachable from the entry. Its nonoverlapping intervals must cover each of the326 retained bytes exactly once and neither gap byte. Dossier incoming references and the two global-xref queries must not enter the omitted jump. These are static-provider observations rather than a claim about every possible computed runtime reference.

A fresh328-byte CodeView3 procedure is independently required. All12 original compiler fields are mandatory external OFFSET16 relocations with the observed frame/target method, call-versus-DGROUP mode, width, zero displacement, and exact position relative to the procedure. Missing, duplicate, extra, overlapping, out-of-bounds, wrong-mode or gap fixups are rejected. A natural nonzero public offset remains supported. The fixed body bytes authenticate the actual stack probe and final register/stack restoration; the source declaration also binds the observed stack helper.

Body328 SHA256: `939d511f0a9f8fb077fc7d8f86d0d348cdcb2a867032cb0c8c6a7c03626561cc`.
Next187 SHA256: `9d03c22879cf936c25fa4c4e492645f076239efff9e4adb3fed1a48b7b36e682`.
Normalized13-block CFG SHA256: `7e0788534542ad11e0a538612c349fa414a1579893f5c6f9d3b48a676c58367e`.

`tests/test_effect_task_extent.py` compiles the final genuine source freshly and validates the unmodified complete evidence before using compact mutation fixtures. It prefers the canonical unit after registration; the checked-in policy-unit record supports pre-registration tests without an ignored-build dependency. Tests challenge every paired linked/raw body-byte mutation, all187 following-body bytes, every CFG block boundary and edge, both retained range boundaries, all proof identities/profiles, both global gap queries, all12 relocation fields, duplicate/out-of-bounds/overlapping/gap fixups, raw completeness and independent CV boundaries.

The source worker retains the full C proof and independent raw OMF audit in `evidence/effect-task-6ab1-match.json`. Production compilation, complete target comparison and complete MZ-site equality remain required independently of this helper. This function's observed odd original start still needs genuine enclosing source context for a complete WORD-aligned module link; this profile does not claim a standalone module placement or add alignment bytes.
