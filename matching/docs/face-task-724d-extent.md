# Fixed 724D complete C dead-return proof

`face_task_extent.py` admits only `face_task_gap_724d_v1`: `_face_task_724d`, complete191-byte ordinary C5 `/AS /Zi` output at image724D..730B and the pinned original CHESS identity. `extent.py` adds only a separate explicit route; other extent policies and ordinary contiguous-body validation remain unchanged.

The exact original body has two ranges totaling189 reachable bytes. The omitted EB08 at72FC..72FD and its preceding live EB0A at72FA both reach the observed six-byte epilogue at7306. Both branch destinations, exact ranges and full restoration bytes are checked.

Required evidence is `rea_task_handler_724d.json`, complete831-byte `rea_face_task_724d_full_context.json`, adjacent complete640-byte successor dossier `rea_task_handler_730c.json`, and separate empty global-xref records for172FC and172FD. All must have the pinned target and same DOS real-mode profile. The helper authenticates the entire191-byte source procedure and all640 bytes of the successor, rather than a short next-entry prefix. Tests independently derive both fixed hashes from the hash-pinned original unpacked image and its unmodified file prefix.

Body191 SHA256: `72958f0d5e83978839ea35234dd588369e03f3b2517b87f0dd3b6559a1dc8f52`.
Next640 SHA256: `69e982d4ad5d4d8b317e227ca48add9148a1019410a28031a67b5356262cd223`.
Normalized9-block CFG SHA256: `8a44e723368f460cab5948f2f343353b156d32fd3ab6b92a9d80512c8341903b`.

The exact9-block CFG must be closed, reachable, nonoverlapping and cover each189 retained byte once, with neither omitted byte included. Every block boundary and edge is pinned. Incoming dossier references and both empty global queries must not enter either gap byte. Static-provider references are evidence of the observed analysis, without claiming enumeration of every possible computed runtime reference.

Independent fresh CodeView191 and all seven actual external OFFSET16 compiler fields are mandatory. Their positions relative to the procedure, widths, call/DGROUP modes, frame/target methods and zero displacement are checked. Missing, duplicate, extra, overlapping, out-of-bounds or gap fixups fail. A nonzero natural public offset is supported without modifying object metadata.

`tests/test_face_task_extent.py` compiles the final genuine source freshly and first validates the full unmodified evidence. It prefers canonical unit metadata after registration, with a checked-in pre-registration fixture rather than an ignored-build dependency. Mutations challenge every paired linked/raw body byte, all640 successor bytes, each CFG block boundary/edge and both range boundaries, both global gap queries, all seven fixup fields and malformed/missing/duplicate fixups, fixed scope/profile, raw completeness and independent CV extent.

The extent proof does not replace source-faithfulness review, pinned compilation, full target/fixup comparison or complete MZ equality. No padding local, synthetic helper, byte mask, instruction patch or metadata patch is introduced. The compiler's trailing alignment byte lies outside CV191 and earns no procedure credit; standalone enclosing-source placement is not inferred from this per-function proof.
