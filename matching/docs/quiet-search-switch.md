# Quiet and special search moves

Three further ordinary C functions match Microsoft C 5.00 `/AS /Zi`:
B5EA at 630 bytes, B860 at 148 and B8F4 at 198. All are now part of
[search_engine_a528_b9ba_full_match.c](../src/search_engine_a528_b9ba_full_match.c).
Its eighteen complete compiler procedures cover one aligned 5,266-byte CODE
SEGDEF, A528..B9B9. There are no holes, unowned bytes or padding.

[The full contribution proof](../evidence/search-engine-a528-b9ba-full.json)
accounts for all 493 fixups exactly once, independently relocates the raw
complete segment, verifies all four original MZ sites A536/A55F/A683/B0DB,
and compares every byte under four load bases. This is additional layout
evidence with no duplicate coverage and no historical module-boundary claim.

B5EA generates quiet moves by piece kind and tries promotions where required.
B860 tries castling candidates; B8F4 tries an en passant candidate. These names
describe static behavior, not recovered original identifiers. Their complete
compiler extents and linked bytes match, including all checked stack frames.

## Complete switch extent

REA retains 616 reachable bytes across B5EA's 630-byte span. It omits an
unreachable two-byte branch at B833 and a twelve-byte table at B845..B850.
The source compiler independently emits all 630 bytes. No bytes are cropped,
masked, patched or replaced by assembly.

`inline_switch_zero_return_v1` verifies this particular shape. It shares the
strict six-case switch checks with `inline_switch_table_v1`, while requiring
the exact fifteen-byte tail:

```text
C7 46 FE 00 00  2B C0  EB 00  5E 5F 8B E5 5D C3
```

That is a zero result stored at BP-2, AX cleared, a jump to the shared restore,
both saved registers restored and a near return. The retained CFG must prove
the nine-byte default-return block reaches the six-byte register restore.
The old five-byte-tail proof cannot be substituted.

Both short branches before the dispatcher must target this default block.
The dispatcher must subtract one, bound the result by five, double the index
and jump through the six-word CS-relative table. Every target must begin a
retained case block; no CFG block or edge may enter either omitted region.
All seven fresh own-CODE OFFSET16 fixups are required: B843, then each word
from B845 through B84F. Complete raw bytes, matching profiles, adjacent B860
and the fresh complete CodeView extent are independently checked.

The same production check passes after consolidation at object offset 4290,
as recorded in [the consolidated switch proof](../evidence/search-engine-a528-b9ba-switch-production.json).
Five additional tests attack the tail, dispatcher, fixups, CFG, provenance and
cross-use of proof kinds. Existing extent rules remain mandatory for all
other functions.

## Compatible C interfaces and real DATA definitions

The matched engine and all search callers now use the same typed
`int legal_move(Move)` declaration and identical eight-byte Move types.
The complete 2,692-byte engine also remains exact. See
[the interface proof](legal-move-aggregate-interface.md).

The ray and initial-board consumers now refer to fields of the actual authored
lookup-table aggregate. Two fresh authentic LINK experiments resolve these
ordinary references to one real DATA definition without absolute aliases.
They preserve the complete original-placement 185/130-byte comparisons;
their harness layouts are not claimed as the game's final layout. See
[the DATA/link evidence](game-move-lookup-data.md).
