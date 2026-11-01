# CRT0 data allocation and authentic LINK emission

The archived CRT0 `_DATA` contribution is an 88-byte **DATA allocation with 12 explicitly initialized bytes and 76 bytes reserved without data records**. It is not an 88-byte LEDATA initializer, and its gap is not a BSS segment. Authentic LINK 3.65 emits all 88 bytes, filling the internal reserved gap with zeros because an initializer follows it at offset 86. This independently explains the original zero bytes without importing them as generator input. No canonical parser/checker rules or coverage totals were changed.

## Independent object ownership

[crt0-data-experiment.json](../evidence/crt0-data-experiment.json) retains every unchanged CRT0 OMF record, checksums, segment extent, public symbols and fixups. Inputs retain the [runtime library pins](runtime-link-plan.md): whole SLIBC.LIB SHA-256 `7eabd615308e9a05de24f6e6e82e61a65f733eb64d12b5318d8b3ed569e389b9`; CRT0 member at library offset `10`, 863 bytes, SHA-256 `c8fa9ca0b70762defb91b280d9676eafda5fceb47475344937eb3f281c9a8705`.

| OMF object record offset | Record | Meaning |
| --- | --- | --- |
| `66` | SEGDEF `98`, attributes `48`, length `0058`, segment index 3 | `_DATA`, class DATA, WORD alignment, PUBLIC combination |
| `70` | SEGDEF `98`, attributes `74`, length `0800`, segment index 4 | STACK, paragraph alignment and STACK combination, no data records |
| `7a` | GRPDEF `9a`, payload `05 ff 03 ff 04` | DGROUP includes `_DATA` and STACK |
| `123` | LEDATA `a0` | Segment 3, offset 0, ten zero bytes before fixups |
| `134` | FIXUPP `9c` | Fixups at data offsets 4 and 8 |
| `142` | LEDATA `a0` | Segment 3, offset 86, two zero bytes before fixup |
| `14b` | FIXUPP `9c` | Fixup at data offset 86 |

There are no LIDATA records in CRT0 and no BSS SEGDEF. In particular, object bytes `10..85` are absent from data records; they are not a hidden repeated-zero initializer. Segment 3's final initializer ends exactly at its declared byte 88.

| Data offset/range | Ownership and symbolic meaning |
| --- | --- |
| `0..1` | Explicit zero word `__asizds`, later written by startup |
| `2..3` | Explicit zero word `__atopsp`, later written by startup |
| `4..5` | Explicit word plus OFFSET16 fixup to code `__exit`; public `__aexit_rtn` |
| `6..7` | Explicit zero offset word at `__abrktb` |
| `8..9` | Explicit word plus BASE16 fixup to DGROUP; DOS MZ relocation required |
| `10..85` | 76 reserved bytes with no data record |
| `86..87` | Explicit word plus OFFSET16 fixup to segment 3 + 6; aliased publics `__abrkp` and `__abrktbe` |

The table interval `__abrktb..__abrktbe` is 80 bytes. Its first four bytes form the initialized far address DGROUP:0000; the remaining 76 bytes fit nineteen more four-byte slots. The archived STDALLOC `__myalloc` references `__abrktb`, `__asizds` and `__psp`, corroborating a runtime allocation-table role rather than an application table. Its independently pinned member metadata and fixups are retained in [crt0-data-consumer.json](../evidence/crt0-data-consumer.json). These facts do not require reconstructing table contents from the game.

## Fresh standalone authentic LINK control

[crt0-data-probe.py](../evidence/crt0-data-probe.py) freshly extracts the pinned member and compiles ordinary [link-only dependency definitions](../src/probes/layout/crt0_dependencies.c) using pinned MSC5.00 `/AS /Gs /Zl`. Those empty functions/globals satisfy the declared externals; they are not runtime replacements or code-match candidates. No reference executable, decoded image, repository drive, library of game code or target byte array is mounted. Each LINK run sees only unchanged CRT0.OBJ, the new DEPS.OBJ, its batch file and the independently pinned official LINK.EXE (SHA-256 `124a3c800edc16b60f696d35a9dfec798b68b78fe2ca90c5988ea76bdeab1a8a`).

Reproduce with `python3 matching/evidence/crt0-data-probe.py`. The retained report contains source/object/compiler/tool-manifest hashes, all commands, full logs/maps and complete MZ metadata. An initial CRT0-only control fails with fourteen unresolved externals. `_edata` and `_end` are supplied by LINK; the other fourteen definitions are required, including declaration-only `__acrtmsg` and `__nullcheck`. The runner rejects errors and does not accept merely existing output files.

Three successful runs establish:

| Control | CRT0 data allocation | DATA word at 4 | DATA word at 8 | DATA word at 86 | Saved SP |
| --- | --- | --- | --- | --- | --- |
| CRT0 + DEPS, `/DOSSEG` | Image `d6..12e`, DGROUP `000d`, offset `0006` | `00c8` = mapped `__exit` | `000d` = DGROUP | `000c` = mapped `__abrktb` | `0800` |
| DEPS + CRT0, `/DOSSEG` | Same image range and group | `0014` = moved `__exit` | `000d` | `000c` | `0800` |
| CRT0 + DEPS, `/DOSSEG /STACK:4096` | Same image range and group | `00c8` | `000d` | `000c` | `1000` |

All 76 gap bytes are zero in each complete fresh MZ image. The file-backed image ends at `12e`, immediately after the final data word, while `_edata` is DGROUP `005e` = image `12e`. The common/BSS contribution follows, and `_end` is image `140`. Therefore CRT0's own startup clearing interval begins **after** all 88 DATA bytes; it cannot be credited with initializing the internal gap. LINK has materialized that gap in the file.

All three successful MZs contain exactly the three CRT0 relocation words: the two code DGROUP loads and the data BASE16 field. The data site is image `de` = `d6+8`. Object order changes code placements as expected; it does not require patches to the archived object. `/STACK:4096` changes SP from `0800` to `1000` and minimum allocation from `0082` to `0102` paragraphs while leaving the complete data contribution unchanged. This supplies a viable source-link control for the original saved SP, but does not prove the original linker used that option rather than combined stack contributions.

## Original comparison and future backend contract

`reference.validate_expanded_read` now accepts an explicit `emitted_mz_sites`
collection. It first requires the independently linked bytes to equal the full
unrelocated reference, requires the exact original relocation-site set, then
adds the known load paragraph `0x1000` modulo 65536 at those words and compares
every raw REA byte. Missing, extra, duplicate, overlapping or crossing sites
fail. Default calls continue to reject MZ overlaps. Focused tests use the full
88-byte CRT0 observation and authentic LINK emission controls below. This
comparison support does not establish source allocation or matching credit;
the future generation backend remains necessary.

A complete 88-byte REA read of the expanded original is retained in [rea-crt0-full-data.json](../evidence/rea-crt0-full-data.json), `ev_eb11974642b5184238f458c3821fa148fe06be7418c5da92bbfc78020ee21459`. It is bound to carrier SHA-256 `faf3516d0e72e30005ad90cb2da165081af5fe6871f5e8c3663980a5d725ef02`, load paragraph `1000`, address `71578`. Thus the original unrelocated contribution starts at image `61578` = DGROUP `5cc2:4958`.

The original words at offsets 4, 8 and 86 are respectively `ec15`, `5cc2` and `495e`, exactly the independently established `__exit`, DGROUP and `__abrktb` placements. REA displays `6cc2` for word 8 because its known MZ loader adds paragraph `1000` at image `61580`; this is one exact forward addition, not masked comparison. Every other word is zero, including the reserved gap. This is consistent with the authentic standalone emission rule; standalone stub code addresses are deliberately not claimed to match original runtime addresses.

A narrow future authentic-LINK backend can safely require: pinned unchanged CRT0 identity; exact four SEGDEFs and GRPDEF; exact two DATA writes, gap and three fixups above; freshly generated legitimate dependency objects; a successful isolated pinned LINK invocation; full public/map bounds; all 88 bytes extracted from its declared allocation; and exact MZ relocation accounting including data offset 8. Preserve a provenance distinction between twelve object-initializer bytes and seventy-six linker-materialized reservation bytes. Do not route this through the C function parser or silently permit arbitrary holes in existing runtime units.

To compare an authentic whole-program result at original addresses, legitimate object ordering must actually place `_TEXT` CRT0 at `ea86`, its DATA contribution at DGROUP `4958`, DGROUP at `5cc2`, and the real `__exit` at `ec15`; the complete generated map and MZ relocation table must prove those placements. The successful probe establishes storage emission and dependency requirements, not a shortcut for substituting absolute target symbols or patching the three words after LINK. The original stack, `_edata=52cc` and `_end=cbe0` remain additional whole-program constraints.
