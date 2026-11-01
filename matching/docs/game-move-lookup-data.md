# Typed game movement DATA contribution

[move_lookup_tables.c](../src/data/move_lookup_tables.c) reconstructs an 80-byte initialized game-data aggregate at DGROUP `04ea`, image `5d10a`. Fresh MSC5.00 `/AS /Zl /Zi` compilation emits one complete 80-byte `_DATA`/DATA contribution with no holes, LIDATA or data fixups. Every byte matches a complete provenance-bound expanded REA read. This is source DATA evidence, with **zero C function count**; it is separate from independently supplied runtime libraries.

The aggregate contains ordinary typed chess tables, not executable bytes or target-sized filler:

| DGROUP offset | Aggregate offset | Definition | Matched consumers |
| --- | ---: | --- | --- |
| `04ea` | 0 | Eight orthogonal/diagonal steps on a 0x88 board | `init_rays_9840`, move generation |
| `04fa` | 16 | Eight knight steps | `init_rays_9840`, move generation |
| `050a` | 32 | Pawn steps `{16,-16}` | `pawn_attacks_99be`, `piece_attacks_98f9` |
| `050c` | 34 | Mask view, indexed by piece kind; indices 1..6 are `{1,2,4,8,16,32}` | `piece_attacks_98f9`, `init_rays_9840` |
| `051a` | 48 | Two castling endpoint pairs for each side | `generate_a348`, castling helpers |
| `052a` | 64 | Eight initial back-rank piece kinds `{3,5,4,2,1,4,5,3}` | `reset_board_7d26` |

The mask base overlaps the negative pawn step: mask index zero is the representation of `-16`, and is unused by the reconstructed consumers. The source expresses this storage relationship through two typed union views. Its initializer supplies the two pawn steps and six piece masks once. It does not allocate a duplicate mask array, add a pointer global, insert a padding word or rely on a linker alias. The castling endpoints are `{2,4}`, `{6,4}`, `{114,116}`, `{118,116}`. Their dimensions follow side and castling-index accesses in the matched C; the back-rank loop independently runs eight entries.

The aggregate grouping is a reconstructed source choice, not a claim to have recovered the historical source file. Its dimensions, field offsets, values and shared word all have matching consumer evidence. Replacing the existing array extern accesses by fields of this aggregate still reproduces the complete 185-byte `init_rays` and 130-byte `reset_board` functions exactly in fresh compiler probes. The former's mask references become the union mask view at aggregate +34; the latter's back-rank reference becomes aggregate +64. These experiments show a usable route into the eventual source program without adding target-derived public aliases. These consumers are now canonical; migration adds no function or byte credit.

## Complete extent, provenance and comparison

Run `python3 matching/evidence/move-lookup-data-probe.py`. Generation compiles the source and relocates the complete DATA contribution through the existing restricted linker, with DGROUP paragraph `5cc2` and contribution offset `04ea`. Since the DATA bytes have zero fixups, no relocation modifies the initializers. Original bytes enter only the subsequent comparison boundary. The probe saves the newly generated object and full DATA bytes under `build/data-tables/`.

[move-lookup-data-experiment.json](../evidence/move-lookup-data-experiment.json) retains source/compiler/tool-manifest hashes, the complete object hash, SEGDEF/PUBDEF metadata, all CodeView type records, field offsets and the two consumer probe compiles/fixup logs. The source object SHA-256 is `70fd45f984a7332ea6c0649741aeac79d04b1fc04729091cad593948b1367251`; complete DATA SHA-256 is `0e92187da0f261ae417243c8ad09ffa344696e7fcb93585cc1dc9873b4dd6b2c`.

The public `_move_lookup_tables` is at segment 2, offset zero, group 1, CodeView type `0217`. That type is a five-field 640-bit aggregate, independently confirming 80 bytes. CodeView field offsets are 0, 16, 32, 48 and 64; the union's two views each begin at offset zero. `_DATA` SEGDEF attributes are `48` (WORD aligned, PUBLIC), length `0050`. Its single LEDATA covers `[0,80)` exactly. `_TEXT`, CONST and `_BSS` all have zero declared length; the only other allocated content is debug type information. No uninitialized range is inferred or completed.

[rea-move-lookup-data.json](../evidence/rea-move-lookup-data.json) contains the full 80-byte raw read at loaded linear `6d10a`, REA `ev_0b2056e518ded92f7bf180c31f957f3c152266d9f79520c396ec14e53ef7ac24`. It binds the derived carrier SHA-256 `faf3516d0e72e30005ad90cb2da165081af5fe6871f5e8c3663980a5d725ef02` and load paragraph `1000`. The comparison uses `build_reference` on the original hash-pinned executable and `validate_expanded_read(..., emitted_mz_sites=[])`. This requires equality with the complete unrelocated expanded reference and the complete raw REA read; there are no MZ words in this extent to mask or normalize.

## Separate strict DATA extraction contract

[cdata.py](../cdata.py) supplies `extract_data(obj, symbol) -> (bytes, metadata)`. It receives a strict-reader OMF object and a public name, without an expected byte count, original image, placement or byte template. The returned size comes from the complete independently declared SEGDEF, never a next public or desired unit size.

It requires one fully initialized `_DATA` contribution of class DATA, explicitly in DGROUP, with the selected public at offset zero and relocatable 16-bit PUBLIC attributes. Other nondebug allocations must have zero extent. All FIXUPP fields, communal definitions, iterated data, partial coverage, overlaps and reserved tails are rejected. Metadata reports the whole segment, public/type index, DGROUP components, each initializer write and its hash. It does not claim that extraction alone establishes an original match.

MSC5.00 includes an unused `__acrtused` EXTDEF even with `/Zl`. The extractor permits exactly this compiler startup-selection marker, records `startup_marker_unused=true`, and still rejects every fixup and every other external. This is not an unresolved game-data address or a placeholder: the complete DATA bytes require no external value. A full source link supplies the real archived CRT0 definition.

The canonical checker category is language `c-data`, backend `msc500-data-omf`, status `c_data_matched`, with separate source-data unit/byte totals and zero C function count. The proposal under `build/data-tables/proposed-unit.json` contains the full80-byte ownership and expanded-reference requirements. The canonical unit is now registered as move_lookup_tables; its individual raw Evidence is retained in rea_move_lookup_table_read.json. No existing function parser is relaxed to admit a DATA object.

Eight focused tests in [test_cdata.py](../tests/test_cdata.py) cover a fresh typed compile and exact REA comparison, full extents independent of subsequent publics, the startup marker exception, and rejection of code/BSS/extra DATA, missing groups, nonzero public offsets, holes, overlaps, reserved tails, LIDATA, communal definitions, fixups, other externals and corrupted OMF checksums.

## Consumer migrations and two-object authentic LINK proof

The standalone migration sources are now [init_rays_tables_match.c](../src/init_rays_tables_match.c) and [reset_board_tables_match.c](../src/reset_board_tables_match.c). They declare the same typed aggregate externally and use its fields; they contain no table definition, alias public, pointer initializer or absolute address. Their retained registry migration proposal is `build/data-tables/consumer-migrations.json`. Fresh original-placement checks retain the full CodeView lengths and all 185/130 original code bytes. Both sources are now used by the canonical registry. The symbol-binding ledger also records the DATA definition at its original comparison placement, DGROUP04EA/image5D10A; this is not a full source-link placement proof.

[data-consumer-link-probe.py](../evidence/data-consumer-link-probe.py) adds two authentic LINK experiments. Each invokes official pinned LINK 3.65 on **two explicit source objects**: freshly compiled MOVETAB.OBJ and a real consumer object. The latter includes the migration source plus an ordinary executable harness: actual ray storage and clearing for `init_rays`; actual board storage, cell assignment and piece-index maintenance for `reset_board`. These harnesses establish meaningful dependencies rather than absolute aliases or empty functions. They are separate [probe dependency sources](../src/probes/data-link/) and receive no canonical credit.

The pinned archived SLIBC.LIB supplies genuine CRT0, `__chkstk` and their runtime dependencies. Each fresh DOSBox drive contains only MOVETAB.OBJ, CONSUMER.OBJ and the build batch; a read-only tools drive contains only hash-verified LINK.EXE and SLIBC.LIB. No CHESS executable, expanded image or repository drive is mounted. The command is:

```text
T:\LINK /NOD /DOSSEG /MAP MOVETAB.OBJ+CONSUMER.OBJ,UNIT.EXE,UNIT.MAP,T:\SLIBC.LIB;
```

[data-consumer-link-experiment.json](../evidence/data-consumer-link-experiment.json) retains complete commands/logs/maps, all object/source/compiler/tool/library hashes, input mount lists, MZ headers/relocation sites, and the consumer fixup records. Both successful runs have clean linker logs and exactly one `_move_lookup_tables` definition in the public-by-name map. No `_steps`, `_knight_steps`, `_masks` or `_back_rank` alias definitions occur.

| Linked consumer | Complete consumer length | Actual aggregate placement | Aggregate bytes |
| --- | ---: | --- | --- |
| `init_rays` | 185 | DGROUP `0061:0042`, image `0652` | Complete80 bytes, exact to source object |
| `reset_board` | 130 | DGROUP `0070:0042`, image `0742` | Complete80 bytes, exact to source object |

In the first link, the consumer has eleven relocations targeting `_move_lookup_tables`. Their object addends are 0 for ray steps, `10` hex for knight steps, and `24`, `26`, `28`, `2a`, `2c` for the selected mask words. Authentic LINK encodes actual aggregate offset `0042` plus each addend, producing `0042`, `0052`, `0066`, `0068`, `006a`, `006c`, `006e` as applicable. In the second link, both back-rank references have addend `40` hex and encode `0082`. The ordinary external symbol resolves to the real DATA object's public, with no post-link patch.

The runner independently applies the existing restricted relocation implementation using the actual generated map and compares the complete consumer body against the authentic LINK output. It also checks the entire80-byte DATA contribution against the original compiled object, and proves there is no MZ relocation word in that contribution. Original CHESS bytes enter a separate comparison only after every compile and authentic LINK run has finished.

These small executable layouts deliberately differ from the eventual full-program placement; their maps do not claim DGROUP `5cc2` or target consumer origins. They prove actual cross-object source resolution and preserve the original-placement code comparisons. A full source build must supply the other genuine objects and allocation order to reach the final layout.

## Complete engine contribution migrated to the typed table

The twelve-function engine contribution now uses the canonical migration source, [move_engine_9a50_tables_match.c](../src/move_engine_9a50_tables_match.c). Its `CastleEndpoints`, `PawnAndMasks` and `MoveLookupTables` typedef prelude is identical to the actual DATA definition. It replaces `steps`, `knight_steps`, `pawn_step` and `castle` extern arrays by fields of the one `_move_lookup_tables` aggregate at DGROUP `04ea`. Castling uses `destination` and `king_home`, matching the DATA type's actual field names and order.

Fresh MSC5.00 `/AS /Zi` compilation preserves the complete **2,692-byte CODE SEGDEF**, image `9a50..a4d4`. All twelve independent CodeView procedure extents retain their exact lengths, cover that complete segment once without gaps or overlaps, and match every original code byte after ordinary relocation. Whole linked CODE SHA-256 is `be2f86f97dd4a8bedbfbacd6c0906e17f8bd4862d8b10af369f380790906cf41`.

The object no longer declares `_steps`, `_knight_steps`, `_pawn_step` or `_castle`. Seven consumer fixups instead target `_move_lookup_tables`, with actual field addends 0 (ray steps), 16 (knight steps), 32 (pawn steps), and 48/50 (the two castling endpoint fields). `generate_captures` has one such fixup, `generate_quiet` four, and `generate_a348` two. This keeps the same encoded addresses without absolute aliases or extra pointer objects. The other nine procedures remain in the same independently compiled contribution and also pass complete comparisons.

Reproduce with [engine-table-migration-probe.py](../evidence/engine-table-migration-probe.py). [engine-table-migration.json](../evidence/engine-table-migration.json) retains fresh compiler/source/object hashes, the complete segment declaration/writes, all twelve CV lengths, every fixup and complete comparison results. The generation phase receives only source, tools and explicit linker placements; the original executable enters its separate comparison after compilation and relocation.

The source-only registry replacement proposal is `build/data-tables/engine-consumer-migrations.json`. It preserves the existing twelve units, flags, origins, lengths and REA boundary evidence while changing the source path and replacing four external-placement names with the real aggregate. This migration adds no DATA initializer, filler, byte patch, function or matching-byte credit. Other table consumers and the complete source-program link remain separate work.
