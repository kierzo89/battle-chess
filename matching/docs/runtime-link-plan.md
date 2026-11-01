# Independently pinned Microsoft C 5.00 runtime linking

The later [runtime expansion](runtime-library-expansion.md) extends this initial CRT0/CHKSTK milestone to 35 complete code segments / 3,917 bytes and nine independently initialized data candidates / 170 bytes.

The complete 179-byte `CRT0` code segment and complete 22-byte `CHKSTK` code
segment now link byte for byte to the original image at `0xea86` and `0xecaa`.
All 26 two-byte fixup fields are resolved, without masking. `CRT0` also emits
exactly its original two MZ relocation sites, image `0xea91` and `0xeb1c`;
`CHKSTK` emits none. This is **201 bytes of independently supplied runtime
library code, zero bytes of authored C reconstruction**. The canonical checker now reports these as `runtime_matched` units in a
separate runtime count and byte total. They receive no C or ASM credit. The
previous assembly reconstruction of the same CHKSTK span was replaced, avoiding
overlap. A final executable build remains outstanding.

The new [library backend](../library16.py) never opens a reference executable.
It extracts members through OMF record boundaries and library page alignment,
checks the whole-library and member SHA-256 pins, validates object checksums,
then relocates complete initialized SEGDEF extents using explicit placements.
It accepts the OFFSET16 and matching-group BASE16 forms required here. Missing
placements, unsupported forms, overlaps, holes and crossing extents fail.
The target supplies comparison bytes and address evidence, never generated
instruction bytes or byte replacements.

## Provenance and pins

The source is the independent historical PCjs preserved distribution:

- Archive: `https://miscdisks.pcjs.org/pcx86/lang/microsoft/c/5.00/MSC500-DISK4-INCLIBS.json`
- Archive SHA-256: `18a0c57eadf4eea0eb236a0e16f57019c6fd05789dfc52d857b84f6bf7edf58c`
- `SLIBC.LIB`: 129,473 bytes, SHA-256 `7eabd615308e9a05de24f6e6e82e61a65f733eb64d12b5318d8b3ed569e389b9`
- `CRT0`: library offset `0x10`, 863 bytes, SHA-256 `c8fa9ca0b70762defb91b280d9676eafda5fceb47475344937eb3f281c9a8705`
- `CHKSTK`: library offset `0xd50`, 210 bytes, SHA-256 `2d7c0c6a8b43ce8b533af02eaada3accee1842f90c7f690ca0a81f3c7005090b`

The executable code hashes after relocation are respectively
`d4cdd4a13398dc3abb17a9b9edfd09ccf9ad7f0570561ccb75a90a9522bb76fd`
and `000d18a388e7759f54254848aa3dc54aa07a7e9506c3beb0c8d0ae1a2b8610f0`.
The original target SHA-256 remains
`c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd`.
The library retains its historical proprietary classification. It is not part
of the separately licensed Microsoft MS-DOS tools release.

The canonical pins and explicit linker inputs are in
[config/runtime500.json](../config/runtime500.json).
The original standalone investigation profile is retained as
[runtime500-placements.json](../evidence/runtime500-placements.json).
The independent full comparison, all relocation arithmetic, original addends,
FIXUPP record offsets/raw fields, generated image locations and MZ sites are in
[runtime500-link-verification.json](../evidence/runtime500-link-verification.json).
This record reports runtime classification separately from C credit.

## Address evidence and complete symbol inventory

Addresses below are original unrelocated image coordinates. Code frame is
paragraph zero. Data offsets use DGROUP paragraph `0x5cc2`, linear image base
`0x5cc20`. `CRT0` object `_TEXT` starts at `0xea86`; its object `_DATA` starts at
DGROUP `0x4958`. `CHKSTK` object `_TEXT` starts at `0xecaa`; its object `_DATA`
starts at DGROUP `0x4a00`.

The startup raw bytes are REA Evidence
`ev_587bfb28c9071a17199d532d2342ac7b6aa29f64a05a4e424d5af57686e6d032`,
retained in [rea_crt_startup_500.json](../evidence/rea_crt_startup_500.json).
Each symbol placement follows the original operand and the independently
archived object's named FIXUPP target. Near-call targets are operand + location
+ two, modulo 65536; data offsets subtract the object's displacement/addend.
For example three separate data references at startup offsets `0x3d`, `0x42`,
and `0x4d` independently constrain `_DATA` to `0x4958`; `_end` is constrained
both by a direct offset and an offset with displacement `0xfffe`.
These are inferred original linker placements, not newly observed runtime
execution or evidence of original linker command-line options.

All 16 declared `CRT0` externals:

| External | Placement | Coverage |
|---|---|---|
| `_edata` | DGROUP `52cc` | Startup offset `68` |
| `_end` | DGROUP `cbe0` | Startup offsets `21`, `6b` |
| `_environ` | DGROUP `49f0` | Startup offset `84` |
| `_exit` | code `ebfe` | Startup offsets `93`, `a2` |
| `_main` | code `0010` | Startup offset `8f`, wrapping near call |
| `__acrtmsg` | unknown | Declaration only; no FIXUPP reference in member |
| `__cinit` | code `eb3a` | Startup offset `76` |
| `__exit` | code `ec15` | Data offset `4`; not required by code segment |
| `__FF_MSGBANNER` | code `f470` | Startup offsets `29`, `a6` |
| `__NMSG_WRITE` | code `f6d7` | Startup offsets `2f`, `a9` |
| `__nullcheck` | unknown | Declaration only; no FIXUPP reference in member |
| `__psp` | DGROUP `49cf` | Startup offset `62` |
| `__setargv` | code `f4b8` | Startup offset `7e` |
| `__setenvp` | code `f646` | Startup offset `7b` |
| `___argc` | DGROUP `49ec` | Startup offset `8c` |
| `___argv` | DGROUP `49ee` | Startup offset `88` |

All `CRT0` publics, derived directly from pinned PUBDEF offsets and the above
segment placements:

| Public | Placement |
|---|---|
| `__abrkp`, `__abrktbe` | DGROUP `49ae` |
| `__abrktb` | DGROUP `495e` |
| `__acrtused` | absolute `9876` (not an image address) |
| `__aexit_rtn` | DGROUP `495c` |
| `__amsg_exit` | code `eb2a` |
| `__asizds` | DGROUP `4958` |
| `__astart` | code `ea86` |
| `__atopsp` | DGROUP `495a` |
| `__cintDIV` | code `eb1b` |

`CHKSTK` declares `_end` and `__amsg_exit`; its code references the latter at
code `eb2a`. Its `_DATA` initialization references `_end+0x100`, producing
`0xcce0`. Its publics are `__chkstk` at code `ecaa` and `STKHQQ` at DGROUP
`4a00`. Raw code is REA Evidence
`ev_d3c811083437faa0acc7c65e0196a83107e65add6ec97fba7b28a24c93a44eca`,
retained in [rea-runtime-chkstk-link.json](../evidence/rea-runtime-chkstk-link.json).

Data is outside the unchanged disk prefix. Independent decoding of the original
EXEPACK image and REA reads of the provenance-bound analysis carrier confirm
`__exit=ec15` and `STKHQQ=cce0`. REA Evidence
`ev_eb11974642b5184238f458c3821fa148fe06be7418c5da92bbfc78020ee21459`
and `ev_6a2cd3bb04d60f261d0e15f367e8ae22dcb6c529776e17d9c8e1769eae7a9534`
are retained in `rea-runtime-data-link.json` and
`rea-runtime-chkstkdata-link.json`. The synthesized analysis carrier SHA-256 is
`faf3516d0e72e30005ad90cb2da165081af5fe6871f5e8c3663980a5d725ef02`.
Ghidra applies its `0x1000` load base to the original MZ relocation at image
`0x61580`: its data read contains `6cc2`, whereas the unrelocated original
contains `5cc2`. That is an analysis loader adjustment, not a byte mismatch.

## Reproduce and validate

Install the independently pinned runtime explicitly (the checker never downloads):

```sh
python3 matching/setup_runtime.py
# Or use the already preserved disk JSON without network access:
python3 matching/setup_runtime.py --archive matching/build/probes/MSC500-DISK4.json
python3 matching/check.py
```

The installer validates the archive before FAT12 extraction and the full
library before publishing a staged installation under `toolchains/runtime500`.
A manifest is checked against the canonical configuration on every runtime
build. The canonical checker re-extracts and links the members on every run;
no cached linked bytes are inputs. Its `runtime/` artifacts and relocation
coverage show the generated member objects and exact linked segments.

The standalone investigation remains reproducible with the preserved library:

```sh
python3 matching/library16.py \
  --library matching/build/probes/SLIBC.LIB \
  --profile matching/evidence/runtime500-placements.json \
  --output matching/build/runtime500-link
python3 -m unittest discover -s matching/tests -p test_library16.py -v
```

Generation writes unchanged extracted objects, full linked code segments, and a
provenance/relocation report. It never reads `CHESS.EXE`. The separate test opens
the independently hash-checked original for full-byte comparison and checks the
complete MZ-site set inside each code extent. Seven tests cover arithmetic,
input immutability, failures, pins/checksums and the two complete runtime matches.
The pinned integration tests explicitly skip if the archive is unavailable.

## Remaining work and integration boundary

This is a restricted library-code linker milestone, not a complete Microsoft
LINK run. The original CRT module includes an 88-byte `_DATA` allocation but
only 12 initialized LEDATA bytes: `[0,10)` and `[86,88)`. Its hole `[10,86)`
is deliberately rejected by the current whole-segment API. Data assembly,
zero-initialization policy, the third CRT MZ site at image `0x61580`, stack
layout, all other runtime members and library ordering remain outside this
match. No runtime data receives credit here. The declarations `__acrtmsg` and
`__nullcheck` remain unplaced because neither has a fixup; inventing addresses
for them is unnecessary and would not add evidence.

The canonical backend consumes the pinned profile and library directly,
re-extracts on every build, emits status `runtime_matched` and classification
`independently_supplied_runtime_library`, and reports complete code bytes/MZ
sites independently from C and ASM. Member, library and generated hashes are
retained. File coverage includes these non-overlapping independently linked
runtime spans. Relocation coverage reports source-emitted and runtime-emitted
sites separately and their union. Full image placement and a real link/EXEPACK
build must still produce every required byte and all 173 original MZ relocation
sites before claiming the user's full-byte goal achieved.

The runtime boundary policy is deliberately separate: it requires a pinned
independent complete CODE SEGDEF, its public at object offset zero, an exact
full raw-byte REA read at that entry, and equality with the independent linked
member. CRT0 additionally must equal the saved original EXEPACK entry. REA
original-target `analyze_function` and `read_function_instructions` reject
`0x1ea86`; the exact containing-procedure query reports `not_in_procedure`
(Evidence `ev_e27b93223205b4faa75b316dc532835d20bd4d3b05e81e1248890e037593e0bf`,
retained in `rea-runtime-startup-entry.json`). No REA procedure boundary is
invented for that runtime member. The existing C/ASM complete analyzed-procedure
policy is unchanged. Incomplete legacy r2 candidate lists no longer veto
independently validated reviewed entries; their original 371-row denominator
remains unchanged, with all reviewed units still present in the main report.

Four additional runtime integration tests check fresh artifacts, separate
classification, retained raw-byte integrity, unchanged C boundary requirements,
and archive/library/manifest rejection.
