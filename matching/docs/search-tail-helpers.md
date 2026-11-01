# Search helpers B2AE and B383

`src/search_tail_helpers_match.c`, compiled using the pinned Microsoft C 5.00
profile with `/AS /Zi`, reproduces both complete original functions:

| Function | Image range | Complete bytes | Independent object boundary |
| --- | --- | ---: | --- |
| `prune_b2ae` | B2AE..B382 | 213 | CodeView3 procedure, offset 0, length 213 |
| `update_b383` | B383..B3E5 | 99 | CodeView3 procedure, offset 213, length 99 |

The first helper checks repetition and the reversible-move count, adjusts the
child search bounds using signed division of `first_score` by four, and reports
a draw. The second copies the principal variation, inserts the current history
move, and updates the root score and optional window bound. Both use the same
222-byte SearchFrame and eight-byte Move layout as the canonical neighboring
search functions. External names and placements were taken from the current
registry, including `first_score` at 53F6 and `history_tail` at 88E4.

Fresh complete contiguous REA dossiers are retained in
`evidence/rea_search_helper_b2ae.json` and
`evidence/rea_search_helper_b383.json`. Production checker builds validated the
retained REA extent, independently emitted complete CodeView extent, complete
relocation-resolved byte equality, and exact original MZ relocation-site sets.
Both MZ site sets are empty. Neither function was trimmed or patched.

`evidence/search_tail_helpers_build.json` retains complete expected and linked
bytes plus production build metadata, compiler/tool pins, source/object hashes,
and relocation records. The source SHA256 is
`1a03c08d43628368d7e0dcee52a2aaa95b2139d0fe286ae28cf2827dac8f5b13`.
The registration proposal is `build/search-tail-units.json`; canonical registry
and checker files were not edited in this scope.
