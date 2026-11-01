# Complete initialized near-pointer DATA

The separate `msc500-pointer-data-omf` backend rebuilds a whole initialized C
DATA contribution with named near-pointer relocations. It grants DATA bytes
only. `cdata.extract_data` remains unchanged and rejects every FIXUPP field.
No pointer DATA earns C function, MZ-site or packed-file credit.

`cdata_pointer.link_pointer_data` derives its entire extent from the independent
PUBLIC WORD `_DATA` SEGDEF and selected public at offset0. It rejects holes,
overlaps, uninitialized tails, iterated data, communal storage, extra nondebug
allocations and inconsistent publics/groups. Only supported external OFFSET16
fields with explicit named DS offsets are admitted. Missing/extra bindings,
unreferenced external names except the unused startup marker, unsupported
frames/widths, overlapping fields and16-bit overflow are errors.

C5 emits external DATA address records in CodeView metadata. These are parsed
record by record: complete supported type records, exactly one bounded kind5
symbol per actual DATA external and its matching FAR16 debug fixup. A segment
named DEBSYM or DEBTYP does not receive a generic exception. All metadata and
raw fixup provenance are retained. Debug fields earn neither bytes nor MZ sites.

The production unit has an explicit `data_address` with paragraph and DS offset.
`reference.validate_data_address` verifies its physical image position and full
initialized extent against the pinned original reference. The frame must match
both original CRT0 BASE16 operands at imageEA91 andEB1C, including their actual
instruction bytes and original MZ sites. The existing complete179-byte REA read
and independently supplied CRT0 member corroborate these operands; see
`pointer-data-dgroup-evidence.json`. This establishes comparison coordinates,
not a recovered original source file or global link map.

All45 menu definitions pass the fresh production path: seven pointer arrays256B
and38 NUL labels396B, totaling652 bytes. The seven arrays contain43 near-pointer
fields. Full exact REA reads are bound separately to every complete unit;44 new
reads supplement the previously retained exact main-table20-byte read. The
original expanded contexts and native menu consumers establish record strides,
sentinels and label boundaries. Alignment bytes between labels stay uncredited.

Two authentic LINK3.65 object orders resolve these45 actual definitions without
backing substitutes or original-address inputs. Both executed consumers check
every record field, all labels and sentinels. Every complete DATA contribution
and all43 fields equal the authentic executable; every name is unique. Only the
consumer code and its expected-string pool are fixtures. The latter's alignment
holes are retained explicitly and receive no whole-pool matching claim.

The16 backend mutation tests and seven production/reference integration tests
cover whole-object ownership, every data field/debug address, actual LINK
outputs, coordinate-frame aliases, the original CRT0 operands and forbidden
bindings. The full regression run and current credit are recorded separately
in `verification-165-menu-data-checkpoint.json`.

Sources and typed fields are in `src/menu_data/`. Original-byte proof:
`menu-data-complete-definitions-match.json`; production review:
`menu-data-production-review.json`; independent real-source LINK closure:
`menu-source-closure-experiment.json`. Original aggregate ownership/order and
the complete program's source link remain unresolved.
