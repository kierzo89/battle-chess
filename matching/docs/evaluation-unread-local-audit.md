# Evaluation unread-local removal control

Four fresh pinned Microsoft C 5.00 `/AS /Gs /Zi` compilations preserve the complete 3902-byte CODE length and all eleven CodeView procedure extents/public placements. The baseline reproduces all eleven original functions. The two independent declaration removals and combined control modify no other source statement.

| Removal | Affected procedure | Complete size | Exact byte differences |
| --- | --- | --- | --- |
| `a` from `pawn_bit_count` | `pawn_bit_count_1094c` | 48 | image10951 frame allocation04→02; image10954/1096D/10975 local displacementFC→FE |
| `e` from `evaluate_candidate` | `evaluate_candidate_10b15` | 538 | image10B1A frame allocation0A→08 |
| Both | Both above | unchanged | Same five positions; other nine procedures remain exact |

Resolved symbolic fixup identities, arithmetic, modes, placements and relocation values remain identical. Removing `a` also reorders several EXTDEF indices; physical OMF record positions and corresponding raw indexed FIXUPP encodings change and are retained explicitly in the evidence. Complete original MZ relocation-site sets still agree for all eleven procedures in all four controls. Fresh object bytes, source/tool hashes, compiler commands/logs, complete linked bytes, all CodeView metadata and fixups are retained in `evidence/evaluation-unread-local-control.json`; reproducible script and all object/binary artifacts are in `build/evaluation-unread-audit/`.

These two current matches depend on unread declarations without a recovered meaningful dataflow role. This audit does not prove what variables existed in the historical source. It supplies no replacement faithful exact source for those two functions. Withdraw candidates are `pawn_bit_count_1094c` and `evaluate_candidate_10b15` (586 procedure bytes). The other nine functions remain byte exact after removing both unread locals. `build/evaluation-unread-audit/retained-nine-units.json` proposes only migrating these nine to `src/probes/evaluation_unpadded_remove_both.c`, without credit for either unmatched function. Canonical files, policies, tests and registry remain untouched.
