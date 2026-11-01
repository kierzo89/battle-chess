# Search setup and recursive entry matches

The four functions below now use the shared canonical source
[search_engine_a528_b5ea_full_match.c](../src/search_engine_a528_b5ea_full_match.c).
The fifteen functions emit the complete aligned
4,290-byte CODE segment A528..B5E9 with no padding or holes. The complete
[proof](../evidence/search-engine-a528-b5ea-full.json) supersedes the isolated
odd-start contribution limitation discussed below. It does not establish
the original historical translation-unit boundary.

Four more search functions reproduce696 original bytes with C5.00 `/AS /Zi`:
stop test A68B(71), setup A6D2(199), window wrapper A799(80), and recursive
entry A7E9(346). Complete retained REA bodies agree with every independent fresh
CodeView extent. Canonical production builds compare every relocated byte.

The stop test performs a signed32-bit time comparison and checks the selected
side's mode. Setup initializes24-by2 eight-byte move slots, clears the first
check-state element and scans each side's home row. The original loops compare
against inclusive23/1 bounds. The two-byte stack slots also depend on the
compiler's local-name allocation; the source's identifiers are analyst choices.

The window/entry pair shares one six-byte `SearchOptions` declaration. The
observed ABI passes alpha, beta, depth, three option words and a near Move
pointer. Three MOVSW instructions copy the options by value. The entry advances
the222-byte search frame, checks its limit, initializes its18-byte prefix,
evaluates the quiet-position bound, invokes generation and restores the frame
pointer before returning. Later reconstruction identifies the stage word at
offset 28; the remaining fields are still reserved storage.

In the earlier isolated experiment, both functions compile together to426 matching CODE bytes with contiguous
80/346-byte procedure extents and no end padding. Their odd target start A799
does not satisfy the contribution's word alignment, so this is a source/type
consolidation experiment rather than an established original object boundary.
The canonical source now incorporates the neighboring functions as described
above. No preceding code or alignment placeholders receive credit.

The original standalone and combined proofs are retained in
`evidence/rea_moves_a799_match.json` and `evidence/moves-search-entry.json`.
Current sources use the archived library name `memcpy` and the canonical
`attacked_9a50` name; fresh canonical source/object hashes are in
`build/report.json`. These identifier/prototype corrections preserve all bytes.
