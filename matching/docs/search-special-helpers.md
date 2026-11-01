# Castling and en passant search helpers

`src/search_special_helpers_match.c` reproduces both complete functions with
the pinned Microsoft C 5.00 compiler and `/AS /Zi`:

| Function | Original complete body | Bytes | CodeView3 offset and length |
| --- | --- | ---: | --- |
| `stage_b860` | B860..B8F3 | 148 | 0, 148 |
| `stage_b8f4` | B8F4..B9B9 | 198 | 148, 198 |

The first tests the two castling candidates from the existing `castle` table.
The second recognizes the previous pawn's two-square advance and tests adjacent
en passant candidates. Both call the existing legality and search validators.
The eight-byte Move union layout and all external names/bases agree with the
canonical neighboring source and registry.

The legality call uses a by-value Move. This ordinary aggregate-call shape
reproduces the original register push at B98F; spelling the same ABI as four
separate scalar/union arguments causes this compiler to push the local stack
slot instead and emits two extra bytes. This is source-shape evidence, not a
claim about recovered original identifier names or declarations.

Retained REA dossiers are `evidence/rea_search_next_b860.json` and
`evidence/rea_search_helper_b8f4.json`; both contain one complete contiguous
body. Production checker builds verified the full REA extent, independent
complete CodeView procedure extent, and complete relocation-resolved byte
equality. Both exact original MZ relocation-site sets are empty. No emitted
bytes were trimmed or patched.

`evidence/search_special_helpers_build.json` retains complete expected and
linked bytes, source/object/tool hashes, relocation records, and production
results. `build/search-special-units.json` is the registration proposal.
Canonical registry, checker, and parser files were not edited.
