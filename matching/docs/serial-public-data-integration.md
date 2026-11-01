# Serial CODE and initialized PUBLIC DATA in one C object

The canonical `src/byte_io_serial_match.c` now defines the two real initialized
`int` globals alongside its six existing procedures. Microsoft C5.00 `/AS /Zi`
emits one object with complete344-byte CODE and complete4-byte PUBLIC DATA.
All six independent CodeView extents cover CODE with no holes or trailing bytes.
The DATA publics are `_serial_irq` at0 and `_serial_base` at2, initialized to4
and0x3f8. The canonical registry builds all eight reviewed units from this one
source, flags and compiler object; it no longer compiles the standalone globals.

This adds zero C or DATA byte credit: six functions and both DATA definitions
were already counted. It replaces assumed external bindings within COM2 setup
with the compiler's actual two internal DATA references. Their untouched OMF
fields retain group1 frames, segment2 targets, offsets330/336 and addends2/0.
The restricted relocator adds the independently evidenced DGROUP offset2EBC;
it neither rewrites the OMF object nor substitutes external symbol records.
Its logs keep `target_symbol: null` and separately identify the owned public.
The complete344 code bytes, all31 code fixups and all four original MZ sites
remain exact.

The new `owned_data16.py` gate authenticates the complete CODE/CV union, DATA
allocation, PUBDEF bounds/types, DGROUP members and both raw internal fixups.
It rejects extra storage, holes, tails, communal/iterated allocations, aliases,
DATA fixups, interior addends and stale external placements. A pure structural
gate permits relocation without reading target files. The checker separately
requires both the full four-byte REA primary and each public's own two-byte
primary before extraction. Their expanded-image credit never becomes packed
file credit. Fifteen focused tests cover the positive fresh compiler object,
negative contracts, all raw fields, full CODE/MZ equality and target-free linking.

[Integration journal](../evidence/owned-public-data-integration.json) retains
both proposal and fresh canonical builds. The earlier two-order authentic
Microsoft LINK experiment remains a separate control of these group relocations;
its diagnostic callback implementations are not original game definitions.
Historical translation-unit ownership and a complete source-built executable
remain unproved. The full byte matching goal stays active.

The complete production regression passes all394 tests in672.182s without
skips. The full checker passes all340 reviewed units and correctly reports
that the independent executable is incomplete. The mixed-object dependency
inventory has150 physical source objects with no duplicate globals or
actionable declaration conflicts. See the
[immutable checkpoint](../evidence/verification-188-owned-data-checkpoint.json).

The189 follow-up additionally requires all six CODE PUBLICs to remain ungrouped.
All16 final PUBLIC-DATA tests pass, including mutations of every CODE public.
This tightens metadata rejection without changing emitted code/data or credit.
The394 full-suite result above precedes189; the final full registry checker and
focused32-test result are recorded in the189 checkpoint.
