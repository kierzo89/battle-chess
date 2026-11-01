# Promotion search B3E6

`src/promotion_search_match.c` builds the complete 100-byte original function
B3E6..B449 using the pinned Microsoft C 5.00 compiler and `/AS /Zi`.
The ordinary C sets the current history move's promotion flag, tries promotion
kinds two through five using `try_move_ab58`, returns success when a candidate
is accepted, and clears the flag before returning failure.

Fresh REA evidence `evidence/rea_search_helper_b3e6.json` records one complete
contiguous 100-byte body. Its assembly observes both the local result variable
and promotion-kind loop; the decompiler's inferred return constant is not used
as source evidence. The compiler independently emits a CodeView3 procedure of
exactly 100 bytes. Production checking verifies complete relocation-resolved
byte equality and the exact empty original MZ relocation-site set. No bytes
were trimmed, patched, or supplied through assembly.

Full linked and expected bytes, source/object/compiler hashes, and relocation
records are in `evidence/promotion_search_build.json`. The proposed unit is in
`build/promotion-search-units.json`. Canonical registry and checker files were
not edited.
